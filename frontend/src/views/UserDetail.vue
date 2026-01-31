<script setup>
import { onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useUserDetail } from '@/stores/user';

const route = useRoute();
const userDetail = useUserDetail();

onMounted(async () => {
    const userId = route.params.id;
    if (userId) {
        await userDetail.fetchUserData(userId);
    }
})
</script>

<template>
    <div v-if="userDetail.user" class="user-card">
    <h1 class="username">{{ userDetail.user.username }}</h1>

    <p class="fullname">
      {{ userDetail.user.first_name }} {{ userDetail.user.last_name }}
    </p>

    <div class="info">
      <span>Email:</span>
      <p>{{ userDetail.user.email }}</p>
    </div>

    <div class="info">
      <span>Телефон:</span>
      <p>{{ userDetail.user.phone_number }}</p>
    </div>
  </div>
</template>

<style>
.user-card {
  max-width: 420px;
  margin: 80px auto;
  padding: 24px 28px;
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  font-family: system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
}

.username {
  margin: 0;
  font-size: 28px;
  font-weight: 700;
  color: #111827;
}

.fullname {
  margin-top: 6px;
  margin-bottom: 20px;
  font-size: 16px;
  color: #6b7280;
}

.info {
  display: flex;
  flex-direction: column;
  margin-bottom: 14px;
}

.info span {
  font-size: 13px;
  color: #9ca3af;
  margin-bottom: 4px;
}

.info p {
  margin: 0;
  font-size: 15px;
  color: #1f2937;
}

</style>