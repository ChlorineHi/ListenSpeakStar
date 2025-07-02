<template>
  <div>
    <div v-if="loading" class="text-center py-12">
      <div class="inline-block animate-spin rounded-full h-8 w-8 border-4 border-primary border-t-transparent"></div>
      <p class="mt-2 text-neutral-dark">加载中...</p>
    </div>
    
    <div v-else-if="!material.id" class="bg-white rounded-lg shadow p-8 text-center">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mx-auto text-neutral-light mb-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <h3 class="text-xl font-semibold text-neutral-darkest mb-2">找不到听力材料</h3>
      <p class="text-neutral-dark mb-4">该听力材料不存在或已被删除。</p>
      <router-link to="/listening" class="btn btn-primary">返回听力列表</router-link>
    </div>
    
    <div v-else>
      <!-- 听力材料标题和信息 -->
      <div class="flex justify-between items-start mb-6">
        <div>
          <h1 class="text-2xl font-bold text-neutral-darkest">{{ material.title }}</h1>
          <div class="flex flex-wrap gap-2 mt-2">
            <span class="badge badge-primary">{{ material.difficulty }}</span>
            <span v-for="topic in material.topic" :key="topic" class="badge badge-secondary">{{ topic }}</span>
          </div>
        </div>
        <button @click="toggleFavorite" class="p-2 text-neutral-dark hover:text-primary">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" :fill="isFavorite ? 'currentColor' : 'none'" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
          </svg>
        </button>
      </div>
      
      <!-- 步骤导航 -->
      <div class="bg-white rounded-lg shadow mb-6">
        <div class="flex border-b">
          <button 
            v-for="(step, index) in steps" 
            :key="index"
            @click="currentStep = index"
            :class="[
              'flex-1 py-3 px-4 text-center font-medium border-b-2 transition-colors',
              currentStep === index 
                ? 'text-primary border-primary' 
                : 'text-neutral-dark border-transparent hover:text-primary hover:border-primary-light'
            ]"
          >
            <span class="inline-block bg-neutral-lighter rounded-full w-6 h-6 leading-6 mr-2">{{ index + 1 }}</span>
            {{ step.name }}
          </button>
        </div>
      </div>
      
      <!-- 步骤内容 -->
      <div class="bg-white rounded-lg shadow p-6">
        <!-- 1. 听力播放 -->
        <div v-if="currentStep === 0">
          <h2 class="text-xl font-semibold text-neutral-darkest mb-4">听力材料</h2>
          
          <!-- 音频播放器 -->
          <div class="mb-6">
            <!-- 音频控制界面 -->
            <div class="bg-neutral-lighter p-4 rounded-lg mb-3">
              <div class="flex items-center justify-between">
                <button @click="togglePlayback" class="btn btn-primary">
                  {{ isPlaying ? '暂停' : '播放' }}
                </button>
                <div class="flex-1 mx-4">
                  <div class="w-full bg-neutral-light rounded-full h-2.5">
                    <div class="bg-primary h-2.5 rounded-full" :style="{width: `${audioProgress}%`}"></div>
                  </div>
                </div>
                <div class="text-neutral-dark text-sm">
                  {{ formatTime(currentTime) }} / {{ formatTime(duration) }}
                </div>
              </div>
            </div>
            <div class="flex justify-between">
              <button @click="replayAudio" class="btn btn-outline-primary">重播</button>
              <button @click="currentStep = 1" class="btn btn-secondary">开始答题</button>
            </div>
          </div>
          
          <!-- 音频文字描述 -->
          <div v-if="showTranscript" class="mt-6 p-4 bg-neutral-lighter rounded-lg">
            <div class="flex justify-between items-center mb-2">
              <h3 class="font-semibold text-neutral-darkest">音频文本</h3>
              <button @click="showTranscript = false" class="text-neutral-dark hover:text-primary">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
                </svg>
              </button>
            </div>
            <p class="text-neutral-dark">{{ material.transcript }}</p>
          </div>
          
          <div v-else class="mt-6">
            <button @click="showTranscript = true" class="text-primary hover:underline flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-8-3a1 1 0 00-.867.5 1 1 0 11-1.731-1A3 3 0 0113 8a3.001 3.001 0 01-2 2.83V11a1 1 0 11-2 0v-1a1 1 0 011-1 1 1 0 100-2zm0 8a1 1 0 100-2 1 1 0 000 2z" clip-rule="evenodd" />
              </svg>
              显示音频文本
            </button>
          </div>
        </div>
        
        <!-- 2. 答题环节 -->
        <div v-else-if="currentStep === 1">
          <h2 class="text-xl font-semibold text-neutral-darkest mb-4">听力理解问题</h2>
          
          <div class="mb-6">
            <p class="text-neutral-dark mb-2">请根据听到的内容回答以下问题：</p>
            <p class="text-neutral-dark text-sm mb-4">共 {{ material.questions.length }} 道题，请完成所有题目后提交。</p>
            
            <!-- 简单的音频控制 -->
            <div class="bg-neutral-lighter p-3 rounded-lg mb-4 flex items-center justify-between">
              <button @click="togglePlayback" class="btn btn-sm btn-primary">
                {{ isPlaying ? '暂停' : '播放' }}
              </button>
              <div class="flex-1 mx-3">
                <div class="w-full bg-neutral-light rounded-full h-2">
                  <div class="bg-primary h-2 rounded-full" :style="{width: `${audioProgress}%`}"></div>
                </div>
              </div>
              <div class="text-neutral-dark text-xs">
                {{ formatTime(currentTime) }}
              </div>
            </div>
            
            <div v-for="(question, index) in material.questions" :key="index" class="mb-6 p-4 bg-neutral-lighter rounded-lg">
              <p class="font-medium text-neutral-darkest mb-3">{{ index + 1 }}. {{ question.question }}</p>
              <div class="space-y-2">
                <div v-for="option in question.options" :key="option" class="flex items-center">
                  <input 
                    type="radio" 
                    :id="`q${index}_${option.charAt(0)}`"
                    :name="`question_${index}`"
                    :value="option.charAt(0)"
                    v-model="userAnswers[index]"
                    class="mr-2"
                  >
                  <label :for="`q${index}_${option.charAt(0)}`" class="text-neutral-dark">{{ option }}</label>
                </div>
              </div>
            </div>
            
            <div class="flex justify-between">
              <button @click="currentStep = 0" class="btn btn-outline-primary">返回听力</button>
              <button @click="submitAnswers" class="btn btn-primary" :disabled="!allQuestionsAnswered">提交答案</button>
            </div>
          </div>
        </div>
        
        <!-- 3. 结果反馈 -->
        <div v-else-if="currentStep === 2">
          <div class="result-container">
            <div class="result-header">
              <h2>练习完成!</h2>
              <div class="score-display">
                <div class="score">{{ score }}/{{ material.questions.length }}</div>
                <div class="percentage">{{ scorePercentage }}%</div>
              </div>
            </div>
            
            <div class="actions-row">
              <button class="action-button retry" @click="retryExercise">
                <i class="fas fa-redo"></i> 重新练习
              </button>
              <button class="action-button recommend" @click="goToRecommendation">
                <i class="fas fa-lightbulb"></i> 智能推荐
              </button>
            </div>
            
            <div class="p-4 rounded-lg bg-neutral-lighter mb-6">
              <div class="flex justify-between items-center mb-3">
                <h3 class="font-semibold text-neutral-darkest">得分情况</h3>
                <div class="text-2xl font-bold">
                  <span class="text-primary">{{ score }}</span>
                  <span class="text-neutral-dark text-lg">/{{ material.questions.length }}</span>
                </div>
              </div>
              
              <div class="w-full bg-neutral-light rounded-full h-2.5 mb-4">
                <div class="bg-primary h-2.5 rounded-full" :style="{width: `${scorePercentage}%`}"></div>
              </div>
              
              <p class="text-neutral-dark" v-if="scorePercentage >= 80">
                太棒了！你对该听力材料的理解非常好。
              </p>
              <p class="text-neutral-dark" v-else-if="scorePercentage >= 60">
                不错！你对该听力材料有良好的理解，但还有提升空间。
              </p>
              <p class="text-neutral-dark" v-else>
                继续努力！多练习可以帮助你提升听力理解能力。
              </p>
            </div>
            
            <div v-if="feedback.loading" class="text-center py-6">
              <div class="inline-block animate-spin rounded-full h-6 w-6 border-4 border-primary border-t-transparent"></div>
              <p class="mt-2 text-neutral-dark">生成学习反馈中...</p>
            </div>
            
            <div v-else class="space-y-6">
              <!-- 备用数据提示 -->
              <div v-if="feedback.is_mock_data" class="p-4 border border-yellow-300 bg-yellow-50 rounded-lg">
                <div class="flex items-start">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-yellow-400 mt-0.5 mr-2" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2h-1V9a1 1 0 00-1-1z" clip-rule="evenodd" />
                  </svg>
                  <p class="text-sm text-yellow-700">由于网络原因，本次反馈由系统自动生成。如需更精准的分析，请稍后重新提交。</p>
                </div>
              </div>
              
              <!-- 重要词汇 -->
              <div class="p-4 border border-neutral-light rounded-lg">
                <h3 class="font-semibold text-neutral-darkest mb-3">重要词汇</h3>
                <div class="flex flex-wrap gap-2">
                  <span v-for="word in feedback.vocabulary" :key="word" class="px-3 py-1 bg-primary-light text-primary-dark rounded-full text-sm">
                    {{ word }}
                  </span>
                </div>
              </div>
              
              <!-- 重要表达 -->
              <div class="p-4 border border-neutral-light rounded-lg">
                <h3 class="font-semibold text-neutral-darkest mb-3">重要表达</h3>
                <div class="flex flex-wrap gap-2">
                  <span v-for="expression in feedback.expressions" :key="expression" class="px-3 py-1 bg-secondary-light text-secondary-dark rounded-full text-sm">
                    {{ expression }}
                  </span>
                </div>
              </div>
              
              <!-- 背景知识 -->
              <div class="p-4 border border-neutral-light rounded-lg">
                <h3 class="font-semibold text-neutral-darkest mb-3">背景知识</h3>
                <p class="text-neutral-dark">{{ feedback.background }}</p>
              </div>
              
              <!-- 听力结构分析 -->
              <div class="p-4 border border-neutral-light rounded-lg">
                <h3 class="font-semibold text-neutral-darkest mb-3">听力结构分析</h3>
                <p class="text-neutral-dark">{{ feedback.structure }}</p>
              </div>

              <!-- 错题分析 -->
              <div v-if="feedback.mistakes_analysis" class="p-4 border border-neutral-light rounded-lg">
                <h3 class="font-semibold text-neutral-darkest mb-3">错题分析与建议</h3>
                <div class="text-neutral-dark">
                  <p v-if="typeof feedback.mistakes_analysis === 'string'">{{ feedback.mistakes_analysis }}</p>
                  <div v-else-if="typeof feedback.mistakes_analysis === 'object'" class="space-y-3">
                    <div v-for="(analysis, key) in feedback.mistakes_analysis" :key="key" class="p-4 bg-neutral-lightest rounded">
                      <h4 class="font-medium text-primary mb-2">题目 {{ key }}:</h4>
                      <div class="whitespace-pre-line">{{ analysis }}</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div class="flex justify-between mt-8">
            <button @click="currentStep = 1" class="btn btn-outline-primary">查看答题</button>
            <button @click="startSpeakingPractice" class="btn btn-primary">进行口语训练</button>
          </div>
        </div>
      </div>
      
      <!-- 进阶推荐 -->
      <div v-if="currentStep === 2 && showAdvanced" class="mt-6 bg-white rounded-lg shadow p-6">
        <h2 class="text-xl font-semibold text-neutral-darkest mb-4">进阶听力训练</h2>
        
        <div v-if="advanced.loading" class="text-center py-6">
          <div class="inline-block animate-spin rounded-full h-6 w-6 border-4 border-primary border-t-transparent"></div>
          <p class="mt-2 text-neutral-dark">获取进阶材料中...</p>
        </div>
        
        <div v-else>
          <p class="text-neutral-dark mb-4">
            恭喜你完成了 {{ material.difficulty }} 难度的训练！尝试更高难度的材料来进一步提升你的听力能力。
          </p>
          
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div v-for="material in advanced.materials" :key="material.id" class="border border-neutral-light rounded-lg p-4 hover:border-primary hover:shadow-sm transition-all">
              <div class="flex justify-between items-start mb-2">
                <h3 class="font-medium text-neutral-darkest">{{ material.title }}</h3>
                <span class="badge badge-primary">{{ material.difficulty }}</span>
              </div>
              <p class="text-neutral-dark text-sm mb-4 line-clamp-2">{{ material.transcript.substring(0, 80) }}...</p>
              <router-link :to="`/listening/${material.id}`" class="btn btn-sm btn-outline-primary w-full">
                开始训练
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 错误处理组件 -->
    <div v-if="error" class="mt-8">
      <ErrorMessage 
        :title="'材料加载失败'" 
        :message="errorMessage"
        @retry="retryFetchMaterial"
      />
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import AudioService from '@/services/AudioService'
import MaterialService from '@/services/MaterialService'
import ErrorMessage from '@/components/ErrorMessage.vue'

export default {
  name: 'ListeningDetail',
  components: {
    ErrorMessage
  },
  data() {
    return {
      material: {},
      loading: true,
      currentStep: 0, // 0: 听力, 1: 答题, 2: 结果
      showTranscript: false,
      isFavorite: false,
      isPlaying: false,
      audioProgress: 0,
      currentTime: 0,
      duration: 0,
      userAnswers: [],
      score: 0,
      scorePercentage: 0,
      showAdvanced: false,
      feedback: {
        loading: false,
        vocabulary: [],
        expressions: [],
        background: '',
        structure: ''
      },
      advanced: {
        loading: false,
        materials: []
      },
      steps: [
        { name: '听力' },
        { name: '答题' },
        { name: '反馈' }
      ],
      audioProgressInterval: null,
      error: false,
      errorMessage: ''
    }
  },
  computed: {
    allQuestionsAnswered() {
      return this.userAnswers.length === this.material.questions.length && 
        !this.userAnswers.includes(undefined)
    }
  },
  async mounted() {
    await this.fetchMaterial()
    
    if (this.material.id) {
      this.checkFavorite()
      this.setupAudioService()
    }
  },
  beforeUnmount() {
    // 清理进度更新计时器
    if (this.audioProgressInterval) {
      clearInterval(this.audioProgressInterval)
    }
    
    // 停止音频播放
    AudioService.pause()
    
    // 移除事件监听器
    AudioService.removeEventListener('play', this._handlePlay)
    AudioService.removeEventListener('pause', this._handlePause)
    AudioService.removeEventListener('ended', this._handleEnded)
  },
  methods: {
    setupAudioService() {
      // 设置音频源
      AudioService.setAudioSource(this.material.audio_url)
      
      // 绑定事件处理函数（保存引用以便后续可以移除）
      this._handlePlay = () => {
        this.isPlaying = true
      }
      
      this._handlePause = () => {
        this.isPlaying = false
      }
      
      this._handleEnded = () => {
        this.isPlaying = false
        this.audioProgress = 0
      }
      
      // 监听播放状态变化
      AudioService.addEventListener('play', this._handlePlay)
      AudioService.addEventListener('pause', this._handlePause)
      AudioService.addEventListener('ended', this._handleEnded)
      
      // 设置定时更新进度
      this.audioProgressInterval = setInterval(() => {
        this.updateAudioProgress()
      }, 100)
      
      // 同步初始状态
      this.isPlaying = AudioService.isPlaying
      this.updateAudioProgress()
    },
    updateAudioProgress() {
      this.currentTime = AudioService.getCurrentTime()
      this.duration = AudioService.getDuration() || 0
      this.audioProgress = AudioService.getProgress()
    },
    formatTime(seconds) {
      if (!seconds || isNaN(seconds)) return '00:00'
      const mins = Math.floor(seconds / 60)
      const secs = Math.floor(seconds % 60)
      return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
    },
    async fetchMaterial() {
      this.loading = true
      this.error = false
      this.errorMessage = ''
      
      try {
        const materialId = this.$route.params.id
        
        // 使用MaterialService获取材料数据
        const material = await MaterialService.getMaterialById(materialId)
        
        // 标准化材料数据结构
        this.material = this.standardizeMaterialData(material)
        
        // 初始化用户答案数组
        if (this.material.questions) {
          this.userAnswers = new Array(this.material.questions.length)
        }
      } catch (error) {
        console.error('获取听力材料失败:', error)
        this.error = true
        this.errorMessage = `无法加载听力材料，请稍后再试。(${error.message || '未知错误'})`
        this.material = {}
      } finally {
        this.loading = false
      }
    },
    /**
     * 标准化材料数据结构，确保前端组件可以正确处理不同来源的材料数据
     */
    standardizeMaterialData(material) {
      const standardizedMaterial = { ...material }
      
      // 处理音频URL
      if (!standardizedMaterial.audio_url && standardizedMaterial.audio_file) {
        const difficulty = standardizedMaterial.difficulty || 'CET4'
        standardizedMaterial.audio_url = `/materials/${difficulty}/${standardizedMaterial.audio_file}`
      }
      
      // 处理题目结构
      if (standardizedMaterial.questions) {
        standardizedMaterial.questions = standardizedMaterial.questions.map(q => {
          // 如果问题已经是标准格式，直接返回
          if (typeof q.options === 'object' && Array.isArray(q.options)) {
            return q
          }
          
          // 如果问题格式不标准，尝试转换
          const standardQuestion = { ...q }
          
          // 处理选项
          if (typeof q.options === 'string') {
            try {
              standardQuestion.options = JSON.parse(q.options)
            } catch (e) {
              // 如果无法解析，尝试用逗号分隔
              standardQuestion.options = q.options.split(',').map(opt => opt.trim())
            }
          }
          
          return standardQuestion
        })
      }
      
      // 处理主题/话题
      if (!standardizedMaterial.topic && standardizedMaterial.topics) {
        standardizedMaterial.topic = standardizedMaterial.topics
      }
      
      return standardizedMaterial
    },
    async checkFavorite() {
      try {
        // 这里使用模拟用户ID，实际项目中应从用户认证系统获取
        const userId = 'user123'
        const response = await axios.post('http://localhost:5000/api/favorites/check', {
          user_id: userId,
          material_id: this.material.id
        })
        this.isFavorite = response.data.is_favorited
      } catch (error) {
        console.error('检查收藏状态失败:', error)
        this.isFavorite = false
      }
    },
    async toggleFavorite() {
      try {
        // 这里使用模拟用户ID，实际项目中应从用户认证系统获取
        const userId = 'user123'
        
        if (this.isFavorite) {
          // 取消收藏
          await axios.post('http://localhost:5000/api/favorites/remove', {
            user_id: userId,
            material_id: this.material.id
          })
        } else {
          // 添加收藏
          await axios.post('http://localhost:5000/api/favorites/add', {
            user_id: userId,
            material_id: this.material.id
          })
        }
        
        this.isFavorite = !this.isFavorite
      } catch (error) {
        console.error('操作收藏失败:', error)
      }
    },
    togglePlayback() {
      if (AudioService.isPlaying) {
        AudioService.pause();
      } else {
        AudioService.play().catch(error => {
          console.error('音频播放失败:', error);
          alert('音频播放失败，请确保音频文件存在并且格式正确。');
        });
      }
    },
    replayAudio() {
      AudioService.reset();
      AudioService.play().catch(error => {
        console.error('音频播放失败:', error);
        alert('音频播放失败，请确保音频文件存在并且格式正确。');
      });
    },
    async submitAnswers() {
      if (!this.allQuestionsAnswered) {
        return;
      }
      
      // 计算得分
      this.score = 0;
      const formattedAnswers = [];
      const userAnswersForRecommendation = [];
      
      this.material.questions.forEach((question, index) => {
        const isCorrect = this.userAnswers[index] === question.answer;
        if (isCorrect) {
          this.score++;
        }
        
        formattedAnswers.push({
          question_id: index,
          question: question.question,
          user_answer: this.userAnswers[index],
          correct_answer: question.answer,
          is_correct: isCorrect
        });
        
        // 构建用户答题数据，用于推荐系统
        userAnswersForRecommendation.push({
          material_id: this.material.id,
          question_id: question.id || index, // 使用question.id或索引作为问题ID
          user_answer: this.userAnswers[index],
          correct_answer: question.answer,
          is_correct: isCorrect,
          question_section: question.section || 'unknown',
          question_tags: this.getQuestionTags(question)
        });
      });
      
      this.scorePercentage = Math.round((this.score / this.material.questions.length) * 100);
      
      // 保存用户答题数据到本地存储，用于推荐系统
      try {
        // 确保数据格式正确并完整保存
        localStorage.setItem('lastAnswers', JSON.stringify(userAnswersForRecommendation));
        console.log('答题数据已保存:', userAnswersForRecommendation.length, '条记录');
      } catch (error) {
        console.error('保存答题数据失败:', error);
      }
      
      // 先切换到结果页，再获取反馈
      this.currentStep = 2;
      
      // 获取学习反馈
      this.fetchFeedback(formattedAnswers);
      
      // 获取进阶材料推荐（如果分数足够高）
      if (this.scorePercentage >= 70) {
        this.showAdvanced = true;
        this.fetchAdvancedMaterials();
      }
    },
    
    getQuestionTags(question) {
      // 从问题中提取标签，用于推荐系统
      const tags = [];
      
      // 防止question为undefined或null
      if (!question) {
        return ['未知'];
      }
      
      // 根据问题部分添加标签
      if (question.section) {
        tags.push(question.section === 'A' ? '新闻听力' : 
                 question.section === 'B' ? '对话听力' : 
                 question.section === 'C' ? '短文听力' : '其他');
      }
      
      // 根据问题内容添加标签
      const questionText = question.question ? question.question.toLowerCase() : '';
      if (questionText.includes('what') || questionText.includes('which')) {
        tags.push('细节理解');
      } else if (questionText.includes('why')) {
        tags.push('原因分析');
      } else if (questionText.includes('how')) {
        tags.push('方式方法');
      } else if (questionText.includes('main') || questionText.includes('topic')) {
        tags.push('主旨理解');
      }
      
      // 检查是否包含数字信息
      if (questionText.includes('many') || 
          questionText.includes('much') || 
          questionText.includes('number') || 
          questionText.includes('percentage')) {
        tags.push('数字信息');
      }
      
      // 确保至少返回一个标签
      if (tags.length === 0) {
        tags.push('一般理解');
      }
      
      return tags;
    },
    async fetchFeedback(answers) {
      this.feedback.loading = true
      try {
        // 发送材料ID和用户答题情况到后端API
        const response = await axios.post('http://localhost:5000/api/listening/feedback', {
          material_id: this.material.id,
          answers: answers
        }, { 
          timeout: 180000 // 增加到180秒超时，给大模型足够的处理时间
        });
        
        // 更新反馈数据
        if (response && response.data) {
          this.feedback = {
            ...response.data,
            loading: false
          }
        } else {
          throw new Error('空响应数据');
        }
      } catch (error) {
        console.error('获取学习反馈失败:', error)
        // 提供后备反馈数据
        this.feedback = {
          loading: false,
          vocabulary: ['请重新提交', '获取反馈失败'],
          expressions: ['请稍后再试'],
          background: '无法获取学习反馈，请检查网络连接或稍后再试。',
          structure: '无法获取听力结构分析，请稍后再试。',
          mistakes_analysis: '系统无法分析您的错题，请稍后再试。'
        }
        
        // 显示错误信息（如果有通知系统）
        if (this.$notify) {
          this.$notify({
            type: 'error',
            title: '获取反馈失败',
            message: '无法从服务器获取学习反馈，将显示基础反馈信息。'
          });
        } else if (this.$message) {
          this.$message.error('获取学习反馈失败，将显示基础反馈信息。');
        } else {
          console.error('获取学习反馈失败，将显示基础反馈信息。');
        }
      }
    },
    async fetchAdvancedMaterials() {
      this.advanced.loading = true
      try {
        const response = await axios.get(`http://localhost:5000/api/listening/advanced/${this.material.difficulty}`)
        this.advanced = {
          loading: false,
          materials: response.data.materials
        }
      } catch (error) {
        console.error('获取进阶材料失败:', error)
        this.advanced = {
          loading: false,
          materials: []
        }
      }
    },
    startSpeakingPractice() {
      this.$router.push(`/speaking/${this.material.id}`)
    },
    retryExercise() {
      this.currentStep = 0
    },
    goToRecommendation() {
      // 跳转到推荐页面
      try {
        const lastAnswersStr = localStorage.getItem('lastAnswers');
        if (lastAnswersStr) {
          const lastAnswers = JSON.parse(lastAnswersStr);
          console.log('找到答题数据，跳转到推荐页面', lastAnswers.length, '条记录');
        } else {
          console.warn('没有找到答题数据，但仍然尝试跳转');
        }
        
        // 无论如何都跳转，让推荐页面处理数据获取
        this.$router.push({
          name: 'recommendation',
          params: {
            fromListening: true
          }
        });
      } catch (error) {
        console.error('跳转到推荐页面失败:', error);
        // 如果出错，尝试使用简单的路由跳转
        this.$router.push('/recommendation');
      }
    },
    retryFetchMaterial() {
      this.fetchMaterial()
    }
  }
}
</script>

<style scoped>
.result-container {
  margin-top: 20px;
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
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

.actions-row {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
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
</style> 