<template>
    <div class="register">
            <h2>Регистрация</h2>
            <form @submit.prevent="register">
                <div>
                    <label>Username</label>
                    <input v-model="form.username" type="text" required>
                </div>
                <div>
                    <label>Email</label>
                    <input v-model="form.email" type="text" required>
                </div>
                <div>
                    <label>Password</label>
                    <input v-model="form.password" type="text" required>
                </div>

                <button type="submit" :disabled="loading">
                    {{ loading ? 'Загрузка...' : 'Зарегистрироваться' }}
                </button>
                <p v-if="error" class="error">{{ error }}</p>
                <p v-if="success" class="success">{{ error }}</p>
                <p></p>
            </form>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import api from '@/services/api'
import { useRouter } from 'vue-router';


const router = useRouter();
const loading = ref(false);
const error = ref('');
const success = ref('');

const form = ref({
    username: "",
    email: "",
    password: ""
})

const register = async () => {
    loading.value = true;
    error.value = ''
    success.value = ''

    try {
        const response = await api.post('users/register/', form.value);
        success.value = 'Регистрация успешна! Авторизуйтесь';

        form.value = {username: '', email: '', password: ''};
        setTimeout(() => {
            router.push('/login')
        }, 2000)
    } catch (err) {
        if (err.response?.data) {
            error.value = Object.values(err.response.data).flat().join(', ');
        } else {
            error.value = 'Ошибка сервака'
        }
    } finally {
    loading.value = false
  }

}
</script>