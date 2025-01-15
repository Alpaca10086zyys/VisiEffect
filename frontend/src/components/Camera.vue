<template>
  <div class="camera-container">
    <button @click="toggleCamera" :class="buttonClass">
      <div class="button-content">
        <span class="button-text">{{ isActive ? '关闭摄像头' : '打开摄像头' }}</span>
        <img class="button-logo" src="../assets/video.svg" alt="Camera Logo" />
      </div>
    </button>
  </div>
</template>

<script setup>
import { ref,computed } from 'vue'

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
  else {
    // 关闭摄像头
    try {
      const response = await fetch('http://localhost:8000/action_recognition/stop_camera/', {
        method: 'POST'
      })
      const data = await response.json()
      console.log('摄像头已关闭:', data)
    } catch (error) {
      console.error('关闭摄像头时出错:', error)
    }
  }
}

const buttonClass = computed(() => ({
  active: isActive.value,
  inactive: !isActive.value
}))
</script>

<style scoped>
.camera-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

button {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 200px; /* 方形按钮的宽度 */
  height: 200px; /* 方形按钮的高度 */
  padding: 10px;
  background-color: #ffffff;
  border-color: rgb(116, 115, 115);
  border-width: 2px;
  border-style: solid;
  border-radius: 8px; /* 圆角 */
  cursor: pointer;
  transition: background-color 0.5s, border-color 0.3s;
}

button.active {
  background-color: #d2d2d2;
}

button.inactive {
  background-color: #ffffff;
}

button:hover {
  background-color: #d2d2d2;
  transition: background-color 0.5s, border-color 0.3s;
}


.button-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.button-text {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 8px;
}

.button-logo {
  width: 40px; /* 设置logo大小 */
  height: 40px;
}
</style>
