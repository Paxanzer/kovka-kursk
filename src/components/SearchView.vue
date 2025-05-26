<template>
  <div class="catalog-container">
    <!-- Хлебные крошки с полем поиска -->
    <nav class="breadcrumbs">
      <img 
        src="@/assets/left-arrow.png" 
        alt="Назад"
        class="catalog_img"
        @click="goToAbout"
      >
      <h1 class="catalog-title">Поиск товаров</h1>
      
      <!-- Поле поиска -->
      <div class="search-box">
        <input 
          v-model="searchQuery"
          class="search-input" 
          placeholder="Введите название товара..."
          type="text"
          @input="handleSearch"
        >
      </div>
    </nav>

    <!-- Лоадер -->
    <div v-if="isLoading" class="loader-overlay">
      <div class="loader"></div>
    </div>

    <!-- Контейнер товаров -->
    <div v-if="!isLoading" class="products-container">
      <!-- Карточка товара -->
      <div 
        v-for="(product, index) in displayedProducts"
        :key="product.id"
        class="product-card"
        :id="'product-card_' + product.id"
        :style="{ '--delay': index * 0.03 + 's' }"
        :class="{ 'animate-in': visibleProductIds.includes('product-card_' + product.id) }"
        @click="goToProductDetail(product.id)"
      >
        <img 
          :src="getImageUrl(product.image)"
          :alt="product.name"
          class="product-image"
          @error="handleImageError"
        >
        <div class="product-info">
          <h3 class="product-name">{{ product.name }}</h3>
          <p class="product-price">{{ product.price }} ₽</p>
          <p class="product-article">Артикул: {{ product.article }}</p>
          <p v-if="product.category" class="product-category">
            {{ product.category.name }}
          </p>
        </div>
      </div>

      <!-- Сообщение если ничего не найдено -->
      <div v-if="searchQuery && displayedProducts.length === 0" class="empty-catalog">
        Товары по запросу "{{ searchQuery }}" не найдены
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const route = useRoute()
const baseUrl = 'http://localhost:8000'

// Реактивные данные
const products = ref([])
const categories = ref([])
const searchQuery = ref(route.query.q || '')
const isLoading = ref(true)
const visibleProductIds = ref([])

// Watcher для параметра q в URL
watch(() => route.query.q, (newQuery) => {
  searchQuery.value = newQuery || ''
})

// Получение всех товаров и категорий
const fetchData = async () => {
  try {
    isLoading.value = true
    const [productsRes, categoriesRes] = await Promise.all([
      axios.get(`${baseUrl}/api/products/`),
      axios.get(`${baseUrl}/api/categories/`)
    ])
    products.value = productsRes.data
    categories.value = categoriesRes.data
  } catch (err) {
    console.error('Ошибка загрузки данных:', err)
  } finally {
    isLoading.value = false
    nextTick(() => {
      initProductsObserver()
    })
  }
}

// Функция для нормализации строки
const normalizeString = (str) => {
  return str.toLowerCase()
    .replace(/[^\wа-яё\d\s]/g, '') // Сохраняем пробелы для разделения слов
    .trim()
}

// Функция для разделения строки на слова и поиска
const fullTextSearch = (productName, query) => {
  if (!query.trim()) return false
  
  const normalizedProduct = normalizeString(productName)
  const normalizedQuery = normalizeString(query)
  
  // Разбиваем запрос на отдельные слова
  const queryWords = normalizedQuery.split(/\s+/).filter(word => word.length > 0)
  
  // Если запрос состоит из одного слова - ищем его вхождение
  if (queryWords.length === 1) {
    return normalizedProduct.includes(queryWords[0])
  }
  
  // Для нескольких слов ищем товары, содержащие все слова запроса
  // (можно изменить на some() если нужно, чтобы совпадало хотя бы одно слово)
  return queryWords.every(word => normalizedProduct.includes(word))
  
  // Альтернативный вариант - поиск по точному совпадению фразы
  // return normalizedProduct.includes(normalizedQuery)
}

// Отображаемые товары
const displayedProducts = computed(() => {
  if (!searchQuery.value.trim()) {
    return products.value
  }
  
  // Разбиваем поисковый запрос на отдельные фразы (если разделены запятыми)
  const searchPhrases = searchQuery.value.split(',')
    .map(phrase => phrase.trim())
    .filter(phrase => phrase.length > 0)
  
  return products.value.filter(product => {
    // Ищем товары, которые соответствуют хотя бы одной из поисковых фраз
    return searchPhrases.some(phrase => 
      fullTextSearch(product.name, phrase)
    )
  })
})

const handleSearch = () => {
  nextTick(() => {
    initProductsObserver()
  })
}

const goToProductDetail = (productId) => {
  router.push(`/product/${productId}`)
}

const goToAbout = () => {
  router.push('/about')
}

const getImageUrl = (imagePath) => {
  if (!imagePath) return require('@/assets/img/no-image.webp')
  if (imagePath.startsWith('http')) return imagePath
  return `${baseUrl}${imagePath}`
}

const handleImageError = (event) => {
  event.target.src = require('@/assets/img/no-image.webp')
}

const initProductsObserver = () => {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const id = entry.target.id
          if (!visibleProductIds.value.includes(id)) {
            visibleProductIds.value.push(id)
          }
        }
      })
    },
    {
      root: null,
      rootMargin: '0px',
      threshold: 0.1,
    }
  )

  displayedProducts.value.forEach(product => {
    const element = document.getElementById(`product-card_${product.id}`)
    if (element) {
      observer.observe(element)
    }
  })
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.product-category {
  color: #DEDEDE;
  font-family: 'Manrope', sans-serif;
  font-style: normal;
  font-size: 14px;
  line-height: 1.2;
  margin-top: 15px;
  opacity: 0.7;
  text-align: center;
  margin-bottom: 0px;
}
/* Основные стили контейнера из вашего шаблона */
.catalog-container {
  max-width: 1200px;
  margin: 20px auto;
  padding: 0 15px;
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: stretch;
}

/* Стили хлебных крошек с поиском */
.breadcrumbs {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 0;
  width: 100%;
  gap: 20px;
  box-sizing: border-box;
  flex-wrap: wrap;
}

.catalog-title {
  color: #DEDEDE;
  font-family: 'Manrope', sans-serif;
  font-style: normal;
  font-size: clamp(18px, 4vw, 24px);
  font-weight: 600;
  white-space: nowrap;
  margin: 0;
}

/* Поле поиска */
.search-box {
  flex-grow: 1;
  min-width: 200px;
  max-width: 400px;
}

.search-input {
  width: 100%;
  padding: 10px 15px;
  background: rgba(0, 0, 0, 0.23);
  border: 1px solid #737373;
  border-radius: 20px;
  color: #DEDEDE;
  font-family: 'Manrope', sans-serif;
  font-size: 16px;
  transition: all 0.3s ease;
}

.search-input:focus {
  outline: none;
  border-color: #474747;
  box-shadow: 0 0 0 2px rgba(177, 177, 177, 0.2);
}

.search-input:hover {
  border-color: #ffffffc2;
}

/* Остальные стили из вашего шаблона */
.catalog_img {
  width: 30px;
  height: 30px;
  opacity: 0.4;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-right: 5px;
}

.catalog_img:hover {
  opacity: 0.75;
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
  border: 5px solid #f3f3f37e;
  border-top: 5px solid #4d4d4d;
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

.products-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 25px;
  width: 100%;
  box-sizing: border-box;
}

.product-card {
  border: 2px solid #737373;
  background: rgba(0, 0, 0, 0.23);
  border-radius: 15px;
  overflow: hidden;
  transition: all 0.3s ease;
  cursor: pointer;
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.5s ease, transform 0.5s ease, box-shadow 0.3s ease, transform 0.3s ease;
  transition-delay: var(--delay, 0s);
  box-sizing: border-box;
}

.product-card.animate-in {
  opacity: 1;
  transform: translateY(0);
}

.product-card:hover {
  transform: translateY(-5px) scale(1.01);
  box-shadow: 0 5px 14px rgba(222, 222, 222, 0.2);
  transition-delay: 0s;
}

.product-image {
  width: 100%;
  height: 220px;
  object-fit: cover;
  border-bottom: 2px solid #737373;
  transition: transform 0.3s ease;
}

.product-card:hover .product-image {
  transform: scale(1.04);
}

.product-info {
  padding: 16px;
  box-sizing: border-box;
}

.product-name {
  margin: 0 0 10px;
  color: #DEDEDE;
  font-family: 'Manrope', sans-serif;
  font-style: normal;
  font-size: 19px;
  line-height: 1.2;
  box-sizing: border-box;
}

.product-price {
  font-weight: bold;
  color: #ffffff;
  font-family: 'Manrope', sans-serif;
  font-style: normal;
  font-size: 20px;
  line-height: 1.2;
  transition: all 0.3s ease;
  box-sizing: border-box;
}

.product-card:hover .product-price {
  transform: scale(1.15) translateX(15px);
  text-shadow: 0 0 8px rgba(222, 222, 222, 0.4);
}

.product-article {
  color: #DEDEDE;
  font-family: 'Manrope', sans-serif;
  font-style: normal;
  font-size: 20px;
  line-height: 1.2;
  margin-bottom: 0;
  box-sizing: border-box;
}

.empty-catalog {
  grid-column: 1 / -1;
  text-align: center;
  padding: 40px;
  font-size: 18px;
  color: #dedede94;
  font-family: 'Manrope', sans-serif;
  font-style: normal;
  box-sizing: border-box;
}

/* Адаптивность */
@media (max-width: 768px) {
  .breadcrumbs {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .search-box {
    width: 100%;
    max-width: 100%;
  }
  
  .products-container {
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 15px;
  }
}
</style>