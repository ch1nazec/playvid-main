<template>
  <div class="container">
    <form class="form-signin" @submit.prevent="handleLogin">
      <img class="mb-4" src="@/assets/logo.png" alt="Logo" width="72" height="57" />
      <h1 class="h3 mb-3 fw-normal">Вход</h1>

      <div class="form-floating">
        <input
          type="text"
          class="form-control"
          id="floatingInput"
          v-model="form.username"
          placeholder="DanilKolbasenko"
          autocomplete="username"
        />
        <label for="floatingInput">Логин</label>
      </div>

      <div class="form-floating">
        <input
          type="password"
          class="form-control"
          id="floatingPassword"
          v-model="form.password"
          placeholder="Пароль"
          autocomplete="current-password"
        />
        <label for="floatingPassword">Пароль</label>
      </div>

      <button
        class="w-100 btn btn-lg btn-primary mt-3"
        type="submit"
        :disabled="loading"
      >
        Вход
      </button>

      <p v-if="error" class="mt-3 text-danger text-center">{{ error }}</p>

      <p class="mt-5 mb-3 text-muted text-center">2026</p>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const router = useRouter()

const loading = ref(false)
const error = ref('')
const form = ref({
  username: '',
  password: ''
})

const handleLogin = async () => {
  error.value = ''
  loading.value = true

  try {
    await authStore.login(form.value)
    router.push('/')
  } catch (err) {
    if (err.response?.status === 401) {
      error.value = 'Неверный логин или пароль'
    } else {
      error.value = err.response?.data?.message || 'Ошибка сервера'
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.container {
        display: grid;
        place-items: center; /* Сокращение для justify-items и align-items */
        /* height: 100vh; */
    }
</style>