import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

import { VitePWA } from 'vite-plugin-pwa'

export default defineConfig({
  plugins: [
    vue(),
    VitePWA({
      devOptions: {
        enabled: true
      },
      includeAssets: ['./src/assets/icon.ico', './src/assets/apple-touch-icon.png', './src/assets/192.png', './src/assets/512.png', './src/assets/mobile.jpg'],
      manifest: {
        name: 't0d0d0d0',
        short_name: 't0d0d0d0',
        description: 'minimalistic t0d0 manager',
        theme_color: '#121212',
        icons: [
          {
            src: '192.png',
            sizes: '192x192',
            type: 'image/png'
          },
          {
            src: '512.png',
            sizes: '512x512',
            type: 'image/png'
          }
        ],screenshots: [ 
        { 
          src: "mobile.jpg", 
          type: "image/jpeg", 
          sizes: "573x1280", 
          form_factor: "narrow" 
        }, 
        { 
          src: "desktop.jpg", 
          type: "image/jpeg", 
          sizes: "1440x720", 
          form_factor: "wide" 
        } 
      ],prefer_related_applications: false
      },
    })
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8001',
      }
}}})
