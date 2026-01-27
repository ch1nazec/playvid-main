import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue';
import VideoDetail from '@/views/VideoDetail.vue';


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView // Главная страница
    },
    {
      path: '/video/:id',
      name: 'video',
      component: VideoDetail
    }
  ]
})

export default router