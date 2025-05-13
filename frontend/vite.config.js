import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

export default defineConfig(({ command }) => ({
  // Enable Vue and Vue DevTools plugins
  plugins: [
    vue(),
    vueDevTools(),
  ],

  // Set base path for static files
  base: '/static/',

  // Build output config for Django backend
  build: {
    outDir: '../backend/static',
    emptyOutDir: true,
    manifest: true
  },

  // Path aliases for cleaner imports
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
      jquery: 'jquery/dist/jquery.js', 
    },
  },

  // Proxy media requests to Django backend
  server: {
    proxy: {
      '/media': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      }
    }
  },

  // Define globals for legacy libraries
  define: {
    global: {},
  },

  // Pre-bundle specific dependencies
  optimizeDeps: {
    include: ['jquery'],
  },
}))
