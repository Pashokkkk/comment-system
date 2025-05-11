import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import VueEasyLightbox from 'vue-easy-lightbox'

const app = createApp(App)
app.component('VueEasyLightbox', VueEasyLightbox)
console.log("🔥 main.js is working");
app.mount('#app')