<script setup>
import { computed, onMounted, ref } from 'vue';
import { useVideosStore } from '@/stores/video';
import { storeToRefs } from 'pinia';
import VideosSort from '@/components/VideosSort.vue';
import _ from 'lodash';


const videosStore = useVideosStore();
const { videos } = storeToRefs(videosStore);
let sortField = ref("date_upload");

const videosSorted = computed(() => {
    return _(videos.value)
    .orderBy(x => x[sortField.value])
    .value();
});

function toggleSort(fieldName) {
    sortField.value = fieldName
}

onMounted(() => {
  videosStore.fetchVideo()
})
</script>

<template>
    <VideosSort :toggleSort="toggleSort"/>
    <div class="videos-container">
        <div v-for="video in videosSorted" :key="video.id" class="video-card">
            <router-link :to="{name: 'video', params: {id: video.id}}">
                <div class="video-preview-container">
                    <img 
                        :src="video.preview || 'src/assets/dont_preview.png'" 
                        :alt="video.name"
                        class="video-preview"
                        loading="lazy"
                    >
                    <div class="video-overlay">
                        <button class="play-button">
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="white">
                                <path d="M8 5v14l11-7z"/>
                            </svg>
                        </button>
                    </div>
                </div>
            </router-link>
            <div class="video-content">
                <div class="channel-info">
                    <div class="channel-avatar">
                        <img 
                            :src="video.channel_avatar || 'src/assets/default_avatar.png'" 
                            :alt="video.channel_name"
                        >
                    </div>
                    <div class="channel-details">
                        <h3 class="channel-name">{{ video.channel_name || "Без названия" }}</h3>
                        <span class="upload-time">2 дня назад</span>
                    </div>
                </div>
                <h2 class="video-title" :title="video.name">
                    {{ video.name }}
                </h2>
                <p v-if="video.description" class="video-description">
                    {{ video.description.length > 100 ? video.description.substring(0, 100) + '...' : video.description }}
                </p>
                <div class="video-stats">
                    <div class="stat-item">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="#909090">
                            <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
                        </svg>
                    </div>
                    <div class="stat-item">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="#909090">
                            <path d="M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z"/>
                        </svg>
                    </div>
                    <div class="stat-item">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="#909090">
                            <path d="M22 4h-20v16h20V4zm-2 14h-16v-12h16v12zM4 6h2v10H4zm4 0h2v10H8zm4 0h2v10h-2zm4 0h2v4h-2z"/>
                        </svg>
                        <span>{{ new Date(video.date_upload).toLocaleDateString('ru-RU') }}</span>
                    </div>
                </div>

                <div v-if="video.tags && video.tags.length" class="video-tags">
                    <span v-for="tag in video.tags.slice(0, 3)" :key="tag.id" class="tag">
                        {{ tag.name }}
                    </span>
                    <span v-if="video.tags.length > 3" class="tag-more">
                        +{{ video.tags.length - 3 }}
                    </span>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
/* === Контейнер для всех видео === */
.videos-container {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
    gap: 24px;
    padding: 20px;
    max-width: 1600px;
    margin: 0 auto;
}

/* === Карточка видео === */
.video-card {
    background: #ffffff;
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    transition: all 0.3s ease;
    border: 1px solid #e5e5e5;
    display: flex;
    flex-direction: column;
    height: 100%;
}

.video-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.15);
    border-color: #d1d1d1;
}

/* === Контейнер превью === */
.video-preview-container {
    position: relative;
    width: 100%;
    height: 190px;
    overflow: hidden;
    background: #f5f5f5;
}

.video-preview {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.4s ease;
}

.video-card:hover .video-preview {
    transform: scale(1.05);
}

.video-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(to top, rgba(0,0,0,0.4), transparent);
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    padding: 16px;
    opacity: 0;
    transition: opacity 0.3s ease;
}

.video-card:hover .video-overlay {
    opacity: 1;
}

.play-button {
    width: 48px;
    height: 48px;
    background: rgba(255, 0, 0, 0.9);
    border: none;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.3s ease;
    backdrop-filter: blur(4px);
}

.play-button:hover {
    background: #ff0000;
    transform: scale(1.1);
}

.duration-badge {
    background: rgba(0, 0, 0, 0.8);
    color: white;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 12px;
    font-weight: 500;
    backdrop-filter: blur(4px);
}

/* === Контент карточки === */
.video-content {
    padding: 20px;
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    gap: 12px;
}

/* === Информация о канале === */
.channel-info {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 4px;
}

.channel-avatar {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    overflow: hidden;
    border: 2px solid #f0f0f0;
    flex-shrink: 0;
}

.channel-avatar img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.channel-details {
    display: flex;
    flex-direction: column;
    gap: 2px;
}

.channel-name {
    font-size: 14px;
    font-weight: 600;
    color: #333;
    margin: 0;
    line-height: 1.2;
}

.channel-name:hover {
    color: #ff0000;
    cursor: pointer;
}

.upload-time {
    font-size: 12px;
    color: #909090;
}

/* === Название видео === */
.video-title {
    font-size: 16px;
    font-weight: 700;
    color: #111;
    margin: 0;
    line-height: 1.4;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    height: 44px;
}

/* === Описание === */
.video-description {
    font-size: 14px;
    color: #606060;
    margin: 0;
    line-height: 1.5;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

/* === Статистика === */
.video-stats {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-top: 8px;
    padding-top: 12px;
    border-top: 1px solid #f0f0f0;
}

.stat-item {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 13px;
    color: #606060;
}

.stat-item svg {
    flex-shrink: 0;
}

/* === Теги === */
.video-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-top: auto;
    padding-top: 12px;
}

.tag {
    background: #f0f0f0;
    color: #606060;
    padding: 4px 10px;
    border-radius: 12px;
    font-size: 12px;
    font-weight: 500;
    transition: all 0.2s ease;
}

.tag:hover {
    background: #e0e0e0;
    color: #333;
    cursor: pointer;
}

.tag-more {
    background: transparent;
    color: #909090;
    padding: 4px 8px;
    font-size: 12px;
}

/* === Адаптивность === */
@media (max-width: 768px) {
    .videos-container {
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 16px;
        padding: 12px;
    }
    
    .video-preview-container {
        height: 170px;
    }
    
    .video-content {
        padding: 16px;
    }
}

@media (max-width: 480px) {
    .videos-container {
        grid-template-columns: 1fr;
    }
    
    .video-preview-container {
        height: 200px;
    }
}

/* === Анимация появления === */
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.video-card {
    animation: fadeIn 0.5s ease forwards;
}

.video-card:nth-child(2) { animation-delay: 0.1s; }
.video-card:nth-child(3) { animation-delay: 0.2s; }
.video-card:nth-child(4) { animation-delay: 0.3s; }
.video-card:nth-child(5) { animation-delay: 0.4s; }
</style>