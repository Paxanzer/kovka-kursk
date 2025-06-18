<template>
  <div class="orders-container">
    <h1>Мои заказы</h1>
    
    <div v-if="isLoading" class="loading">
      <div class="spinner"></div>
      <span>Загрузка заказов...</span>
    </div>
    
    <div v-else-if="error" class="error-message">
      {{ error }}
      <button @click="fetchOrders" class="retry-button">Повторить попытку</button>
    </div>
    
    <div v-else-if="orders.length === 0" class="no-orders">
      <p>У вас пока нет заказов</p>
      <router-link to="/catalog" class="browse-catalog">
        Перейти к покупкам
      </router-link>
    </div>
    
    <div v-else class="orders-list">
      <div v-for="order in orders" :key="order.id" class="order-card">
        <div class="order-header">
          <div class="order-info">
            <span class="order-number">Заказ #{{ order.id }}</span>
            <span class="order-date">{{ formatDate(order.created_at) }}</span>
          </div>
          <div class="order-status" :class="order.status">
            {{ getStatusText(order.status) }}
          </div>
        </div>
        
        <div class="order-items">
          <div v-for="item in order.items" :key="item.id" class="order-item">
            <img :src="getImageUrl(item.product.image)" :alt="item.product.name">
            <div class="item-details">
              <h3>{{ item.product.name }}</h3>
              <p class="item-quantity">Количество: {{ item.quantity }}</p>
              <p class="item-price">{{ item.product.price }} ₽</p>
            </div>
          </div>
        </div>
        
        <div class="order-footer">
          <div class="order-total">
            <span>Итого:</span>
            <span class="total-price">{{ calculateTotal(order.items) }} ₽</span>
          </div>
          
          <div v-if="order.code" class="order-code">
            <span>Код получения:</span>
            <span class="code">{{ order.code }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const orders = ref([])
const isLoading = ref(true)
const error = ref(null)
const baseUrl = 'https://pashok00191.pythonanywhere.com'

const fetchOrders = async () => {
  try {
    isLoading.value = true
    error.value = null
    const response = await axios.get(`${baseUrl}/api/orders/`)
    orders.value = response.data
  } catch (err) {
    error.value = 'Не удалось загрузить заказы'
    console.error('Error fetching orders:', err)
  } finally {
    isLoading.value = false
  }
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('ru-RU', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const getStatusText = (status) => {
  const statusMap = {
    'pending': 'Ожидает получения',
    'completed': 'Получен',
    'cancelled': 'Отменён'
  }
  return statusMap[status] || status
}

const calculateTotal = (items) => {
  return items.reduce((total, item) => total + (item.product.price * item.quantity), 0)
}

const getImageUrl = (imagePath) => {
  if (!imagePath) return require('@/assets/img/no-image.webp')
  if (imagePath.startsWith('http')) return imagePath
  return `${baseUrl}${imagePath}`
}

onMounted(() => {
  fetchOrders()
})
</script>

<style scoped>
.orders-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.orders-container h1 {
  color: #ffffff;
  margin-bottom: 30px;
  font-family: 'Manrope', sans-serif;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
  color: #dededecb;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: #8d8d8d;
  animation: spin 1s ease-in-out infinite;
}

.error-message {
  background: rgba(255, 77, 79, 0.2);
  padding: 20px;
  border-radius: 16px;
  text-align: center;
  color: #ff5252;
  border: 1px solid rgba(255, 77, 79, 0.5);
}

.retry-button {
  margin-top: 15px;
  padding: 8px 16px;
  background: rgba(255, 77, 79, 0.3);
  border: none;
  border-radius: 8px;
  color: white;
  cursor: pointer;
}

.no-orders {
  text-align: center;
  color: #dededecb;
  padding: 40px;
}

.browse-catalog {
  display: inline-block;
  margin-top: 20px;
  padding: 10px 20px;
  background: #474747;
  color: white;
  text-decoration: none;
  border-radius: 8px;
  transition: background 0.3s;
}

.browse-catalog:hover {
  background: #5a5a5a;
}

.order-card {
  background: rgba(0, 0, 0, 0.23);
  border: 1px solid #737373;
  border-radius: 16px;
  margin-bottom: 20px;
  overflow: hidden;
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid rgba(115, 115, 115, 0.3);
}

.order-info {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.order-number {
  color: #ffffff;
  font-weight: 500;
}

.order-date {
  color: #8d8d8d;
  font-size: 14px;
}

.order-status {
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 14px;
}

.order-status.pending {
  background: rgba(255, 193, 7, 0.2);
  color: #ffc107;
}

.order-status.completed {
  background: rgba(76, 175, 80, 0.2);
  color: #4caf50;
}

.order-status.cancelled {
  background: rgba(244, 67, 54, 0.2);
  color: #f44336;
}

.order-items {
  padding: 20px;
}

.order-item {
  display: flex;
  gap: 20px;
  padding: 10px 0;
  border-bottom: 1px solid rgba(115, 115, 115, 0.3);
}

.order-item:last-child {
  border-bottom: none;
}

.order-item img {
  width: 80px;
  height: 80px;
  object-fit: cover;
  border-radius: 8px;
}

.item-details {
  flex: 1;
}

.item-details h3 {
  margin: 0;
  color: #ffffff;
  font-size: 16px;
}

.item-quantity {
  color: #8d8d8d;
  margin: 5px 0;
}

.item-price {
  color: #dededecb;
  font-weight: 500;
  margin: 5px 0;
}

.order-footer {
  padding: 20px;
  background: rgba(0, 0, 0, 0.1);
  border-top: 1px solid rgba(115, 115, 115, 0.3);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.order-total {
  color: #ffffff;
  font-size: 18px;
}

.total-price {
  font-weight: 500;
  margin-left: 10px;
}

.order-code {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #dededecb;
}

.code {
  background: rgba(71, 71, 71, 0.3);
  padding: 6px 12px;
  border-radius: 6px;
  font-family: 'Manrope', sans-serif;
  font-size: 16px;
  color: #ffffff;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .order-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .order-footer {
    flex-direction: column;
    gap: 15px;
  }
  
  .order-code {
    width: 100%;
    justify-content: space-between;
  }
}

@media (max-width: 480px) {
  .order-item {
    flex-direction: column;
    text-align: center;
  }
  
  .order-item img {
    width: 120px;
    height: 120px;
    margin: 0 auto;
  }
}
</style> 