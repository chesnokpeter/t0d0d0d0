import './assets/base.css'

import { createApp } from 'vue'
import App from './App.vue'
import { createAirDatepicker } from 'vue-air-datepicker'
import router from './router'

const app = createApp(App)
const vad = createAirDatepicker({css:false})

app.use(router)
app.use(vad)
app.mount('#app')
