import { createRouter, createWebHistory } from 'vue-router'
import MigrationFlow from '../views/MigrationFlow.vue'
import NeighborhoodAnalysis from '../views/NeighborhoodAnalysis.vue'
import GentrificationAnalysis from '../views/GentrificationAnalysis.vue'

const routes = [
  {
    path: '/',
    redirect: '/gentrification' // Default landing page
  },
  {
    path: '/gentrification',
    name: 'GentrificationAnalysis',
    component: GentrificationAnalysis,
    meta: { title: 'LA Gentrification - Analysis' }
  },
  {
    path: '/neighborhood',
    name: 'NeighborhoodAnalysis',
    component: NeighborhoodAnalysis,
    meta: { title: 'LA Gentrification - Neighborhood Analysis' }
  },
  {
    path: '/migration',
    name: 'MigrationFlow',
    component: MigrationFlow,
    meta: { title: 'LA Gentrification - Migration Flow' }
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

// Update page title on route change
router.beforeEach((to, from, next) => {
  document.title = to.meta.title || 'LA Gentrification Dashboard'
  next()
})

export default router