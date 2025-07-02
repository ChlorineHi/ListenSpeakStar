<template>
  <div class="recommendation-page">
    <div class="page-header">
      <h1>智能学习推荐</h1>
      <p class="subtitle">基于您的答题情况，我们为您定制了个性化学习计划</p>
      
      <!-- 添加开始训练按钮 -->
      <div v-if="hasRecommendations && !loading && !error" class="quick-start-section">
        <button @click="startBestMaterial" class="quick-start-button">
          <span class="button-icon">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="24" height="24">
              <path d="M8 5v14l11-7z"/>
            </svg>
          </span>
          开始最适合的训练
        </button>
        <p class="quick-start-hint">直接进入最匹配您能力的训练材料</p>
      </div>
    </div>
    
    <div v-if="error" class="error-section">
      <ErrorMessage 
        :title="'推荐生成失败'" 
        :message="errorMessage"
        @retry="retryFetchRecommendations"
      />
    </div>
    
    <div v-else-if="!hasAnswerData" class="no-data-section">
      <div class="no-data-message">
        <div class="no-data-icon">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 22C6.477 22 2 17.523 2 12S6.477 2 12 2s10 4.477 10 10-4.477 10-10 10zm0-2a8 8 0 1 0 0-16 8 8 0 0 0 0 16zm-1-5h2v2h-2v-2zm0-8h2v6h-2V7z"/>
          </svg>
        </div>
        <h2>没有答题数据</h2>
        <p>您需要先完成一些听力练习，系统才能为您生成个性化推荐。</p>
        <router-link to="/listening" class="action-button">
          去练习
        </router-link>
      </div>
    </div>
    
    <RecommendationResult
      v-else
      :loading="loading"
      :weakAreas="weakAreas"
      :strongAreas="strongAreas"
      :performanceScore="performanceScore"
      :recommendations="recommendations"
      :improvementSuggestions="improvementSuggestions"
    />
  </div>
</template>

<script>
import RecommendationResult from '@/components/RecommendationResult.vue'
import ErrorMessage from '@/components/ErrorMessage.vue'
import axios from 'axios'
import RecommendationService from '@/services/RecommendationService'

export default {
  name: 'RecommendationPage',
  components: {
    RecommendationResult,
    ErrorMessage
  },
  data() {
    return {
      loading: true,
      error: false,
      errorMessage: '',
      hasAnswerData: false,
      weakAreas: [],
      strongAreas: [],
      performanceScore: 0,
      recommendations: [],
      improvementSuggestions: '',
      userAnswers: [],
      hasRecommendations: false
    }
  },
  created() {
    // 从路由参数或本地存储获取用户答题数据
    if (this.$route.params.userAnswers) {
      this.userAnswers = this.$route.params.userAnswers;
      this.hasAnswerData = true;
      this.fetchRecommendations();
    } else if (this.$route.params.fromListening) {
      console.log('从听力练习页面跳转过来，尝试从本地存储获取答题数据');
      this.loadAnswersFromLocalStorage();
    } else {
      this.loadAnswersFromLocalStorage();
    }
  },
  methods: {
    async fetchRecommendations() {
      this.loading = true;
      this.error = false;
      this.errorMessage = '';
      
      try {
        // 创建RecommendationService实例，注意这里不再使用new关键字
        const recommendationService = RecommendationService;
        
        // 获取用户答题数据
        const userAnswers = this.getUserAnswers();
        
        // 使用RecommendationService获取推荐
        const result = await recommendationService.getRecommendations(userAnswers);
        console.log('RecommendationService返回结果:', result);
        
        // 检查结果是否有效
        if (result) {
          // 处理新的API响应格式
          if (result.recommendations && Array.isArray(result.recommendations)) {
            this.recommendations = result.recommendations;
            this.weakAreas = result.weak_areas || [];
            this.strongAreas = result.strong_areas || [];
            this.performanceScore = result.performance_score || 0;
            this.improvementSuggestions = result.improvement_suggestions || '';
            this.hasRecommendations = this.recommendations.length > 0;
            
            console.log('成功获取推荐结果:', {
              recommendations: this.recommendations.length,
              weakAreas: this.weakAreas,
              strongAreas: this.strongAreas,
              performanceScore: this.performanceScore
            });
          } 
          // 处理旧的响应格式（直接返回推荐数组）
          else if (Array.isArray(result)) {
            this.recommendations = result;
            this.hasRecommendations = result.length > 0;
            
            // 计算综合表现分数和薄弱/擅长领域
            this.calculatePerformanceScore(userAnswers);
            this.analyzeStrengthsAndWeaknesses(userAnswers);
            
            // 生成改进建议
            this.generateImprovementSuggestions();
            
            console.log('使用旧格式处理推荐结果:', this.recommendations.length);
          }
          else {
            console.warn('无效的推荐结果格式:', result);
            this.hasRecommendations = false;
            this.errorMessage = '获取到的推荐数据格式不正确，请稍后再试';
            this.error = true;
          }
        } else {
          console.warn('没有获取到推荐材料');
          this.hasRecommendations = false;
          this.errorMessage = '无法获取推荐材料，请稍后再试';
          this.error = true;
        }
      } catch (error) {
        console.error('获取推荐失败:', error);
        this.error = true;
        this.errorMessage = `无法生成推荐，请稍后再试。(${error.message || '未知错误'})`;
        
        // 如果API调用失败但有答题数据，使用模拟数据
        if (this.hasAnswerData) {
          this.setMockData();
          this.error = false; // 使用模拟数据时不显示错误
        }
      } finally {
        this.loading = false;
      }
    },
    
    // 开始最适合的训练材料
    startBestMaterial() {
      if (this.recommendations && this.recommendations.length > 0) {
        // 获取匹配度最高的材料
        const bestMaterial = this.recommendations.sort((a, b) => {
          return b.match_score - a.match_score;
        })[0];
        
        console.log('最佳匹配材料:', bestMaterial);
        
        if (bestMaterial) {
          // 确保使用正确的ID属性
          const materialId = bestMaterial.id || bestMaterial.materialId;
          
          if (materialId) {
            console.log(`导航到最佳匹配的听力材料: ${materialId}`);
            
            // 在跳转前检查材料是否存在
            this.checkMaterialExists(materialId).then(exists => {
              if (exists) {
                this.$router.push(`/listening/${materialId}`);
              } else {
                console.error(`材料ID ${materialId} 不存在，无法跳转`);
                alert(`抱歉，推荐的材料 ${materialId} 暂时无法访问，请选择其他材料。`);
              }
            }).catch(error => {
              console.error('检查材料是否存在时出错:', error);
            });
          } else {
            console.error('无法找到有效的材料ID');
          }
        } else {
          console.warn('没有可用的推荐材料');
        }
      } else {
        console.warn('没有可用的推荐材料');
      }
    },
    
    // 检查材料是否存在
    async checkMaterialExists(materialId) {
      try {
        // 尝试获取材料的难度级别
        const idParts = materialId.split('_');
        const difficultyPrefix = idParts[0].toUpperCase();
        let difficulty;
        
        switch (difficultyPrefix) {
          case 'CET4':
            difficulty = 'CET4';
            break;
          case 'CET6':
            difficulty = 'CET6';
            break;
          case 'IELTS':
            difficulty = 'IELTS';
            break;
          case 'TOEFL':
            difficulty = 'TOEFL';
            break;
          default:
            // 尝试从年份格式判断
            if (/^\d{4}$/.test(difficultyPrefix)) {
              // 如果是年份格式，直接使用materialId
              const response = await fetch(`/materials/${materialId}/materials.json`);
              return response.ok;
            } else {
              difficulty = 'CET4'; // 默认难度
            }
        }
        
        // 先尝试从难度目录获取
        let response = await fetch(`/materials/${difficulty}/materials.json`);
        
        if (response.ok) {
          const data = await response.json();
          // 检查材料是否存在于JSON中
          return data.materials.some(material => material.id === materialId);
        }
        
        // 如果从难度目录无法获取，尝试直接从材料ID目录获取
        response = await fetch(`/materials/${materialId}/materials.json`);
        return response.ok;
      } catch (error) {
        console.error(`检查材料 ${materialId} 是否存在时出错:`, error);
        return false;
      }
    },
    
    // 计算综合表现分数
    calculatePerformanceScore(userAnswers) {
      let totalQuestions = 0;
      let correctAnswers = 0;
      
      // 遍历所有答题数据
      if (userAnswers && userAnswers.answers) {
        Object.keys(userAnswers.answers).forEach(materialId => {
          const answers = userAnswers.answers[materialId];
          
          answers.forEach(answer => {
            totalQuestions++;
            if (answer.isCorrect) {
              correctAnswers++;
            }
          });
        });
      }
      
      // 计算正确率并转换为0-100的分数
      if (totalQuestions > 0) {
        this.performanceScore = Math.round((correctAnswers / totalQuestions) * 100);
      } else {
        this.performanceScore = 0;
      }
      
      console.log(`计算综合表现: ${correctAnswers}/${totalQuestions} = ${this.performanceScore}`);
    },
    
    // 分析强项和弱项
    analyzeStrengthsAndWeaknesses(userAnswers) {
      // 初始化标签统计
      const tagStats = {};
      
      // 遍历所有答题数据，统计每个标签的正确和错误次数
      if (userAnswers && userAnswers.answers) {
        Object.keys(userAnswers.answers).forEach(materialId => {
          const answers = userAnswers.answers[materialId];
          
          answers.forEach(answer => {
            // 获取问题标签（这里假设问题有tags属性，如果没有则使用默认标签）
            const tags = answer.tags || this.getDefaultTags(answer.questionId);
            
            tags.forEach(tag => {
              if (!tagStats[tag]) {
                tagStats[tag] = { correct: 0, total: 0 };
              }
              
              tagStats[tag].total++;
              if (answer.isCorrect) {
                tagStats[tag].correct++;
              }
            });
          });
        });
      }
      
      // 计算每个标签的正确率
      const tagAccuracy = {};
      Object.keys(tagStats).forEach(tag => {
        const stats = tagStats[tag];
        if (stats.total > 0) {
          tagAccuracy[tag] = stats.correct / stats.total;
        }
      });
      
      // 按正确率排序标签
      const sortedTags = Object.keys(tagAccuracy).sort((a, b) => {
        return tagAccuracy[b] - tagAccuracy[a];
      });
      
      // 选择前3个作为强项，后3个作为弱项
      this.strongAreas = sortedTags.slice(0, 3);
      this.weakAreas = sortedTags.slice(-3).reverse();
      
      // 如果标签不足，使用默认标签
      if (this.strongAreas.length === 0) {
        this.strongAreas = ['主旨理解', '推理判断'];
      }
      
      if (this.weakAreas.length === 0) {
        this.weakAreas = ['细节理解', '数字信息'];
      }
      
      console.log('强项:', this.strongAreas);
      console.log('弱项:', this.weakAreas);
    },
    
    // 获取默认标签（根据问题ID生成一些标签）
    getDefaultTags(questionId) {
      const allTags = ['主旨理解', '细节理解', '推理判断', '数字信息', '词汇理解', '语法结构'];
      const index = (questionId && typeof questionId === 'string') 
        ? questionId.charCodeAt(questionId.length - 1) % allTags.length 
        : Math.floor(Math.random() * allTags.length);
      
      return [allTags[index]];
    },
    
    // 生成改进建议
    generateImprovementSuggestions() {
      if (this.weakAreas.length > 0) {
        const suggestions = {
          '细节理解': '建议在听力练习中特别注意记录关键细节，可以尝试做笔记来提高细节捕捉能力。',
          '数字信息': '数字信息是您的薄弱环节，建议专门练习包含数字、日期、时间等信息的听力材料。',
          '词汇理解': '建议扩大词汇量，特别是常见听力材料中出现的专业词汇和表达。',
          '语法结构': '复杂句型理解需要加强，建议多听多模仿包含复杂句型的材料。',
          '推理判断': '需要提高基于上下文的推理能力，练习时可以尝试预测说话者接下来要表达的内容。',
          '主旨理解': '把握文章主旨的能力需要提升，建议练习概括段落大意和总结中心思想的能力。'
        };
        
        // 根据最弱的领域生成建议
        const weakestArea = this.weakAreas[0];
        this.improvementSuggestions = suggestions[weakestArea] || 
          '建议针对您的薄弱环节进行有针对性的练习，多听多练习是提高听力能力的关键。';
      } else {
        this.improvementSuggestions = '建议继续保持良好的学习习惯，多听多练习是提高听力能力的关键。';
      }
    },
    
    // 获取用户答题数据
    getUserAnswers() {
      // 如果已经有用户答题数据，直接返回
      if (this.userAnswers && this.userAnswers.userId && this.userAnswers.answers) {
        return this.userAnswers;
      }
      
      // 尝试从localStorage获取
      try {
        const lastAnswersStr = localStorage.getItem('lastAnswers');
        if (lastAnswersStr) {
          const lastAnswers = JSON.parse(lastAnswersStr);
          
          // 检查数据是否有效
          if (Array.isArray(lastAnswers) && lastAnswers.length > 0) {
            // 转换为推荐系统需要的格式
            const userAnswers = {
              userId: 'user123',
              answers: {}
            };
            
            // 按材料ID分组
            lastAnswers.forEach(answer => {
              if (!answer.material_id) return;
              
              if (!userAnswers.answers[answer.material_id]) {
                userAnswers.answers[answer.material_id] = [];
              }
              
              userAnswers.answers[answer.material_id].push({
                questionId: answer.question_id,
                isCorrect: answer.is_correct,
                userAnswer: answer.user_answer,
                correctAnswer: answer.correct_answer,
                // 添加标签信息
                tags: answer.question_tags || this.getDefaultTags(answer.question_id)
              });
            });
            
            return userAnswers;
          }
        }
      } catch (e) {
        console.error('获取用户答题数据失败:', e);
      }
      
      // 如果没有有效数据，返回默认数据
      return {
        userId: 'user123',
        answers: {
          'cet4_001': [
            { questionId: 'q1', isCorrect: true, tags: ['主旨理解', '推理判断'] },
            { questionId: 'q2', isCorrect: false, tags: ['细节理解', '数字信息'] },
            { questionId: 'q3', isCorrect: true, tags: ['词汇理解'] }
          ],
          '2022_06': [
            { questionId: 'q1', isCorrect: false, tags: ['细节理解'] },
            { questionId: 'q2', isCorrect: false, tags: ['数字信息'] },
            { questionId: 'q3', isCorrect: true, tags: ['主旨理解'] }
          ]
        }
      };
    },
    
    retryFetchRecommendations() {
      this.fetchRecommendations()
    },
    setMockData() {
      // 当API调用失败时使用的模拟数据
      this.weakAreas = ['细节理解', '数字信息']
      this.strongAreas = ['主旨理解', '推理判断']
      this.performanceScore = 65
      this.recommendations = [
        {
          id: '2023_06_1',
          title: '2023年六月四级听力真题第一套',
          reason: '该套题包含多个细节理解题型，特别关注数字信息的理解，与您的薄弱环节匹配度高。',
          match_score: 0.92
        },
        {
          id: 'cet4_001',
          title: 'CET4 听力训练 - 校园生活',
          reason: '这套材料专注于训练细节捕捉能力，包含大量需要理解具体数字和事实的题目。',
          match_score: 0.85
        }
      ]
      this.improvementSuggestions = '建议在听力练习中特别注意记录关键数字信息，培养快速捕捉细节的能力。'
    },
    // 添加新方法用于从本地存储加载答题数据
    loadAnswersFromLocalStorage() {
      try {
        // 尝试从本地存储获取答题数据
        const lastAnswersStr = localStorage.getItem('lastAnswers');
        if (lastAnswersStr) {
          const lastAnswers = JSON.parse(lastAnswersStr);
          console.log('从本地存储获取到答题数据:', lastAnswers.length, '条记录');
          
          // 检查数据是否有效
          if (Array.isArray(lastAnswers) && lastAnswers.length > 0) {
            // 转换为推荐系统需要的格式
            const userAnswers = {
              userId: 'user123',
              answers: {}
            };
            
            // 按材料ID分组
            lastAnswers.forEach(answer => {
              if (!answer.material_id) return;
              
              if (!userAnswers.answers[answer.material_id]) {
                userAnswers.answers[answer.material_id] = [];
              }
              
              userAnswers.answers[answer.material_id].push({
                questionId: answer.question_id,
                isCorrect: answer.is_correct,
                userAnswer: answer.user_answer,
                correctAnswer: answer.correct_answer,
                tags: answer.question_tags || this.getDefaultTags(answer.question_id)
              });
            });
            
            // 检查是否有有效的答题数据
            const materialIds = Object.keys(userAnswers.answers);
            if (materialIds.length > 0) {
              this.userAnswers = userAnswers;
              this.hasAnswerData = true;
              this.fetchRecommendations();
              return;
            }
          }
        }
        
        // 如果没有有效数据，设置为无数据状态
        console.log('没有找到有效的答题数据');
        this.loading = false;
        this.hasAnswerData = false;
      } catch (e) {
        console.error('解析用户答题数据失败:', e);
        this.loading = false;
        this.hasAnswerData = false;
      }
    }
  }
}
</script>

<style scoped>
.recommendation-page {
  padding: 20px;
  max-width: 1000px;
  margin: 0 auto;
}

.page-header {
  text-align: center;
  margin-bottom: 30px;
}

.page-header h1 {
  margin-bottom: 10px;
  color: #1976d2;
}

.subtitle {
  color: #666;
  font-size: 16px;
  margin-bottom: 20px;
}

/* 快速开始训练按钮样式 */
.quick-start-section {
  margin: 30px auto;
  max-width: 400px;
}

.quick-start-button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  background-color: #4CAF50;
  color: white;
  padding: 15px 20px;
  border: none;
  border-radius: 8px;
  font-size: 18px;
  font-weight: bold;
  cursor: pointer;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
}

.quick-start-button:hover {
  background-color: #45a049;
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.25);
}

.button-icon {
  margin-right: 10px;
}

.quick-start-hint {
  text-align: center;
  color: #666;
  font-size: 14px;
  margin-top: 10px;
}

.no-data-section {
  display: flex;
  justify-content: center;
  padding: 40px 0;
}

.no-data-message {
  text-align: center;
  max-width: 400px;
}

.no-data-icon {
  color: #FFC107;
  width: 64px;
  height: 64px;
  margin: 0 auto 20px;
}

.no-data-message h2 {
  font-size: 24px;
  margin-bottom: 10px;
  color: #333;
}

.no-data-message p {
  color: #666;
  margin-bottom: 20px;
}

.action-button {
  display: inline-block;
  background-color: #1976d2;
  color: white;
  padding: 10px 20px;
  border-radius: 4px;
  font-weight: bold;
  text-decoration: none;
  transition: background-color 0.2s;
}

.action-button:hover {
  background-color: #1565c0;
}
</style> 