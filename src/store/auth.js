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

  // 1. ДОБАВЛЕН REF ДЛЯ ХРАНЕНИЯ СООБЩЕНИЯ
  const logoutMessage = ref(null)

  const isAuthenticated = computed(() => !!accessToken.value)
  const isAdmin = computed(() => userRole.value === 'admin')

  // Функция для создания экземпляра API
  const createApiClient = () => {
    const instance = axios.create({
      baseURL: 'https://pashok00191.pythonanywhere.com/api/',
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
            const response = await axios.post('https://pashok00191.pythonanywhere.com/api/auth/refresh/', {
              refresh: refreshToken.value
            })
            
            accessToken.value = response.data.access
            localStorage.setItem('access_token', accessToken.value)
            originalRequest.headers.Authorization = `Bearer ${accessToken.value}`
            
            return instance(originalRequest)
          } catch (refreshError) {
            // 2. ИЗМЕНЕНИЕ: ПЕРЕДАЕМ СООБЩЕНИЕ В LOGOUT
            await logout('Простите, сессия истекла или сервер был перезапущен. Пожалуйста, войдите снова.')
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
    const response = await axios.post('https://pashok00191.pythonanywhere.com/api/auth/login/', userData)
    
    accessToken.value = response.data.access
    refreshToken.value = response.data.refresh
    userRole.value = response.data.role
    
    localStorage.setItem('access_token', accessToken.value)
    localStorage.setItem('refresh_token', refreshToken.value)
    localStorage.setItem('user_role', userRole.value)
    
    const api = getApiClient()
    const userResponse = await api.get('auth/user/')
    
    currentUser.value = userResponse.data
    localStorage.setItem('user_data', JSON.stringify(userResponse.data))
    
    router.push('/about')
  }

  async function register(userData) {
    const response = await axios.post('https://pashok00191.pythonanywhere.com/api/auth/register/', userData)
    
    accessToken.value = response.data.access
    refreshToken.value = response.data.refresh
    userRole.value = response.data.role
    
    localStorage.setItem('access_token', accessToken.value)
    localStorage.setItem('refresh_token', refreshToken.value)
    localStorage.setItem('user_role', userRole.value)
    
    const api = getApiClient()
    const userResponse = await api.get('auth/user/')
    
    currentUser.value = userResponse.data
    localStorage.setItem('user_data', JSON.stringify(userResponse.data))
    
    router.push('/')
  }

  // 3. ОБНОВЛЕННАЯ ФУНКЦИЯ LOGOUT
  async function logout(message = null) {
    if (message) {
      logoutMessage.value = message
    }

    try {
      const api = axios.create({ baseURL: 'https://pashok00191.pythonanywhere.com/api/' })
      await api.post('auth/logout/', {
        refresh_token: refreshToken.value
      })
    } catch (error) {
      console.error('Ошибка при выходе (возможно, токен уже недействителен):', error)
    } finally {
      accessToken.value = null
      refreshToken.value = null
      userRole.value = null
      currentUser.value = null
      
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('user_role')
      localStorage.removeItem('user_data')
      
      if (router.currentRoute.value.path !== '/login') {
        router.push('/login')
      }
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

  // 4. ДОБАВЛЕНА ФУНКЦИЯ ОЧИСТКИ СООБЩЕНИЯ
  function clearLogoutMessage() {
    logoutMessage.value = null
  }

  // 5. ДОБАВЛЕНЫ НОВЫЕ ЭЛЕМЕНТЫ В RETURN
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
    getApiClient,
    logoutMessage,
    clearLogoutMessage,
  }
})