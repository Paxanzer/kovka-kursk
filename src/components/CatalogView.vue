<template>
    <!-- Основной контейнер -->
    <div class="catalog-container">
      <!-- Хлебные крошки (верхняя часть страницы) -->
      <nav class="breadcrumbs">
        
        <img 
        src="@/assets/left-arrow.png" 
        alt="Назад"
        class="catalog_img"
         @click="goToAbout"
      >
        <!-- Заголовок (под хлебными крошками) -->
      <h1 class="catalog-title">{{ currentCategoryName }}</h1>
      </nav>
  
      
  
      <!-- Лоадер (центр страницы, поверх контента) -->
      <div v-if="isLoading" class="loader-overlay">
        <div class="loader"></div>
      </div>
  
      <!-- Сообщение об ошибке (под заголовком) -->
      <div v-if="error" class="error-message">
        {{ error }}
        <button @click="fetchProducts" class="retry-button">Повторить попытку</button>
      </div>
  
      <!-- Контейнер товаров (основная область контента) -->
  <div v-if="!isLoading" class="products-container">
    <!-- Карточка товара -->
    <div 
      v-for="(product, index) in filteredProducts"
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
      </div>
    </div>

    <!-- Сообщение при отсутствии товаров -->
    <div v-if="filteredProducts.length === 0" class="empty-catalog">
      В этой категории пока нет товаров
      
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

const products = ref([])
const isLoading = ref(true)
const error = ref(null)
const baseUrl = 'http://localhost:8000'
const visibleProductIds = ref([]) // Для отслеживания видимых карточек

const categoryId = computed(() => parseInt(route.params.categoryId))

const goToProductDetail = (productId) => {
  router.push(`/product/${productId}`)
}

const fetchProducts = async () => {
  try {
    isLoading.value = true
    const response = await axios.get(`${baseUrl}/api/products/`)
    products.value = response.data
    console.log('Raw products data:', products.value)
  } catch (err) {
    error.value = 'Ошибка загрузки товаров'
    console.error('Fetch error:', err)
  } finally {
    isLoading.value = false
    nextTick(() => {
      initProductsObserver()
    })
  }
}

const filteredProducts = computed(() => {
  return products.value.filter(product => {
    const catId = product.category?.id ?? product.category
    return catId == categoryId.value
  })
})

const currentCategoryName = computed(() => {
  const product = products.value.find(p => {
    const catId = p.category?.id ?? p.category
    return catId == categoryId.value
  })
  return product?.category?.name ?? `Категория ${categoryId.value}`
})

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

  // Наблюдаем за всеми карточками товаров
  filteredProducts.value.forEach(product => {
    const element = document.getElementById(`product-card_${product.id}`)
    if (element) {
      observer.observe(element)
    }
  })
}
//  Добавляем метод для перехода на страницу About
const goToAbout = () => {
  router.push('/about');
};

onMounted(() => {
  fetchProducts()
})

watch(filteredProducts, () => {
  nextTick(() => {
    initProductsObserver()
  })
}, { deep: true })
</script>
  
  <style scoped>
  
/* Основные стили контейнера */
.catalog-container {
    max-width: 1200px;
    margin: 20px auto; /* Добавляем отступ сверху и снизу */
    padding: 0 15px;
    position: relative;
    display: flex;          /* Используем flexbox */
    flex-direction: column; /* Размещаем элементы вертикально */
    align-items: stretch;    /* Растягиваем элементы по ширине */
}

/* Стили хлебных крошек (верх страницы) */
.breadcrumbs {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px 0;
    width: 100%;
    gap: 20px; /* Начальный отступ между элементами */
    box-sizing: border-box;
}

.breadcrumb-link {
    color: #DEDEDE;
    font-family: 'Manrope', sans-serif;
    font-style: normal;
    font-size: 20px;
    text-align: center;
    transition: color 0.3s;
    text-decoration: none;
    white-space: nowrap; /* Запрещаем перенос текста */
}

.breadcrumb-link:hover {
    color: #dedede96;
    text-decoration: none;
}

.breadcrumb-separator {
    margin: 0 8px;
    color: #777;
}

.breadcrumb-current {
    color: #2c3e50;
    font-weight: 500;
}

/* Заголовок каталога */
.catalog-title {
    color: #DEDEDE;
    font-family: 'Manrope', sans-serif;
    font-style: normal;
    font-size: clamp(18px, 4vw, 24px); /* Адаптивный размер шрифта */
    font-weight: 600;
    text-align: right;
    white-space: nowrap; /* Запрещаем перенос текста */
    overflow: hidden;
    text-overflow: ellipsis; /* Добавляем многоточие если текст не помещается */
    margin-bottom: 20px;  /* Добавляем отступ снизу */
    box-sizing: border-box;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* Адаптивность - уменьшаем отступы и размеры */
@media (max-width: 992px) {
    .breadcrumbs {
        gap: 15px;
    }
}

@media (max-width: 768px) {
    .breadcrumbs {
        gap: 10px;
        padding: 10px 0;
    }


}

@media (max-width: 576px) {
    .breadcrumbs {
        gap: 5px;
    }

    .catalog-title {
        font-size: 16px;
    }
}

@media (max-width: 400px) {
    .breadcrumbs {
        gap: 2px;
    }
}

/* Сообщение об ошибке */
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

.retry-button:hover {
    background: #ff0000;
}

/* Контейнер товаров */
.products-container {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 25px;
    width: 100%; /* Занимает всю доступную ширину */
    box-sizing: border-box;
}

/* Карточка товара */
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
.catalog_img {
    width: 30px; /* Меньше на мобильных */
    height: 30px; /* Меньше на мобильных */
    /*left: 323px; Удалено, позиционирование обрабатывается flexbox */
    /*top: 19px;  Удалено, позиционирование обрабатывается flexbox */
    opacity: 0.4;
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.2s ease;
    margin-right: 5px; /* Отступ между картинкой и текстом */
    position: relative;
}

.catalog_img:hover {
    opacity: 0.75;
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

/* Сообщение о пустом каталоге */
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

.card_txt {
    width: 248px;
    height: 137px;
    font-family: 'Manrope', sans-serif;
    font-style: normal;
    font-weight: 400;
    font-size: 30px;
    line-height: 1.2;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    color: #DEDEDE;
    margin-top: -4px;
    transition: text-shadow 0.3s ease;
    overflow: hidden;
    word-break: break-word;
}

/* Адаптивность контейнера товаров */
@media (max-width: 768px) {
    .products-container {
        grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); /* Уменьшаем минимальную ширину */
        gap: 15px; /* Уменьшаем отступы между товарами */
    }
}
</style>