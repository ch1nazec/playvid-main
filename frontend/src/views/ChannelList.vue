<script setup>
import { useChannelsList } from '@/stores/channel';
import { onMounted } from 'vue';
import { useRoute } from 'vue-router';


const router = useRoute();
const channelList = useChannelsList();

channelList.fetchChannelList()
</script>

<template>
{{ channelList.channels }}
</template>

<style>

</style>