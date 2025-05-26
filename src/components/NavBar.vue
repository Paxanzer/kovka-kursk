<template>
    <nav>
        <router-link v-if="!authStore.isAuthenticated" to="/register">Регистрация</router-link>
        <router-link v-if="!authStore.isAuthenticated" to="/login">Войти</router-link>
        <router-link v-if="authStore.isAuthenticated" to="/profile">Профиль</router-link>
        <router-link 
      v-if="authStore.isAuthenticated && authStore.isAdmin" 
      to="/admin-panel"
    >
      Админ-панель
    </router-link>
      
    </nav>
  </template>
  
  <script setup>
  import { useAuthStore } from '@/store/auth.js'
  
  const authStore = useAuthStore()
  </script>
  
  <style scoped>
  nav {
    padding: 1rem;
    background: #f0f0f0;
    display: flex;
    gap: 1rem;
  }
  
  nav a, nav button {
    padding: 0.5rem 1rem;
    text-decoration: none;
    color: #333;
    background: #fff;
    border: 1px solid #ddd;
    border-radius: 4px;
    cursor: pointer;
  }
  
  nav a:hover, nav button:hover {
    background: #e0e0e0;
  }
  </style>