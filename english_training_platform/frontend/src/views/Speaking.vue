<template>
  <div class="speaking-page">
    <h1>口语训练</h1>
    
    <div class="speaking-categories">
      <div class="category-card" @click="selectType('daily')">
        <div class="category-icon">💬</div>
        <h2>日常口语</h2>
        <p>练习日常对话和社交场景中的英语口语表达</p>
      </div>
      
      <div class="category-card" @click="selectType('academic')">
        <div class="category-icon">🎓</div>
        <h2>学术口语</h2>
        <p>针对学术讨论、演讲和报告的口语训练</p>
      </div>
      
      <div class="category-card" @click="selectType('business')">
        <div class="category-icon">💼</div>
        <h2>商务口语</h2>
        <p>商务会议、谈判和职场交流的口语练习</p>
      </div>
      
      <div class="category-card" @click="selectType('test')">
        <div class="category-icon">📝</div>
        <h2>考试口语</h2>
        <p>针对四六级、雅思和托福等考试的口语训练</p>
      </div>
    </div>
    
    <div v-if="selectedType" class="topic-selection">
      <h2>{{ typeTitles[selectedType] }}话题</h2>
      
      <div class="topics-container">
        <div 
          v-for="topic in filteredTopics" 
          :key="topic.id"
          class="topic-card"
          @click="selectTopic(topic)"
        >
          <h3>{{ topic.title }}</h3>
          <p>{{ topic.description }}</p>
          <div class="topic-meta">
            <span class="level">{{ topic.level }}</span>
            <span class="duration">{{ topic.duration }}分钟</span>
          </div>
        </div>
      </div>
    </div>
    
    <div v-if="selectedTopic" class="modal">
      <div class="modal-content">
        <div class="modal-header">
          <h2>开始练习 - {{ selectedTopic.title }}</h2>
          <button class="close-btn" @click="closeModal">×</button>
        </div>
        <div class="modal-body">
          <p>{{ selectedTopic.description }}</p>
          <div class="topic-meta">
            <span class="level">{{ selectedTopic.level }}</span>
            <span class="duration">{{ selectedTopic.duration }}分钟</span>
          </div>
          <div class="tasks-info">
            <h3>练习内容</h3>
            <ul>
              <li>句子模仿（重复语音）</li>
              <li>回答问题</li>
              <li>情境对话</li>
              <li>话题讨论</li>
            </ul>
          </div>
        </div>
        <div class="modal-footer">
          <button class="cancel-btn" @click="closeModal">取消</button>
          <router-link 
            :to="{ name: 'SpeakingPractice', params: { id: selectedTopic.id } }" 
            class="start-btn"
          >
            开始练习
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SpeakingView',
  data() {
    return {
      selectedType: null,
      selectedTopic: null,
      typeTitles: {
        daily: '日常口语',
        academic: '学术口语',
        business: '商务口语',
        test: '考试口语'
      },
      topics: [
        {
          id: 's-101',
          type: 'daily',
          title: '旅行与探索',
          description: '关于旅行经历、旅游景点和文化体验的口语练习',
          level: '初级',
          duration: 15
        },
        {
          id: 's-102',
          type: 'daily',
          title: '饮食与健康',
          description: '讨论食物、饮食习惯和健康生活方式的口语训练',
          level: '初级',
          duration: 12
        },
        {
          id: 's-201',
          type: 'academic',
          title: '学术讨论技巧',
          description: '学习如何在学术环境中参与讨论、表达观点和回应他人',
          level: '中级',
          duration: 20
        },
        {
          id: 's-202',
          type: 'academic',
          title: '学术演讲基础',
          description: '掌握学术演讲的结构、语言和表达技巧',
          level: '中高级',
          duration: 25
        },
        {
          id: 's-301',
          type: 'business',
          title: '商务会议',
          description: '学习在商务会议中的发言、提问和讨论技巧',
          level: '中级',
          duration: 18
        },
        {
          id: 's-302',
          type: 'business',
          title: '商务谈判',
          description: '掌握商务谈判中的语言策略和沟通技巧',
          level: '高级',
          duration: 22
        },
        {
          id: 's-401',
          type: 'test',
          title: '雅思口语应对策略',
          description: '针对雅思考试三个部分的口语练习和应对技巧',
          level: '中高级',
          duration: 30
        },
        {
          id: 's-402',
          type: 'test',
          title: '托福口语备考',
          description: '针对托福口语考试的独立和综合任务的练习',
          level: '高级',
          duration: 28
        }
      ]
    };
  },
  computed: {
    filteredTopics() {
      return this.topics.filter(topic => topic.type === this.selectedType);
    }
  },
  methods: {
    selectType(type) {
      this.selectedType = type;
      window.scrollTo({
        top: document.querySelector('.topic-selection').offsetTop - 20,
        behavior: 'smooth'
      });
    },
    selectTopic(topic) {
      this.selectedTopic = topic;
      document.body.classList.add('modal-open');
    },
    closeModal() {
      this.selectedTopic = null;
      document.body.classList.remove('modal-open');
    }
  }
};
</script>

<style scoped>
.speaking-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

h1 {
  text-align: center;
  margin-bottom: 2rem;
  color: #2c3e50;
}

.speaking-categories {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.category-card {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
  text-align: center;
  transition: transform 0.2s, box-shadow 0.2s;
  cursor: pointer;
}

.category-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
}

.category-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.category-card h2 {
  margin-bottom: 1rem;
  color: #2c3e50;
  font-size: 1.5rem;
}

.category-card p {
  color: #6c757d;
  line-height: 1.5;
}

.topic-selection {
  margin-top: 3rem;
}

.topic-selection h2 {
  margin-bottom: 1.5rem;
  text-align: center;
  color: #2c3e50;
}

.topics-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.topic-card {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
  transition: transform 0.2s, box-shadow 0.2s;
  cursor: pointer;
}

.topic-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.topic-card h3 {
  margin-bottom: 0.75rem;
  color: #2c3e50;
}

.topic-card p {
  color: #6c757d;
  margin-bottom: 1.5rem;
  line-height: 1.5;
}

.topic-meta {
  display: flex;
  gap: 1rem;
  font-size: 0.9rem;
}

.level {
  color: #41b883;
  font-weight: 500;
}

.duration {
  color: #6c757d;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  border-radius: 8px;
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.modal-header {
  padding: 1.5rem;
  border-bottom: 1px solid #e9ecef;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h2 {
  margin: 0;
  color: #2c3e50;
  font-size: 1.5rem;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #6c757d;
  cursor: pointer;
}

.modal-body {
  padding: 1.5rem;
}

.modal-body p {
  margin-bottom: 1.5rem;
  color: #6c757d;
  line-height: 1.6;
}

.tasks-info {
  margin-top: 1.5rem;
  background-color: #f8f9fa;
  padding: 1rem;
  border-radius: 4px;
}

.tasks-info h3 {
  margin-bottom: 1rem;
  color: #2c3e50;
  font-size: 1.1rem;
}

.tasks-info ul {
  padding-left: 1.5rem;
  color: #495057;
}

.tasks-info li {
  margin-bottom: 0.5rem;
}

.modal-footer {
  padding: 1.5rem;
  border-top: 1px solid #e9ecef;
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}

.cancel-btn, .start-btn {
  padding: 0.5rem 1.5rem;
  border-radius: 4px;
  font-weight: 500;
  cursor: pointer;
  text-align: center;
}

.cancel-btn {
  background-color: #f8f9fa;
  color: #6c757d;
  border: 1px solid #dee2e6;
}

.start-btn {
  background-color: #41b883;
  color: white;
  border: none;
  text-decoration: none;
}

:global(body.modal-open) {
  overflow: hidden;
}
</style> 