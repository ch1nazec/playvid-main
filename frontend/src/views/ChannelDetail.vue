<script setup>
import { onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useChannelDetail } from '@/stores/channel';
import defaultAvatar from '@/assets/default_avatar.png';

const route = useRoute();
const channelDetail = useChannelDetail()

onMounted(async () => {
    const channelId = route.params.id;
    if (channelId) {
        await channelDetail.fetchChannel(channelId);}
})

</script>

<template>
  <div v-if="channelDetail.channel" class="channel-page">
    <div class="channel-header">
      <img
        :src="channelDetail.channel.avatar || defaultAvatar"
        alt="Channel avatar"
        class="channel-avatar"
      />

      <div class="channel-meta">
        <h1 class="channel-name">
          {{ channelDetail.channel.channel_name }}
        </h1>

        <span class="channel-date">
          Создан: {{ channelDetail.channel.created_date }}
        </span>
      </div>
    </div>

    <div class="channel-description">
      {{ channelDetail.channel.description }}
    </div>
  </div>
</template>

<style>
.channel-page {
  min-height: 100vh;
  width: 100%;
  padding: 48px 64px;
  background: #f9fafb;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
}

.channel-header {
  display: flex;
  align-items: center;
  gap: 32px;
  margin-bottom: 40px;
}

.channel-avatar {
  width: 140px;
  height: 140px;
  border-radius: 50%;
  object-fit: cover;
  border: 4px solid #e5e7eb;
}

.channel-meta {
  display: flex;
  flex-direction: column;
}

.channel-name {
  margin: 0;
  font-size: 36px;
  font-weight: 700;
  color: #111827;
}

.channel-date {
  margin-top: 6px;
  font-size: 14px;
  color: #6b7280;
}

.channel-description {
  max-width: 900px;
  font-size: 18px;
  line-height: 1.7;
  color: #374151;
}

</style>