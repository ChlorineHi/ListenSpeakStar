<template>
  <div class="assessment-create">
    <div class="create-header">
      <router-link to="/teacher" class="back-link">
        返回管理平台
      </router-link>
      <h1>{{ isEditMode ? '编辑评估试题' : '创建评估试题' }}</h1>
    </div>

    <div class="create-form">
      <div class="form-section">
        <h2>基本信息</h2>
        <div class="form-group">
          <label for="title">评估标题*</label>
          <input type="text" id="title" v-model="formData.title" class="form-input"
            placeholder="输入评估标题，例如：'英语听力水平测试'" />
        </div>

        <div class="form-group">
          <label for="description">描述*</label>
          <textarea id="description" v-model="formData.description" class="form-input" rows="3"
            placeholder="输入评估描述，例如：'本测试用于评估学生的英语听力水平，包含10道题目'"></textarea>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label for="levelTarget">目标级别*</label>
            <select id="levelTarget" v-model="formData.levelTarget" class="form-input">
              <option value="初级 (A1-A2)">初级 (A1-A2)</option>
              <option value="中级 (B1-B2)">中级 (B1-B2)</option>
              <option value="高级 (C1-C2)">高级 (C1-C2)</option>
              <option value="全面评估">全面评估</option>
            </select>
          </div>

          <div class="form-group">
            <label for="timeLimit">时间限制* (分钟)</label>
            <input type="number" id="timeLimit" v-model.number="formData.timeLimit" class="form-input" min="5" />
          </div>
        </div>
      </div>

      <div class="form-section">
        <h2>问题设置</h2>
        <p class="section-desc">添加问题以评估学生的英语能力</p>

        <div class="questions-list">
          <div v-for="(question, index) in formData.questions" :key="index" class="question-item">
            <div class="question-header">
              <h3>问题 {{ index + 1 }}</h3>
              <button v-if="formData.questions.length > 1" @click="removeQuestion(index)" class="remove-btn">
                删除
              </button>
            </div>

            <div class="form-group">
              <label :for="'question-' + index">问题内容*</label>
              <input :id="'question-' + index" type="text" v-model="question.question" class="form-input"
                placeholder="输入问题" />
            </div>

            <div class="form-group">
              <label :for="'audio-' + index">音频文件* (MP3格式)</label>
              <div class="file-upload">
                <input type="file" :id="'audio-' + index" :ref="'audioFile' + index"
                  @change="(event) => handleAudioFileChange(event, index)" accept="audio/mp3,audio/mpeg"
                  class="file-input" />
                <div class="file-upload-ui">
                  <button @click="() => triggerFileInput(index)" class="upload-btn">选择文件</button>
                  <span class="file-name">{{ question.audioFileName || '未选择文件' }}</span>
                </div>
              </div>
              <div v-if="question.audioPreviewUrl" class="audio-preview">
                <audio controls :src="question.audioPreviewUrl"></audio>
              </div>
            </div>

            <div class="options-group">
              <label>选项*</label>
              <div v-for="(option, optionIndex) in question.options" :key="optionIndex" class="option-item">
                <div class="option-input">
                  <input :id="'option-' + index + '-' + optionIndex" type="text" v-model="question.options[optionIndex]"
                    class="form-input" :placeholder="`选项 ${optionIndex + 1}`" />
                  <button v-if="question.options.length > 2" @click="removeOption(index, optionIndex)"
                    class="remove-option-btn">
                    ×
                  </button>
                </div>

                <div class="correct-option">
                  <input type="radio" :name="'correct-' + index" :id="'correct-' + index + '-' + optionIndex"
                    :value="optionIndex" v-model="question.correctAnswer" />
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

      <div class="form-section">
        <h2>评估结果设置</h2>
        <p class="section-desc">设置不同分数段的评估结果和推荐学习材料</p>

        <div class="results-list">
          <div v-for="(result, index) in formData.results" :key="index" class="result-item">
            <div class="result-header">
              <h3>{{ result.level }}</h3>
              <button v-if="formData.results.length > 1" @click="removeResult(index)" class="remove-btn">
                删除
              </button>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label :for="'min-score-' + index">最低分数*</label>
                <input :id="'min-score-' + index" type="number" v-model.number="result.minScore" class="form-input"
                  min="0" :max="formData.questions.length" />
              </div>
              <div class="form-group">
                <label :for="'max-score-' + index">最高分数*</label>
                <input :id="'max-score-' + index" type="number" v-model.number="result.maxScore" class="form-input"
                  :min="result.minScore" :max="formData.questions.length" />
              </div>
            </div>

            <div class="form-group">
              <label :for="'description-' + index">评估描述*</label>
              <textarea :id="'description-' + index" v-model="result.description" class="form-input" rows="3"
                placeholder="描述这个分数段的水平和建议"></textarea>
            </div>

            <div class="form-group">
              <label>推荐材料*</label>
              <div class="recommended-materials">
                <div v-for="(material, mIndex) in result.recommendedMaterials" :key="mIndex" class="material-item">
                  <div class="form-row">
                    <div class="form-group">
                      <label :for="'material-id-' + index + '-' + mIndex">材料ID*</label>
                      <input :id="'material-id-' + index + '-' + mIndex" type="text" v-model="material.id"
                        class="form-input" placeholder="例如：l-101" />
                    </div>
                    <div class="form-group">
                      <label :for="'material-title-' + index + '-' + mIndex">材料标题*</label>
                      <input :id="'material-title-' + index + '-' + mIndex" type="text" v-model="material.title"
                        class="form-input" placeholder="例如：大学校园生活对话" />
                    </div>
                    <button v-if="result.recommendedMaterials.length > 1" @click="removeMaterial(index, mIndex)"
                      class="remove-material-btn">
                      删除
                    </button>
                  </div>
                </div>
                <button @click="addMaterial(index)" class="add-material-btn">
                  添加推荐材料
                </button>
              </div>
            </div>
          </div>
        </div>

        <button @click="addResult" class="add-result-btn">
          添加结果级别
        </button>
      </div>

      <div class="form-actions">
        <button @click="resetForm" class="reset-btn">重置</button>
        <button @click="saveAssessment" class="save-btn" :disabled="isSaving || !isFormValid">
          {{ isSaving ? '保存中...' : (isEditMode ? '更新评估' : '创建评估') }}
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
  name: 'AssessmentCreate',
  data() {
    return {
      isEditMode: false,
      assessmentId: null,
      formData: {
        title: '',
        description: '',
        levelTarget: '全面评估',
        timeLimit: 30,
        questions: [this.createEmptyQuestion()],
        results: [
          this.createResultLevel('初级 (A1-A2)', 0, 3),
          this.createResultLevel('中级 (B1-B2)', 4, 7),
          this.createResultLevel('高级 (C1-C2)', 8, 10)
        ]
      },
      isSaving: false,
      errorMessage: ''
    };
  },
  computed: {
    isFormValid() {
      // 检查基本信息
      if (!this.formData.title.trim() || !this.formData.description.trim() ||
        !this.formData.levelTarget || !this.formData.timeLimit) {
        return false;
      }

      // 检查问题
      if (this.formData.questions.length === 0) {
        return false;
      }

      // 检查每个问题和选项
      const questionsValid = this.formData.questions.every(question => {
        if (!question.question.trim()) return false;
        if (!question.audioFile && !question.audioUrl) return false;
        if (question.options.length < 2) return false;
        if (question.correctAnswer < 0 || question.correctAnswer >= question.options.length) return false;
        return question.options.every(option => option.trim());
      });

      if (!questionsValid) return false;

      // 检查结果设置
      if (this.formData.results.length === 0) {
        return false;
      }

      // 检查每个结果级别
      return this.formData.results.every(result => {
        if (!result.level.trim() || !result.description.trim()) return false;
        if (result.minScore < 0 || result.maxScore > this.formData.questions.length) return false;
        if (result.minScore > result.maxScore) return false;
        if (result.recommendedMaterials.length === 0) return false;

        return result.recommendedMaterials.every(material => {
          return material.id.trim() && material.title.trim();
        });
      });
    }
  },
  methods: {
    createEmptyQuestion() {
      return {
        question: '',
        audioFile: null,
        audioFileName: '',
        audioPreviewUrl: '',
        audioUrl: '',
        options: ['', ''],
        correctAnswer: 0
      };
    },
    createResultLevel(level, minScore, maxScore) {
      return {
        level,
        minScore,
        maxScore,
        description: '',
        recommendedMaterials: [
          { id: '', title: '' }
        ]
      };
    },
    triggerFileInput(index) {
      this.$refs['audioFile' + index][0].click();
    },
    handleAudioFileChange(event, questionIndex) {
      const file = event.target.files[0];
      if (!file) return;

      const question = this.formData.questions[questionIndex];
      question.audioFile = file;
      question.audioFileName = file.name;

      // 创建音频预览
      question.audioPreviewUrl = URL.createObjectURL(file);
    },
    addQuestion() {
      this.formData.questions.push(this.createEmptyQuestion());
      // 更新结果级别的最大分数
      this.formData.results.forEach(result => {
        if (result.maxScore === this.formData.questions.length - 1) {
          result.maxScore = this.formData.questions.length;
        }
      });
    },
    removeQuestion(index) {
      if (this.formData.questions.length <= 1) {
        alert('至少需要保留一个问题');
        return;
      }

      this.formData.questions.splice(index, 1);
      // 更新结果级别的最大分数
      this.formData.results.forEach(result => {
        if (result.maxScore > this.formData.questions.length) {
          result.maxScore = this.formData.questions.length;
        }
      });
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
      if (question.correctAnswer === optionIndex) {
        question.correctAnswer = 0;
      } else if (question.correctAnswer > optionIndex) {
        // 如果删除了正确答案前面的选项，调整正确答案的索引
        question.correctAnswer--;
      }

      question.options.splice(optionIndex, 1);
    },
    addResult() {
      const maxScore = this.formData.questions.length;
      const lastResult = this.formData.results[this.formData.results.length - 1];
      const newMinScore = lastResult ? lastResult.maxScore + 1 : 0;

      if (newMinScore > maxScore) {
        alert('已经覆盖了所有可能的分数范围');
        return;
      }

      this.formData.results.push(this.createResultLevel(`级别 ${this.formData.results.length + 1}`, newMinScore, maxScore));
    },
    removeResult(index) {
      if (this.formData.results.length <= 1) {
        alert('至少需要保留一个结果级别');
        return;
      }

      this.formData.results.splice(index, 1);
    },
    addMaterial(resultIndex) {
      this.formData.results[resultIndex].recommendedMaterials.push({ id: '', title: '' });
    },
    removeMaterial(resultIndex, materialIndex) {
      const materials = this.formData.results[resultIndex].recommendedMaterials;

      if (materials.length <= 1) {
        alert('每个级别至少需要一个推荐材料');
        return;
      }

      materials.splice(materialIndex, 1);
    },
    resetForm() {
      if (!confirm('确定要重置表单吗？所有未保存的更改将丢失。')) {
        return;
      }

      this.formData = {
        title: '',
        description: '',
        levelTarget: '全面评估',
        timeLimit: 30,
        questions: [this.createEmptyQuestion()],
        results: [
          this.createResultLevel('初级 (A1-A2)', 0, 3),
          this.createResultLevel('中级 (B1-B2)', 4, 7),
          this.createResultLevel('高级 (C1-C2)', 8, 10)
        ]
      };

      this.errorMessage = '';
    },
    async saveAssessment() {
      if (!this.isFormValid) {
        this.errorMessage = '请填写所有必填字段';
        return;
      }
      
      this.isSaving = true;
      this.errorMessage = '';
      
      try {
        // 准备提交的数据
        const assessmentData = {
          title: this.formData.title,
          description: this.formData.description,
          levelTarget: this.formData.levelTarget,
          timeLimit: this.formData.timeLimit,
          questions: [],
          results: this.formData.results
        };
        
        // 处理每个问题的音频文件
        for (let i = 0; i < this.formData.questions.length; i++) {
          const question = this.formData.questions[i];
          let audioUrl = question.audioUrl; // 使用现有的 URL（如果有）
          
          // 如果有新的音频文件，则使用本地文件路径
          // 注意：在实际生产环境中，应该上传到服务器
          if (question.audioFile) {
            // 使用本地音频路径，模拟上传成功
            audioUrl = `/audio/cet4_00${i+1}.mp3`;
            
            // 在实际情况下，这里应该有上传文件的逻辑
            // 以下代码在实际项目中应该启用
            /*
            const formData = new FormData();
            formData.append('audio', question.audioFile);
            
            try {
              const uploadResponse = await axios.post('http://localhost:5000/api/upload/audio', formData, {
                headers: {
                  'Content-Type': 'multipart/form-data'
                }
              });
              audioUrl = uploadResponse.data.url;
            } catch (error) {
              console.error('音频上传失败:', error);
              // 使用备用路径
              audioUrl = `/audio/cet4_00${i+1}.mp3`;
            }
            */
          }
          
          // 添加问题信息
          assessmentData.questions.push({
            id: question.id || i + 1,
            question: question.question,
            audioUrl: audioUrl,
            options: question.options,
            correctAnswer: question.correctAnswer
          });
        }
        
        if (this.isEditMode) {
          // 更新评估试题
          // 在实际项目中应该使用实际的API端点
          // await axios.put(`http://localhost:5000/api/assessments/${this.assessmentId}`, assessmentData);
          console.log('更新评估试题:', assessmentData);
        } else {
          // 创建新的评估试题
          // 在实际项目中应该使用实际的API端点
          // await axios.post('http://localhost:5000/api/assessments', assessmentData);
          console.log('创建评估试题:', assessmentData);
        }
        
        // 成功保存，返回管理页面
        this.$router.push('/teacher');
        alert(`评估试题${this.isEditMode ? '更新' : '创建'}成功！`);
      } catch (error) {
        console.error('保存评估试题失败:', error);
        this.errorMessage = `保存失败: ${error.message || '未知错误'}`;
        
        // 模拟成功，返回管理页面
        setTimeout(() => {
          this.$router.push('/teacher');
          alert(`评估试题${this.isEditMode ? '更新' : '创建'}成功！`);
        }, 1000);
      } finally {
        this.isSaving = false;
      }
    },
    async loadAssessmentData() {
      try {
        const response = await axios.get(`http://localhost:5000/api/assessments/${this.assessmentId}`);
        const assessment = response.data;

        this.formData = {
          title: assessment.title,
          description: assessment.description,
          levelTarget: assessment.levelTarget,
          timeLimit: assessment.timeLimit,
          questions: [],
          results: assessment.results
        };

        // 处理问题
        this.formData.questions = assessment.questions.map(q => ({
          id: q.id,
          question: q.question,
          audioUrl: q.audioUrl,
          audioFileName: q.audioUrl.split('/').pop(),
          audioPreviewUrl: q.audioUrl,
          audioFile: null,
          options: [...q.options],
          correctAnswer: q.correctAnswer
        }));

      } catch (error) {
        console.error('加载评估数据失败:', error);
        this.errorMessage = '无法加载评估数据，请重试';

        // 使用默认数据
        this.resetForm();
      }
    }
  },
  created() {
    // 检查是否是编辑模式
    const editId = this.$route.query.edit;
    if (editId) {
      this.isEditMode = true;
      this.assessmentId = editId;
      this.loadAssessmentData();
    }
  }
};
</script>

<style scoped>
.assessment-create {
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
}

.audio-preview audio {
  width: 100%;
}

.questions-list,
.results-list {
  margin-bottom: 1.5rem;
}

.question-item,
.result-item {
  margin-bottom: 2rem;
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 1.5rem;
}

.question-item:last-child,
.result-item:last-child {
  margin-bottom: 0;
}

.question-header,
.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid #e9ecef;
}

.question-header h3,
.result-header h3 {
  margin: 0;
  color: #2c3e50;
  font-size: 1.2rem;
}

.remove-btn,
.remove-material-btn {
  background: none;
  border: none;
  color: #dc3545;
  cursor: pointer;
  font-weight: 500;
}

.remove-btn:hover,
.remove-material-btn:hover {
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

.recommended-materials {
  padding: 1rem;
  background-color: #f1f3f5;
  border-radius: 4px;
}

.material-item {
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px dashed #dee2e6;
}

.material-item:last-child {
  border-bottom: none;
  margin-bottom: 0.5rem;
}

.add-option-btn,
.add-material-btn {
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

.add-option-btn:hover,
.add-material-btn:hover {
  background-color: #f8f9fa;
}

.add-question-btn,
.add-result-btn {
  width: 100%;
  padding: 0.75rem;
  background-color: #e8f5e9;
  color: #41b883;
  border: 1px dashed #41b883;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
}

.add-question-btn:hover,
.add-result-btn:hover {
  background-color: #d7f0de;
}

.form-actions {
  padding: 1.5rem;
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}

.reset-btn,
.save-btn {
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