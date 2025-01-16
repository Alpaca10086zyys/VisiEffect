<template>
    <div class="upload-container">
      <!-- 上传按钮 -->
      <button @click="openFilePicker">
        <div class="button-content">
          <span class="button-text">上传视频</span>
          <img class="button-logo" src="../assets/edit.svg" alt="Upload Logo" />
        </div>
      </button>
      <!-- 隐藏的文件输入框 -->
      <input ref="fileInput" type="file" accept="video/mp4" style="display: none;" @change="handleFileUpload" />
    
      <!-- 显示上传进度条 -->
      <div v-if="uploadProgress > 0" class="progress-container">
        <div class="progress-bar" :style="{ width: `${uploadProgress}%` }"></div>
        <p>{{ uploadProgress }}%</p>
      </div>
    
      <!-- 弹窗显示下载按钮，右下角弹窗 -->
      <div v-if="showDownload" class="download-modal">
      <p style="padding-left: 5px;"><b>处理完成！</b></p>
      <!-- 圆形按钮，中央显示图标 -->
      <button @click="downloadProcessedVideo">
        <img src="../assets/download.svg" alt="Download Icon" class="download-icon" />
      </button>
    </div>
    </div>
</template>
    
<script setup>
    import { ref } from 'vue'
    
    const fileInput = ref(null) // 引用隐藏的文件输入框
    const uploadProgress = ref(0) // 上传进度
    const showDownload = ref(false) // 控制下载弹窗的显示
    const processedVideoUrl = ref('') // 存储后端返回的处理后视频URL
    
    // 打开文件选择器
    const openFilePicker = () => {
      fileInput.value.click() // 触发文件选择
    }
    
    // 处理文件上传
    const handleFileUpload = async (event) => {
      const file = event.target.files[0]
      if (file && file.type === 'video/mp4') {
        await uploadVideo(file)
      } else {
        alert('仅支持上传MP4文件！')
      }
    }
    
    // 上传视频并获取处理进度
    const uploadVideo = async (file) => {
      const formData = new FormData()
      formData.append('video', file)
    
      try {
        const response = await fetch('http://localhost:8000/edit_video/upload/', {
          method: 'POST',
          body: formData,
        })
    
        if (!response.ok) {
          throw new Error('上传失败！')
        }
    
        // 获取处理后的视频URL
        // const { videoUrl } = await response.json()
        // processedVideoUrl.value = videoUrl // 存储视频URL
        // showDownload.value = true // 显示下载弹窗


        const contentDisposition = response.headers.get('content-disposition');
        let filename = 'downloaded-video.mp4'; // 默认文件名
        if (contentDisposition) {
          const filenameMatch = contentDisposition.match(/filename="?(.+?)"?;/);
          if (filenameMatch.length > 1) {
            filename = filenameMatch[1];
          }
        }

        // 将响应体转换为Blob
        const blob = await response.blob();

        // 创建一个链接元素用于下载
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();

        // 清理和释放URL对象
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);


      } catch (error) {
        console.error('上传出错:', error)
        alert('上传失败，请重试！')
      }
    }
    
    // 下载处理后的视频
    const downloadProcessedVideo = () => {
      const a = document.createElement('a')
      a.href = processedVideoUrl.value
      a.download = 'processed_video.mp4'
      a.click()
    }
</script>
    
<style scoped>
  .upload-container {
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
    width: 200px;
    height: 200px;
    padding: 10px;
    background-color: #ffffff;
    border-color: rgb(116, 115, 115);
    border-width: 2px;
    border-style: solid;
    border-radius: 8px;
    cursor: pointer;
    transition: background-color 0.5s, border-color 0.3s;
  }
  
  button:hover {
    background-color: #d2d2d2;
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
    width: 40px;
    height: 40px;
  }
  
  /* 右下角弹窗样式 */
  /* 右下角弹窗样式 */
.download-modal {
  position: fixed;
  display: flex;
  bottom: 20px;
  right: 20px;
  width: 200px;
  height: 60px;
  padding-left: 15px;
  padding-top: 10px;
  border-radius: 40px;
  background-color: #03030314;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
  z-index: 9999;
}

.download-modal button {
  margin-left: 50px;
  width: 50px;
  height: 50px;
  border-radius: 50%; /* 使按钮变圆形 */
  background-color: #4CAF50;
  color: white;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.download-modal button:hover {
  background-color: #45a049;
}

.download-icon {
  width: 30px;
  height: 30px; /* 控制图标的大小 */
}
  </style>
  