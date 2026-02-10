<template>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

<header class="p-4 mb-4 border-bottom" style="min-height: 80px;">
    <div class="container">
      <div class="d-flex flex-wrap align-items-center justify-content-center justify-content-lg-start">

        <img src="@/assets/logo.png" alt="Логотип" width="40" height="32"class="me-2">
        <ul class="nav me-lg-auto mb-2 mb-md-0">
          <li><router-link to="/" class="nav-link px-2 link-secondary">Главная</router-link></li>
        </ul>

        <form class="col-12 col-lg-auto mb-3 mb-lg-0 me-lg-3">
          <input type="search" class="form-control" placeholder="Поиск видео" aria-label="Search">
        </form>

        <div class="dropdown text-end" v-if="authStore.isAuthenticated && !isLoading">
          <a href="#" class="d-block link-dark text-decoration-none dropdown-toggle" id="dropdownUser1" data-bs-toggle="dropdown" aria-expanded="false">
            <img :src="avatar" alt="mdo" width="32" height="32" class="rounded-circle">
          </a>
          <ul class="dropdown-menu text-small" aria-labelledby="dropdownUser1">
            <li><router-link class="dropdown-item" to="profile">Профиль</router-link></li>
            <li><hr class="dropdown-divider"></li>
            <li><router-link class="dropdown-item" to="logout">Выход</router-link></li>
          </ul>
        </div>
        <div v-else>
          <router-link 
          to="/login" 
          class="login-responsive"
        >
          <i class="bi bi-box-arrow-in-right"></i>
          <span class="login-text">Войти</span>
      </router-link>
        </div>
      </div>
    </div>
  </header>

</template>

<script setup>

import { useAuthStore } from '@/stores/auth';
import { computed, onMounted, ref } from 'vue';


const authStore = useAuthStore()
const avatar = ref(false)
const error = ref(null)
const isLoading = ref(authStore.isLoading)

onMounted(async () => {
  try {
    if (authStore.isAuthenticated && !authStore.user) {
      await authStore.fetchUser()}
    
    if (authStore.user?.avatar) {
      avatar.value = authStore.user.avatar
    }
    else {
      avatar.value = new URL('@/assets/default_avatar.png', import.meta.url).href
    }

  } catch (error) {
    console.error('Ошибка загрузки аватара:', error)
    avatar.value = new URL('@/assets/default_avatar.png', import.meta.url).href
  }
})
</script scoped>

<style>
.login-responsive {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.875rem;
  font-weight: 500;
  color: #4b5563;
  text-decoration: none;
  padding: 8px 16px;
  border-radius: 6px;
  transition: all 0.3s ease;
}

.login-responsive:hover {
  color: #2563eb;
  background-color: rgba(37, 99, 235, 0.05);
}

.login-responsive i {
  font-size: 1rem;
}

.login-text {
  display: inline;
}

@media (max-width: 768px) {
  .login-text {
    display: none;
  }
  
  .login-responsive {
    padding: 8px;
    width: 40px;
    height: 40px;
    justify-content: center;
  }
}
</style>