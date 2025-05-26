<template>
    <div class="product-detail-container">
      <!-- Breadcrumbs -->
      <nav class="breadcrumbs">
        <router-link to="/about" class="breadcrumb-link">Все категории</router-link>
        <span class="breadcrumb-separator">/</span>
        <router-link 
          :to="`/about/${product.category?.id || product.category}`" 
          class="breadcrumb-link"
        >
          {{ product.category?.name || `Категория ${product.category}` }}
        </router-link>
        <span class="breadcrumb-separator">/</span>
        <span class="breadcrumb-current">{{ product.name }}</span>
      </nav>
  
      <!-- Main Content -->
      <div v-if="isLoading" class="loader-overlay">
        <div class="loader"></div>
      </div>
  
      <div v-else-if="error" class="error-message">
        {{ error }}
        <button @click="fetchProduct" class="retry-button">Повторить попытку</button>
      </div>
  
      <div v-else class="product-detail-content">
        <!-- Product Images -->
        <div class="product-images">
          <img 
            :src="mainImage || getImageUrl(product.image)" 
            :alt="product.name"
            class="main-image"
          >
          <div v-if="product.images && product.images.length > 1" class="thumbnail-container">
            <img
              v-for="(img, index) in product.images"
              :key="index"
              :src="getImageUrl(img)"
              @click="mainImage = getImageUrl(img)"
              :class="['thumbnail', { active: mainImage === getImageUrl(img) }]"
            >
          </div>
        </div>
  
        <!-- Product Info -->
        <div class="product-info">
          <h1 class="product-title">{{ product.name }}</h1>
          <p class="product-price">{{ product.price }} ₽</p>
          <p class="product-article">Артикул: {{ product.article }}</p>
  
          <div class="product-description" v-html="product.description"></div>
  
          <div class="product-actions">
            <button class="add-to-cart" @click="addToCart">Добавить в корзину</button>
            <button class="buy-now" @click="buyNow">Купить сейчас</button>
          </div>
  
          <div class="product-meta">
            <div class="meta-item" v-if="product.availability">
              <span class="meta-label">Наличие:</span>
              <span class="meta-value">{{ product.availability }}</span>
            </div>
            <div class="meta-item" v-if="product.brand">
              <span class="meta-label">Бренд:</span>
              <span class="meta-value">{{ product.brand }}</span>
            </div>
            <div class="meta-item" v-if="product.weight">
              <span class="meta-label">Вес:</span>
              <span class="meta-value">{{ product.weight }} г</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import axios from 'axios'
  
  const route = useRoute()
  const router = useRouter()
  const product = ref({})
  const isLoading = ref(true)
  const error = ref(null)
  const mainImage = ref(null)
  const baseUrl = 'http://localhost:8000'
  
  const fetchProduct = async () => {
    try {
      isLoading.value = true
      const response = await axios.get(`${baseUrl}/api/products/${route.params.productId}/`)
      product.value = response.data
      mainImage.value = getImageUrl(product.value.image)
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
  
  const addToCart = () => {
    // Implement cart functionality
    console.log('Added to cart:', product.value.id)
    router.push('/cart')  // Example of using router
  }
  
  const buyNow = () => {
    // Implement quick purchase
    console.log('Buy now:', product.value.id)
    router.push('/checkout')  // Example of using router
  }
  
  onMounted(() => {
    fetchProduct()
  })
  </script>
  
  <style scoped>
  .product-detail-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
  }
  
  .product-detail-content {
    display: flex;
    gap: 40px;
    margin-top: 30px;
  }
  
  .product-images {
    flex: 1;
  }
  
  .main-image {
    width: 100%;
    max-height: 500px;
    object-fit: contain;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    margin-bottom: 20px;
  }
  
  .thumbnail-container {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
  }
  
  .thumbnail {
    width: 80px;
    height: 80px;
    object-fit: cover;
    border: 1px solid #e0e0e0;
    border-radius: 4px;
    cursor: pointer;
    transition: border-color 0.3s;
  }
  
  .thumbnail:hover, .thumbnail.active {
    border-color: #42b983;
  }
  
  .product-info {
    flex: 1;
  }
  
  .product-title {
    font-size: 28px;
    margin-bottom: 15px;
    color: #2c3e50;
  }
  
  .product-price {
    font-size: 24px;
    font-weight: bold;
    color: #42b983;
    margin-bottom: 15px;
  }
  
  .product-article {
    color: #777;
    margin-bottom: 20px;
  }
  
  .product-description {
    margin-bottom: 30px;
    line-height: 1.6;
  }
  
  .product-actions {
    display: flex;
    gap: 15px;
    margin-bottom: 30px;
  }
  
  .add-to-cart, .buy-now {
    padding: 12px 24px;
    border: none;
    border-radius: 4px;
    font-size: 16px;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  .add-to-cart {
    background-color: #42b983;
    color: white;
  }
  
  .add-to-cart:hover {
    background-color: #369f6e;
  }
  
  .buy-now {
    background-color: #2c3e50;
    color: white;
  }
  
  .buy-now:hover {
    background-color: #1a2634;
  }
  
  .product-meta {
    border-top: 1px solid #e0e0e0;
    padding-top: 20px;
  }
  
  .meta-item {
    margin-bottom: 10px;
    display: flex;
  }
  
  .meta-label {
    font-weight: bold;
    width: 100px;
    color: #555;
  }
  
  .meta-value {
    flex: 1;
  }
  
  /* Shared styles from catalog (loader, error message, breadcrumbs) */
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
    border: 5px solid #f3f3f37e;
    border-top: 5px solid #4d4d4d;
    border-radius: 50%;
    width: 50px;
    height: 50px;
    animation: spin 1s linear infinite;
    margin-bottom: 15px;
  }
  
  .error-message {
    background: #ffebee;
    padding: 15px;
    border-radius: 8px;
    margin-bottom: 20px;
    color: #ff5252;
    text-align: center;
  }
  
  .retry-button {
    background: #ff5252;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    margin-top: 10px;
    cursor: pointer;
    transition: background 0.3s;
  }
  
  .breadcrumbs {
    margin-bottom: 20px;
    font-size: 16px;
    display: flex;
    align-items: center;
  }
  
  .breadcrumb-link {
    color: #42b983;
    text-decoration: none;
    transition: color 0.3s;
  }
  
  .breadcrumb-link:hover {
    color: #2c3e50;
    text-decoration: underline;
  }
  
  .breadcrumb-separator {
    margin: 0 8px;
    color: #777;
  }
  
  .breadcrumb-current {
    color: #2c3e50;
    font-weight: 500;
  }
  
  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
  </style>