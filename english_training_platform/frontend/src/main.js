import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './assets/tailwind.css'

// 导入 AudioService
import AudioService from './services/AudioService'

// 创建 Vue 应用实例
const app = createApp(App)

// 全局注册 AudioService，使其在任何组件中可用
app.config.globalProperties.$audio = AudioService

// 监听路由变化，当用户离开页面时暂停音频
router.beforeEach((to, from, next) => {
          // 简化判断逻辑，任何路由变化都停止音频
          if (to.path !== from.path) {
                    AudioService.stopAndReset()
          }
          next()
})

// 使用插件并挂载应用
app.use(router).mount('#app') 