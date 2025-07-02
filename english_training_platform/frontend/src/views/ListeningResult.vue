<template>
  <div class="listening-result">
    <div class="result-header">
      <h1>练习结果</h1>
      <div class="score-display">
        <div class="score">{{ correctCount }}/{{ totalQuestions }}</div>
        <div class="percentage">{{ scorePercentage }}%</div>
      </div>
    </div>
    
    <div class="actions-container">
      <button class="action-button retry" @click="retryExercise">
        <i class="fas fa-redo"></i> 重新练习
      </button>
      <button class="action-button recommend" @click="getRecommendations">
        <i class="fas fa-lightbulb"></i> 智能推荐
      </button>
      <button class="action-button back" @click="backToList">
        <i class="fas fa-list"></i> 返回列表
      </button>
    </div>
    
    <div class="questions-review">
      <h2>答题回顾</h2>
      <div v-for="(answer, index) in userAnswers" :key="index" class="question-item">
        <div class="question-header" :class="{ 'correct': answer.is_correct, 'incorrect': !answer.is_correct }">
          <div class="question-number">问题 {{ answer.question_id }}</div>
          <div class="question-result">
            {{ answer.is_correct ? '正确' : '错误' }}
          </div>
        </div>
        
        <div class="question-content">
          <p>{{ getQuestionText(answer.question_id) }}</p>
          <div class="options">
            <div 
              v-for="option in getQuestionOptions(answer.question_id)" 
              :key="option.slice(0, 1)"
              class="option"
              :class="{
                'user-selected': option.startsWith(answer.user_answer),
                'correct-answer': option.startsWith(answer.correct_answer),
                'wrong-answer': option.startsWith(answer.user_answer) && answer.user_answer !== answer.correct_answer
              }"
            >
              {{ option }}
            </div>
          </div>
        </div>
        
        <div v-if="!answer.is_correct" class="explanation">
          <strong>解析:</strong> {{ getExplanation(answer.question_id) }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ListeningResult',
  props: {
    material: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      userAnswers: []
    }
  },
  computed: {
    totalQuestions() {
      return this.userAnswers.length
    },
    correctCount() {
      return this.userAnswers.filter(answer => answer.is_correct).length
    },
    scorePercentage() {
      if (this.totalQuestions === 0) return 0
      return Math.round((this.correctCount / this.totalQuestions) * 100)
    }
  },
  created() {
    // 从本地存储或路由参数获取用户答题数据
    if (this.$route.params.userAnswers) {
      this.userAnswers = this.$route.params.userAnswers
    } else if (localStorage.getItem('userAnswers')) {
      try {
        this.userAnswers = JSON.parse(localStorage.getItem('userAnswers'))
      } catch (e) {
        console.error('解析用户答题数据失败:', e)
        this.userAnswers = []
      }
    }
    
    // 保存答题数据以便推荐系统使用
    localStorage.setItem('lastAnswers', JSON.stringify(this.userAnswers))
  },
  methods: {
    getQuestionText(questionId) {
      const question = this.material.questions.find(q => q.id === questionId)
      return question ? question.question : '问题不可用'
    },
    getQuestionOptions(questionId) {
      const question = this.material.questions.find(q => q.id === questionId)
      return question ? question.options : []
    },
    getExplanation(questionId) {
      const question = this.material.questions.find(q => q.id === questionId)
      return question ? question.explanation : '解析不可用'
    },
    retryExercise() {
      // 重新开始当前练习
      this.$router.push(`/listening/${this.material.id}`)
    },
    backToList() {
      // 返回听力材料列表
      this.$router.push('/listening')
    },
    getRecommendations() {
      // 跳转到推荐页面，并传递用户答题数据
      this.$router.push({
        name: 'recommendation',
        params: {
          userAnswers: this.userAnswers
        }
      })
    }
  }
}
</script>

<style scoped>
.listening-result {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.score-display {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.score {
  font-size: 24px;
  font-weight: bold;
  color: #333;
}

.percentage {
  font-size: 32px;
  font-weight: bold;
  color: #1976d2;
}

.actions-container {
  display: flex;
  gap: 15px;
  margin-bottom: 30px;
  flex-wrap: wrap;
}

.action-button {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  font-weight: bold;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: background-color 0.2s;
}

.action-button i {
  font-size: 16px;
}

.retry {
  background-color: #f5f5f5;
  color: #333;
}

.retry:hover {
  background-color: #e0e0e0;
}

.recommend {
  background-color: #1976d2;
  color: white;
}

.recommend:hover {
  background-color: #1565c0;
}

.back {
  background-color: #f5f5f5;
  color: #333;
}

.back:hover {
  background-color: #e0e0e0;
}

.questions-review {
  margin-top: 20px;
}

.questions-review h2 {
  margin-bottom: 20px;
  color: #333;
}

.question-item {
  margin-bottom: 25px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  overflow: hidden;
}

.question-header {
  display: flex;
  justify-content: space-between;
  padding: 12px 15px;
  font-weight: bold;
}

.question-header.correct {
  background-color: rgba(76, 175, 80, 0.1);
  color: #4caf50;
}

.question-header.incorrect {
  background-color: rgba(244, 67, 54, 0.1);
  color: #f44336;
}

.question-content {
  padding: 15px;
  background-color: #fff;
}

.options {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 10px;
}

.option {
  padding: 8px 12px;
  border-radius: 4px;
  background-color: #f5f5f5;
}

.user-selected {
  font-weight: bold;
}

.correct-answer {
  background-color: rgba(76, 175, 80, 0.1);
  border-left: 4px solid #4caf50;
}

.wrong-answer {
  background-color: rgba(244, 67, 54, 0.1);
  border-left: 4px solid #f44336;
}

.explanation {
  padding: 15px;
  background-color: #f9f9f9;
  border-top: 1px solid #e0e0e0;
  font-size: 14px;
  color: #666;
}

@media (max-width: 768px) {
  .result-header {
    flex-direction: column;
    text-align: center;
    gap: 15px;
  }
  
  .actions-container {
    justify-content: center;
  }
}
</style> 