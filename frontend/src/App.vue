<script setup>
import Camera from './components/Camera.vue'
import Upload from './components/Upload.vue'
</script>

<template>
  <div>
    <h1>动作识别系统</h1>
    <div class="button-container">
      <Camera />
      <Upload />
    </div>
  </div>
</template>

<style scoped>
.button-container {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  gap: 2rem;
}
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
