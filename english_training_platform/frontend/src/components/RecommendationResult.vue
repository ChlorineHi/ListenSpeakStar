<template>
  <div class="recommendation-result">
    <div v-if="loading" class="loading-container">
      <div class="spinner"></div>
      <p>正在分析您的答题情况，生成个性化推荐...</p>
    </div>
    
    <div v-else class="result-container">
      <div class="analysis-section">
        <h3>能力分析</h3>
        <div class="analysis-card">
          <div class="score-display">
            <div class="score-circle" :style="{ background: getScoreColor(performanceScore) }">
              {{ performanceScore }}
            </div>
            <div class="score-label">综合表现</div>
          </div>
          
          <div class="areas-container">
            <div class="area-box">
              <h4>薄弱领域</h4>
              <div class="tags-container">
                <span v-for="(area, index) in weakAreas" :key="'weak-'+index" class="tag weak-tag">
                  {{ area }}
                </span>
              </div>
            </div>
            
            <div class="area-box">
              <h4>擅长领域</h4>
              <div class="tags-container">
                <span v-for="(area, index) in strongAreas" :key="'strong-'+index" class="tag strong-tag">
                  {{ area }}
                </span>
              </div>
            </div>
          </div>
        </div>
        
        <div class="suggestion-box" v-if="improvementSuggestions">
          <h4>提升建议</h4>
          <p>{{ improvementSuggestions }}</p>
        </div>
      </div>
      
      <div class="recommendations-section">
        <h3>推荐材料</h3>
        <p class="recommendation-intro">基于您的答题情况，我们为您推荐以下听力材料：</p>
        
        <div class="materials-list">
          <div class="material-card" v-for="(material, index) in recommendations" :key="index">
            <div class="material-header">
              <h4>{{ material.title }}</h4>
              <div class="match-score">匹配度: {{ getMatchScore(material) }}</div>
            </div>
            
            <p class="material-reason">{{ material.reason }}</p>
            
            <button class="material-button" @click="goToMaterial(material.id || material.materialId)">
              开始练习
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'RecommendationResult',
  props: {
    loading: {
      type: Boolean,
      default: false
    },
    weakAreas: {
      type: Array,
      default: () => []
    },
    strongAreas: {
      type: Array,
      default: () => []
    },
    performanceScore: {
      type: Number,
      default: 0
    },
    recommendations: {
      type: Array,
      default: () => []
    },
    improvementSuggestions: {
      type: String,
      default: ''
    }
  },
  methods: {
    getScoreColor(score) {
      if (score >= 80) return 'linear-gradient(135deg, #4CAF50, #8BC34A)';
      if (score >= 60) return 'linear-gradient(135deg, #FFC107, #FFEB3B)';
      return 'linear-gradient(135deg, #FF5722, #F44336)';
    },
    goToMaterial(materialId) {
      if (!materialId) {
        console.error('材料ID不存在');
        return;
      }
      
      // 直接使用传入的materialId
      console.log(`导航到听力材料: ${materialId}`);
      this.$router.push(`/listening/${materialId}`);
    },
    getMatchScore(material) {
      if (material.match_score) {
        return (material.match_score * 100).toFixed(0) + '%';
      } else {
        return 'N/A';
      }
    }
  }
}
</script>

<style scoped>
.recommendation-result {
  padding: 20px;
  max-width: 900px;
  margin: 0 auto;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 0;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 5px solid rgba(0, 0, 0, 0.1);
  border-radius: 50%;
  border-top-color: #1976d2;
  animation: spin 1s ease-in-out infinite;
  margin-bottom: 20px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.result-container {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.analysis-card {
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.score-display {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 10px;
}

.score-circle {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  font-weight: bold;
  color: white;
  margin-bottom: 10px;
}

.score-label {
  font-size: 16px;
  color: #666;
}

.areas-container {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}

.area-box {
  flex: 1;
  min-width: 200px;
}

.area-box h4 {
  margin-top: 0;
  margin-bottom: 10px;
  color: #333;
}

.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag {
  padding: 6px 12px;
  border-radius: 16px;
  font-size: 14px;
}

.weak-tag {
  background-color: rgba(244, 67, 54, 0.1);
  color: #f44336;
}

.strong-tag {
  background-color: rgba(76, 175, 80, 0.1);
  color: #4caf50;
}

.suggestion-box {
  background-color: #f5f5f5;
  border-left: 4px solid #1976d2;
  padding: 15px;
  margin-top: 20px;
}

.suggestion-box h4 {
  margin-top: 0;
  margin-bottom: 10px;
  color: #1976d2;
}

.recommendations-section h3 {
  margin-bottom: 10px;
}

.recommendation-intro {
  margin-bottom: 20px;
  color: #666;
}

.materials-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.material-card {
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 20px;
  transition: transform 0.2s, box-shadow 0.2s;
}

.material-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.material-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.material-header h4 {
  margin: 0;
  color: #333;
}

.match-score {
  background-color: #e3f2fd;
  color: #1976d2;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 14px;
  font-weight: bold;
}

.material-reason {
  color: #666;
  margin-bottom: 15px;
  line-height: 1.5;
}

.material-button {
  background-color: #1976d2;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.2s;
}

.material-button:hover {
  background-color: #1565c0;
}

@media (max-width: 768px) {
  .areas-container {
    flex-direction: column;
  }
  
  .material-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
}
</style> 