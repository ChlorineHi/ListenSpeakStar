<template>
  <nav class="navbar">
    <div class="container mx-auto px-4">
      <div class="flex justify-between items-center py-4">
        <div class="logo">
          <router-link to="/" class="text-xl font-bold text-blue-600">英语听说训练平台</router-link>
        </div>
        
        <div class="nav-links hidden md:flex space-x-6">
          <router-link to="/" class="nav-link">首页</router-link>
          <router-link to="/listening" class="nav-link">听力训练</router-link>
          <router-link to="/speaking" class="nav-link">口语训练</router-link>
          <router-link to="/assessment" class="nav-link">水平评估</router-link>
          <router-link to="/agent-recommendation" class="nav-link">
            <span class="flex items-center">
              <span>智能推荐</span>
              <span class="ml-1 px-1.5 py-0.5 text-xs bg-blue-600 text-white rounded-md">AI</span>
            </span>
          </router-link>
          <router-link to="/favorites" class="nav-link">我的收藏</router-link>
        </div>
        
        <div class="mobile-menu-btn md:hidden">
          <button @click="toggleMobileMenu" class="text-gray-600 focus:outline-none">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path v-if="!mobileMenuOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
              <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>
      </div>
      
      <!-- Mobile Menu -->
      <div v-if="mobileMenuOpen" class="mobile-menu md:hidden py-4">
        <router-link to="/" class="block py-2 px-4 hover:bg-gray-100">首页</router-link>
        <router-link to="/listening" class="block py-2 px-4 hover:bg-gray-100">听力训练</router-link>
        <router-link to="/speaking" class="block py-2 px-4 hover:bg-gray-100">口语训练</router-link>
        <router-link to="/assessment" class="block py-2 px-4 hover:bg-gray-100">水平评估</router-link>
        <router-link to="/agent-recommendation" class="block py-2 px-4 hover:bg-gray-100">
          <span class="flex items-center">
            <span>智能推荐</span>
            <span class="ml-1 px-1.5 py-0.5 text-xs bg-blue-600 text-white rounded-md">AI</span>
          </span>
        </router-link>
        <router-link to="/favorites" class="block py-2 px-4 hover:bg-gray-100">我的收藏</router-link>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'Navbar',
  data() {
    return {
      mobileMenuOpen: false
    }
  },
  methods: {
    toggleMobileMenu() {
      this.mobileMenuOpen = !this.mobileMenuOpen
    }
  }
}
</script>

<style scoped>
.navbar {
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.nav-link {
  color: #4b5563;
  font-weight: 500;
  transition: color 0.2s;
}

.nav-link:hover,
.router-link-exact-active {
  color: #3b82f6;
}
</style> 