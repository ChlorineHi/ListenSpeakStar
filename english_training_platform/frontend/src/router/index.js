import { createRouter, createWebHistory } from 'vue-router'
import ListeningCreate from '../views/teacher/ListeningCreate.vue'
import AssessmentCreate from '../views/teacher/AssessmentCreate.vue'
import Home from '../views/Home.vue'
import Listening from '../views/Listening.vue'
import ListeningDetail from '../views/ListeningDetail.vue'
import ListeningResult from '../views/ListeningResult.vue'
import SpeakingPractice from '../views/SpeakingPractice.vue'
import Favorites from '../views/Favorites.vue'
import RecommendationPage from '../views/RecommendationPage.vue'

const routes = [
          {
                    path: '/',
                    name: 'Home',
                    component: Home
          },
          {
                    path: '/listening',
                    name: 'Listening',
                    component: Listening
          },
          {
                    path: '/listening/:id',
                    name: 'ListeningDetail',
                    component: ListeningDetail,
                    props: true
          },
          {
                    path: '/result/:id',
                    name: 'ListeningResult',
                    component: ListeningResult,
                    props: true
          },
          {
                    path: '/speaking',
                    name: 'Speaking',
                    component: () => import('../views/Speaking.vue')
          },
          {
                    path: '/speaking/:materialId',
                    name: 'SpeakingPractice',
                    component: SpeakingPractice,
                    props: true
          },
          {
                    path: '/favorites',
                    name: 'Favorites',
                    component: Favorites
          },
          {
                    path: '/assessment',
                    name: 'Assessment',
                    component: () => import('../views/Assessment.vue')
          },
          {
                    path: '/agent-recommendation',
                    name: 'AgentRecommendation',
                    component: () => import('../views/AgentRecommendation.vue')
          },
          {
                    path: '/recommendation',
                    name: 'recommendation',
                    component: RecommendationPage
          },
          // 教师端路由
          {
                    path: '/teacher',
                    name: 'TeacherDashboard',
                    component: () => import('../views/teacher/Dashboard.vue')
          },
          {
                    path: '/teacher/listening/create',
                    name: 'ListeningCreate',
                    component: ListeningCreate
          },
          {
                    path: '/teacher/listening/edit/:id',
                    name: 'ListeningEdit',
                    component: () => import('../views/teacher/ListeningEdit.vue')
          },
          {
                    path: '/teacher/speaking/create',
                    name: 'SpeakingCreate',
                    component: () => import('../views/teacher/SpeakingCreate.vue')
          },
          {
                    path: '/teacher/speaking/edit/:id',
                    name: 'SpeakingEdit',
                    component: () => import('../views/teacher/SpeakingEdit.vue')
          },
          {
                    path: '/teacher/assessment/create',
                    name: 'AssessmentCreate',
                    component: AssessmentCreate
          },
          {
                    path: '/:pathMatch(.*)*',
                    name: 'NotFound',
                    component: () => import('../views/NotFound.vue')
          }
]

const router = createRouter({
          history: createWebHistory(process.env.BASE_URL),
          routes
})

export default router 