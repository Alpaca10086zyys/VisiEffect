<template>
  <div class="camera-container">
    <button @click="toggleCamera">{{ isActive ? '关闭摄像头' : '打开摄像头' }}</button>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const isActive = ref(false)

const toggleCamera = async () => {
  isActive.value = !isActive.value
  if (isActive.value) {
    try {
      const response = await fetch('http://localhost:8000/action_recognition/start_camera/', {
        method: 'POST'
      })
      const data = await response.json()
      console.log(data)
    } catch (error) {
      console.error('Error:', error)
      isActive.value = false
    }
  }
}
</script>

<style scoped>
.camera-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

button {
  padding: 10px 20px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
}
</style> 