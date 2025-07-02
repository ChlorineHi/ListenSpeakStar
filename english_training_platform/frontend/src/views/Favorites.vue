<template>
  <div class="favorites-page">
    <h1>我的收藏</h1>
    
    <div v-if="loading" class="loading">
      <p>加载中...</p>
    </div>
    
    <div v-else-if="favorites.length === 0" class="empty-state">
      <div class="empty-icon">📚</div>
      <h2>暂无收藏内容</h2>
      <p>您还没有收藏任何学习材料。浏览听力材料并点击收藏按钮来添加到这里。</p>
      <router-link to="/" class="browse-btn">浏览学习材料</router-link>
    </div>
    
    <div v-else class="favorites-list">
      <div class="filters">
        <button 
          @click="currentFilter = 'all'" 
          :class="{ active: currentFilter === 'all' }"
        >
          全部
        </button>
        <button 
          @click="currentFilter = 'cet4'" 
          :class="{ active: currentFilter === 'cet4' }"
        >
          四级
        </button>
        <button 
          @click="currentFilter = 'cet6'" 
          :class="{ active: currentFilter === 'cet6' }"
        >
          六级
        </button>
        <button 
          @click="currentFilter = 'ielts'" 
          :class="{ active: currentFilter === 'ielts' }"
        >
          雅思
        </button>
        <button 
          @click="currentFilter = 'toefl'" 
          :class="{ active: currentFilter === 'toefl' }"
        >
          托福
        </button>
      </div>
      
      <div class="material-cards">
        <div 
          v-for="item in filteredFavorites" 
          :key="item.id" 
          class="material-card"
        >
          <div class="card-tag" :class="item.type">{{ getTypeLabel(item.type) }}</div>
          <h3>{{ item.title }}</h3>
          <p class="description">{{ item.description }}</p>
          <div class="card-meta">
            <span class="level">{{ item.level }}</span>
            <span class="duration">{{ item.duration }}分钟</span>
            <span class="date">收藏于 {{ formatDate(item.addedAt) }}</span>
          </div>
          <div class="card-actions">
            <router-link :to="{ name: 'Listening', params: { id: item.id } }" class="study-btn">
              开始学习
            </router-link>
            <button @click="removeFavorite(item.id)" class="remove-btn">
              移除收藏
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'FavoritesView',
  data() {
    return {
      loading: true,
      currentFilter: 'all',
      favorites: [
        {
          id: 'l-101',
          title: '大学校园生活对话',
          description: '两位大学生讨论校园生活、课程选择和课外活动。',
          type: 'cet4',
          level: '初级',
          duration: 5,
          addedAt: '2023-06-10T08:30:00Z'
        },
        {
          id: 'l-203',
          title: '科技新闻报道',
          description: '关于最新科技趋势和创新的英语新闻报道。',
          type: 'cet6',
          level: '中级',
          duration: 8,
          addedAt: '2023-06-12T14:20:00Z'
        },
        {
          id: 'l-305',
          title: '环境问题讨论',
          description: '专家讨论全球环境挑战和可持续发展解决方案。',
          type: 'ielts',
          level: '高级',
          duration: 12,
          addedAt: '2023-06-15T19:45:00Z'
        },
        {
          id: 'l-402',
          title: '学术讲座：全球经济',
          description: '关于全球经济趋势和国际贸易的学术讲座。',
          type: 'toefl',
          level: '高级',
          duration: 15,
          addedAt: '2023-06-18T10:15:00Z'
        }
      ]
    };
  },
  computed: {
    filteredFavorites() {
      if (this.currentFilter === 'all') {
        return this.favorites;
      }
      return this.favorites.filter(item => item.type === this.currentFilter);
    }
  },
  methods: {
    getTypeLabel(type) {
      const labels = {
        cet4: '四级',
        cet6: '六级',
        ielts: '雅思',
        toefl: '托福'
      };
      return labels[type] || type;
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
    },
    removeFavorite(id) {
      // 这里应该有实际的API调用来删除收藏
      this.favorites = this.favorites.filter(item => item.id !== id);
    }
  },
  mounted() {
    // 模拟API调用
    setTimeout(() => {
      this.loading = false;
    }, 500);
  }
};
</script>

<style scoped>
.favorites-page {
  max-width: 1000px;
  margin: 0 auto;
  padding: 2rem;
}

h1 {
  text-align: center;
  margin-bottom: 2rem;
  color: #2c3e50;
}

.loading {
  text-align: center;
  padding: 3rem;
  font-size: 1.2rem;
  color: #6c757d;
}

.empty-state {
  text-align: center;
  padding: 3rem;
  background-color: #f8f9fa;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.empty-state h2 {
  margin-bottom: 1rem;
  color: #495057;
}

.empty-state p {
  margin-bottom: 2rem;
  color: #6c757d;
  max-width: 500px;
  margin-left: auto;
  margin-right: auto;
}

.browse-btn {
  display: inline-block;
  background-color: #41b883;
  color: white;
  text-decoration: none;
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  font-weight: 500;
  transition: background-color 0.2s;
}

.browse-btn:hover {
  background-color: #399a6e;
}

.filters {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}

.filters button {
  padding: 0.5rem 1rem;
  border: 1px solid #dee2e6;
  border-radius: 20px;
  background-color: white;
  color: #495057;
  cursor: pointer;
  transition: all 0.2s;
}

.filters button:hover {
  background-color: #f8f9fa;
}

.filters button.active {
  background-color: #41b883;
  color: white;
  border-color: #41b883;
}

.material-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.material-card {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
  position: relative;
  transition: transform 0.2s, box-shadow 0.2s;
}

.material-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.card-tag {
  position: absolute;
  top: 0;
  right: 1.5rem;
  padding: 0.25rem 1rem;
  border-radius: 0 0 8px 8px;
  color: white;
  font-size: 0.85rem;
  font-weight: 500;
}

.card-tag.cet4 {
  background-color: #2196f3;
}

.card-tag.cet6 {
  background-color: #4caf50;
}

.card-tag.ielts {
  background-color: #ff9800;
}

.card-tag.toefl {
  background-color: #9c27b0;
}

.material-card h3 {
  margin: 0.5rem 0 1rem;
  color: #2c3e50;
  font-size: 1.2rem;
}

.description {
  color: #6c757d;
  margin-bottom: 1.5rem;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
  font-size: 0.85rem;
}

.level {
  color: #41b883;
  font-weight: 500;
}

.duration, .date {
  color: #6c757d;
}

.card-actions {
  display: flex;
  gap: 0.75rem;
}

.study-btn, .remove-btn {
  flex: 1;
  padding: 0.5rem;
  border-radius: 4px;
  text-align: center;
  font-weight: 500;
  cursor: pointer;
}

.study-btn {
  background-color: #41b883;
  color: white;
  text-decoration: none;
}

.remove-btn {
  background-color: #f8f9fa;
  color: #dc3545;
  border: 1px solid #dc3545;
}
</style> 