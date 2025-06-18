<template>
  <div class="admin-orders-container">
    <h1>Поиск заказа по коду</h1>

    <!-- Форма поиска -->
    <div class="search-form">
      <input 
        v-model="searchCode" 
        type="text" 
        placeholder="Введите код заказа"
        class="search-input"
        @keyup.enter="searchOrder"
      >
      <button @click="searchOrder" class="search-button">
        <span v-if="!isLoading">Найти заказ</span>
        <div v-else class="button-spinner"></div>
      </button>
    </div>

    <!-- Ошибка -->
    <div v-if="error" class="error-message">
      {{ error }}
    </div>

    <!-- Результат поиска -->
    <div v-if="order" class="order-details">
      <div class="order-header">
        <h2>Заказ #{{ order.id }}</h2>
        <div class="order-status" :class="order.status">
          {{ getStatusText(order.status) }}
        </div>
      </div>

      <!-- Информация о пользователе -->
      <div class="user-info">
        <h3>Информация о покупателе</h3>
        <div class="info-grid">
          <div class="info-item">
            <span class="label">Имя пользователя:</span>
            <span class="value">{{ order.user?.username || 'Не указано' }}</span>
          </div>
          <div class="info-item">
            <span class="label">Email:</span>
            <span class="value">{{ order.user?.email || 'Не указан' }}</span>
          </div>
          <div class="info-item">
            <span class="label">Телефон:</span>
            <span class="value">{{ order.user?.phone || 'Не указан' }}</span>
          </div>
          <div class="info-item">
            <span class="label">Дата регистрации:</span>
            <span class="value">{{ order.user?.date_joined ? formatDate(order.user.date_joined) : 'Не указана' }}</span>
          </div>
        </div>
      </div>

      <!-- Детали заказа -->
      <div class="order-items">
        <h3>Товары в заказе</h3>
        <div class="items-list">
          <div v-for="item in order.items" :key="item.id" class="order-item">
            <img 
              :src="getImageUrl(item.product.image)" 
              :alt="item.product.name"
              class="item-image"
              @error="handleImageError"
            >
            <div class="item-details">
              <h4>{{ item.product.name }}</h4>
              <p class="item-article">Артикул: {{ item.product.article }}</p>
              <div class="item-meta">
                <span class="quantity">{{ item.quantity }} шт.</span>
                <span class="price">{{ item.product.price }} ₽</span>
              </div>
            </div>
          </div>
        </div>
        
        <div class="order-summary">
          <div class="total">
            <span>Итого:</span>
            <span class="total-price">{{ calculateTotal(order.items) }} ₽</span>
          </div>
          <div class="order-code">
            <span>Код получения:</span>
            <span class="code">{{ order.code }}</span>
          </div>
          <div class="order-date">
            <span>Создан:</span>
            <span>{{ formatDate(order.created_at) }}</span>
          </div>
        </div>
      </div>

      <!-- Управление статусом -->
      <div class="order-actions">
        <select v-model="order.status" @change="handleStatusChange" class="status-select">
          <option value="pending">Ожидает получения</option>
          <option value="completed">Получен</option>
          <option value="cancelled">Отменён</option>
        </select>
      </div>
    </div>

    <!-- Модальное окно для причины отмены -->
    <div v-if="showCancelModal" class="modal-overlay" @click.self="cancelStatusChange">
      <div class="cancel-modal">
        <h3>Укажите причину отмены заказа</h3>
        <textarea 
          v-model="cancelReason" 
          class="cancel-reason-input"
          placeholder="Введите причину отмены заказа..."
        ></textarea>
        <div class="modal-buttons">
          <button @click="cancelStatusChange" class="cancel-btn">
            Отмена
          </button>
          <button @click="confirmStatusChange" class="confirm-btn">
            Подтвердить
          </button>
        </div>
      </div>
    </div>

    <!-- Секция последних заказов -->
    <div class="recent-orders">
      <h2>Последние заказы</h2>
      
      <div v-if="isLoadingRecent" class="loading-overlay">
        <div class="spinner"></div>
        <span>Загрузка заказов...</span>
      </div>

      <div v-else-if="filteredOrders.length === 0" class="no-orders">
        Нет активных заказов
      </div>

      <div v-else class="orders-grid">
        <div v-for="order in filteredOrders" :key="order.code" class="order-card" @click="loadOrder(order.code)">
          <div class="order-card-header">
            <span class="order-code">Код: {{ order.code }}</span>
            <span class="order-status" :class="order.status">
              {{ getStatusText(order.status) }}
            </span>
          </div>
          
          <div class="order-card-content">
            <div class="order-info-row">
              <span class="label">Покупатель:</span>
              <span class="value">{{ order.user.username }}</span>
            </div>
            <div class="order-info-row">
              <span class="label">Дата создания:</span>
              <span class="value">{{ formatDate(order.created_at) }}</span>
            </div>
            <div class="order-info-row">
              <span class="label">Сумма:</span>
              <span class="value">{{ order.total_price }} ₽</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '@/store/auth'

const authStore = useAuthStore()
const baseUrl = 'https://pashok00191.pythonanywhere.com'

const searchCode = ref('')
const order = ref(null)
const isLoading = ref(false)
const error = ref(null)
const showCancelModal = ref(false)
const cancelReason = ref('')
const previousStatus = ref('')

// Добавляем состояния для последних заказов
const recentOrders = ref([])
const isLoadingRecent = ref(false)

// Вычисляемое свойство для фильтрации заказов
const filteredOrders = computed(() => {
  return recentOrders.value.filter(order => order.status === 'pending')
})

// Загрузка последних заказов
const loadRecentOrders = async () => {
  try {
    isLoadingRecent.value = true
    const api = authStore.getApiClient()
    const response = await api.get('orders/')
    recentOrders.value = response.data
  } catch (err) {
    console.error('Ошибка загрузки последних заказов:', err)
  } finally {
    isLoadingRecent.value = false
  }
}

// Загрузка конкретного заказа по коду
const loadOrder = (code) => {
  searchCode.value = code
  searchOrder()
}

onMounted(() => {
  loadRecentOrders()
})

// Поиск заказа по коду
const searchOrder = async () => {
  if (!searchCode.value) {
    error.value = 'Введите код заказа'
    return
  }

  try {
    isLoading.value = true
    error.value = null
    const api = authStore.getApiClient()
    const response = await api.get(`orders/search/${searchCode.value}/`)
    order.value = response.data
  } catch (err) {
    console.error('Ошибка поиска заказа:', err)
    error.value = 'Заказ не найден или произошла ошибка'
    order.value = null
  } finally {
    isLoading.value = false
  }
}

// Обработка изменения статуса
const handleStatusChange = () => {
  // Сохраняем предыдущий статус перед изменением
  previousStatus.value = order.value.status
  
  if (order.value.status === 'cancelled') {
    showCancelModal.value = true
  } else {
    updateOrderStatus()
  }
}

// Отмена изменения статуса
const cancelStatusChange = () => {
  order.value.status = previousStatus.value
  showCancelModal.value = false
  cancelReason.value = ''
}

// Подтверждение изменения статуса
const confirmStatusChange = () => {
  if (!cancelReason.value.trim()) {
    alert('Пожалуйста, укажите причину отмены заказа')
    return
  }
  updateOrderStatus()
  showCancelModal.value = false
}

// Обновление статуса заказа
const updateOrderStatus = async () => {
  try {
    const api = authStore.getApiClient()
    const data = {
      status: order.value.status
    }
    
    // Добавляем причину отмены только если статус "cancelled"
    if (order.value.status === 'cancelled') {
      data.cancel_reason = cancelReason.value
    }
    
    const response = await api.patch(`orders/${order.value.code}/`, data)
    
    // Показываем уведомление об успешном обновлении
    alert('Статус заказа успешно обновлен')
    
    // Обновляем данные заказа из ответа
    if (response.data) {
      order.value = response.data
    }
    
    // Очищаем причину отмены
    cancelReason.value = ''
  } catch (err) {
    console.error('Ошибка обновления статуса:', err)
    error.value = err.response?.data?.detail || 'Не удалось обновить статус заказа'
    
    // Возвращаем предыдущий статус в случае ошибки
    order.value.status = previousStatus.value
  }
}

// Вспомогательные функции
const getStatusText = (status) => {
  const statusMap = {
    'pending': 'Ожидает получения',
    'completed': 'Получен',
    'cancelled': 'Отменён'
  }
  return statusMap[status] || status
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

const getImageUrl = (imagePath) => {
  if (!imagePath) return require('@/assets/img/no-image.webp')
  if (imagePath.startsWith('http')) return imagePath
  return `${baseUrl}${imagePath}`
}

const handleImageError = (e) => {
  e.target.src = require('@/assets/img/no-image.webp')
}

const calculateTotal = (items) => {
  return items.reduce((total, item) => total + (item.product.price * item.quantity), 0)
}
</script>

<style scoped>
.admin-orders-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.admin-orders-container h1 {
  color: #ffffff;
  margin-bottom: 30px;
  font-family: 'Manrope', sans-serif;
}

/* Форма поиска */
.search-form {
  display: flex;
  gap: 10px;
  margin-bottom: 30px;
}

.search-input {
  flex: 1;
  padding: 12px;
  border: 1px solid #737373;
  border-radius: 8px;
  background: rgba(0, 0, 0, 0.23);
  color: #ffffff;
  font-size: 16px;
  font-family: 'Manrope', sans-serif;
}

.search-button {
  padding: 12px 24px;
  background: #474747;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  min-width: 120px;
  display: flex;
  justify-content: center;
  align-items: center;
  font-family: 'Manrope', sans-serif;
}

.search-button:hover {
  background: #5a5a5a;
  transform: translateY(-1px);
}

.button-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: #ffffff;
  animation: spin 1s linear infinite;
}

/* Сообщение об ошибке */
.error-message {
  padding: 15px;
  background: rgba(255, 77, 79, 0.2);
  border: 1px solid rgba(255, 77, 79, 0.5);
  color: #ff5252;
  border-radius: 8px;
  margin-bottom: 20px;
}

/* Результаты поиска */
.order-details {
  background: rgba(0, 0, 0, 0.23);
  border: 1px solid #737373;
  border-radius: 16px;
  padding: 20px;
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.order-header h2 {
  color: #ffffff;
  margin: 0;
  font-family: 'Manrope', sans-serif;
}

.order-status {
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 14px;
  font-family: 'Manrope', sans-serif;
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

/* Информация о пользователе */
.user-info {
  background: rgba(0, 0, 0, 0.1);
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 20px;
}

.user-info h3 {
  color: #ffffff;
  margin-top: 0;
  margin-bottom: 15px;
  font-family: 'Manrope', sans-serif;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.info-item .label {
  color: #8d8d8d;
  font-size: 14px;
  font-family: 'Manrope', sans-serif;
}

.info-item .value {
  color: #ffffff;
  font-family: 'Manrope', sans-serif;
}

/* Список товаров */
.order-items {
  margin-top: 20px;
}

.order-items h3 {
  color: #ffffff;
  margin-bottom: 15px;
  font-family: 'Manrope', sans-serif;
}

.items-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.order-item {
  display: flex;
  gap: 15px;
  padding: 15px;
  background: rgba(0, 0, 0, 0.1);
  border-radius: 12px;
}

.item-image {
  width: 100px;
  height: 100px;
  object-fit: cover;
  border-radius: 8px;
}

.item-details {
  flex: 1;
}

.item-details h4 {
  color: #ffffff;
  margin: 0 0 5px 0;
  font-family: 'Manrope', sans-serif;
}

.item-article {
  color: #8d8d8d;
  font-size: 14px;
  margin: 5px 0;
  font-family: 'Manrope', sans-serif;
}

.item-meta {
  display: flex;
  justify-content: space-between;
  margin-top: 10px;
  color: #dededecb;
}

.item-meta .quantity,
.item-meta .price {
  font-family: 'Manrope', sans-serif;
}

/* Итоги заказа */
.order-summary {
  margin-top: 20px;
  padding: 20px;
  background: rgba(0, 0, 0, 0.1);
  border-radius: 12px;
}

.order-summary .total,
.order-summary .order-code,
.order-summary .order-date {
  font-family: 'Manrope', sans-serif;
}

.total span,
.order-code span,
.order-date span {
  font-family: 'Manrope', sans-serif;
}

.total {
  display: flex;
  justify-content: space-between;
  color: #ffffff;
  font-size: 18px;
  margin-bottom: 10px;
}

.order-code {
  display: flex;
  justify-content: space-between;
  margin: 10px 0;
  color: #ffffff;
  font-weight: 500;
}

.code {
  font-family: 'Manrope', sans-serif;
  background: rgba(71, 71, 71, 0.3);
  padding: 6px 12px;
  border-radius: 6px;
  color: #ffffff;
}

.order-date {
  display: flex;
  justify-content: space-between;
  color: #8d8d8d;
  font-size: 14px;
  font-family: 'Manrope', sans-serif;
}

/* Управление статусом */
.order-actions {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid rgba(115, 115, 115, 0.3);
}

.status-select {
  width: 100%;
  padding: 12px;
  background: rgba(71, 71, 71, 0.3);
  border: 1px solid #737373;
  border-radius: 8px;
  color: #ffffff;
  cursor: pointer;
  font-family: 'Manrope', sans-serif;
}

/* Анимации */
@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Адаптивность */
@media (max-width: 768px) {
  .search-form {
    flex-direction: column;
  }
  
  .order-header {
    flex-direction: column;
    gap: 10px;
    align-items: flex-start;
  }
  
  .order-item {
    flex-direction: column;
  }
  
  .item-image {
    width: 100%;
    height: 200px;
  }
}

/* Стили для модального окна */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  animation: fadeIn 0.3s ease-out;
}

.cancel-modal {
  background: rgba(0, 0, 0, 0.8);
  border: 1px solid #737373;
  border-radius: 16px;
  padding: 25px;
  width: 90%;
  max-width: 500px;
  animation: slideIn 0.3s ease-out;
}

.cancel-modal h3 {
  color: #dededecb;
  margin-bottom: 20px;
  text-align: center;
  font-family: 'Manrope', sans-serif;
  font-size: 1.2em;
}

.cancel-reason-input {
  width: 100%;
  min-height: 120px;
  padding: 12px;
  background: rgba(0, 0, 0, 0.23);
  border: 1px solid #737373;
  border-radius: 8px;
  color: #ffffff;
  font-size: 16px;
  font-family: 'Manrope', sans-serif;
  margin-bottom: 20px;
  resize: vertical;
}

.cancel-reason-input:focus {
  outline: none;
  border-color: rgba(255, 77, 79, 0.5);
}

.modal-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.cancel-btn, .confirm-btn {
  padding: 8px 16px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-family: 'Manrope', sans-serif;
  transition: all 0.3s ease;
}

.cancel-btn {
  background: rgba(71, 71, 71, 0.3);
  border: 1px solid #737373;
  color: #dededecb;
}

.cancel-btn:hover {
  background: rgba(71, 71, 71, 0.5);
  transform: translateY(-1px);
}

.confirm-btn {
  background: rgba(255, 77, 79, 0.3);
  border: 1px solid rgba(255, 77, 79, 0.5);
  color: white;
}

.confirm-btn:hover {
  background: rgba(255, 77, 79, 0.5);
  transform: translateY(-1px);
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideIn {
  from {
    transform: translateY(-20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

/* Стили для секции последних заказов */
.recent-orders {
  margin-top: 40px;
}

.recent-orders h2 {
  color: #ffffff;
  margin-bottom: 20px;
  font-family: 'Manrope', sans-serif;
  font-weight: 400;
}

.orders-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.order-card {
  background: rgba(0, 0, 0, 0.23);
  border: 1px solid #737373;
  border-radius: 12px;
  padding: 15px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.order-card:hover {
  transform: translateY(-2px);
  border-color: rgba(222, 222, 222, 0.3);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.order-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid rgba(115, 115, 115, 0.3);
}

.order-card-header .order-code {
  font-family: 'Manrope', sans-serif;
}

.order-info-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.order-info-row .label {
  color: #8d8d8d;
  font-size: 14px;
  font-family: 'Manrope', sans-serif;
}

.order-info-row .value {
  color: #ffffff;
  font-weight: 500;
  font-family: 'Manrope', sans-serif;
}

/* Адаптивность для мобильных устройств */
@media (max-width: 768px) {
  .orders-grid {
    grid-template-columns: 1fr;
  }
  
  .order-card {
    margin-bottom: 15px;
  }
}

/* Стили для статусов заказов */
.order-status {
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 14px;
  font-family: 'Manrope', sans-serif;
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

.order-id {
  font-family: 'Manrope', sans-serif;
}

.item-quantity, .item-price {
  font-family: 'Manrope', sans-serif;
}

.total-price {
  font-family: 'Manrope', sans-serif;
  font-weight: 500;
}
</style> 