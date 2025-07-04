import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import { createPinia } from 'pinia'
import axios from 'axios'


axios.defaults.baseURL = 'https://pashok00191.pythonanywhere.com'
axios.interceptors.request.use(config => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config
})


const app = createApp(App)

app.use(createPinia())
app.use(store)
app.use(router)

app.mount('#app')

