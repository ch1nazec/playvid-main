<script setup>
import { useRoute } from 'vue-router';
import { onMounted, ref } from 'vue';
import { useVideoDetail } from '@/stores/video';

const router = useRoute();
const videoDetail = useVideoDetail();

onMounted(async () => {
    const videoId = router.params.id
    if (videoId) {
        await videoDetail.fetchDetailVideo(videoId)
    }
})

</script>

<template>
  <div class="video-container">
    <video controls :src="videoDetail.video.video" :poster="videoDetail.video.preview || 'src/assets/dont_preview.png'" class="video"></video>
    <h2 class="title">{{ videoDetail.video.name }}</h2>
    <p class="desc">{{ videoDetail.video.description }}</p>
  </div>
</template>

<style scoped>
.video-container {
  max-width: 800px;
  margin: 20px auto;
  padding: 0;
}

.video {
  width: 100%;
  border-radius: 8px;
  margin-bottom: 12px;
}

.title {
  font-size: 20px;
  margin: 8px 0;
  color: #333;
}

.desc {
  color: #666;
  line-height: 1.4;
  margin: 8px 0;
}

.date {
  color: #999;
  font-size: 14px;
}
</style>