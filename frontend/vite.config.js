import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  build: {
    outDir: '../backend/static',  // 这会将构建后的文件输出到 Django 的 static 目录
    emptyOutDir: true,            // 每次构建前删除旧的静态文件
  }
})
