// Import global CSS
import './assets/main.css'

// Import Vue core and root component
import { createApp } from 'vue'
import App from './App.vue'

// Import lightbox plugins
import VueEasyLightbox from 'vue-easy-lightbox'
import 'lightbox2/dist/css/lightbox.min.css'
import 'lightbox2/dist/js/lightbox.min.js'

// Import jQuery
import $ from 'jquery'

// Create Vue app
const app = createApp(App)

// Register lightbox component
app.component('VueEasyLightbox', VueEasyLightbox)

// Mount the app to DOM
console.log("🔥 main.js is working")
app.mount('#app')

// Make jQuery globally accessible (for lightbox2)
window.$ = $
window.jQuery = $
