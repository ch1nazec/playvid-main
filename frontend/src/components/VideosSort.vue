<script>
export default {
    props: {
      toggleSort: {
      type: Function,
      required: true,}
    },
    methods: {
        handle(name) {
            this.toggleSort(name);
        }
    },
}
</script>

<template>
    <div>
        <button @click="handle('channel_name')">По названию канала</button><br>
        <button @click="handle('name')">По названию видео</button>
    </div>
</template>