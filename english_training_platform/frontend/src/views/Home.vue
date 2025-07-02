<template>
  <div class="home">
    <!-- 主要内容 -->
    <div class="container mx-auto px-4 py-8">
      <!-- 特色功能部分 -->
      <section class="features py-12">
        <h2 class="text-2xl font-bold mb-8 text-center">平台特色</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div class="feature-card bg-white rounded-lg shadow-md p-6">
            <div class="icon-container mb-4">
              <svg class="w-12 h-12 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3"></path>
              </svg>
            </div>
            <h3 class="text-xl font-semibold mb-2">多层次听力材料</h3>
            <p>提供四六级、雅思、托福等不同难度的听力材料，覆盖多种话题，满足不同学习需求。</p>
          </div>
          
          <div class="feature-card bg-white rounded-lg shadow-md p-6">
            <div class="icon-container mb-4">
              <svg class="w-12 h-12 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"></path>
              </svg>
            </div>
            <h3 class="text-xl font-semibold mb-2">口语实时测评</h3>
            <p>提供听后口语训练功能，AI技术实时评估发音、流利度和内容准确性，帮助提升口语表达能力。</p>
          </div>
          
          <div class="feature-card bg-white rounded-lg shadow-md p-6">
            <div class="icon-container mb-4">
              <svg class="w-12 h-12 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
              </svg>
            </div>
            <h3 class="text-xl font-semibold mb-2">智能学习反馈</h3>
            <p>根据学习情况，提供重要单词、表达、背景知识和听力结构分析，帮助更全面理解听力内容。</p>
          </div>
        </div>
      </section>
      
      <!-- Agent推荐系统宣传 -->
      <section class="agent-recommendation py-12 bg-blue-50 rounded-xl p-8 my-12">
        <div class="flex flex-col md:flex-row items-center">
          <div class="md:w-1/2 mb-6 md:mb-0 md:pr-8">
            <h2 class="text-3xl font-bold mb-4 text-blue-800">AI智能推荐系统</h2>
            <p class="text-lg mb-4">基于LangChain和LangGraph构建的多Agent协作系统，为您提供真正个性化的学习体验。</p>
            <ul class="list-disc pl-5 mb-6 space-y-2">
              <li><span class="font-medium">分析Agent</span>：深入分析您的答题情况，识别听力薄弱环节</li>
              <li><span class="font-medium">推荐Agent</span>：根据您的能力特点，精准推荐最适合的学习材料</li>
              <li><span class="font-medium">协调Agent</span>：管理整个推荐流程，确保推荐结果的准确性</li>
            </ul>
            <router-link to="/agent-recommendation" class="inline-block bg-blue-600 text-white font-medium py-2 px-6 rounded-md hover:bg-blue-700 transition">
              体验智能推荐
            </router-link>
          </div>
          <div class="md:w-1/2">
            <img src="../assets/agent-system.svg" alt="Agent系统示意图" class="w-full h-auto rounded-lg shadow-lg" />
          </div>
        </div>
      </section>
      
      <!-- 其他现有内容 -->
      <!-- 头部横幅 -->
      <section class="bg-primary text-white px-4 py-12 rounded-lg shadow-md mb-10">
        <div class="max-w-4xl mx-auto">
          <h1 class="text-3xl md:text-4xl font-bold mb-4">AI赋能的英语听说训练智能平台</h1>
          <p class="text-lg md:text-xl mb-6">提供四六级、雅思、托福等难度的听力材料及口语训练功能，通过自适应推送和智能反馈帮助你提升英语听力和口语能力。</p>
          <div class="flex flex-wrap gap-4">
            <router-link to="/assessment" class="btn btn-secondary text-neutral-darkest">开始能力评估</router-link>
            <router-link to="/listening" class="btn btn-outline border-white text-white hover:bg-white hover:text-primary">浏览听力材料</router-link>
          </div>
        </div>
      </section>

      <!-- 功能介绍 -->
      <section class="mb-12">
        <h2 class="text-2xl font-bold text-neutral-darkest mb-6 text-center">平台特色功能</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <!-- 听力材料 -->
          <div class="card hover:shadow-medium transition-shadow">
            <div class="bg-primary-light text-primary-dark p-3 rounded-full w-12 h-12 flex items-center justify-center mb-4">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3" />
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-neutral-darkest mb-2">多层次听力材料</h3>
            <p class="text-neutral-dark">提供四六级、雅思、托福等不同难度的听力材料，覆盖多种话题，满足不同水平学习者的需求。</p>
          </div>

          <!-- 听力评估 -->
          <div class="card hover:shadow-medium transition-shadow">
            <div class="bg-secondary-light text-secondary-dark p-3 rounded-full w-12 h-12 flex items-center justify-center mb-4">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-neutral-darkest mb-2">智能水平评估</h3>
            <p class="text-neutral-dark">通过评估试题精准检测你的英语听力水平，为你推荐最适合的学习材料。</p>
          </div>

          <!-- 口语训练 -->
          <div class="card hover:shadow-medium transition-shadow">
            <div class="bg-success-light text-success-dark p-3 rounded-full w-12 h-12 flex items-center justify-center mb-4">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-neutral-darkest mb-2">口语实时测评</h3>
            <p class="text-neutral-dark">提供听后口语训练功能，AI技术实时评估发音、流利度和内容准确性，给出个性化改进建议。</p>
          </div>

          <!-- 学习反馈 -->
          <div class="card hover:shadow-medium transition-shadow">
            <div class="bg-danger-light text-danger-dark p-3 rounded-full w-12 h-12 flex items-center justify-center mb-4">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-neutral-darkest mb-2">智能学习反馈</h3>
            <p class="text-neutral-dark">根据你的学习情况，提供重要单词、表达、背景知识和听力结构分析，助你全面提升听力理解能力。</p>
          </div>
        </div>
      </section>

      <!-- 难度等级介绍 -->
      <section class="mb-12">
        <h2 class="text-2xl font-bold text-neutral-darkest mb-6 text-center">适应不同水平的学习者</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <!-- CET4 -->
          <div class="bg-white rounded-lg overflow-hidden shadow hover:shadow-medium transition-shadow">
            <div class="bg-primary text-white p-4">
              <h3 class="text-xl font-bold">CET-4</h3>
              <p class="text-sm">大学英语四级水平</p>
            </div>
            <div class="p-4">
              <ul class="space-y-2">
                <li class="flex items-start">
                  <span class="text-success mr-2">✓</span>
                  <span>日常对话和校园生活话题</span>
                </li>
                <li class="flex items-start">
                  <span class="text-success mr-2">✓</span>
                  <span>基础词汇和简单句式结构</span>
                </li>
                <li class="flex items-start">
                  <span class="text-success mr-2">✓</span>
                  <span>清晰发音和适中语速</span>
                </li>
              </ul>
              <router-link to="/listening?difficulty=CET4" class="btn btn-outline-primary mt-4 inline-block">
                浏览CET-4材料
              </router-link>
            </div>
          </div>
          
          <!-- CET6 -->
          <div class="bg-white rounded-lg overflow-hidden shadow hover:shadow-medium transition-shadow">
            <div class="bg-primary-dark text-white p-4">
              <h3 class="text-xl font-bold">CET-6</h3>
              <p class="text-sm">大学英语六级水平</p>
            </div>
            <div class="p-4">
              <ul class="space-y-2">
                <li class="flex items-start">
                  <span class="text-success mr-2">✓</span>
                  <span>社会、文化和科技等话题</span>
                </li>
                <li class="flex items-start">
                  <span class="text-success mr-2">✓</span>
                  <span>扩展词汇和较复杂句式</span>
                </li>
                <li class="flex items-start">
                  <span class="text-success mr-2">✓</span>
                  <span>自然语速和多样口音</span>
                </li>
              </ul>
              <router-link to="/listening?difficulty=CET6" class="btn btn-outline-primary mt-4 inline-block">
                浏览CET-6材料
              </router-link>
            </div>
          </div>
          
          <!-- IELTS -->
          <div class="bg-white rounded-lg overflow-hidden shadow hover:shadow-medium transition-shadow">
            <div class="bg-secondary text-neutral-darkest p-4">
              <h3 class="text-xl font-bold">IELTS</h3>
              <p class="text-sm">雅思考试水平</p>
            </div>
            <div class="p-4">
              <ul class="space-y-2">
                <li class="flex items-start">
                  <span class="text-success mr-2">✓</span>
                  <span>学术话题和社会议题讨论</span>
                </li>
                <li class="flex items-start">
                  <span class="text-success mr-2">✓</span>
                  <span>高级词汇和丰富表达</span>
                </li>
                <li class="flex items-start">
                  <span class="text-success mr-2">✓</span>
                  <span>各种英语口音和自然对话</span>
                </li>
              </ul>
              <router-link to="/listening?difficulty=IELTS" class="btn btn-outline-primary mt-4 inline-block">
                浏览IELTS材料
              </router-link>
            </div>
          </div>
          
          <!-- TOEFL -->
          <div class="bg-white rounded-lg overflow-hidden shadow hover:shadow-medium transition-shadow">
            <div class="bg-secondary-dark text-white p-4">
              <h3 class="text-xl font-bold">TOEFL</h3>
              <p class="text-sm">托福考试水平</p>
            </div>
            <div class="p-4">
              <ul class="space-y-2">
                <li class="flex items-start">
                  <span class="text-success mr-2">✓</span>
                  <span>学术讲座和专业领域内容</span>
                </li>
                <li class="flex items-start">
                  <span class="text-success mr-2">✓</span>
                  <span>专业术语和学术表达</span>
                </li>
                <li class="flex items-start">
                  <span class="text-success mr-2">✓</span>
                  <span>快速语速和复杂内容</span>
                </li>
              </ul>
              <router-link to="/listening?difficulty=TOEFL" class="btn btn-outline-primary mt-4 inline-block">
                浏览TOEFL材料
              </router-link>
            </div>
          </div>
        </div>
      </section>

      <!-- 开始使用 CTA -->
      <section class="bg-neutral-lighter p-8 rounded-lg text-center">
        <h2 class="text-2xl font-bold text-neutral-darkest mb-3">准备好提升你的英语能力了吗？</h2>
        <p class="text-neutral-dark mb-6 max-w-2xl mx-auto">
          通过我们的AI赋能听说训练平台，科学评估你的当前水平，获取个性化学习建议，实现英语听力和口语能力的突破性提升。
        </p>
        <router-link to="/assessment" class="btn btn-primary">开始能力评估</router-link>
      </section>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Home'
}
</script> 