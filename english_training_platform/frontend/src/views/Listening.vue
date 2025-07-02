<template>
  <div class="listening-page">
    <div class="page-header">
      <HeadphonesIcon class="header-icon" />
      <h1>听力训练</h1>
    </div>
    
    <!-- 筛选器 -->
    <div class="filter-section">
      <div class="filter-row">
        <div class="filter-group">
          <label for="difficulty">
            <AdjustmentsIcon class="filter-icon" />
            难度级别:
          </label>
          <select id="difficulty" v-model="selectedDifficulty" @change="applyFilters">
            <option value="">所有难度</option>
            <option value="CET4">CET-4</option>
            <option value="CET6">CET-6</option>
            <option value="IELTS">IELTS</option>
            <option value="TOEFL">TOEFL</option>
          </select>
        </div>
        
        <div class="filter-group">
          <label for="topic">
            <TagIcon class="filter-icon" />
            主题:
          </label>
          <select id="topic" v-model="selectedTopic" @change="applyFilters">
            <option value="">所有主题</option>
            <option v-for="topic in topics" :key="topic" :value="topic">{{ topic }}</option>
          </select>
        </div>
        
        <div class="filter-group search">
          <div class="search-wrapper">
            <SearchIcon class="search-icon" />
            <input type="text" v-model="searchQuery" placeholder="搜索听力材料..." @input="applyFilters">
          </div>
        </div>
      </div>
    </div>
    
    <!-- 加载状态 -->
    <div v-if="isLoading" class="loading-section">
      <div class="loader"></div>
      <p>加载中...</p>
    </div>
    
    <!-- 错误信息 -->
    <div v-else-if="error" class="error-section">
      <ExclamationCircleIcon class="error-icon" />
      <p>{{ error }}</p>
      <button @click="fetchMaterials" class="primary-btn">
        <RefreshIcon class="btn-icon" />
        重试
      </button>
    </div>
    
    <!-- 材料列表 -->
    <div v-else class="materials-section">
      <div v-if="filteredMaterials.length === 0" class="no-materials">
        <InboxIcon class="empty-icon" />
        <p>没有找到符合条件的听力材料</p>
      </div>
      
      <div v-else class="materials-grid">
        <div v-for="material in filteredMaterials" :key="material.id" class="material-card">
          <div class="material-header">
            <span class="difficulty-badge">{{ material.difficulty }}</span>
            <h3>{{ material.title }}</h3>
          </div>
          
          <div class="material-topics">
            <span v-for="topic in material.topics" :key="topic" class="topic-tag">
              <HashtagIcon class="topic-icon" />
              {{ topic }}
            </span>
          </div>
          
          <div class="material-actions">
            <router-link :to="{ name: 'ListeningDetail', params: { id: material.id } }" class="primary-btn">
              <PlayIcon class="btn-icon" />
              开始练习
            </router-link>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 评估入口 -->
    <div class="assessment-section">
      <div class="assessment-content">
        <ChartBarIcon class="assessment-icon" />
        <div>
          <h2>英语水平评估</h2>
          <p>不确定从哪里开始？参加我们的听力水平评估，获取个性化学习建议。</p>
        </div>
        <router-link :to="{ name: 'Assessment', query: { difficulty: selectedDifficulty || 'CET4' } }" class="assessment-btn">
          <ArrowRightIcon class="btn-icon" />
          开始评估
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import MaterialService from '@/services/MaterialService'
import { 
  SpeakerWaveIcon as HeadphonesIcon, 
  AdjustmentsVerticalIcon as AdjustmentsIcon, 
  TagIcon, 
  MagnifyingGlassIcon as SearchIcon,
  PlayIcon,
  HashtagIcon,
  ChartBarIcon,
  ArrowRightIcon,
  ExclamationCircleIcon,
  ArrowPathIcon as RefreshIcon,
  InboxIcon
} from '@heroicons/vue/24/outline'

export default {
  name: 'ListeningView',
  components: {
    HeadphonesIcon,
    AdjustmentsIcon,
    TagIcon,
    SearchIcon,
    PlayIcon,
    HashtagIcon,
    ChartBarIcon,
    ArrowRightIcon,
    ExclamationCircleIcon,
    RefreshIcon,
    InboxIcon
  },
  data() {
    return {
      materials: [],
      topics: [],
      selectedDifficulty: '',
      selectedTopic: '',
      searchQuery: '',
      isLoading: false,
      error: null
    }
  },
  computed: {
    filteredMaterials() {
      let result = [...this.materials]
      
      // 按难度筛选
      if (this.selectedDifficulty) {
        result = result.filter(material => material.difficulty === this.selectedDifficulty)
      }
      
      // 按主题筛选
      if (this.selectedTopic) {
        result = result.filter(material => 
          material.topics && material.topics.includes(this.selectedTopic)
        )
      }
      
      // 按搜索关键词筛选
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase()
        result = result.filter(material => 
          material.title.toLowerCase().includes(query) ||
          (material.topics && material.topics.some(topic => topic.toLowerCase().includes(query)))
        )
      }
      
      return result
    }
  },
  created() {
    this.fetchMaterials()
    this.fetchTopics()
  },
  methods: {
    async fetchMaterials() {
      this.isLoading = true
      this.error = null
      
      try {
        // 获取所有难度级别的材料
        const index = await MaterialService.getMaterialsIndex()
        const allMaterials = []
        
        for (const difficulty of index.difficulties) {
          try {
            const materials = await MaterialService.getMaterialsByDifficulty(difficulty.id)
            allMaterials.push(...materials)
          } catch (error) {
            console.error(`获取${difficulty.id}材料失败:`, error)
          }
        }
        
        this.materials = allMaterials
      } catch (error) {
        console.error('获取听力材料失败:', error)
        this.error = '获取听力材料失败，请稍后再试'
      } finally {
        this.isLoading = false
      }
    },
    async fetchTopics() {
      try {
        this.topics = await MaterialService.getAllTopics()
      } catch (error) {
        console.error('获取主题列表失败:', error)
      }
    },
    applyFilters() {
      // 筛选逻辑已在计算属性中实现
    }
  }
}
</script>

<style scoped>
.listening-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 2.5rem;
}

.header-icon {
  width: 2.5rem;
  height: 2.5rem;
  color: #41b883;
  margin-right: 1rem;
}

h1 {
  text-align: center;
  color: #2c3e50;
  font-size: 2.2rem;
  font-weight: 700;
}

.filter-section {
  background-color: #f8f9fa;
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.filter-section:hover {
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.08);
}

.filter-row {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
}

.filter-group {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-width: 200px;
}

.filter-group label {
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #495057;
  display: flex;
  align-items: center;
}

.filter-icon {
  width: 1.2rem;
  height: 1.2rem;
  margin-right: 0.5rem;
  color: #41b883;
}

.filter-group select {
  padding: 0.7rem;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  font-size: 1rem;
  background-color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.04);
  transition: all 0.2s ease;
}

.filter-group select:focus {
  border-color: #41b883;
  box-shadow: 0 0 0 3px rgba(65, 184, 131, 0.2);
  outline: none;
}

.filter-group.search {
  flex: 2;
}

.search-wrapper {
  position: relative;
}

.search-icon {
  position: absolute;
  left: 0.8rem;
  top: 50%;
  transform: translateY(-50%);
  width: 1.2rem;
  height: 1.2rem;
  color: #6c757d;
}

.filter-group input {
  padding: 0.7rem 0.7rem 0.7rem 2.5rem;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  font-size: 1rem;
  width: 100%;
  background-color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.04);
  transition: all 0.2s ease;
}

.filter-group input:focus {
  border-color: #41b883;
  box-shadow: 0 0 0 3px rgba(65, 184, 131, 0.2);
  outline: none;
}

.loading-section,
.error-section {
  text-align: center;
  padding: 3rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.loader {
  border: 3px solid #f3f3f3;
  border-top: 3px solid #41b883;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-icon {
  width: 3rem;
  height: 3rem;
  color: #dc3545;
  margin-bottom: 1rem;
}

.error-section p {
  color: #dc3545;
  margin-bottom: 1rem;
}

.materials-section {
  margin-bottom: 3rem;
}

.no-materials {
  text-align: center;
  padding: 3rem;
  background-color: #f8f9fa;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.empty-icon {
  width: 4rem;
  height: 4rem;
  color: #adb5bd;
  margin-bottom: 1rem;
}

.materials-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.5rem;
}

.material-card {
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border: 1px solid rgba(0, 0, 0, 0.05);
  height: 100%;
}

.material-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 20px rgba(0, 0, 0, 0.1);
  border-color: rgba(65, 184, 131, 0.3);
}

.material-header {
  margin-bottom: 1rem;
}

.difficulty-badge {
  display: inline-block;
  padding: 0.35rem 0.7rem;
  background-color: #41b883;
  color: white;
  border-radius: 20px;
  font-size: 0.8rem;
  margin-bottom: 0.8rem;
  font-weight: 500;
  letter-spacing: 0.5px;
}

.material-header h3 {
  margin: 0;
  font-size: 1.3rem;
  color: #2c3e50;
  line-height: 1.4;
}

.material-topics {
  margin-bottom: 1.5rem;
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.topic-tag {
  display: flex;
  align-items: center;
  padding: 0.3rem 0.7rem;
  background-color: #e9ecef;
  color: #495057;
  border-radius: 20px;
  font-size: 0.8rem;
  transition: background-color 0.2s;
}

.topic-tag:hover {
  background-color: #dee2e6;
}

.topic-icon {
  width: 0.8rem;
  height: 0.8rem;
  margin-right: 0.3rem;
}

.material-actions {
  margin-top: auto;
}

.primary-btn,
.assessment-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.6rem 1.2rem;
  background-color: #41b883;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  text-align: center;
  text-decoration: none;
  transition: all 0.2s ease;
  box-shadow: 0 2px 4px rgba(65, 184, 131, 0.3);
}

.primary-btn:hover,
.assessment-btn:hover {
  background-color: #3aa876;
  box-shadow: 0 4px 8px rgba(65, 184, 131, 0.4);
  transform: translateY(-2px);
}

.btn-icon {
  width: 1rem;
  height: 1rem;
  margin-right: 0.5rem;
}

.assessment-section {
  background: linear-gradient(135deg, #f1f8f5 0%, #e6f3ee 100%);
  border-radius: 12px;
  padding: 0.5rem;
  margin-top: 3rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

.assessment-content {
  border: 2px dashed rgba(65, 184, 131, 0.3);
  border-radius: 8px;
  padding: 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.assessment-icon {
  width: 3.5rem;
  height: 3.5rem;
  color: #41b883;
  margin-right: 1.5rem;
}

.assessment-section h2 {
  color: #2c3e50;
  margin-bottom: 0.8rem;
  font-size: 1.5rem;
}

.assessment-section p {
  color: #495057;
  margin-bottom: 0;
  max-width: 600px;
}

.assessment-btn {
  font-size: 1.1rem;
  padding: 0.75rem 1.5rem;
  white-space: nowrap;
  margin-left: 1.5rem;
}

@media (max-width: 992px) {
  .assessment-content {
    flex-direction: column;
    text-align: center;
  }
  
  .assessment-icon {
    margin-right: 0;
    margin-bottom: 1rem;
  }
  
  .assessment-btn {
    margin-left: 0;
    margin-top: 1.5rem;
  }
}

@media (max-width: 768px) {
  .filter-group {
    min-width: 100%;
  }
  
  .materials-grid {
    grid-template-columns: 1fr;
  }
  
  .page-header {
    flex-direction: column;
  }
  
  .header-icon {
    margin-right: 0;
    margin-bottom: 0.5rem;
  }
}
</style> 