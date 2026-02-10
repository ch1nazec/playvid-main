import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue';
import VideoDetail from '@/views/VideoDetail.vue';
import ChannelList from '@/views/ChannelList.vue';
import UserDetail from '@/views/UserDetail.vue';
import ChannelDetail from '@/views/ChannelDetail.vue';
import { useAuthStore } from '@/stores/auth';


const routes = [
    {
      path: '/',
      name: 'home',
      component: HomeView // Главная страница
    },
    {
      path: '/video/:id',
      name: 'video',
      component: VideoDetail
    },
    {
      path: '/channel',
      name: 'channels',
      component: ChannelList
    },
    {
      path: '/channel/:id',
      name: 'channel',
      component: ChannelDetail
    },
    {
      path: '/user/:id',
      name: 'user',
      component: UserDetail
    },

    // Register & login
    {
      path: '/register',
      component: () => import('@/components/Register.vue'),
      meta: {requiresGuest: true}
    },
    {
      path: '/login',
      component: () => import('@/components/Login.vue'),
      meta: {requiresGuest: true}
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('@/components/Profile.vue'),
      meta: {requiresAuth: true}
    },
    {
      path: '/logout',
      name: 'logout',
      component: () => import('@/views/Logout.vue'),
      meta: {requiresAuth: true}
    }
  ]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const auth = useAuthStore()

  if (!auth.isInitialized) {
    return next()
  }

  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    next('/login')
  } else if (to.meta.requiresGuest && auth.isAuthenticated) {
    next('/')
  } else {
    next()
  }
})


export default router