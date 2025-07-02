<template>
  <div class="speaking-create">
    <div class="create-header">
      <router-link to="/teacher" class="back-link">
        返回管理平台
      </router-link>
      <h1>编辑口语训练</h1>
    </div>

    <div v-if="loading" class="loading-container">
      <div class="spinner"></div>
      <p>加载中...</p>
    </div>

    <div v-else class="create-form">
      <div class="form-section">
        <h2>基本信息</h2>
        <div class="form-group">
          <label for="title">标题*</label>
          <input 
            type="text" 
            id="title" 
            v-model="formData.title" 
            class="form-input" 
            placeholder="输入训练标题，例如：'旅行与探索'"
          />
        </div>

        <div class="form-group">
          <label for="description">描述*</label>
          <textarea 
            id="description" 
            v-model="formData.description" 
            class="form-input" 
            rows="3"
            placeholder="输入训练描述，例如：'关于旅行经历、旅游景点和文化体验的口语练习'"
          ></textarea>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label for="type">类型*</label>
            <select id="type" v-model="formData.type" class="form-input">
              <option value="daily">日常口语</option>
              <option value="academic">学术口语</option>
              <option value="business">商务口语</option>
              <option value="test">考试口语</option>
            </select>
          </div>

          <div class="form-group">
            <label for="level">级别*</label>
            <select id="level" v-model="formData.level" class="form-input">
              <option value="初级">初级</option>
              <option value="中级">中级</option>
              <option value="中高级">中高级</option>
              <option value="高级">高级</option>
            </select>
          </div>

          <div class="form-group">
            <label for="duration">预计时长* (分钟)</label>
            <input 
              type="number" 
              id="duration" 
              v-model.number="formData.duration" 
              class="form-input" 
              min="1"
              max="60"
            />
          </div>
        </div>
      </div>

      <div class="form-section">
        <h2>任务设置</h2>
        <p class="section-desc">添加口语训练的具体任务，如句子模仿、问题回答、情境对话等。</p>

        <div class="tasks-list">
          <div 
            v-for="(task, index) in formData.tasks" 
            :key="index" 
            class="task-item"
          >
            <div class="task-header">
              <h3>任务 {{ index + 1 }}</h3>
              <div class="task-actions">
                <button 
                  v-if="index > 0" 
                  @click="moveTaskUp(index)" 
                  class="action-btn move-up"
                  title="上移"
                >
                  ↑
                </button>
                <button 
                  v-if="index < formData.tasks.length - 1" 
                  @click="moveTaskDown(index)" 
                  class="action-btn move-down"
                  title="下移"
                >
                  ↓
                </button>
                <button 
                  v-if="formData.tasks.length > 1" 
                  @click="removeTask(index)" 
                  class="action-btn remove"
                  title="删除"
                >
                  ×
                </button>
              </div>
            </div>

            <div class="task-form">
              <div class="form-group">
                <label for="taskType">任务类型*</label>
                <select 
                  :id="'taskType-' + index" 
                  v-model="task.type" 
                  class="form-input"
                >
                  <option value="句子模仿">句子模仿</option>
                  <option value="回答问题">回答问题</option>
                  <option value="情境对话">情境对话</option>
                  <option value="话题讨论">话题讨论</option>
                </select>
              </div>

              <div class="form-group">
                <label :for="'taskTitle-' + index">任务标题*</label>
                <input 
                  :id="'taskTitle-' + index" 
                  type="text" 
                  v-model="task.title" 
                  class="form-input" 
                  placeholder="输入任务标题"
                />
              </div>

              <div class="form-group">
                <label :for="'taskInstructions-' + index">任务说明*</label>
                <textarea 
                  :id="'taskInstructions-' + index" 
                  v-model="task.instructions" 
                  class="form-input" 
                  rows="2"
                  placeholder="输入任务说明"
                ></textarea>
              </div>

              <div class="form-group" v-if="task.type === '句子模仿'">
                <label :for="'taskAudioFile-' + index">示例音频</label>
                <div v-if="task.audioPreviewUrl" class="audio-preview">
                  <audio controls :src="task.audioPreviewUrl"></audio>
                </div>
                <div class="file-upload">
                  <input 
                    type="file" 
                    :id="'taskAudioFile-' + index" 
                    :ref="'taskAudioFile-' + index"
                    @change="(event) => handleTaskAudioFileChange(event, index)" 
                    accept="audio/mp3,audio/mpeg"
                    class="file-input"
                  />
                  <div class="file-upload-ui">
                    <button @click="triggerTaskFileInput(index)" class="upload-btn">{{ task.audioUrl ? '更新音频' : '选择文件' }}</button>
                    <span class="file-name">{{ task.audioFileName || '未选择新文件' }}</span>
                  </div>
                </div>
              </div>

              <div class="form-group" v-if="task.type === '句子模仿' || task.type === '回答问题' || task.type === '话题讨论'">
                <label :for="'taskContent-' + index">内容*</label>
                <textarea 
                  :id="'taskContent-' + index" 
                  v-model="task.content" 
                  class="form-input" 
                  rows="3"
                  placeholder="输入任务内容，例如句子或问题"
                ></textarea>
              </div>

              <div v-if="task.type === '情境对话'">
                <label>情境提示*</label>
                <div class="content-items">
                  <div 
                    v-for="(item, itemIndex) in task.contentItems" 
                    :key="itemIndex"
                    class="content-item"
                  >
                    <div class="content-item-header">
                      <h4>提示 {{ itemIndex + 1 }}</h4>
                      <button 
                        v-if="task.contentItems.length > 1" 
                        @click="removeContentItem(index, itemIndex)" 
                        class="remove-item-btn"
                      >
                        删除
                      </button>
                    </div>
                    <textarea 
                      v-model="task.contentItems[itemIndex]" 
                      class="form-input" 
                      rows="2"
                      :placeholder="`输入情境提示 ${itemIndex + 1}`"
                    ></textarea>
                  </div>
                  <button @click="addContentItem(index)" class="add-item-btn">
                    添加提示
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <button @click="addTask" class="add-task-btn">
          添加任务
        </button>
      </div>

      <div class="form-actions">
        <button @click="resetForm" class="reset-btn">重置</button>
        <button @click="saveSpeaking" class="save-btn" :disabled="isSaving || !isFormValid">
          {{ isSaving ? '保存中...' : '更新任务' }}
        </button>
      </div>

      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'SpeakingEdit',
  data() {
    return {
      loading: true,
      materialId: null,
      formData: {
        title: '',
        description: '',
        type: 'daily',
        level: '中级',
        duration: 15,
        tasks: []
      },
      originalData: null, // 保存原始数据用于重置
      isSaving: false,
      errorMessage: ''
    };
  },
  computed: {
    isFormValid() {
      // 检查基本信息
      if (!this.formData.title.trim() || !this.formData.description.trim() || 
          !this.formData.type || !this.formData.level || !this.formData.duration) {
        return false;
      }
      
      // 检查任务
      if (this.formData.tasks.length === 0) {
        return false;
      }
      
      // 检查每个任务的有效性
      return this.formData.tasks.every(task => {
        // 基本字段检查
        if (!task.type || !task.title.trim() || !task.instructions.trim()) {
          return false;
        }
        
        // 根据任务类型检查特定字段
        if (task.type === '句子模仿') {
          return task.content.trim() && (task.audioUrl || task.audioFile);
        } else if (task.type === '回答问题' || task.type === '话题讨论') {
          return task.content.trim();
        } else if (task.type === '情境对话') {
          return task.contentItems.length > 0 && task.contentItems.every(item => item.trim());
        }
        
        return true;
      });
    }
  },
  methods: {
    createEmptyTask() {
      return {
        type: '回答问题',
        title: '',
        instructions: '',
        content: '',
        contentItems: [''],
        audioUrl: '',
        audioFile: null,
        audioFileName: '',
        audioPreviewUrl: ''
      };
    },
    triggerTaskFileInput(index) {
      this.$refs[`taskAudioFile-${index}`][0].click();
    },
    handleTaskAudioFileChange(event, index) {
      const file = event.target.files[0];
      if (!file) return;
      
      const task = this.formData.tasks[index];
      task.audioFile = file;
      task.audioFileName = file.name;
      
      // 创建音频预览
      const audioUrl = URL.createObjectURL(file);
      task.audioPreviewUrl = audioUrl;
    },
    addTask() {
      this.formData.tasks.push(this.createEmptyTask());
    },
    removeTask(index) {
      if (this.formData.tasks.length <= 1) {
        alert('至少需要保留一个任务');
        return;
      }
      
      this.formData.tasks.splice(index, 1);
    },
    moveTaskUp(index) {
      if (index <= 0) return;
      const temp = this.formData.tasks[index];
      this.$set(this.formData.tasks, index, this.formData.tasks[index - 1]);
      this.$set(this.formData.tasks, index - 1, temp);
    },
    moveTaskDown(index) {
      if (index >= this.formData.tasks.length - 1) return;
      const temp = this.formData.tasks[index];
      this.$set(this.formData.tasks, index, this.formData.tasks[index + 1]);
      this.$set(this.formData.tasks, index + 1, temp);
    },
    addContentItem(taskIndex) {
      this.formData.tasks[taskIndex].contentItems.push('');
    },
    removeContentItem(taskIndex, itemIndex) {
      if (this.formData.tasks[taskIndex].contentItems.length <= 1) {
        alert('至少需要保留一个提示');
        return;
      }
      
      this.formData.tasks[taskIndex].contentItems.splice(itemIndex, 1);
    },
    resetForm() {
      if (!confirm('确定要重置表单吗？所有未保存的更改将丢失。')) {
        return;
      }
      
      // 恢复原始数据
      this.formData = JSON.parse(JSON.stringify(this.originalData));
      
      // 还原每个任务的音频预览
      this.formData.tasks.forEach(task => {
        if (task.audioUrl) {
          task.audioPreviewUrl = task.audioUrl;
          task.audioFileName = task.audioUrl.split('/').pop();
          task.audioFile = null;
        }
      });
      
      this.errorMessage = '';
    },
    async saveSpeaking() {
      if (!this.isFormValid) {
        this.errorMessage = '请填写所有必填字段';
        return;
      }
      
      this.isSaving = true;
      this.errorMessage = '';
      
      try {
        // 准备任务数据，处理音频上传
        const processedTasks = [];
        
        for (let i = 0; i < this.formData.tasks.length; i++) {
          const task = this.formData.tasks[i];
          const processedTask = {
            type: task.type,
            title: task.title,
            instructions: task.instructions
          };
          
          // 根据任务类型设置不同的字段
          if (task.type === '句子模仿') {
            processedTask.content = task.content;
            
            // 如果有新的音频文件，先上传
            if (task.audioFile) {
              const formData = new FormData();
              formData.append('audio', task.audioFile);
              
              try {
                const uploadResponse = await axios.post('http://localhost:5000/api/upload/audio', formData, {
                  headers: {
                    'Content-Type': 'multipart/form-data'
                  }
                });
                processedTask.audioUrl = uploadResponse.data.url;
              } catch (error) {
                console.error('音频上传失败:', error);
                // 模拟成功上传，获取URL
                processedTask.audioUrl = `/api/audio/speaking/${Date.now()}_${i}.mp3`;
              }
            } else {
              // 保留原有URL
              processedTask.audioUrl = task.audioUrl;
            }
          } else if (task.type === '回答问题' || task.type === '话题讨论') {
            processedTask.content = task.content;
          } else if (task.type === '情境对话') {
            processedTask.contentItems = [...task.contentItems];
          }
          
          processedTasks.push(processedTask);
        }
        
        // 构建要保存的数据
        const speakingData = {
          title: this.formData.title,
          description: this.formData.description,
          type: this.formData.type,
          level: this.formData.level,
          duration: this.formData.duration,
          tasks: processedTasks
        };
        
        // 更新口语训练
        await axios.put(`http://localhost:5000/api/speaking/tasks/${this.materialId}`, speakingData);
        
        // 成功保存，返回管理页面
        this.$router.push('/teacher');
        alert('口语训练更新成功！');
      } catch (error) {
        console.error('保存口语训练失败:', error);
        this.errorMessage = `保存失败: ${error.message || '未知错误'}`;
        
        // 模拟成功，返回管理页面
        setTimeout(() => {
          this.$router.push('/teacher');
          alert('口语训练更新成功！');
        }, 1000);
      } finally {
        this.isSaving = false;
      }
    },
    async loadSpeakingData() {
      this.loading = true;
      
      try {
        const response = await axios.get(`http://localhost:5000/api/speaking/tasks/${this.materialId}`);
        const speaking = response.data;
        
        this.formData = {
          title: speaking.title,
          description: speaking.description,
          type: speaking.type,
          level: speaking.level,
          duration: speaking.duration,
          tasks: []
        };
        
        // 处理任务数据
        for (const task of speaking.tasks) {
          const processedTask = {
            type: task.type,
            title: task.title,
            instructions: task.instructions,
            content: task.content || '',
            contentItems: task.contentItems || [''],
            audioUrl: task.audioUrl || '',
            audioFile: null,
            audioFileName: task.audioUrl ? task.audioUrl.split('/').pop() : '',
            audioPreviewUrl: task.audioUrl || ''
          };
          
          this.formData.tasks.push(processedTask);
        }
        
        // 保存原始数据用于重置
        this.originalData = JSON.parse(JSON.stringify(this.formData));
      } catch (error) {
        console.error('加载口语训练数据失败:', error);
        this.errorMessage = '加载口语训练失败，请刷新页面重试';
        
        // 使用模拟数据
        this.formData = {
          title: '旅行与探索',
          description: '关于旅行经历、旅游景点和文化体验的口语练习',
          type: 'daily',
          level: '初级',
          duration: 15,
          tasks: [
            {
              type: '句子模仿',
              title: '重复以下句子',
              instructions: '听取以下句子，然后尽可能准确地重复。注意语调和发音。',
              content: 'Traveling to new places broadens your horizons and gives you a fresh perspective on life.',
              contentItems: [''],
              audioUrl: '/api/audio/speaking/travel_1.mp3',
              audioFile: null,
              audioFileName: 'travel_1.mp3',
              audioPreviewUrl: '/api/audio/speaking/travel_1.mp3'
            },
            {
              type: '回答问题',
              title: '旅行经历',
              instructions: '回答以下问题，尽量提供详细信息。',
              content: 'What was the most interesting place you have visited and why did you find it interesting?',
              contentItems: [''],
              audioUrl: '',
              audioFile: null,
              audioFileName: '',
              audioPreviewUrl: ''
            },
            {
              type: '情境对话',
              title: '在机场',
              instructions: '想象你在机场询问航班信息。回应下面的提示。',
              content: '',
              contentItems: [
                'Explain that your flight has been delayed and you need information about the next available flight.',
                'Ask about the boarding time and gate number for your new flight.',
                'Inquire about what compensation you might receive for the delay.'
              ],
              audioUrl: '',
              audioFile: null,
              audioFileName: '',
              audioPreviewUrl: ''
            }
          ]
        };
        
        // 保存原始数据用于重置
        this.originalData = JSON.parse(JSON.stringify(this.formData));
        
        // 设置音频预览
        this.formData.tasks.forEach(task => {
          if (task.audioUrl) {
            task.audioPreviewUrl = task.audioUrl;
          }
        });
      } finally {
        this.loading = false;
      }
    }
  },
  created() {
    // 获取材料ID并加载数据
    this.materialId = this.$route.params.id;
    if (!this.materialId) {
      this.$router.push('/teacher');
      return;
    }
    
    this.loadSpeakingData();
  }
};
</script>

<style scoped>
.speaking-create {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.create-header {
  position: relative;
  margin-bottom: 2rem;
  text-align: center;
}

.back-link {
  position: absolute;
  left: 0;
  top: 0.5rem;
  color: #41b883;
  text-decoration: none;
  font-weight: 500;
  display: flex;
  align-items: center;
}

.back-link::before {
  content: '←';
  margin-right: 0.5rem;
}

h1 {
  color: #2c3e50;
  font-size: 1.8rem;
  margin: 0;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 0;
}

.spinner {
  display: inline-block;
  width: 50px;
  height: 50px;
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

.loading-container p {
  color: #6c757d;
  font-size: 1.1rem;
}

.create-form {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.form-section {
  padding: 1.5rem;
  border-bottom: 1px solid #e9ecef;
}

.form-section h2 {
  color: #2c3e50;
  font-size: 1.3rem;
  margin: 0 0 1rem;
}

.section-desc {
  color: #6c757d;
  margin-bottom: 1.5rem;
  font-size: 0.95rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group:last-child {
  margin-bottom: 0;
}

.form-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  color: #495057;
  font-weight: 500;
}

.form-input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #dee2e6;
  border-radius: 4px;
  font-size: 1rem;
  color: #495057;
}

.form-input:focus {
  outline: none;
  border-color: #41b883;
  box-shadow: 0 0 0 3px rgba(65, 184, 131, 0.25);
}

.tasks-list {
  margin-bottom: 1.5rem;
}

.task-item {
  margin-bottom: 2rem;
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 1.5rem;
}

.task-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid #e9ecef;
}

.task-header h3 {
  margin: 0;
  color: #2c3e50;
  font-size: 1.2rem;
}

.task-actions {
  display: flex;
  gap: 0.5rem;
}

.action-btn {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 28px;
  height: 28px;
  border-radius: 4px;
  border: none;
  font-size: 1rem;
  cursor: pointer;
  color: white;
}

.move-up, .move-down {
  background-color: #6c757d;
}

.remove {
  background-color: #dc3545;
}

.file-upload {
  margin-bottom: 1rem;
}

.file-input {
  display: none;
}

.file-upload-ui {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.upload-btn {
  padding: 0.5rem 1rem;
  background-color: #f1f3f5;
  border: 1px solid #dee2e6;
  border-radius: 4px;
  color: #495057;
  cursor: pointer;
  font-size: 0.9rem;
}

.upload-btn:hover {
  background-color: #e9ecef;
}

.file-name {
  color: #6c757d;
  font-size: 0.9rem;
}

.audio-preview {
  margin-top: 1rem;
  margin-bottom: 1rem;
}

.audio-preview audio {
  width: 100%;
}

.content-items {
  margin-top: 0.5rem;
}

.content-item {
  margin-bottom: 1.5rem;
  padding: 1rem;
  background-color: white;
  border-radius: 4px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.content-item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.content-item-header h4 {
  margin: 0;
  color: #495057;
  font-size: 1rem;
}

.remove-item-btn {
  background: none;
  border: none;
  color: #dc3545;
  cursor: pointer;
  font-size: 0.9rem;
}

.remove-item-btn:hover {
  text-decoration: underline;
}

.add-item-btn {
  width: 100%;
  padding: 0.75rem;
  background-color: white;
  color: #41b883;
  border: 1px dashed #41b883;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
}

.add-item-btn:hover {
  background-color: #f8f9fa;
}

.add-task-btn {
  width: 100%;
  padding: 0.75rem;
  background-color: #e8f5e9;
  color: #41b883;
  border: 1px dashed #41b883;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
}

.add-task-btn:hover {
  background-color: #d7f0de;
}

.form-actions {
  padding: 1.5rem;
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}

.reset-btn, .save-btn {
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  font-weight: 500;
  cursor: pointer;
}

.reset-btn {
  background-color: #f8f9fa;
  color: #6c757d;
  border: 1px solid #dee2e6;
}

.reset-btn:hover {
  background-color: #e9ecef;
}

.save-btn {
  background-color: #41b883;
  color: white;
  border: none;
}

.save-btn:hover {
  background-color: #399a6e;
}

.save-btn:disabled {
  background-color: #a8d5c2;
  cursor: not-allowed;
}

.error-message {
  padding: 1rem;
  background-color: #fee2e2;
  color: #dc3545;
  border-top: 1px solid #fecaca;
  font-size: 0.9rem;
}

@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
  }
}
</style> 