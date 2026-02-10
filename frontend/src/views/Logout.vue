<template>
<button @click="handleLogout">Выйти из аккаунта</button>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router';

const authStore = useAuthStore()
const router = useRouter()

const handleLogout = async () => {
    await authStore.logout();
    router.push('/login')
}
</script>