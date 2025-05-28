<template>
  <div class="detail-container fade-in">
    <!-- Хлебные крошки -->
    <nav class="breadcrumbs">
      <router-link to="/catalog" class="breadcrumb-link">Все категории</router-link>
      <span class="breadcrumb-separator">/</span>
      <router-link 
        :to="`/catalog/${product.category?.id || product.category}`" 
        class="breadcrumb-link"
      >
        {{ product.category?.name || `Категория ${product.category}` }}
      </router-link>
      <span class="breadcrumb-separator">/</span>
      <span class="breadcrumb-current">{{ product.name }}</span>
    </nav>

    <!-- Лоадер -->
    <div v-if="isLoading" class="loading-overlay">
      <div class="spinner"></div>
      <span>Загрузка товара...</span>
    </div>

   <!-- Основное содержимое -->
    <div v-if="!isLoading && product" class="product-detail">
      <div class="product-gallery">
        <div class="image-container" @click="openModal(mainImage || product.image)">
          <!-- Размытый фон -->
          <img 
            :src="getImageUrl(mainImage || product.image)" 
            :alt="product.name + ' background'"
            class="image-background"
            @error="handleImageError"
          >
          <!-- Основное изображение -->
          <img 
            :src="getImageUrl(mainImage || product.image)" 
            :alt="product.name" 
            class="main-image"
            @error="handleImageError"
          >
        </div>
        
        <div v-if="product.images && product.images.length > 1" class="thumbnail-container">
          <img
            v-for="(img, index) in product.images"
            :key="index"
            :src="getImageUrl(img)"
            @click="mainImage = img"
            class="thumbnail"
            :class="{ 'active-thumbnail': mainImage === img }"
          >
        </div>
      </div>

      <div class="product-info">
        <h1 class="product-title">{{ product.name }}</h1>
        <p class="product-price">{{ product.price }} ₽</p>
        <p class="product-article">Артикул: {{ product.article }}</p>

        <div v-if="product.description" class="product-description">
          <h3>Описание:</h3>
          <p>{{ product.description }}</p>
        </div>

        <div v-if="product.specifications" class="product-specs">
          <h3>Характеристики:</h3>
          <p>{{ product.specifications }}</p>
        </div>

        <button 
          class="add-to-cart" 
          :class="{ 'in-cart': isInCart }"
          @click="toggleCart"
        >
          <span>{{ isInCart ? 'В корзине' : 'Добавить в корзину' }}</span>
        </button>
      </div>
    </div>

    
    <div v-if="error" class="error-message">
      {{ error }}
      <button @click="fetchProduct" class="retry-button">Повторить попытку</button>
    </div>

    <div v-if="showImageModal" class="image-modal-overlay" @click.self="closeModal">
      <div class="image-modal-content">
        <button class="close-modal-btn" @click="closeModal">×</button>
        <img 
          :src="getImageUrl(modalImageUrl)" 
          :alt="'Увеличенное изображение ' + product.name"
          class="modal-image"
          @error="handleModalImageError"
        >
      </div>
    </div>
  </div>
  
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useStore } from 'vuex'
import { useAuthStore } from '@/store/auth'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const store = useStore()
const authStore = useAuthStore()
const product = ref({})
const isLoading = ref(true)
const error = ref(null)
const mainImage = ref(null)
const baseUrl = 'http://localhost:8000'

// Добавляем состояния для модального окна
const showImageModal = ref(false)
const modalImageUrl = ref('')

// Проверяем, находится ли товар в корзине
const isInCart = computed(() => {
  return store.state.cart.items.some(item => item.id === product.value.id)
})

const productId = computed(() => parseInt(route.params.productId))

const fetchProduct = async () => {
  try {
    isLoading.value = true
    const response = await axios.get(`${baseUrl}/api/products/${productId.value}/`)
    product.value = response.data
    mainImage.value = product.value.image
  } catch (err) {
    error.value = 'Ошибка загрузки товара'
    console.error('Fetch error:', err)
  } finally {
    isLoading.value = false
  }
}

const getImageUrl = (imagePath) => {
  if (!imagePath) return require('@/assets/img/no-image.webp')
  if (imagePath.startsWith('http')) return imagePath
  return `${baseUrl}${imagePath}`
}

const handleImageError = (e) => {
  e.target.src = require('@/assets/img/no-image.webp')
}

// Функции для работы с модальным окном
const openModal = (imgUrl) => {
  modalImageUrl.value = imgUrl
  showImageModal.value = true
  document.body.style.overflow = 'hidden' // Блокируем скролл страницы
}

const closeModal = () => {
  showImageModal.value = false
  document.body.style.overflow = '' // Восстанавливаем скролл
}

const handleModalImageError = (e) => {
  e.target.src = require('@/assets/img/no-image.webp')
}

// Функция для добавления/удаления товара из корзины
const toggleCart = () => {
  if (!authStore.isAuthenticated) {
    // Если пользователь не авторизован, перенаправляем на страницу регистрации
    router.push('/register')
    return
  }

  if (isInCart.value) {
    store.commit('cart/removeItem', product.value.id)
  } else {
    store.commit('cart/addItem', {
      id: product.value.id,
      name: product.value.name,
      price: product.value.price,
      image: product.value.image
    })
  }
}

onMounted(() => {
  fetchProduct()
})
</script>

<style scoped>

/* Стили для модального окна */
.image-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.9);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  animation: fadeIn 0.3s ease-out;
}

.image-modal-content {
  position: relative;
  max-width: 90vw;
  max-height: 90vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-image {
  height: 90vh; /* Занимает 90% высоты экрана */
  width: auto; /* Ширина по пропорциям */
  object-fit: contain; /* Для модального окна используем contain */
  object-position: center;
  max-width: 90vw; /* Ограничение по ширине */
}

.close-modal-btn {
  position: absolute;
  top: 20px;
  right: 20px;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: none;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  font-size: 24px;
  cursor: pointer;
  transition: all 0.3s ease;
  z-index: 1001;
}

.close-modal-btn:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: scale(1.1);
}

/* Адаптация для разных экранов */
@media (max-width: 768px) {
  .image-container {
    height: 400px;
  }
  
  .modal-image {
    height: 70vh;
  }
}

@media (max-width: 480px) {
  .image-container {
    height: 300px;
  }
  
  .modal-image {
    height: 60vh;
  }
}

.fade-in {
  opacity: 0;
  transform: translateY(10px);
  animation: fadeIn 0.3s ease-out forwards;
}

.detail-container {
  display: flex;
  flex-direction: column;
  min-height: calc(100vh - 160px);
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

/* Хлебные крошки */
.breadcrumbs {
  margin-bottom: 20px;
  font-size: 16px;
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
  font-family: 'Manrope', sans-serif;
}

.breadcrumb-link {
  color: #dededecb;
  text-decoration: none;
  transition: color 0.3s;
}

.breadcrumb-link:hover {
  color: #ffffff;
  text-decoration: underline;
}

.breadcrumb-separator {
  color: #737373;
}

.breadcrumb-current {
  color: #ffffff;
  font-weight: 500;
}

/* Лоадер */
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background: rgba(0, 0, 0, 0.185);
  z-index: 1000;
  color: #dededecb;
  gap: 15px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: #8d8d8d;
  animation: spin 1s ease-in-out infinite;
}

/* Основное содержимое товара */
.product-detail {
  display: flex;
  gap: 40px;
  margin-top: 20px;
  flex: 1;
}

.product-gallery {
  flex: 1;
  max-width: 600px;
}

.image-container {
  position: relative;
  width: 100%;
  height: 600px; /* Фиксированная высота */
  border-radius: 16px;
  overflow: hidden;
  background: rgba(0, 0, 0, 0.23);
  border: 1px solid #737373;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: zoom-in;
}
.image-container:hover {
  transform: scale(1.01);
  box-shadow: 0 0 20px rgba(222, 222, 222, 0.1);
}

.image-background {
  position: absolute;
  width: 100%;
  height: 100%;
  object-fit: cover;
  filter: blur(16px) brightness(0.6);
  opacity: 0.8;
  transform: scale(1.1);
  z-index: 1;
}

.main-image {
  height: 80%; /* Занимает всю высоту контейнера */
  width: auto; /* Ширина автоматически по пропорциям */
  object-fit: cover; /* Заполнение с сохранением пропорций */
  object-position: center; /* Центрируем изображение */
  z-index: 2;
}

.thumbnail-container {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  margin-top: 15px;
}

.thumbnail {
  width: 80px;
  height: 80px;
  object-fit: cover;
  border: 1px solid #737373;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  background: rgba(0, 0, 0, 0.23);
}

.thumbnail:hover {
  border-color: #8d8d8d;
  transform: scale(1.05);
}

.active-thumbnail {
  border: 2px solid #8d8d8d;
}

.product-info {
  flex: 1;
  padding: 20px;
  background: rgba(0, 0, 0, 0.23);
  border: 1px solid #737373;
  border-radius: 16px;
}

.product-title {
  font-size: 28px;
  margin: 0 0 15px;
  color: #ffffff;
  font-family: 'Manrope', sans-serif;
  font-weight: 400;
}

.product-price {
  font-size: 24px;
  font-weight: bold;
  color: #dededecb;
  margin: 0 0 15px;
  font-family: 'Manrope', sans-serif;
}

.product-article {
  color: #8d8d8d;
  margin: 0 0 20px;
  font-family: 'Manrope', sans-serif;
}

.product-description, .product-specs {
  margin: 25px 0;
  padding: 20px 0;
  border-top: 1px solid rgba(115, 115, 115, 0.3);
  border-bottom: 1px solid rgba(115, 115, 115, 0.3);
  color: #dededecb;
  font-family: 'Manrope', sans-serif;
}

.product-description h3, .product-specs h3 {
  color: #ffffff;
  margin-bottom: 15px;
  font-family: 'Manrope', sans-serif;
  font-weight: 500;
}

.add-to-cart {
  width: 100%;
  padding: 15px;
  background: #474747;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.add-to-cart:hover {
  background: #5a5a5a;
  transform: translateY(-1px);
}

.add-to-cart.in-cart {
  background: #2c5282;
}

.add-to-cart.in-cart:hover {
  background: #2b4c7e;
}

/* Сообщения об ошибках */
.error-message {
  background: rgba(255, 77, 79, 0.2);
  padding: 20px;
  border-radius: 16px;
  margin: 20px 0;
  color: #ff5252;
  text-align: center;
  border: 1px solid rgba(255, 77, 79, 0.5);
  font-family: 'Manrope', sans-serif;
}

.retry-button {
  background-color: rgba(255, 77, 79, 0.3);
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s ease;
  margin-top: 15px;
  font-family: 'Manrope', sans-serif;
}

.retry-button:hover {
  background-color: rgba(255, 77, 79, 0.5);
}

/* Анимации */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Адаптация для мобильных */
@media (max-width: 768px) {
  .product-detail {
    flex-direction: column;
    gap: 20px;
  }
  
  .product-gallery {
    max-width: 100%;
  }

  .product-info {
    padding: 15px;
  }

  .product-title {
    font-size: 24px;
  margin-bottom: 10px;
  }

  .product-price {
    font-size: 20px;
  }
}

@media (max-width: 480px) {
  .detail-container {
    padding: 15px;
  }

  .breadcrumbs {
    font-size: 14px;
  }

  .thumbnail {
    width: 60px;
    height: 60px;
  border-radius: 6px;
  }

  .product-title {
    font-size: 20px;
  }
}
</style>