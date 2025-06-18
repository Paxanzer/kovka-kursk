import axios from 'axios'

const api = axios.create({
  baseURL: 'https://pashok00191.pythonanywhere.com', // Ваш Django API URL
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
})


export default api