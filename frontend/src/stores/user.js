import { defineStore } from "pinia";
import axios from 'axios'


export const useUserDetail = defineStore('user', {
    state: () => ({
        user: null,
    }),

    actions: {
        async fetchUserData(id) {
            const response = await axios.get(`/api/users/${id}`);
            this.user = response.data;
        }
    }
})