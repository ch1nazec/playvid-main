import { defineStore } from "pinia";
import axios from 'axios';


export const useChannelsList = defineStore('channels', {
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


export const useChannelDetail = defineStore('channel', {
    state: () => ({
        channel: null,
    }),
    actions: {
        async fetchChannel(id) {
            const response = await axios.get(`/api/users/channel/${id}`);
            this.channel = response.data;
        }
    }
})