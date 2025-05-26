<template>
    <div class="container">
      <h1>Данные из API</h1>
      
      <!-- Общий лоадер -->
      <div v-if="isLoading" class="loader-overlay">
        <div class="loader"></div>
        <p>Загрузка данных...</p>
      </div>
  
      <!-- Общее сообщение об ошибке -->
      <div v-if="error" class="error-message">
        <p>⚠️ {{ error }}</p>
        <button @click="fetchData">Повторить попытку</button>
      </div>
  
      <div class="cards-container" v-else>
        <!-- Карточка пользователя -->
        <div class="card">
          <h2>Пользователь</h2>
          <template v-if="userLoading">
            <div class="card-loader"></div>
          </template>
          <template v-else-if="userError">
            <div class="card-error">
              <p>Ошибка загрузки пользователя</p>
              <button @click="fetchUser">Повторить</button>
            </div>
          </template>
          <template v-else>
            <img 
              :src="userImageUrl" 
              alt="Аватар пользователя"
              class="card-image"
              @error="handleImageError"
            >
            <div class="card-content">
              <p><strong>Имя:</strong> {{ user.username }}</p>
              <p><strong>Email:</strong> {{ user.email || 'не указан'}}</p>
              <p><strong>Телефон:</strong> {{ user.phone || 'не указан' }}</p>
              <p><strong>Роль:</strong> {{ user.role }}</p>
            </div>
          </template>
        </div>
  
        <!-- Карточка категории -->
        <div class="card">
          <h2>Категория</h2>
          <template v-if="categoryLoading">
            <div class="card-loader"></div>
          </template>
          <template v-else-if="categoryError">
            <div class="card-error">
              <p>Ошибка загрузки категории</p>
              <button @click="fetchCategory">Повторить</button>
            </div>
          </template>
          <template v-else>
            <img 
              :src="categoryImageUrl" 
              :alt="category.name"
              class="card-image"
              @error="handleImageError"
            >
            <div class="card-content">
              <p><strong>Название:</strong> {{ category.name }}</p>
              <p><strong>ID:</strong> {{ category.id }}</p>
            </div>
          </template>
        </div>
  
        <!-- Карточка продукта -->
        <div class="card">
          <h2>Продукт</h2>
          <template v-if="productLoading">
            <div class="card-loader"></div>
          </template>
          <template v-else-if="productError">
            <div class="card-error">
              <p>Ошибка загрузки продукта</p>
              <button @click="fetchProduct">Повторить</button>
            </div>
          </template>
          <template v-else>
            <img 
              :src="productImageUrl" 
              :alt="product.name"
              class="card-image"
              @error="handleImageError"
            >
            <div class="card-content">
              <p><strong>Название:</strong> {{ product.name }}</p>
              <p><strong>Артикул:</strong> {{ product.article }}</p>
              <p><strong>Цена:</strong> {{ product.price }} ₽</p>
              <p><strong>Категория:</strong> {{ product.category?.name }}</p>
            </div>
          </template>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import axios from 'axios'
  
  const baseUrl = 'http://localhost:8000' // Замените на ваш API URL
  
  // Данные
  const user = ref(null)
  const category = ref(null)
  const product = ref(null)
  
  // URL изображений
  const userImageUrl = ref('https://via.placeholder.com/150?text=User')
  const categoryImageUrl = ref('https://via.placeholder.com/150?text=Category')
  const productImageUrl = ref('https://via.placeholder.com/150?text=Product')
  
  // Состояния загрузки
  const isLoading = ref(true)
  const userLoading = ref(true)
  const categoryLoading = ref(true)
  const productLoading = ref(true)
  
  // Ошибки
  const error = ref(null)
  const userError = ref(null)
  const categoryError = ref(null)
  const productError = ref(null)
  
  // Обработка ошибок изображений
  const handleImageError = (event) => {
    event.target.src = 'https://via.placeholder.com/150?text=Image+Not+Found'
  }
  
  // Загрузка пользователя
  const fetchUser = async () => {
    userLoading.value = true
    userError.value = null
    try {
      const response = await axios.get(`${baseUrl}/api/users/1/`)
      user.value = response.data
      if (user.value.image) {
        userImageUrl.value = `${baseUrl}${user.value.image}`
      }
    } catch (err) {
      userError.value = 'Не удалось загрузить данные пользователя'
      console.error('Ошибка загрузки пользователя:', err)
    } finally {
      userLoading.value = false
    }
  }
  
  // Загрузка категории
  const fetchCategory = async () => {
    categoryLoading.value = true
    categoryError.value = null
    try {
      const response = await axios.get(`${baseUrl}/api/categories/1/`)
      category.value = response.data
      if (category.value.image) {
        categoryImageUrl.value = `${baseUrl}${category.value.image}`
      }
    } catch (err) {
      categoryError.value = 'Не удалось загрузить данные категории'
      console.error('Ошибка загрузки категории:', err)
    } finally {
      categoryLoading.value = false
    }
  }
  
  // Загрузка продукта
  const fetchProduct = async () => {
    productLoading.value = true
    productError.value = null
    try {
      const response = await axios.get(`${baseUrl}/api/products/1/`)
      product.value = response.data
      if (product.value.image) {
        productImageUrl.value = `${baseUrl}${product.value.image}`
      }
    } catch (err) {
      productError.value = 'Не удалось загрузить данные продукта'
      console.error('Ошибка загрузки продукта:', err)
    } finally {
      productLoading.value = false
    }
  }
  
  // Основная загрузка данных
  const fetchData = async () => {
    isLoading.value = true
    error.value = null
    try {
      await Promise.all([
        fetchUser(),
        fetchCategory(),
        fetchProduct()
      ])
    } catch (err) {
      error.value = 'Произошла ошибка при загрузке данных. Пожалуйста, попробуйте позже.'
      console.error('Ошибка загрузки данных:', err)
    } finally {
      isLoading.value = false
    }
  }
  
  // Загружаем данные при монтировании
  onMounted(fetchData)
  </script>
  
  <style scoped>
  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
    position: relative;
  }
  
  .loader-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.219);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    z-index: 1000;
  }
  
  .loader {
    border: 5px solid #f3f3f3;
    border-top: 5px solid #3498db;
    border-radius: 50%;
    width: 50px;
    height: 50px;
    animation: spin 1s linear infinite;
    margin-bottom: 15px;
  }
  
  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
  
  .error-message {
    background: #ffebee;
    padding: 20px;
    border-radius: 8px;
    text-align: center;
    margin: 20px 0;
  }
  
  .error-message button {
    background: #ff5252;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    cursor: pointer;
    margin-top: 10px;
  }
  
  .cards-container {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    justify-content: center;
  }
  
  .card {
    width: 300px;
    border: 1px solid #ddd;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease;
    min-height: 400px;
    display: flex;
    flex-direction: column;
  }
  
  .card:hover {
    transform: translateY(-5px);
  }
  
  .card-image {
    width: 100%;
    height: 200px;
    object-fit: cover;
  }
  
  .card-content {
    padding: 15px;
    flex-grow: 1;
  }
  
  .card-content p {
    margin: 8px 0;
  }
  
  .card-loader {
    height: 200px;
    background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
    background-size: 200% 100%;
    animation: shimmer 1.5s infinite;
    flex-grow: 1;
  }
  
  .card-error {
    padding: 20px;
    text-align: center;
    color: #ff5252;
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }
  
  .card-error button {
    background: #ff5252;
    color: white;
    border: none;
    padding: 5px 10px;
    border-radius: 4px;
    cursor: pointer;
    margin-top: 10px;
    align-self: center;
  }
  
  @keyframes shimmer {
    0% { background-position: 200% 0; }
    100% { background-position: -200% 0; }
  }
  </style>