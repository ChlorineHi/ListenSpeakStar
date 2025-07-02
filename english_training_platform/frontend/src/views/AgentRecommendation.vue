<template>
  <div class="agent-recommendation">
    <div class="container mx-auto px-4 py-8">
      <h1 class="text-3xl font-bold mb-6">智能推荐 - Agent系统</h1>
      
      <div v-if="isLoading" class="loading-container">
        <div class="spinner"></div>
        <p class="mt-4">正在分析您的学习数据并生成个性化推荐...</p>
      </div>
      
      <div v-else-if="error" class="error-container">
        <div class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-6" role="alert">
          <p>{{ error }}</p>
        </div>
        <button @click="fetchRecommendations" class="primary-btn">重试</button>
      </div>
      
      <div v-else-if="recommendation" class="recommendation-container">
        <!-- 能力分析部分 -->
        <div class="analysis-section bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 class="text-2xl font-semibold mb-4">听力能力分析</h2>
          
          <div class="performance-score mb-4">
            <div class="score-circle">
              <span class="score-number">{{ recommendation.performance_score }}</span>
            </div>
            <div class="score-label">综合评分</div>
          </div>
          
          <div class="areas-container grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <div class="weak-areas">
              <h3 class="text-lg font-medium mb-2 text-red-600">需要提高的领域</h3>
              <ul class="list-disc pl-5">
                <li v-for="(area, index) in recommendation.weak_areas" :key="`weak-${index}`">
                  {{ area }}
                </li>
              </ul>
            </div>
            
            <div class="strong-areas">
              <h3 class="text-lg font-medium mb-2 text-green-600">擅长的领域</h3>
              <ul class="list-disc pl-5">
                <li v-for="(area, index) in recommendation.strong_areas" :key="`strong-${index}`">
                  {{ area }}
                </li>
              </ul>
            </div>
          </div>
          
          <div v-if="recommendation.improvement_suggestions" class="improvement-suggestions mt-4 p-4 bg-blue-50 rounded-md">
            <h3 class="text-lg font-medium mb-2">提升建议</h3>
            <p>{{ recommendation.improvement_suggestions }}</p>
          </div>
        </div>
        
        <!-- 推荐材料部分 -->
        <div class="recommendations-section bg-white rounded-lg shadow-md p-6">
          <h2 class="text-2xl font-semibold mb-4">推荐学习材料</h2>
          
          <div v-if="recommendation.recommendations && recommendation.recommendations.length > 0" class="materials-list">
            <div v-for="(material, index) in recommendation.recommendations" :key="`rec-${index}`" 
                 class="material-card mb-4 border border-gray-200 rounded-md overflow-hidden">
              <div class="card-header bg-gray-50 px-4 py-3 flex justify-between items-center">
                <h3 class="text-lg font-medium">{{ material.title }}</h3>
                <div class="match-score">
                  <span class="match-label">匹配度:</span>
                  <span class="match-value">{{ (material.match_score * 100).toFixed(0) }}%</span>
                </div>
              </div>
              
              <div class="card-body p-4">
                <p class="reason mb-3">{{ material.reason }}</p>
                
                <div class="material-meta flex flex-wrap gap-2 mb-3">
                  <span class="meta-item bg-blue-100 text-blue-800 px-2 py-1 rounded-md text-sm">
                    {{ material.difficulty || '未知难度' }}
                  </span>
                  <span v-for="(topic, tIndex) in (material.topics || [])" :key="`topic-${tIndex}`"
                        class="meta-item bg-green-100 text-green-800 px-2 py-1 rounded-md text-sm">
                    {{ topic }}
                  </span>
                </div>
                
                <router-link :to="{ name: 'Listening', params: { id: material.id } }" class="primary-btn">
                  开始学习
                </router-link>
              </div>
            </div>
          </div>
          
          <div v-else class="no-recommendations">
            <p>暂无推荐材料。请完成更多练习，以便我们为您提供更准确的推荐。</p>
          </div>
        </div>
      </div>
      
      <div v-else class="empty-state">
        <p>请先完成一些听力练习，系统将根据您的表现生成个性化推荐。</p>
        <router-link :to="{ name: 'Assessment' }" class="primary-btn mt-4">
          开始听力评估
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'AgentRecommendation',
  data() {
    return {
      isLoading: false,
      error: null,
      recommendation: null,
      mockUserAnswers: [
        {
          "material_id": "cet4_001",
          "question_id": 1,
          "user_answer": "A",
          "correct_answer": "B",
          "is_correct": false,
          "question_tags": ["细节理解", "教育"],
          "question_type": "选择题",
          "question_content": "What does the woman want to do?"
        },
        {
          "material_id": "cet4_001",
          "question_id": 2,
          "user_answer": "C",
          "correct_answer": "C",
          "is_correct": true,
          "question_tags": ["主旨理解", "校园生活"],
          "question_type": "选择题",
          "question_content": "What is the conversation mainly about?"
        },
        {
          "material_id": "cet4_002",
          "question_id": 5,
          "user_answer": "B",
          "correct_answer": "A",
          "is_correct": false,
          "question_tags": ["数字信息", "环保"],
          "question_type": "选择题",
          "question_content": "How many tons of plastic waste are produced annually?"
        }
      ]
    };
  },
  created() {
    this.fetchRecommendations();
  },
  methods: {
    async fetchRecommendations() {
      this.isLoading = true;
      this.error = null;
      
      try {
        // 从本地存储获取用户答题记录
        const userAnswers = localStorage.getItem('userAnswers');
        
        // 如果有用户答题记录，使用真实数据，否则使用模拟数据
        const payload = {
          user_answers: userAnswers ? JSON.parse(userAnswers) : this.mockUserAnswers
        };
        
        const response = await axios.post('/api/recommendation/recommend', payload);
        this.recommendation = response.data;
      } catch (error) {
        console.error('获取推荐失败', error);
        this.error = '无法获取推荐，请稍后重试';
      } finally {
        this.isLoading = false;
      }
    }
  }
};
</script>

<style scoped>
.agent-recommendation {
  min-height: 80vh;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 300px;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 5px solid rgba(0, 0, 0, 0.1);
  border-radius: 50%;
  border-top-color: #3b82f6;
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.performance-score {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 2rem;
}

.score-circle {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background: linear-gradient(135deg, #4ade80 0%, #3b82f6 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 0.5rem;
}

.score-number {
  font-size: 2rem;
  font-weight: bold;
  color: white;
}

.score-label {
  font-size: 1rem;
  color: #4b5563;
}

.primary-btn {
  display: inline-block;
  background-color: #3b82f6;
  color: white;
  font-weight: 500;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  text-align: center;
  transition: background-color 0.2s;
}

.primary-btn:hover {
  background-color: #2563eb;
}

.match-score {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.match-label {
  font-size: 0.875rem;
  color: #6b7280;
}

.match-value {
  font-weight: 600;
  color: #3b82f6;
}

.empty-state, .no-recommendations {
  text-align: center;
  padding: 3rem 1rem;
  color: #6b7280;
}
</style> 