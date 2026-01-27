import { defineStore } from "pinia";
import axios from 'axios'


export const useVideosStore = defineStore('video', {
    state: () => ({
        videos: [],
    }),
    actions: {
        async fetchVideo() {
            const response = await axios.get('/api/video/');
            this.videos = response.data
        }
    }
})


export const useVideoDetail = defineStore('videoDetail', {
    state: () => ({
        video: {},
    }),
    actions: {
        async fetchDetailVideo(id) {
            const response = await axios.get(`/api/video/${id}`);
            this.video = Object.assign({}, response.data);
        }
    }
})