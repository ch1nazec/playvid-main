<script setup>
import Header from './components/Header.vue';

</script>

<template>

    <div class="app-root">
    <Header />
    <main class="main-content">
      <router-view />
    </main>
    
  </div>
</template>

<style>
.app-root {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1 0 auto;
}
</style>