import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

export const useAuthStore = defineStore('auth', () => {
  const router = useRouter()
  const accessToken = ref(localStorage.getItem('access_token'))
  const refreshToken = ref(localStorage.getItem('refresh_token'))
  const userRole = ref(localStorage.getItem('user_role'))
  const currentUser = ref(JSON.parse(localStorage.getItem('user_data') || 'null'))

  const isAuthenticated = computed(() => !!accessToken.value)
  const isAdmin = computed(() => userRole.value === 'admin')

  // Функция для создания экземпляра API
  const createApiClient = () => {
    const instance = axios.create({
      baseURL: 'http://localhost:8000/api/',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken.value}`
      }
    })

    // Интерцептор для обработки 401 ошибки и refresh токена
    instance.interceptors.response.use(
      response => response,
      async error => {
        const originalRequest = error.config
        
        if (error.response?.status === 401 && !originalRequest._retry) {
          originalRequest._retry = true
          
          try {
            const response = await axios.post('http://localhost:8000/api/auth/refresh/', {
              refresh: refreshToken.value
            })
            
            accessToken.value = response.data.access
            localStorage.setItem('access_token', accessToken.value)
            originalRequest.headers.Authorization = `Bearer ${accessToken.value}`
            
            return instance(originalRequest)
          } catch (refreshError) {
            await logout()
            return Promise.reject(refreshError)
          }
        }
        
        return Promise.reject(error)
      }
    )
    
    return instance
  }

  // Метод для получения API клиента
  const getApiClient = () => {
    if (!accessToken.value) {
      throw new Error('Not authenticated')
    }
    return createApiClient()
  }

  async function login(userData) {
    const response = await axios.post('http://localhost:8000/api/auth/login/', userData)
    
    accessToken.value = response.data.access
    refreshToken.value = response.data.refresh
    userRole.value = response.data.role
    
    localStorage.setItem('access_token', accessToken.value)
    localStorage.setItem('refresh_token', refreshToken.value)
    localStorage.setItem('user_role', userRole.value)
    
    // Получаем данные пользователя
    const api = getApiClient()
    const userResponse = await api.get('auth/user/')
    
    currentUser.value = userResponse.data
    localStorage.setItem('user_data', JSON.stringify(userResponse.data))
    
    router.push('/about')
  }

  async function register(userData) {
    const response = await axios.post('http://localhost:8000/api/auth/register/', userData)
    
    accessToken.value = response.data.access
    refreshToken.value = response.data.refresh
    userRole.value = response.data.role
    
    localStorage.setItem('access_token', accessToken.value)
    localStorage.setItem('refresh_token', refreshToken.value)
    localStorage.setItem('user_role', userRole.value)
    
    // Получаем данные пользователя 1
    const api = getApiClient()
    const userResponse = await api.get('auth/user/')
    
    currentUser.value = userResponse.data
    localStorage.setItem('user_data', JSON.stringify(userResponse.data))
    
    router.push('/')
  }

  async function logout() {
    try {
      const api = getApiClient()
      await api.post('auth/logout/', {
        refresh_token: refreshToken.value
      })
    } catch (error) {
      console.error('Ошибка при выходе:', error)
    } finally {
      accessToken.value = null
      refreshToken.value = null
      userRole.value = null
      currentUser.value = null
      
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('user_role')
      localStorage.removeItem('user_data')
      
      router.push('/login')
    }
  }

  async function fetchUserData() {
    if (!isAuthenticated.value) return
    
    try {
      const api = getApiClient()
      const response = await api.get('auth/user/')
      currentUser.value = response.data
      localStorage.setItem('user_data', JSON.stringify(response.data))
    } catch (error) {
      console.error('Ошибка загрузки данных пользователя:', error)
    }
  }

  return { 
    accessToken,
    refreshToken,
    userRole,
    currentUser,
    isAuthenticated,
    isAdmin,
    login,
    register,
    logout,
    fetchUserData,
    getApiClient // Экспортируем метод для получения API клиента
  }
})