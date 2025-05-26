<template>
    <button 
      v-if="isAuthenticated"
      @click="logout" 
      class="logout-button"
    >
      Выйти
    </button>
  </template>
  
  <script setup>
  import { computed } from 'vue'
  import { useRouter } from 'vue-router'
  
  const router = useRouter()
  
  // Проверка авторизации
  const isAuthenticated = computed(() => {
    return !!localStorage.getItem('access_token')
  })
  
  const logout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user_role')
    router.push('/login')
  }
  </script>
  
  <style scoped>
  .logout-button {
    padding: 8px 16px;
    background-color: #f44336;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  .logout-button:hover {
    background-color: #d32f2f;
  }
  </style>