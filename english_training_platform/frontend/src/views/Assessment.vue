<template>
  <div class="assessment-page">
    <h1>英语水平评估</h1>
    <div class="assessment-container">
      <div v-if="isLoading" class="loading-section">
        <p>加载中...</p>
      </div>

      <div v-else-if="error" class="error-section">
        <p>{{ error }}</p>
        <button @click="fetchAssessmentData" class="primary-btn">重试</button>
      </div>

      <div v-else-if="!assessmentStarted" class="start-section">
        <p>通过这个测试，我们将评估您的英语听力水平，并为您推荐适合的学习材料。</p>
        <p class="assessment-info" v-if="questions.length > 0">
          本次评估由教师发布，共 {{ questions.length }} 道题目。
        </p>
        <button @click="startAssessment" class="primary-btn">开始评估</button>
      </div>

      <div v-else-if="assessmentStarted && !assessmentCompleted" class="question-section">
        <h2>问题 {{ currentQuestionIndex + 1 }}/{{ questions.length }}</h2>
        <div class="audio-player">
          <button @click="playAudio" class="play-btn">
            <span v-if="isPlaying">暂停</span>
            <span v-else>播放</span>
          </button>
          <div class="progress-bar">
            <div class="progress" :style="{ width: audioProgress + '%' }"></div>
          </div>
          <div class="time-display">
            {{ formatTime(currentTime) }} / {{ formatTime(duration) }}
          </div>
        </div>

        <div class="question-content">
          <p>{{ currentQuestion.question }}</p>
          <div class="options">
            <div v-for="(option, index) in currentQuestion.options" :key="index" class="option"
              :class="{ selected: selectedOption === index }" @click="selectOption(index)">
              <span class="option-label">{{ String.fromCharCode(65 + index) }}</span>
              <span class="option-text">{{ option }}</span>
            </div>
          </div>
        </div>

        <div class="navigation-buttons">
          <button @click="previousQuestion" class="secondary-btn" :disabled="currentQuestionIndex === 0">
            上一题
          </button>
          <button @click="nextQuestion" class="primary-btn" :disabled="selectedOption === null">
            {{ currentQuestionIndex === questions.length - 1 ? '完成评估' : '下一题' }}
          </button>
        </div>
      </div>

      <div v-else-if="assessmentCompleted && assessmentResult" class="result-section">
        <h2>评估结果</h2>
        <div class="result-card">
          <div class="level-indicator">
            <span class="level">{{ assessmentResult.level }}</span>
            <div class="score">得分: {{ assessmentResult.score }}/{{ assessmentResult.total }}</div>
          </div>
          <p>{{ assessmentResult.description }}</p>
          <div class="recommendations">
            <h3>推荐学习材料</h3>
            <ul>
              <li v-for="(material, index) in assessmentResult.recommendedMaterials" :key="index">
                <router-link :to="{ name: 'Listening', params: { id: material.id } }">
                  {{ material.title }}
                </router-link>
              </li>
            </ul>
          </div>
          <button @click="goToRecommendations" class="primary-btn">开始学习</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AudioService from '@/services/AudioService'
import MaterialService from '@/services/MaterialService'
import axios from 'axios'

export default {
  name: 'AssessmentView',
  data() {
    return {
      assessmentStarted: false,
      assessmentCompleted: false,
      currentQuestionIndex: 0,
      selectedOption: null,
      isPlaying: false,
      audioProgress: 0,
      currentTime: 0,
      duration: 0,
      questions: [],
      userAnswers: [],
      assessmentResult: null,
      isLoading: false,
      error: null,
      audioProgressInterval: null,
      assessmentMaterial: null,
      difficulty: 'CET4',
      useAgentRecommendation: true,
      agentRecommendationResult: null,
      isLoadingAgentRecommendation: false,
    };
  },
  computed: {
    currentQuestion() {
      return this.questions[this.currentQuestionIndex];
    }
  },
  created() {
    if (this.$route.query.difficulty) {
      this.difficulty = this.$route.query.difficulty;
    }
    this.fetchAssessmentData();
  },
  mounted() {
    this.setupAudioProgressUpdater();
  },
  beforeUnmount() {
    if (this.audioProgressInterval) {
      clearInterval(this.audioProgressInterval);
    }
    
    AudioService.pause();
  },
  methods: {
    setupAudioProgressUpdater() {
      this.audioProgressInterval = setInterval(() => {
        this.updateAudioProgress();
      }, 100);
    },
    updateAudioProgress() {
      if (AudioService.audio) {
        this.currentTime = AudioService.getCurrentTime();
        this.duration = AudioService.getDuration() || 0;
        this.audioProgress = AudioService.getProgress();
        this.isPlaying = AudioService.isPlaying;
      }
    },
    formatTime(seconds) {
      if (!seconds || isNaN(seconds)) return '00:00';
      const mins = Math.floor(seconds / 60);
      const secs = Math.floor(seconds % 60);
      return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    },
    async fetchAssessmentData() {
      this.isLoading = true;
      try {
        const materials = await MaterialService.getMaterialsByDifficulty(this.difficulty);
        
        if (materials && materials.length > 0) {
          const randomIndex = Math.floor(Math.random() * materials.length);
          this.assessmentMaterial = materials[randomIndex];
          
          const fullMaterial = await MaterialService.getMaterialById(this.assessmentMaterial.id);
          
          this.questions = fullMaterial.questions.map(q => ({
            id: q.id,
            question: q.question,
            options: q.options,
            correctAnswer: q.options.findIndex(opt => opt.startsWith(q.answer + '.')),
            audioUrl: fullMaterial.audio_url
          }));
        } else {
          throw new Error(`没有找到${this.difficulty}难度的评估材料`);
        }
        
        await new Promise(resolve => setTimeout(resolve, 500));
      } catch (error) {
        this.error = '获取评估材料失败，请稍后再试';
        console.error('获取评估材料出错:', error);
      } finally {
        this.isLoading = false;
      }
    },
    startAssessment() {
      if (this.questions.length === 0) {
        this.error = '当前没有可用的评估材料';
        return;
      }
      this.error = null;
      this.assessmentStarted = true;
      this.userAnswers = new Array(this.questions.length).fill(null);
      
      if (this.currentQuestion) {
        AudioService.setAudioSource(this.currentQuestion.audioUrl);
      }
    },
    selectOption(index) {
      this.selectedOption = index;
      this.userAnswers[this.currentQuestionIndex] = index;
    },
    playAudio() {
      if (AudioService.isPlaying) {
        AudioService.pause();
      } else {
        AudioService.setAudioSource(this.currentQuestion.audioUrl);
        AudioService.play().catch(error => {
          console.error('音频播放失败:', error);
          alert('音频播放失败，请确保音频文件存在并且格式正确。路径: ' + this.currentQuestion.audioUrl);
        });
      }
    },
    previousQuestion() {
      if (this.currentQuestionIndex > 0) {
        this.currentQuestionIndex--;
        this.selectedOption = this.userAnswers[this.currentQuestionIndex];
        this.resetAudio();
      }
    },
    nextQuestion() {
      if (this.currentQuestionIndex < this.questions.length - 1) {
        this.currentQuestionIndex++;
        this.selectedOption = this.userAnswers[this.currentQuestionIndex];
        this.resetAudio();
      } else {
        this.completeAssessment();
      }
    },
    resetAudio() {
      AudioService.pause();
      
      if (this.currentQuestion) {
        AudioService.setAudioSource(this.currentQuestion.audioUrl);
      }
      
      this.isPlaying = false;
      this.audioProgress = 0;
    },
    async completeAssessment() {
      this.isLoading = true;
      try {
        const correctAnswers = this.userAnswers.filter((answer, index) => 
          answer === this.questions[index].correctAnswer
        ).length;
        
        let level, description, recommendedMaterials;
        
        if (correctAnswers <= 3) {
          level = "初级 (A1-A2)";
          description = "您的英语听力水平处于初级阶段，建议加强基础听力训练和词汇积累。";
          recommendedMaterials = [
            { id: "l-101", title: "基础英语对话" },
            { id: "l-102", title: "日常生活英语" }
          ];
        } else if (correctAnswers <= 7) {
          level = "中级 (B1-B2)";
          description = "您具备基本的英语听力能力，能理解日常对话和简单的学术内容。您应该专注于提高理解速度和扩展词汇量。";
          recommendedMaterials = [
            { id: "l-203", title: "科技新闻报道" },
            { id: "l-204", title: "学术讨论" }
          ];
        } else {
          level = "高级 (C1-C2)";
          description = "您的英语听力能力很好，能够理解复杂的内容和学术讨论。建议继续提高专业领域词汇和理解能力。";
          recommendedMaterials = [
            { id: "l-305", title: "专业领域讨论" },
            { id: "l-306", title: "高级学术讲座" }
          ];
        }
        
        this.assessmentResult = {
          level,
          description,
          recommendedMaterials,
          score: correctAnswers,
          total: this.questions.length
        };
        
        this.assessmentCompleted = true;
      } catch (error) {
        this.error = '提交评估失败，请稍后再试';
        console.error('提交评估出错:', error);
      } finally {
        this.isLoading = false;
      }
    },
    goToRecommendations() {
      this.$router.push({ name: 'Listening' });
    },
    async submitAnswers() {
      this.isSubmitting = true;
      
      try {
        let correctCount = 0;
        const userAnswers = [];
        
        this.questions.forEach((section, sectionIndex) => {
          section.questions.forEach((question, questionIndex) => {
            const userAnswer = this.userAnswers[sectionIndex][questionIndex];
            const isCorrect = userAnswer === question.answer;
            
            if (isCorrect) {
              correctCount++;
            }
            
            userAnswers.push({
              material_id: section.id || `section_${sectionIndex}`,
              question_id: question.id || questionIndex + 1,
              user_answer: userAnswer,
              correct_answer: question.answer,
              is_correct: isCorrect,
              question_tags: question.tags || ["听力理解"],
              question_type: question.type || "选择题",
              question_content: question.question
            });
          });
        });
        
        const score = Math.round((correctCount / this.totalQuestions) * 100);
        
        this.assessmentResult = {
          score: correctCount,
          total: this.totalQuestions,
          percentage: score,
          level: this.determineLevel(score),
          description: this.generateDescription(score),
          recommendedMaterials: []
        };
        
        const apiEndpoint = this.useAgentRecommendation 
          ? '/api/recommendation/recommend'
          : '/api/listening/assessment/evaluate';
          
        const response = await axios.post(apiEndpoint, { 
          user_answers: userAnswers 
        });
        
        if (this.useAgentRecommendation) {
          this.agentRecommendationResult = response.data;
          
          if (response.data.recommendations && response.data.recommendations.length > 0) {
            const recommendedMaterials = [];
            for (const rec of response.data.recommendations) {
              try {
                const material = await MaterialService.getMaterialById(rec.id);
                if (material) {
                  recommendedMaterials.push({
                    ...material,
                    reason: rec.reason,
                    match_score: rec.match_score
                  });
                }
              } catch (error) {
                console.error(`获取推荐材料详情失败: ${rec.id}`, error);
                recommendedMaterials.push({
                  id: rec.id,
                  title: rec.title || `推荐材料 (${rec.id})`,
                  reason: rec.reason,
                  match_score: rec.match_score
                });
              }
            }
            this.assessmentResult.recommendedMaterials = recommendedMaterials;
          }
          
          if (response.data.weak_areas && response.data.weak_areas.length > 0) {
            this.assessmentResult.weakAreas = response.data.weak_areas;
            this.assessmentResult.strongAreas = response.data.strong_areas || [];
            this.assessmentResult.improvementSuggestions = response.data.improvement_suggestions || "";
            
            this.assessmentResult.description = `您的听力水平为${this.assessmentResult.level}。您在${response.data.weak_areas.join('、')}方面有待提高，而在${response.data.strong_areas.join('、')}方面表现较好。`;
          }
        } else {
          if (response.data.recommended_materials) {
            this.assessmentResult.recommendedMaterials = response.data.recommended_materials;
          }
          
          if (response.data.analysis) {
            this.assessmentResult.description = response.data.analysis;
          }
        }
      } catch (error) {
        console.error('提交答案失败', error);
        this.error = '评估失败，请稍后重试';
      } finally {
        this.isSubmitting = false;
        this.assessmentCompleted = true;
      }
    },
  }
};
</script>

<style scoped>
.assessment-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

h1 {
  text-align: center;
  margin-bottom: 2rem;
  color: #2c3e50;
}

.assessment-container {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 2rem;
}

.start-section {
  text-align: center;
}

.start-section p {
  margin-bottom: 1.5rem;
  font-size: 1.1rem;
  line-height: 1.6;
}

.question-section {
  margin-top: 1rem;
}

.audio-player {
  display: flex;
  align-items: center;
  margin: 1.5rem 0;
  background-color: #f8f9fa;
  border-radius: 4px;
  padding: 0.5rem 1rem;
}

.play-btn {
  background-color: #41b883;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 0.5rem 1rem;
  cursor: pointer;
  margin-right: 1rem;
  min-width: 80px;
}

.progress-bar {
  flex: 1;
  height: 8px;
  background-color: #e9ecef;
  border-radius: 4px;
  overflow: hidden;
  margin-right: 1rem;
}

.progress {
  height: 100%;
  background-color: #41b883;
  transition: width 0.1s linear;
}

.time-display {
  font-size: 0.8rem;
  color: #6c757d;
  min-width: 80px;
  text-align: right;
}

.question-content {
  margin-bottom: 1.5rem;
}

.question-content p {
  font-size: 1.1rem;
  margin-bottom: 1rem;
}

.options {
  display: grid;
  gap: 1rem;
}

.option {
  display: flex;
  align-items: center;
  padding: 0.75rem;
  border: 1px solid #dee2e6;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.option:hover {
  background-color: #f8f9fa;
}

.option.selected {
  background-color: #e8f5e9;
  border-color: #41b883;
}

.option-label {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 30px;
  height: 30px;
  background-color: #f1f3f5;
  border-radius: 50%;
  margin-right: 1rem;
  font-weight: bold;
}

.option.selected .option-label {
  background-color: #41b883;
  color: white;
}

.navigation-buttons {
  display: flex;
  justify-content: space-between;
  margin-top: 2rem;
}

.primary-btn,
.secondary-btn {
  padding: 0.5rem 1.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
}

.primary-btn {
  background-color: #41b883;
  color: white;
}

.primary-btn:disabled {
  background-color: #a8d5c2;
  cursor: not-allowed;
}

.secondary-btn {
  background-color: #e9ecef;
  color: #495057;
}

.secondary-btn:disabled {
  color: #adb5bd;
  cursor: not-allowed;
}

.result-section {
  text-align: center;
}

.result-card {
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 2rem;
  margin-top: 1.5rem;
}

.level-indicator {
  display: inline-block;
  margin-bottom: 1.5rem;
  text-align: center;
  width: 100%;
}

.level {
  display: inline-block;
  padding: 0.5rem 1.5rem;
  background-color: #41b883;
  color: white;
  border-radius: 20px;
  font-weight: bold;
  font-size: 1.2rem;
}

.score {
  margin-top: 0.5rem;
  font-size: 1.1rem;
  color: #41b883;
  font-weight: bold;
}

.recommendations {
  margin: 1.5rem 0;
  text-align: left;
}

.recommendations h3 {
  margin-bottom: 1rem;
  font-size: 1.1rem;
  color: #2c3e50;
}

.recommendations ul {
  list-style: none;
  padding-left: 0;
}

.recommendations li {
  margin-bottom: 0.5rem;
  padding: 0.5rem;
  border-radius: 4px;
  background-color: #e8f5e9;
}

.recommendations li a {
  color: #41b883;
  text-decoration: none;
  display: block;
}

.loading-section,
.error-section {
  text-align: center;
  padding: 2rem;
}

.error-section p {
  color: #dc3545;
  margin-bottom: 1rem;
}

.assessment-info {
  margin-top: 1rem;
  padding: 0.5rem;
  background-color: #e8f5e9;
  border-radius: 4px;
  font-weight: 500;
}

.hidden {
  display: none;
}
</style>