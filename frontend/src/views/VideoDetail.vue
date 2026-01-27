<script setup>
import { useRoute } from 'vue-router';
import { ref } from 'vue';
import { useVideoDetail } from '@/stores/video';

const router = useRoute();
const video_id = router.params.id

const videoDetail = useVideoDetail(video_id);

</script>

<template>
{{ video_id }}
</template>

<style>
    
</style>