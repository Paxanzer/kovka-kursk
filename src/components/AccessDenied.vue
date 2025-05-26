<template>
    <div class="register-form">
      <h2>Регистрация</h2>
      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label>Логин</label>
          <input v-model="form.username" type="text" required>
        </div>
        <div class="form-group">
          <label>Пароль</label>
          <input v-model="form.password" type="password" required>
        </div>
        <div class="form-group">
          <label>Email</label>
          <input v-model="form.email" type="email">
        </div>
        <div class="form-group">
          <label>Телефон</label>
          <input v-model="form.phone" type="tel">
        </div>
        <button type="submit" :disabled="loading">
          {{ loading ? 'Загрузка...' : 'Зарегистрироваться' }}
        </button>
        <p v-if="error" class="error">{{ error }}</p>
      </form>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import axios from 'axios'
  import { useRouter } from 'vue-router'
  
  const router = useRouter()
  const form = ref({
    username: '',
    password: '',
    email: '',
    phone: ''
  })
  const loading = ref(false)
  const error = ref(null)
  
  const handleRegister = async () => {
    try {
      loading.value = true
      error.value = null
      const response = await axios.post('http://localhost:8000/api/auth/register/', form.value)
      
      // Сохраняем токен и перенаправляем
      localStorage.setItem('access_token', response.data.access)
      localStorage.setItem('refresh_token', response.data.refresh)
      router.push('/')
    } catch (err) {
      error.value = err.response?.data || 'Ошибка регистрации'
    } finally {
      loading.value = false
    }
  }
  </script>
  
  <style scoped>
  .register-form {
    max-width: 400px;
    margin: 0 auto;
    padding: 20px;
  }
  .form-group {
    margin-bottom: 15px;
  }
  .error {
    color: red;
  }
  </style>