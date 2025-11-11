import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// Import Bootstrap CSS and JS
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'

// Optional: Import Mapbox CSS (uncomment when ready to use Mapbox)
// import 'mapbox-gl/dist/mapbox-gl.css'

const app = createApp(App)

app.use(router)

app.mount('#app')