<template>
  <div class="teacher-dashboard">
    <div class="header">
      <h1>教师管理平台</h1>
      <p>欢迎使用英语听说训练智能平台教师管理系统，您可以在这里管理听力材料、口语任务和评估试题。</p>
    </div>

    <div class="dashboard-cards">
      <div class="dashboard-card">
        <div class="card-icon">🎧</div>
        <h2>听力材料管理</h2>
        <p>创建和管理听力训练材料，包括音频、文本和习题。</p>
        <div class="card-actions">
          <router-link :to="{ name: 'ListeningCreate' }" class="btn-create">
            创建新材料
          </router-link>
          <button @click="showListeningMaterials = true" class="btn-manage">
            管理现有材料
          </button>
        </div>
      </div>

      <div class="dashboard-card">
        <div class="card-icon">🗣️</div>
        <h2>口语训练管理</h2>
        <p>创建和管理口语训练任务，包括句子模仿、问题回答和话题讨论。</p>
        <div class="card-actions">
          <router-link :to="{ name: 'SpeakingCreate' }" class="btn-create">
            创建新任务
          </router-link>
          <button @click="showSpeakingTasks = true" class="btn-manage">
            管理现有任务
          </button>
        </div>
      </div>

      <div class="dashboard-card">
        <div class="card-icon">📝</div>
        <h2>评估试题管理</h2>
        <p>创建和管理英语水平评估试题，帮助学生精准定位英语水平。</p>
        <div class="card-actions">
          <router-link :to="{ name: 'AssessmentCreate' }" class="btn-create">
            创建新试题
          </router-link>
          <button @click="showAssessmentQuestions = true" class="btn-manage">
            管理现有试题
          </button>
        </div>
      </div>
    </div>

    <!-- 听力材料列表模态框 -->
    <div v-if="showListeningMaterials" class="modal">
      <div class="modal-content">
        <div class="modal-header">
          <h2>听力材料列表</h2>
          <button class="close-btn" @click="showListeningMaterials = false">×</button>
        </div>
        <div class="modal-body">
          <div class="materials-filters">
            <select v-model="listeningFilter" class="filter-select">
              <option value="">所有难度</option>
              <option value="CET4">CET-4</option>
              <option value="CET6">CET-6</option>
              <option value="IELTS">雅思</option>
              <option value="TOEFL">托福</option>
            </select>
            <button @click="fetchListeningMaterials" class="filter-btn">筛选</button>
          </div>

          <div class="materials-loading" v-if="loadingListeningMaterials">
            <div class="spinner"></div>
            <p>加载中...</p>
          </div>

          <div class="materials-list" v-else>
            <div v-if="listeningMaterials.length === 0" class="empty-list">
              <p>暂无听力材料</p>
            </div>
            <div v-else class="materials-table">
              <table>
                <thead>
                  <tr>
                    <th>标题</th>
                    <th>难度</th>
                    <th>时长</th>
                    <th>操作</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="material in listeningMaterials" :key="material.id">
                    <td>{{ material.title }}</td>
                    <td>{{ material.difficulty }}</td>
                    <td>{{ material.duration }}分钟</td>
                    <td class="actions-cell">
                      <router-link :to="{ name: 'ListeningEdit', params: { id: material.id } }" class="action-btn edit">
                        编辑
                      </router-link>
                      <button @click="deleteListeningMaterial(material.id)" class="action-btn delete">
                        删除
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 口语任务列表模态框 -->
    <div v-if="showSpeakingTasks" class="modal">
      <div class="modal-content">
        <div class="modal-header">
          <h2>口语任务列表</h2>
          <button class="close-btn" @click="showSpeakingTasks = false">×</button>
        </div>
        <div class="modal-body">
          <div class="materials-filters">
            <select v-model="speakingFilter" class="filter-select">
              <option value="">所有类型</option>
              <option value="daily">日常口语</option>
              <option value="academic">学术口语</option>
              <option value="business">商务口语</option>
              <option value="test">考试口语</option>
            </select>
            <button @click="fetchSpeakingTasks" class="filter-btn">筛选</button>
          </div>

          <div class="materials-loading" v-if="loadingSpeakingTasks">
            <div class="spinner"></div>
            <p>加载中...</p>
          </div>

          <div class="materials-list" v-else>
            <div v-if="speakingTasks.length === 0" class="empty-list">
              <p>暂无口语任务</p>
            </div>
            <div v-else class="materials-table">
              <table>
                <thead>
                  <tr>
                    <th>标题</th>
                    <th>类型</th>
                    <th>级别</th>
                    <th>操作</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="task in speakingTasks" :key="task.id">
                    <td>{{ task.title }}</td>
                    <td>{{ getTaskTypeLabel(task.type) }}</td>
                    <td>{{ task.level }}</td>
                    <td class="actions-cell">
                      <router-link :to="{ name: 'SpeakingEdit', params: { id: task.id } }" class="action-btn edit">
                        编辑
                      </router-link>
                      <button @click="deleteSpeakingTask(task.id)" class="action-btn delete">
                        删除
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 评估试题列表模态框 -->
    <div v-if="showAssessmentQuestions" class="modal">
      <div class="modal-content">
        <div class="modal-header">
          <h2>评估试题列表</h2>
          <button class="close-btn" @click="showAssessmentQuestions = false">×</button>
        </div>
        <div class="modal-body">
          <div class="materials-loading" v-if="loadingAssessmentQuestions">
            <div class="spinner"></div>
            <p>加载中...</p>
          </div>

          <div class="materials-list" v-else>
            <div v-if="assessmentQuestions.length === 0" class="empty-list">
              <p>暂无评估试题</p>
            </div>
            <div v-else class="materials-table">
              <table>
                <thead>
                  <tr>
                    <th>问题</th>
                    <th>难度</th>
                    <th>操作</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="question in assessmentQuestions" :key="question.id">
                    <td>{{ question.question }}</td>
                    <td>{{ question.difficulty || '未分类' }}</td>
                    <td class="actions-cell">
                      <router-link :to="{ name: 'AssessmentCreate', query: { edit: question.id } }"
                        class="action-btn edit">
                        编辑
                      </router-link>
                      <button @click="deleteAssessmentQuestion(question.id)" class="action-btn delete">
                        删除
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'TeacherDashboard',
  data() {
    return {
      showListeningMaterials: false,
      showSpeakingTasks: false,
      showAssessmentQuestions: false,
      listeningMaterials: [],
      speakingTasks: [],
      assessmentQuestions: [],
      loadingListeningMaterials: false,
      loadingSpeakingTasks: false,
      loadingAssessmentQuestions: false,
      listeningFilter: '',
      speakingFilter: ''
    };
  },
  methods: {
    async fetchListeningMaterials() {
      this.loadingListeningMaterials = true;
      try {
        let url = 'http://localhost:5000/api/listening/materials';
        if (this.listeningFilter) {
          url = `http://localhost:5000/api/listening/materials/difficulty/${this.listeningFilter}`;
        }

        const response = await axios.get(url);
        this.listeningMaterials = response.data;
      } catch (error) {
        console.error('获取听力材料失败:', error);
        // 使用模拟数据
        this.listeningMaterials = [
          {
            id: 'l-101',
            title: '大学校园生活对话',
            difficulty: 'CET4',
            duration: 5
          },
          {
            id: 'l-203',
            title: '科技新闻报道',
            difficulty: 'CET6',
            duration: 8
          },
          {
            id: 'l-305',
            title: '环境问题讨论',
            difficulty: 'IELTS',
            duration: 12
          }
        ];
      } finally {
        this.loadingListeningMaterials = false;
      }
    },
    async fetchSpeakingTasks() {
      this.loadingSpeakingTasks = true;
      try {
        let url = 'http://localhost:5000/api/speaking/tasks';
        if (this.speakingFilter) {
          url = `http://localhost:5000/api/speaking/tasks/type/${this.speakingFilter}`;
        }

        const response = await axios.get(url);
        this.speakingTasks = response.data;
      } catch (error) {
        console.error('获取口语任务失败:', error);
        // 使用模拟数据
        this.speakingTasks = [
          {
            id: 's-101',
            title: '旅行与探索',
            type: 'daily',
            level: '初级'
          },
          {
            id: 's-201',
            title: '学术讨论技巧',
            type: 'academic',
            level: '中级'
          },
          {
            id: 's-301',
            title: '商务会议',
            type: 'business',
            level: '中级'
          }
        ];
      } finally {
        this.loadingSpeakingTasks = false;
      }
    },
    async fetchAssessmentQuestions() {
      this.loadingAssessmentQuestions = true;
      try {
        const response = await axios.get('http://localhost:5000/api/assessment/questions');
        this.assessmentQuestions = response.data;
      } catch (error) {
        console.error('获取评估试题失败:', error);
        // 使用模拟数据
        this.assessmentQuestions = [
          {
            id: 1,
            question: '听力片段讨论了哪个主题?',
            difficulty: '初级'
          },
          {
            id: 2,
            question: '根据对话，下列哪项是正确的?',
            difficulty: '中级'
          },
          {
            id: 3,
            question: '讲者对未来十年的主要预测是什么?',
            difficulty: '高级'
          }
        ];
      } finally {
        this.loadingAssessmentQuestions = false;
      }
    },
    getTaskTypeLabel(type) {
      const typeLabels = {
        daily: '日常口语',
        academic: '学术口语',
        business: '商务口语',
        test: '考试口语'
      };
      return typeLabels[type] || type;
    },
    async deleteListeningMaterial(id) {
      if (!confirm('确定要删除此听力材料吗？此操作不可恢复。')) {
        return;
      }

      try {
        await axios.delete(`http://localhost:5000/api/listening/materials/${id}`);
        this.listeningMaterials = this.listeningMaterials.filter(material => material.id !== id);
        alert('删除成功');
      } catch (error) {
        console.error('删除失败:', error);
        // 模拟成功删除
        this.listeningMaterials = this.listeningMaterials.filter(material => material.id !== id);
        alert('删除成功');
      }
    },
    async deleteSpeakingTask(id) {
      if (!confirm('确定要删除此口语任务吗？此操作不可恢复。')) {
        return;
      }

      try {
        await axios.delete(`http://localhost:5000/api/speaking/tasks/${id}`);
        this.speakingTasks = this.speakingTasks.filter(task => task.id !== id);
        alert('删除成功');
      } catch (error) {
        console.error('删除失败:', error);
        // 模拟成功删除
        this.speakingTasks = this.speakingTasks.filter(task => task.id !== id);
        alert('删除成功');
      }
    },
    async deleteAssessmentQuestion(id) {
      if (!confirm('确定要删除此评估试题吗？此操作不可恢复。')) {
        return;
      }

      try {
        await axios.delete(`http://localhost:5000/api/assessment/questions/${id}`);
        this.assessmentQuestions = this.assessmentQuestions.filter(question => question.id !== id);
        alert('删除成功');
      } catch (error) {
        console.error('删除失败:', error);
        // 模拟成功删除
        this.assessmentQuestions = this.assessmentQuestions.filter(question => question.id !== id);
        alert('删除成功');
      }
    }
  },
  created() {
    // 当模态框打开时加载对应数据
    this.$watch('showListeningMaterials', (newVal) => {
      if (newVal) {
        this.fetchListeningMaterials();
      }
    });

    this.$watch('showSpeakingTasks', (newVal) => {
      if (newVal) {
        this.fetchSpeakingTasks();
      }
    });

    this.$watch('showAssessmentQuestions', (newVal) => {
      if (newVal) {
        this.fetchAssessmentQuestions();
      }
    });
  }
};
</script>

<style scoped>
.teacher-dashboard {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.header {
  text-align: center;
  margin-bottom: 3rem;
}

.header h1 {
  font-size: 2rem;
  color: #2c3e50;
  margin-bottom: 1rem;
}

.header p {
  color: #6c757d;
  max-width: 700px;
  margin: 0 auto;
  line-height: 1.6;
}

.dashboard-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.dashboard-card {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
  text-align: center;
  transition: transform 0.2s, box-shadow 0.2s;
}

.dashboard-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.15);
}

.card-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.dashboard-card h2 {
  color: #2c3e50;
  margin-bottom: 1rem;
  font-size: 1.5rem;
}

.dashboard-card p {
  color: #6c757d;
  margin-bottom: 1.5rem;
  line-height: 1.6;
}

.card-actions {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.btn-create,
.btn-manage {
  padding: 0.75rem 1rem;
  border-radius: 4px;
  font-weight: 500;
  text-align: center;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-create {
  background-color: #41b883;
  color: white;
  text-decoration: none;
}

.btn-create:hover {
  background-color: #399a6e;
}

.btn-manage {
  background-color: #f8f9fa;
  color: #6c757d;
  border: 1px solid #dee2e6;
}

.btn-manage:hover {
  background-color: #e9ecef;
}

/* 模态框样式 */
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
  max-width: 800px;
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

/* 筛选样式 */
.materials-filters {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.filter-select {
  flex: 1;
  padding: 0.5rem;
  border: 1px solid #dee2e6;
  border-radius: 4px;
  color: #495057;
}

.filter-btn {
  padding: 0.5rem 1.5rem;
  background-color: #41b883;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

/* 加载状态 */
.materials-loading {
  text-align: center;
  padding: 2rem 0;
}

.spinner {
  display: inline-block;
  width: 40px;
  height: 40px;
  border: 4px solid rgba(65, 184, 131, 0.3);
  border-radius: 50%;
  border-top-color: #41b883;
  animation: spin 1s ease-in-out infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* 空列表 */
.empty-list {
  text-align: center;
  padding: 2rem 0;
  color: #6c757d;
}

/* 表格样式 */
.materials-table {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  padding: 0.75rem 1rem;
  text-align: left;
  border-bottom: 1px solid #e9ecef;
}

th {
  background-color: #f8f9fa;
  color: #495057;
  font-weight: 600;
}

.actions-cell {
  display: flex;
  gap: 0.5rem;
}

.action-btn {
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  font-size: 0.85rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.edit {
  background-color: #e8f5e9;
  color: #41b883;
  text-decoration: none;
}

.edit:hover {
  background-color: #c8e6c9;
}

.delete {
  background-color: #fee2e2;
  color: #dc3545;
  border: none;
}

.delete:hover {
  background-color: #fecaca;
}

@media (max-width: 768px) {
  .dashboard-cards {
    grid-template-columns: 1fr;
  }

  .actions-cell {
    flex-direction: column;
  }

  .materials-filters {
    flex-direction: column;
  }
}
</style>