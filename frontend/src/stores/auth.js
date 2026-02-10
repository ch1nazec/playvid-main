import { defineStore } from "pinia"
import { ref, computed } from "vue"
import Cookies from "js-cookie"
import api from '@/services/api'
import router from "@/router"
import '@/assets/main.css'


export const useAuthStore = defineStore('auth', () => {
    const user = ref(null)
    const isInitialized = ref(false)
    const isLoading = ref(false)
    
    const isAuthenticated = computed(() => {
        return !!localStorage.getItem('access_token')
    })
    
    const fetchUser = async() => {
        try {
            const {data} = await api.get('/users/me')
            user.value = data;
            return data
        } catch (e) {
            logout()
        }
    }

    const initialize = async () => {
        if (localStorage.getItem('access_token')) {
            await fetchUser()
        }
        isInitialized.value = true
    }
    
    const login = async (credential) => {
        const { data } = await api.post('/token/', credential);
        localStorage.setItem('access_token', data.access)
        localStorage.setItem('refresh_token', data.refresh)

        await fetchUser();
        router.push('/')
    }

    const logout = async () => {
        isLoading.value = true

        try {
            clearUser()  
        } catch (error) {
            isLoading.value = false
        }
    }

    const clearUser = () => {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')

        user.value = null

        Cookies.remove('access_token')
        Cookies.remove('refresh_token')   
    }

    return {
        user,
        isAuthenticated,
        isInitialized,
        fetchUser,
        login,
        logout,
        initialize
    }
})