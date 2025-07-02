<template>
  <div class="speaking-practice">
    <div class="practice-header">
      <router-link :to="{ name: 'Speaking' }" class="back-btn">
        返回
      </router-link>
      <h1>{{ practice.title }}</h1>
      <div class="progress-indicator">
        <span>任务 {{ currentTaskIndex + 1 }}/{{ practice.tasks.length }}</span>
        <div class="progress-bar">
          <div 
            class="progress" 
            :style="{ width: progressPercent + '%' }"
          ></div>
        </div>
      </div>
    </div>
    
    <div class="practice-container">
      <div class="task-panel">
        <div class="task-type">{{ currentTask.type }}</div>
        <h2>{{ currentTask.title }}</h2>
        <p class="instructions">{{ currentTask.instructions }}</p>
        
        <div v-if="currentTask.audioUrl" class="audio-player">
          <button @click="playReferenceAudio" class="play-btn">
            <span v-if="isReferenceAudioPlaying">暂停</span>
            <span v-else>播放示例</span>
          </button>
        </div>
        
        <div class="content-display">
          <p v-if="currentTask.content" class="content-text">{{ currentTask.content }}</p>
          <div v-else-if="currentTask.contentItems" class="content-items">
            <div 
              v-for="(item, index) in currentTask.contentItems" 
              :key="index"
              class="content-item"
            >
              <div class="item-number">{{ index + 1 }}</div>
              <div class="item-text">{{ item }}</div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="recording-panel">
        <div class="recording-status" :class="{ active: isRecording }">
          <div class="status-indicator"></div>
          <div class="status-text">
            {{ isRecording ? '录音中...' : '准备录音' }}
          </div>
        </div>
        
        <div class="visualizer">
          <div 
            v-for="n in 20" 
            :key="n" 
            class="visualizer-bar"
            :style="{ 
              height: isRecording ? Math.random() * 60 + 10 + 'px' : '10px',
              opacity: isRecording ? 1 : 0.5
            }"
          ></div>
        </div>
        
        <div class="recording-controls">
          <button 
            @click="toggleRecording" 
            class="record-btn"
            :class="{ recording: isRecording }"
          >
            {{ isRecording ? '停止' : '开始录音' }}
          </button>
          
          <button 
            v-if="recordingComplete" 
            @click="playRecording" 
            class="play-recording-btn"
          >
            播放录音
          </button>
        </div>
        
        <div v-if="recordingComplete" class="feedback-panel">
          <h3>AI 评估</h3>
          <div class="feedback-scores">
            <div class="score-item">
              <div class="score-label">发音</div>
              <div class="score-bar">
                <div 
                  class="score-fill" 
                  :style="{ width: feedback.pronunciation + '%' }"
                ></div>
              </div>
              <div class="score-value">{{ feedback.pronunciation }}/100</div>
            </div>
            
            <div class="score-item">
              <div class="score-label">流利度</div>
              <div class="score-bar">
                <div 
                  class="score-fill" 
                  :style="{ width: feedback.fluency + '%' }"
                ></div>
              </div>
              <div class="score-value">{{ feedback.fluency }}/100</div>
            </div>
            
            <div class="score-item">
              <div class="score-label">内容</div>
              <div class="score-bar">
                <div 
                  class="score-fill" 
                  :style="{ width: feedback.content + '%' }"
                ></div>
              </div>
              <div class="score-value">{{ feedback.content }}/100</div>
            </div>
          </div>
          
          <div class="feedback-comments">
            <h4>改进建议</h4>
            <p>{{ feedback.comments }}</p>
          </div>
        </div>
      </div>
    </div>
    
    <div class="navigation-buttons">
      <button 
        @click="previousTask" 
        class="secondary-btn"
        :disabled="currentTaskIndex === 0"
      >
        上一题
      </button>
      
      <button 
        @click="nextTask" 
        class="primary-btn"
        :disabled="!recordingComplete && currentTaskIndex < practice.tasks.length - 1"
      >
        {{ currentTaskIndex === practice.tasks.length - 1 ? '完成练习' : '下一题' }}
      </button>
    </div>
    
    <div v-if="showCompletionModal" class="completion-modal">
      <div class="modal-content">
        <div class="modal-header">
          <h2>练习完成</h2>
        </div>
        <div class="modal-body">
          <div class="completion-icon">🎉</div>
          <p>恭喜您完成了"{{ practice.title }}"的口语练习！</p>
          
          <div class="overall-score">
            <h3>总体得分</h3>
            <div class="score-circle">
              <span>{{ overallScore }}</span>
            </div>
          </div>
          
          <div class="completion-summary">
            <h3>练习总结</h3>
            <ul>
              <li>您完成了 {{ practice.tasks.length }} 个口语任务</li>
              <li>发音表现: {{ getPerformanceLevel(averagePronunciation) }}</li>
              <li>流利度表现: {{ getPerformanceLevel(averageFluency) }}</li>
              <li>内容表现: {{ getPerformanceLevel(averageContent) }}</li>
            </ul>
          </div>
          
          <div class="practice-suggestion">
            <h3>练习建议</h3>
            <p>{{ practiceRecommendation }}</p>
          </div>
        </div>
        <div class="modal-footer">
          <router-link to="/speaking" class="secondary-btn">返回话题列表</router-link>
          <button @click="restartPractice" class="primary-btn">重新练习</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SpeakingPracticeView',
  data() {
    return {
      currentTaskIndex: 0,
      isRecording: false,
      recordingComplete: false,
      isReferenceAudioPlaying: false,
      showCompletionModal: false,
      practice: {
        id: 's-101',
        title: '旅行与探索',
        tasks: [
          {
            type: '句子模仿',
            title: '重复以下句子',
            instructions: '听取以下句子，然后尽可能准确地重复。注意语调和发音。',
            audioUrl: '/api/audio/speaking/travel_1.mp3',
            content: 'Traveling to new places broadens your horizons and gives you a fresh perspective on life.'
          },
          {
            type: '回答问题',
            title: '旅行经历',
            instructions: '回答以下问题，尽量提供详细信息。',
            content: 'What was the most interesting place you have visited and why did you find it interesting?'
          },
          {
            type: '情境对话',
            title: '在机场',
            instructions: '想象你在机场询问航班信息。回应下面的提示。',
            contentItems: [
              'Explain that your flight has been delayed and you need information about the next available flight.',
              'Ask about the boarding time and gate number for your new flight.',
              'Inquire about what compensation you might receive for the delay.'
            ]
          },
          {
            type: '话题讨论',
            title: '旅行的影响',
            instructions: '讨论以下话题，提供你的观点和个人经历。',
            content: 'How can travel experiences change a person\'s understanding of different cultures? Share specific examples if possible.'
          }
        ]
      },
      feedback: {
        pronunciation: 85,
        fluency: 78,
        content: 92,
        comments: '发音整体良好，但在某些词汇如"perspective"的发音上需要改进。流利度方面，有些停顿过长，建议通过更多练习来提高。内容丰富，表达清晰。'
      },
      taskFeedbacks: []
    };
  },
  computed: {
    currentTask() {
      return this.practice.tasks[this.currentTaskIndex];
    },
    progressPercent() {
      return ((this.currentTaskIndex + 1) / this.practice.tasks.length) * 100;
    },
    overallScore() {
      if (this.taskFeedbacks.length === 0) {
        return Math.round((this.feedback.pronunciation + this.feedback.fluency + this.feedback.content) / 3);
      }
      
      let totalScore = 0;
      this.taskFeedbacks.forEach(feedback => {
        totalScore += (feedback.pronunciation + feedback.fluency + feedback.content) / 3;
      });
      
      return Math.round(totalScore / this.taskFeedbacks.length);
    },
    averagePronunciation() {
      if (this.taskFeedbacks.length === 0) return this.feedback.pronunciation;
      
      let total = 0;
      this.taskFeedbacks.forEach(feedback => {
        total += feedback.pronunciation;
      });
      
      return Math.round(total / this.taskFeedbacks.length);
    },
    averageFluency() {
      if (this.taskFeedbacks.length === 0) return this.feedback.fluency;
      
      let total = 0;
      this.taskFeedbacks.forEach(feedback => {
        total += feedback.fluency;
      });
      
      return Math.round(total / this.taskFeedbacks.length);
    },
    averageContent() {
      if (this.taskFeedbacks.length === 0) return this.feedback.content;
      
      let total = 0;
      this.taskFeedbacks.forEach(feedback => {
        total += feedback.content;
      });
      
      return Math.round(total / this.taskFeedbacks.length);
    },
    practiceRecommendation() {
      if (this.overallScore >= 90) {
        return '您的口语水平已经很棒了！建议尝试更高级的口语练习，如辩论或公开演讲。';
      } else if (this.overallScore >= 75) {
        return '您的口语表现良好。建议继续练习流利度，特别是减少不必要的停顿，并扩展您的词汇量。';
      } else if (this.overallScore >= 60) {
        return '您的口语基础不错。建议重点练习发音和语调，多听英语材料并模仿原声。';
      } else {
        return '建议从基础的句子和表达开始练习，逐步提高发音准确度和流利度。可以尝试使用慢速英语材料进行练习。';
      }
    }
  },
  methods: {
    toggleRecording() {
      this.isRecording = !this.isRecording;
      
      if (!this.isRecording) {
        // 模拟录音完成后的处理
        this.recordingComplete = true;
        
        // 保存当前任务的反馈
        this.taskFeedbacks.push({...this.feedback});
      }
    },
    playReferenceAudio() {
      this.isReferenceAudioPlaying = !this.isReferenceAudioPlaying;
      
      if (this.isReferenceAudioPlaying) {
        // 模拟音频播放结束
        setTimeout(() => {
          this.isReferenceAudioPlaying = false;
        }, 5000);
      }
    },
    playRecording() {
      // 模拟播放录音
      alert('播放录音功能将连接到实际的音频API');
    },
    previousTask() {
      if (this.currentTaskIndex > 0) {
        this.currentTaskIndex--;
        this.resetTaskState();
      }
    },
    nextTask() {
      if (this.currentTaskIndex < this.practice.tasks.length - 1) {
        this.currentTaskIndex++;
        this.resetTaskState();
      } else {
        this.completePractice();
      }
    },
    resetTaskState() {
      this.isRecording = false;
      this.recordingComplete = false;
      
      // 检查当前任务是否已有反馈
      if (this.taskFeedbacks[this.currentTaskIndex]) {
        this.recordingComplete = true;
        this.feedback = this.taskFeedbacks[this.currentTaskIndex];
      }
    },
    completePractice() {
      this.showCompletionModal = true;
    },
    restartPractice() {
      this.currentTaskIndex = 0;
      this.taskFeedbacks = [];
      this.showCompletionModal = false;
      this.resetTaskState();
    },
    getPerformanceLevel(score) {
      if (score >= 90) return '优秀';
      if (score >= 75) return '良好';
      if (score >= 60) return '一般';
      return '需要改进';
    }
  },
  mounted() {
    // 初始化任务反馈数组
    this.taskFeedbacks = new Array(this.practice.tasks.length);
  }
};
</script>

<style scoped>
.speaking-practice {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem;
}

.practice-header {
  display: flex;
  flex-direction: column;
  margin-bottom: 1.5rem;
  position: relative;
}

.back-btn {
  position: absolute;
  left: 0;
  top: 0;
  display: flex;
  align-items: center;
  color: #41b883;
  text-decoration: none;
  font-weight: 500;
}

h1 {
  text-align: center;
  margin: 0.5rem 0 1.5rem;
  color: #2c3e50;
}

.progress-indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.progress-indicator span {
  font-size: 0.9rem;
  color: #6c757d;
}

.progress-bar {
  width: 100%;
  max-width: 500px;
  height: 8px;
  background-color: #e9ecef;
  border-radius: 4px;
  overflow: hidden;
}

.progress {
  height: 100%;
  background-color: #41b883;
  transition: width 0.3s ease;
}

.practice-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

@media (max-width: 768px) {
  .practice-container {
    grid-template-columns: 1fr;
  }
}

.task-panel, .recording-panel {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
}

.task-type {
  display: inline-block;
  background-color: #e8f5e9;
  color: #41b883;
  font-size: 0.85rem;
  font-weight: 500;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  margin-bottom: 1rem;
}

.task-panel h2 {
  margin-bottom: 1rem;
  color: #2c3e50;
}

.instructions {
  color: #6c757d;
  margin-bottom: 1.5rem;
  line-height: 1.6;
}

.audio-player {
  margin-bottom: 1.5rem;
}

.play-btn {
  background-color: #41b883;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 0.5rem 1rem;
  cursor: pointer;
}

.content-display {
  background-color: #f8f9fa;
  padding: 1.5rem;
  border-radius: 4px;
  margin-top: 1rem;
}

.content-text {
  color: #2c3e50;
  line-height: 1.6;
  font-size: 1.1rem;
}

.content-items {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.content-item {
  display: flex;
  gap: 1rem;
}

.item-number {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 28px;
  height: 28px;
  background-color: #41b883;
  color: white;
  border-radius: 50%;
  font-weight: bold;
  flex-shrink: 0;
}

.item-text {
  flex: 1;
  color: #2c3e50;
  line-height: 1.6;
}

.recording-status {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.status-indicator {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background-color: #e9ecef;
  position: relative;
}

.status-indicator::after {
  content: '';
  position: absolute;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background-color: #dc3545;
  transform: scale(0);
  transition: transform 0.2s ease;
}

.recording-status.active .status-indicator::after {
  transform: scale(1);
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0% {
    transform: scale(0.8);
    opacity: 1;
  }
  50% {
    transform: scale(1.2);
    opacity: 0.8;
  }
  100% {
    transform: scale(0.8);
    opacity: 1;
  }
}

.status-text {
  font-size: 0.9rem;
  color: #6c757d;
}

.recording-status.active .status-text {
  color: #dc3545;
  font-weight: 500;
}

.visualizer {
  display: flex;
  align-items: flex-end;
  height: 70px;
  gap: 3px;
  background-color: #f8f9fa;
  border-radius: 4px;
  padding: 0.5rem;
  margin-bottom: 1.5rem;
}

.visualizer-bar {
  flex: 1;
  background-color: #41b883;
  border-radius: 2px;
  transition: height 0.1s ease;
}

.recording-controls {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.record-btn {
  padding: 0.75rem 1.5rem;
  border-radius: 30px;
  border: none;
  background-color: #41b883;
  color: white;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.record-btn.recording {
  background-color: #dc3545;
  box-shadow: 0 0 0 5px rgba(220, 53, 69, 0.2);
  animation: record-pulse 1.5s infinite;
}

@keyframes record-pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(220, 53, 69, 0.4);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(220, 53, 69, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(220, 53, 69, 0);
  }
}

.play-recording-btn {
  padding: 0.75rem 1.5rem;
  border-radius: 30px;
  border: 1px solid #41b883;
  background-color: white;
  color: #41b883;
  font-weight: 500;
  cursor: pointer;
}

.feedback-panel {
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid #e9ecef;
}

.feedback-panel h3 {
  margin-bottom: 1.5rem;
  color: #2c3e50;
  text-align: center;
}

.feedback-scores {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.score-item {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.score-label {
  width: 60px;
  font-weight: 500;
  color: #495057;
}

.score-bar {
  flex: 1;
  height: 12px;
  background-color: #e9ecef;
  border-radius: 6px;
  overflow: hidden;
}

.score-fill {
  height: 100%;
  background-color: #41b883;
  border-radius: 6px;
  transition: width 0.5s ease;
}

.score-value {
  width: 60px;
  text-align: right;
  font-weight: 500;
  color: #41b883;
}

.feedback-comments {
  background-color: #f8f9fa;
  padding: 1rem;
  border-radius: 4px;
}

.feedback-comments h4 {
  margin-bottom: 0.5rem;
  color: #2c3e50;
}

.feedback-comments p {
  color: #6c757d;
  line-height: 1.6;
}

.navigation-buttons {
  display: flex;
  justify-content: space-between;
  margin-top: 1.5rem;
}

.primary-btn, .secondary-btn {
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  font-weight: 500;
  cursor: pointer;
}

.primary-btn {
  background-color: #41b883;
  color: white;
  border: none;
}

.primary-btn:disabled {
  background-color: #a8d5c2;
  cursor: not-allowed;
}

.secondary-btn {
  background-color: white;
  color: #6c757d;
  border: 1px solid #dee2e6;
}

.secondary-btn:disabled {
  color: #adb5bd;
  cursor: not-allowed;
}

.completion-modal {
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
  text-align: center;
}

.modal-header h2 {
  margin: 0;
  color: #2c3e50;
}

.modal-body {
  padding: 1.5rem;
  text-align: center;
}

.completion-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.modal-body p {
  margin-bottom: 2rem;
  color: #6c757d;
}

.overall-score {
  margin-bottom: 2rem;
}

.overall-score h3 {
  margin-bottom: 1rem;
  color: #2c3e50;
}

.score-circle {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background-color: #41b883;
  color: white;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 2.5rem;
  font-weight: bold;
  margin: 0 auto;
}

.completion-summary, .practice-suggestion {
  text-align: left;
  margin-bottom: 2rem;
}

.completion-summary h3, .practice-suggestion h3 {
  margin-bottom: 1rem;
  color: #2c3e50;
}

.completion-summary ul {
  list-style-type: none;
  padding-left: 0;
}

.completion-summary li {
  margin-bottom: 0.5rem;
  color: #495057;
  padding-left: 1.5rem;
  position: relative;
}

.completion-summary li::before {
  content: '✓';
  color: #41b883;
  position: absolute;
  left: 0;
}

.practice-suggestion p {
  color: #495057;
  line-height: 1.6;
  margin: 0;
}

.modal-footer {
  padding: 1.5rem;
  border-top: 1px solid #e9ecef;
  display: flex;
  justify-content: center;
  gap: 1rem;
}
</style> 