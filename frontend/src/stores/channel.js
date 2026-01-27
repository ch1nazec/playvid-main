import { defineStore } from "pinia";
import axios from 'axios';


export const useChannelsList = defineStore('channel', {
    state: () => ({
        channels: [],
    }),
    actions: {
        async fetchChannelList() {
            const response = await axios.get('/api/users/channel/');
            this.channels = response.data;
        }
    }
})