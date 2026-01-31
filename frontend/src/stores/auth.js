import { defineStore } from "pinia"
import { ref, computed } from "vue"
import api from '@/services/api'
import router from "@/router"


export const useAuthStore = defineStore('auth', () => {
    const user = ref(null)
    const isAuthenticated = computed(() => !!user.value)

    const login = async (credential) => {
        try {
            const response = await api.post('/token/', credential)
            localStorage.setItem('access_token', response.data.success)
            localStorage.setItem('refresh_token', response.data.refresh)
            
            await fetchUser()
            router.push('/')
        } catch (error) {
            throw error
        }
    }
    const logout = () => {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        user.value = null
        router.push('/login')
    }
    const fetchUser = async () => {
        try {
            const response = await api.get('/user/me')
            user.value = response.data
        } catch (error) {
            console.log('Failed to fetch user')
        }
    }
    const initialize = () => {
        const token = localStorage.getItem('access_token')
        if (token) {
            fetchUser()
        }
    }

    return {
        user,
        isAuthenticated,
        login,
        logout,
        fetchUser,
        initialize
    }
})