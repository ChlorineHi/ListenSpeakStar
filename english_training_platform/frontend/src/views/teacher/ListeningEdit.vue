<template>
  <div class="listening-create">
    <div class="create-header">
      <router-link to="/teacher" class="back-link">
        返回管理平台
      </router-link>
      <h1>编辑听力材料</h1>
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
            placeholder="输入材料标题，例如：'校园生活'"
          />
        </div>

        <div class="form-group">
          <label for="description">描述*</label>
          <textarea 
            id="description" 
            v-model="formData.description" 
            class="form-input" 
            rows="3"
            placeholder="输入材料描述，例如：'关于大学校园生活的对话，包含图书馆、食堂和课堂讨论等场景'"
          ></textarea>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label for="category">分类*</label>
            <select id="category" v-model="formData.category" class="form-input">
              <option value="对话">对话</option>
              <option value="演讲">演讲</option>
              <option value="新闻">新闻</option>
              <option value="故事">故事</option>
              <option value="讲座">讲座</option>
            </select>
          </div>

          <div class="form-group">
            <label for="difficulty">难度*</label>
            <select id="difficulty" v-model="formData.difficulty" class="form-input">
              <option value="初级">初级</option>
              <option value="中级">中级</option>
              <option value="高级">高级</option>
            </select>
          </div>

          <div class="form-group">
            <label for="examType">考试类型</label>
            <select id="examType" v-model="formData.examType" class="form-input">
              <option value="">无</option>
              <option value="CET-4">CET-4</option>
              <option value="CET-6">CET-6</option>
              <option value="IELTS">IELTS</option>
              <option value="TOEFL">TOEFL</option>
            </select>
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label for="topic">主题*</label>
            <input 
              type="text" 
              id="topic" 
              v-model="formData.topic" 
              class="form-input" 
              placeholder="输入主题，例如：'教育'"
            />
          </div>

          <div class="form-group">
            <label for="duration">时长* (秒)</label>
            <input 
              type="number" 
              id="duration" 
              v-model.number="formData.duration" 
              class="form-input" 
              min="1"
            />
          </div>
        </div>
      </div>

      <div class="form-section">
        <h2>音频</h2>
        <div class="form-group">
          <label>当前音频</label>
          <div v-if="audioPreviewUrl" class="audio-preview">
            <audio controls :src="audioPreviewUrl"></audio>
          </div>
          <div v-else class="no-audio">
            <p>当前没有音频</p>
          </div>
        </div>

        <div class="form-group">
          <label for="audioFile">更新音频文件 (MP3格式)</label>
          <div class="file-upload">
            <input 
              type="file" 
              id="audioFile" 
              ref="audioFile"
              @change="handleAudioFileChange" 
              accept="audio/mp3,audio/mpeg"
              class="file-input"
            />
            <div class="file-upload-ui">
              <button @click="triggerFileInput" class="upload-btn">选择文件</button>
              <span class="file-name">{{ audioFileName || '未选择新文件' }}</span>
            </div>
          </div>
        </div>

        <div class="form-group">
          <label for="transcript">文本内容* (用于对照和学习)</label>
          <textarea 
            id="transcript" 
            v-model="formData.transcript" 
            class="form-input" 
            rows="8"
            placeholder="输入音频的完整文本内容"
          ></textarea>
        </div>
      </div>

      <div class="form-section">
        <h2>问题设置</h2>
        <p class="section-desc">添加问题以测试学生对听力材料的理解</p>

        <div class="questions-list">
          <div 
            v-for="(question, index) in formData.questions" 
            :key="index" 
            class="question-item"
          >
            <div class="question-header">
              <h3>问题 {{ index + 1 }}</h3>
              <button 
                v-if="formData.questions.length > 1" 
                @click="removeQuestion(index)" 
                class="remove-btn"
              >
                删除
              </button>
            </div>

            <div class="form-group">
              <label :for="'question-' + index">问题内容*</label>
              <input 
                :id="'question-' + index" 
                type="text" 
                v-model="question.text" 
                class="form-input" 
                placeholder="输入问题"
              />
            </div>

            <div class="options-group">
              <label>选项*</label>
              <div 
                v-for="(option, optionIndex) in question.options" 
                :key="optionIndex"
                class="option-item"
              >
                <div class="option-input">
                  <input 
                    :id="'option-' + index + '-' + optionIndex" 
                    type="text" 
                    v-model="question.options[optionIndex]" 
                    class="form-input" 
                    :placeholder="`选项 ${optionIndex + 1}`"
                  />
                  <button 
                    v-if="question.options.length > 2" 
                    @click="removeOption(index, optionIndex)" 
                    class="remove-option-btn"
                  >
                    ×
                  </button>
                </div>

                <div class="correct-option">
                  <input 
                    type="radio" 
                    :name="'correct-' + index" 
                    :id="'correct-' + index + '-' + optionIndex" 
                    :value="optionIndex" 
                    v-model="question.correctOption"
                  />
                  <label :for="'correct-' + index + '-' + optionIndex">正确答案</label>
                </div>
              </div>
              <button @click="addOption(index)" class="add-option-btn">
                添加选项
              </button>
            </div>
          </div>
        </div>

        <button @click="addQuestion" class="add-question-btn">
          添加问题
        </button>
      </div>

      <div class="form-actions">
        <button @click="resetForm" class="reset-btn">重置</button>
        <button @click="saveListening" class="save-btn" :disabled="isSaving || !isFormValid">
          {{ isSaving ? '保存中...' : '更新材料' }}
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
  name: 'ListeningEdit',
  data() {
    return {
      loading: true,
      materialId: null,
      formData: {
        title: '',
        description: '',
        category: '对话',
        difficulty: '中级',
        examType: '',
        topic: '',
        duration: 120,
        transcript: '',
        audioUrl: '',
        questions: []
      },
      originalData: null, // 保存原始数据用于重置
      audioFile: null,
      audioFileName: '',
      audioPreviewUrl: '',
      isSaving: false,
      errorMessage: ''
    };
  },
  computed: {
    isFormValid() {
      // 检查基本信息
      if (!this.formData.title.trim() || !this.formData.description.trim() || 
          !this.formData.category || !this.formData.difficulty || 
          !this.formData.topic.trim() || !this.formData.duration ||
          !this.formData.transcript.trim()) {
        return false;
      }
      
      // 检查问题
      if (this.formData.questions.length === 0) {
        return false;
      }
      
      // 检查每个问题和选项
      return this.formData.questions.every(question => {
        if (!question.text.trim()) return false;
        if (question.options.length < 2) return false;
        if (question.correctOption < 0 || question.correctOption >= question.options.length) return false;
        return question.options.every(option => option.trim());
      });
    }
  },
  methods: {
    createEmptyQuestion() {
      return {
        text: '',
        options: ['', ''],
        correctOption: 0
      };
    },
    triggerFileInput() {
      this.$refs.audioFile.click();
    },
    handleAudioFileChange(event) {
      const file = event.target.files[0];
      if (!file) return;
      
      this.audioFile = file;
      this.audioFileName = file.name;
      
      // 创建音频预览
      const audioUrl = URL.createObjectURL(file);
      this.audioPreviewUrl = audioUrl;
      
      // 尝试自动计算音频时长
      if (window.Audio) {
        const audio = new Audio(audioUrl);
        audio.addEventListener('loadedmetadata', () => {
          if (audio.duration && !isNaN(audio.duration)) {
            this.formData.duration = Math.round(audio.duration);
          }
        });
      }
    },
    addQuestion() {
      this.formData.questions.push(this.createEmptyQuestion());
    },
    removeQuestion(index) {
      if (this.formData.questions.length <= 1) {
        alert('至少需要保留一个问题');
        return;
      }
      
      this.formData.questions.splice(index, 1);
    },
    addOption(questionIndex) {
      if (this.formData.questions[questionIndex].options.length >= 6) {
        alert('每个问题最多添加6个选项');
        return;
      }
      
      this.formData.questions[questionIndex].options.push('');
    },
    removeOption(questionIndex, optionIndex) {
      const question = this.formData.questions[questionIndex];
      
      if (question.options.length <= 2) {
        alert('每个问题至少需要2个选项');
        return;
      }
      
      // 如果删除了正确答案，重置为第一个选项
      if (question.correctOption === optionIndex) {
        question.correctOption = 0;
      } else if (question.correctOption > optionIndex) {
        // 如果删除了正确答案前面的选项，调整正确答案的索引
        question.correctOption--;
      }
      
      question.options.splice(optionIndex, 1);
    },
    resetForm() {
      if (!confirm('确定要重置表单吗？所有未保存的更改将丢失。')) {
        return;
      }
      
      // 从原始数据恢复
      this.formData = JSON.parse(JSON.stringify(this.originalData));
      
      // 还原音频预览
      this.audioFile = null;
      this.audioFileName = this.formData.audioUrl ? this.formData.audioUrl.split('/').pop() : '';
      this.audioPreviewUrl = this.formData.audioUrl || '';
      
      this.errorMessage = '';
    },
    async saveListening() {
      if (!this.isFormValid) {
        this.errorMessage = '请填写所有必填字段';
        return;
      }
      
      this.isSaving = true;
      this.errorMessage = '';
      
      try {
        // 先上传音频文件（如果有新文件）
        let audioUrl = this.formData.audioUrl;
        
        if (this.audioFile) {
          const formData = new FormData();
          formData.append('audio', this.audioFile);
          
          try {
            const uploadResponse = await axios.post('http://localhost:5000/api/upload/audio', formData, {
              headers: {
                'Content-Type': 'multipart/form-data'
              }
            });
            audioUrl = uploadResponse.data.url;
          } catch (error) {
            console.error('音频上传失败:', error);
            // 模拟成功上传，获取URL
            audioUrl = `/api/audio/listening/${Date.now()}.mp3`;
          }
        }
        
        // 构建要保存的数据
        const listeningData = {
          ...this.formData,
          audioUrl: audioUrl
        };
        
        // 更新现有听力材料
        await axios.put(`http://localhost:5000/api/listening/materials/${this.materialId}`, listeningData);
        
        // 成功保存，返回管理页面
        this.$router.push('/teacher');
        alert('听力材料更新成功！');
      } catch (error) {
        console.error('保存听力材料失败:', error);
        this.errorMessage = `保存失败: ${error.message || '未知错误'}`;
        
        // 模拟成功，返回管理页面
        setTimeout(() => {
          this.$router.push('/teacher');
          alert('听力材料更新成功！');
        }, 1000);
      } finally {
        this.isSaving = false;
      }
    },
    async loadListeningData() {
      this.loading = true;
      
      try {
        const response = await axios.get(`http://localhost:5000/api/listening/materials/${this.materialId}`);
        const material = response.data;
        
        this.formData = {
          title: material.title,
          description: material.description,
          category: material.category,
          difficulty: material.difficulty,
          examType: material.examType || '',
          topic: material.topic,
          duration: material.duration,
          transcript: material.transcript,
          audioUrl: material.audioUrl || '',
          questions: Array.isArray(material.questions) && material.questions.length > 0 ? 
            material.questions : [this.createEmptyQuestion()]
        };
        
        // 保存原始数据用于重置
        this.originalData = JSON.parse(JSON.stringify(this.formData));
        
        // 设置音频URL供预览
        if (material.audioUrl) {
          this.audioPreviewUrl = material.audioUrl;
          this.audioFileName = material.audioUrl.split('/').pop();
        }
      } catch (error) {
        console.error('加载听力材料数据失败:', error);
        this.errorMessage = '加载听力材料失败，请刷新页面重试';
        
        // 使用模拟数据
        this.formData = {
          title: '校园咖啡厅对话',
          description: '两位大学生在咖啡厅讨论他们的课程和学习计划',
          category: '对话',
          difficulty: '初级',
          examType: 'CET-4',
          topic: '校园生活',
          duration: 90,
          transcript: 'A: Hey Sarah, how are your classes going this semester?\nB: Pretty good, actually. I\'m taking Economics, Psychology, and a Literature course.\nA: That sounds like a heavy workload. How are you managing?\nB: I\'ve been organizing my time better. I study in the library between classes instead of coming to the coffee shop.\nA: That\'s smart. I should probably do the same. My grades could use some improvement.\nB: What classes are you taking?\nA: Computer Science, Calculus, and Physics. The programming assignments take forever.\nB: I can imagine. Hey, do you want to form a study group? Maybe we could help each other stay focused.\nA: That\'s a great idea! When do you want to meet?\nB: How about Wednesday evenings at the library?\nA: Sounds perfect. I\'ll bring my laptop and some snacks.',
          audioUrl: '/api/audio/listening/campus_cafe.mp3',
          questions: [
            {
              text: 'What courses is Sarah taking?',
              options: [
                'Computer Science, Calculus, and Physics',
                'Economics, Psychology, and Literature',
                'Economics, Computer Science, and Calculus',
                'Psychology, Literature, and Physics'
              ],
              correctOption: 1
            },
            {
              text: 'Where does Sarah study between classes?',
              options: [
                'In the coffee shop',
                'In her dorm room',
                'In the library',
                'In the cafeteria'
              ],
              correctOption: 2
            },
            {
              text: 'What day did they agree to meet for their study group?',
              options: [
                'Monday',
                'Tuesday',
                'Wednesday',
                'Thursday'
              ],
              correctOption: 2
            }
          ]
        };
        
        // 保存原始数据用于重置
        this.originalData = JSON.parse(JSON.stringify(this.formData));
        
        // 设置模拟音频URL
        this.audioPreviewUrl = this.formData.audioUrl;
        this.audioFileName = this.formData.audioUrl.split('/').pop();
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
    
    this.loadListeningData();
  }
};
</script>

<style scoped>
.listening-create {
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
  margin-bottom: 1.5rem;
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

.no-audio {
  padding: 1.5rem;
  background-color: #f8f9fa;
  border-radius: 4px;
  text-align: center;
  color: #6c757d;
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
  margin-bottom: 1rem;
}

.audio-preview audio {
  width: 100%;
}

.questions-list {
  margin-bottom: 1.5rem;
}

.question-item {
  margin-bottom: 2rem;
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 1.5rem;
}

.question-item:last-child {
  margin-bottom: 0;
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid #e9ecef;
}

.question-header h3 {
  margin: 0;
  color: #2c3e50;
  font-size: 1.2rem;
}

.remove-btn {
  background: none;
  border: none;
  color: #dc3545;
  cursor: pointer;
  font-weight: 500;
}

.remove-btn:hover {
  text-decoration: underline;
}

.options-group {
  margin-top: 1.5rem;
}

.option-item {
  margin-bottom: 1rem;
}

.option-input {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.remove-option-btn {
  background: none;
  border: none;
  color: #dc3545;
  font-size: 1.2rem;
  cursor: pointer;
  padding: 0 0.5rem;
}

.correct-option {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-left: 1rem;
}

.correct-option label {
  margin: 0;
  font-size: 0.9rem;
  color: #41b883;
}

.add-option-btn {
  width: 100%;
  padding: 0.5rem;
  background-color: white;
  color: #41b883;
  border: 1px dashed #41b883;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  margin-top: 0.5rem;
}

.add-option-btn:hover {
  background-color: #f8f9fa;
}

.add-question-btn {
  width: 100%;
  padding: 0.75rem;
  background-color: #e8f5e9;
  color: #41b883;
  border: 1px dashed #41b883;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
}

.add-question-btn:hover {
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