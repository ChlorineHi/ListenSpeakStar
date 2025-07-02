<template>
  <div class="flex flex-col min-h-screen bg-neutral-lighter">
    <!-- 顶部导航栏 -->
    <header class="bg-white shadow-sm">
      <div class="container mx-auto px-4 py-3 flex justify-between items-center">
        <div class="flex items-center">
          <img src="@/assets/logo.svg" alt="Logo" class="h-10 w-10 mr-2" />
          <h1 class="text-xl font-bold text-primary">英语听说训练智能平台</h1>
        </div>
        <nav class="flex space-x-6">
          <router-link to="/" class="text-neutral-dark hover:text-primary transition-colors">首页</router-link>
          <router-link to="/listening" class="text-neutral-dark hover:text-primary transition-colors">听力训练</router-link>
          <router-link to="/speaking" class="text-neutral-dark hover:text-primary transition-colors">口语训练</router-link>
          <router-link to="/favorites" class="text-neutral-dark hover:text-primary transition-colors">我的收藏</router-link>

          <router-link to="/teacher" class="text-neutral-dark hover:text-primary transition-colors">教师端</router-link>

        </nav>
      </div>
    </header>

    <!-- 主内容区 -->
    <main class="flex-grow container mx-auto px-4 py-6">
      <router-view />
    </main>

    <!-- 页脚 -->
    <footer class="bg-neutral-darker text-neutral-light py-6">
      <div class="container mx-auto px-4">
        <div class="flex flex-col md:flex-row justify-between items-center">
          <div class="mb-4 md:mb-0">
            <p class="text-sm">© 2024 英语听说训练智能平台. 所有权利保留.</p>
          </div>
          <div class="flex space-x-4">
            <a href="#" class="text-sm hover:text-white transition-colors">关于我们</a>
            <a href="#" class="text-sm hover:text-white transition-colors">使用条款</a>
            <a href="#" class="text-sm hover:text-white transition-colors">隐私政策</a>
            <a href="#" class="text-sm hover:text-white transition-colors">联系我们</a>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

body {
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>
