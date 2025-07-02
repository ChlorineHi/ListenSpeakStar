<template>
  <div class="error-container">
    <div class="error-icon">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
        <path d="M12 22C6.477 22 2 17.523 2 12S6.477 2 12 2s10 4.477 10 10-4.477 10-10 10zm0-2a8 8 0 1 0 0-16 8 8 0 0 0 0 16zm-1-5h2v2h-2v-2zm0-8h2v6h-2V7z"/>
      </svg>
    </div>
    <h2 class="error-title">{{ title || '加载失败' }}</h2>
    <p class="error-message">{{ message || '无法加载请求的资源，请稍后再试。' }}</p>
    <div class="error-actions">
      <button class="retry-button" @click="$emit('retry')" v-if="showRetry">
        重试
      </button>
      <button class="back-button" @click="goBack">
        返回
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ErrorMessage',
  props: {
    title: {
      type: String,
      default: ''
    },
    message: {
      type: String,
      default: ''
    },
    showRetry: {
      type: Boolean,
      default: true
    }
  },
  methods: {
    goBack() {
      if (window.history.length > 1) {
        this.$router.go(-1)
      } else {
        this.$router.push('/')
      }
    }
  }
}
</script>

<style scoped>
.error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  text-align: center;
  max-width: 500px;
  margin: 0 auto;
}

.error-icon {
  color: #f44336;
  width: 64px;
  height: 64px;
  margin-bottom: 20px;
}

.error-title {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin-bottom: 10px;
}

.error-message {
  font-size: 16px;
  color: #666;
  margin-bottom: 30px;
  line-height: 1.5;
}

.error-actions {
  display: flex;
  gap: 15px;
}

.retry-button, .back-button {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.2s;
}

.retry-button {
  background-color: #1976d2;
  color: white;
}

.retry-button:hover {
  background-color: #1565c0;
}

.back-button {
  background-color: #f5f5f5;
  color: #333;
}

.back-button:hover {
  background-color: #e0e0e0;
}
</style> 