import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueJsx from '@vitejs/plugin-vue-jsx'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueJsx(),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  server: {
    host: true, // чтобы можно было открыть сайт на телефоне в локальной сети, ну и для трёх букв
    watch: {
      // listings.json перезаписывается парсером; свежие данные приложение
      // подтягивает через fetch, поэтому HMR-перезагрузка страницы не нужна
      ignored: ['**/src/data/listings.json'],
    },
  },
})
