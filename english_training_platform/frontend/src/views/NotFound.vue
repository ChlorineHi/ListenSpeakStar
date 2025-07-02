<template>
  <div class="not-found">
    <div class="not-found-content">
      <div class="error-code">404</div>
      <h1>页面未找到</h1>
      <p>抱歉，您尝试访问的页面不存在或已被移除。</p>
      <router-link to="/" class="home-btn">返回首页</router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NotFoundView'
}
</script>

<style scoped>
.not-found {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 64px);
  background-color: #f8f9fa;
  text-align: center;
}

.not-found-content {
  max-width: 500px;
  padding: 2rem;
}

.error-code {
  font-size: 8rem;
  font-weight: bold;
  color: #41b883;
  line-height: 1;
  margin-bottom: 1rem;
  text-shadow: 3px 3px 0 rgba(0, 0, 0, 0.1);
}

h1 {
  font-size: 2rem;
  color: #2c3e50;
  margin-bottom: 1rem;
}

p {
  color: #6c757d;
  margin-bottom: 2rem;
  font-size: 1.1rem;
}

.home-btn {
  display: inline-block;
  background-color: #41b883;
  color: white;
  text-decoration: none;
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  font-weight: 500;
  transition: background-color 0.2s;
}

.home-btn:hover {
  background-color: #399a6e;
}
</style> 