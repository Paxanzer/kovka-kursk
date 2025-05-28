<template>
  <div class="profile-container fade-in">
    <div class="profile-card">
      <h2>Профиль пользователя</h2>

      <div v-if="isLoading" class="loading-overlay">
        <div class="spinner"></div>
        <span>Загрузка профиля...</span>
      </div>
      
      <div v-if="user" class="profile-content">
        <div class="profile-field">
          <span class="field-label">Логин:</span>
          <span class="field-value">{{ user.username }}</span>
        </div>
        
        <div class="profile-field">
          <span class="field-label">Email:</span>
          <span class="field-value">{{ user.email || 'Не указан' }}</span>
        </div>
        
        <div class="profile-field">
          <span class="field-label">Телефон:</span>
          <span class="field-value">{{ user.phone || 'Не указан' }}</span>
        </div>
        
      </div>

      <!-- Секция заказов -->
      <div v-if="user && user.orders" class="orders-section">
        <h3>Мои заказы</h3>
        
        <!-- Вкладки -->
        <div class="orders-tabs">
          <button 
            class="tab-button" 
            :class="{ active: currentTab === 'pending' }"
            @click="currentTab = 'pending'"
            data-tab="pending"
          >
            Ждут получения
          </button>
          <button 
            class="tab-button" 
            :class="{ active: currentTab === 'completed' }"
            @click="currentTab = 'completed'"
            data-tab="completed"
          >
            Завершенные
          </button>
          <button 
            class="tab-button" 
            :class="{ active: currentTab === 'cancelled' }"
            @click="currentTab = 'cancelled'"
            data-tab="cancelled"
          >
            Отмененные
          </button>
        </div>

        <div v-if="filteredOrders.length === 0" class="no-orders">
          <template v-if="currentTab === 'pending'">
            У вас нет заказов, ожидающих получения
          </template>
          <template v-else-if="currentTab === 'completed'">
            У вас нет завершенных заказов
          </template>
          <template v-else>
            У вас нет отмененных заказов
          </template>
        </div>
        
        <div v-else class="orders-list">
          <div v-for="order in filteredOrders" :key="order.id" class="order-card">
            <div class="order-header">
              <div class="order-info">
                <span class="order-code">Код заказа: {{ order.code }}</span>
                <span class="order-date">{{ formatDate(order.created_at) }}</span>
              </div>
              <div class="order-status" :class="order.status">
                {{ getStatusText(order.status) }}
              </div>
            </div>
            
            <!-- Причина отмены -->
            <div v-if="order.status === 'cancelled' && order.cancel_reason" class="cancel-reason">
              <h4>Причина отмены:</h4>
              <p>{{ order.cancel_reason }}</p>
            </div>

            <div class="order-items">
              <div v-for="item in order.items" :key="item.product.id" class="order-item">
                <img 
                  :src="getImageUrl(item.product.image)" 
                  :alt="item.product.name"
                  class="item-image"
                  @error="handleImageError"
                >
                <div class="item-details">
                  <span class="item-name">{{ item.product.name }}</span>
                  <span class="item-article">Артикул: {{ item.product.article }}</span>
                  <div class="item-price-qty">
                    <span class="item-quantity">{{ item.quantity }} шт.</span>
                    <span class="item-price">{{ item.price }} ₽</span>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="order-footer">
              <span class="order-total">Итого: {{ order.total_price }} ₽</span>
            </div>
          </div>
        </div>
      </div>
      
      <button 
        @click="showLogoutConfirm = true" 
        class="logout-btn"
        :disabled="isLoading"
      >
        <span class="btn-content">
          <span v-if="isLoading" class="spinner small"></span>
          <span>Выйти</span>
        </span>
      </button>
    </div>

    <!-- Модальное окно подтверждения выхода -->
    <div v-if="showLogoutConfirm" class="modal-overlay" @click.self="showLogoutConfirm = false">
      <div class="confirm-modal">
        <h3>Подтверждение выхода</h3>
        <p>Вы действительно хотите выйти из аккаунта?</p>
        
        <div class="modal-buttons">
          <button @click="showLogoutConfirm = false" class="cancel-btn">
            Отмена
          </button>
          <button @click="confirmLogout" class="confirm-btn">
            Выйти
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { useAuthStore } from '@/store/auth.js'

const authStore = useAuthStore()
const user = ref(null)
const isLoading = ref(false)
const showLogoutConfirm = ref(false)
const baseUrl = 'http://localhost:8000'
const currentTab = ref('pending')

// Фильтрация заказов по статусу
const filteredOrders = computed(() => {
  if (!user.value?.orders) return []
  return user.value.orders.filter(order => order.status === currentTab.value)
})

const confirmLogout = () => {
  showLogoutConfirm.value = false
  authStore.logout()
}

const formatDate = (dateString) => {
  const options = { 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }
  return new Date(dateString).toLocaleDateString('ru-RU', options)
}

const getImageUrl = (imagePath) => {
  if (!imagePath) return require('@/assets/img/no-image.webp')
  if (imagePath.startsWith('http')) return imagePath
  return `${baseUrl}${imagePath}`
}

const handleImageError = (e) => {
  e.target.src = require('@/assets/img/no-image.webp')
}

// Получение текста статуса
const getStatusText = (status) => {
  const statusMap = {
    'pending': 'Ожидает получения',
    'completed': 'Получен',
    'cancelled': 'Отменён'
  }
  return statusMap[status] || status
}

onMounted(async () => {
  try {
    isLoading.value = true
    const response = await axios.get('http://localhost:8000/api/auth/user/', {
      headers: {
        'Authorization': `Bearer ${authStore.accessToken}`,
        'Content-Type': 'application/json'
      },
      withCredentials: true
    })
    user.value = response.data
  } catch (error) {
    console.error('Ошибка загрузки профиля:', error)
    if (error.response?.status === 403) {
      alert('Сессия истекла. Пожалуйста, войдите снова.')
      authStore.logout()
    }
  } finally {
    isLoading.value = false
  }
})
</script>

<style scoped>
.profile-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 160px);
  padding: 20px;
  opacity: 0;
  transform: translateY(20px);
  animation: fadeIn 0.8s ease-out forwards;
}

.profile-card {
  width: 100%;
  max-width: 500px;
  padding: 30px;
  background: rgba(0, 0, 0, 0.23);
  border: 1px solid #737373;
  border-radius: 32px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  transition: all 0.3s ease;
  will-change: transform;
  backface-visibility: hidden;
  transform: translateZ(0);
  -webkit-font-smoothing: subpixel-antialiased;
}

.profile-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(222, 222, 222, 0.11);
}

/* Стили лоадера */
.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background: rgba(0, 0, 0, 0.5);
  z-index: 10;
  border-radius: 32px;
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

.spinner.small {
  width: 16px;
  height: 16px;
  border-width: 2px;
  margin-right: 8px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

h2 {
  text-align: center;
  font-family: 'Manrope', sans-serif;
  font-weight: 400;
  color: #dededecb;
  margin-bottom: 30px;
}

.profile-content {
  margin-bottom: 30px;
}

.profile-field {
  display: flex;
  justify-content: space-between;
  padding: 12px 0;
  border-bottom: 1px solid rgba(115, 115, 115, 0.3);
}

.profile-field:last-child {
  border-bottom: none;
}

.field-label {
  font-weight: 500;
  color: #dededecb;
  font-family: 'Manrope', sans-serif;
}

.field-value {
  color: #ffffff;
  font-family: 'Manrope', sans-serif;
}

.logout-btn {
  width: 100%;
  padding: 12px;
  background-color: #474747;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  transition: all 0.3s ease;
  margin-top: 20px;
}

.logout-btn:hover {
  background-color: #5a5a5a;
  transform: translateY(-1px);
}

.logout-btn:active {
  transform: translateY(0);
}

.btn-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
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

/* Адаптация для мобильных */
@media (max-width: 600px) {
  .profile-card {
    padding: 20px;
    border-radius: 24px;
  }
  
  .profile-field {
    flex-direction: column;
    gap: 5px;
  }
  
  .field-value {
    text-align: right;
  }
}

/* Стили модального окна */
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
  z-index: 100;
  animation: fadeIn 0.3s ease-out;
}

.confirm-modal {
  background: rgba(0, 0, 0, 0.8);
  border: 1px solid #737373;
  border-radius: 16px;
  padding: 25px;
  max-width: 400px;
  width: 90%;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

.confirm-modal h3 {
  color: #dededecb;
  margin-bottom: 15px;
  font-size: 1.3rem;
  text-align: center;
  font-family: 'Manrope', sans-serif;
}

.confirm-modal p {
  color: #cccccc;
  margin-bottom: 25px;
  text-align: center;
  font-family: 'Manrope', sans-serif;
}

.modal-buttons {
  display: flex;
  justify-content: center;
  gap: 15px;
}

.cancel-btn, .confirm-btn {
  padding: 10px 20px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s ease;
}

.cancel-btn {
  background-color: rgba(71, 71, 71, 0.5);
  border: 1px solid #737373;
  color: #dededecb;
}

.cancel-btn:hover {
  background-color: rgba(71, 71, 71, 0.8);
}

.confirm-btn {
  background-color: rgba(255, 77, 79, 0.3);
  border: 1px solid rgba(255, 77, 79, 0.5);
  color: white;
}

.confirm-btn:hover {
  background-color: rgba(255, 77, 79, 0.5);
}

/* Стили для секции заказов */
.orders-section {
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid rgba(115, 115, 115, 0.3);
}

.orders-section h3 {
  font-size: 20px;
  color: #dededecb;
  margin-bottom: 20px;
  font-family: 'Manrope', sans-serif;
  font-weight: 500;
}

.no-orders {
  text-align: center;
  color: #8d8d8d;
  padding: 20px;
  font-family: 'Manrope', sans-serif;
}

.orders-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.order-card {
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(115, 115, 115, 0.5);
  border-radius: 16px;
  padding: 15px;
  transition: all 0.3s ease;
}

.order-card:hover {
  border-color: rgba(222, 222, 222, 0.3);
  transform: translateY(-2px);
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid rgba(115, 115, 115, 0.3);
}

.order-info {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.order-code {
  font-weight: 500;
  color: #ffffff;
  font-size: 16px;
  font-family: 'Manrope', sans-serif;
}

.order-date {
  color: #8d8d8d;
  font-size: 14px;
  font-family: 'Manrope', sans-serif;
}

.order-status {
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 500;
  font-family: 'Manrope', sans-serif;
}

.order-status.pending {
  background: rgba(255, 193, 7, 0.2);
  color: #ffc107;
}

.order-status.completed {
  background: rgba(66, 185, 131, 0.2);
  color: #42b983;
}

.order-status.cancelled {
  background: rgba(255, 77, 79, 0.2);
  color: #ff4d4f;
}

.order-items {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.order-item {
  display: flex;
  gap: 15px;
  padding: 10px;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 12px;
}

.item-image {
  width: 80px;
  height: 80px;
  object-fit: cover;
  border-radius: 8px;
}

.item-details {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.item-name {
  color: #ffffff;
  font-weight: 500;
  font-family: 'Manrope', sans-serif;
}

.item-article {
  color: #8d8d8d;
  font-size: 14px;
  font-family: 'Manrope', sans-serif;
}

.item-price-qty {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: auto;
}

.item-quantity {
  color: #8d8d8d;
  font-family: 'Manrope', sans-serif;
}

.item-price {
  color: #ffffff;
  font-weight: 500;
  font-family: 'Manrope', sans-serif;
}

.order-footer {
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px solid rgba(115, 115, 115, 0.3);
  text-align: right;
}

.order-total {
  color: #ffffff;
  font-weight: 500;
  font-size: 18px;
  font-family: 'Manrope', sans-serif;
}

/* Адаптивность для мобильных устройств */
@media (max-width: 768px) {
  .order-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }

  .order-item {
    flex-direction: column;
  }

  .item-image {
    width: 100%;
    height: 200px;
  }

  .item-price-qty {
    flex-direction: column;
    align-items: flex-start;
    gap: 5px;
  }
}

/* Стили для вкладок */
.orders-tabs {
  display: flex;
    gap: 10px;
    margin-bottom: 20px;
    flex-wrap: wrap;
    justify-content: center;
}

.tab-button {
  padding: 8px 16px;
  border-radius: 20px;
  border: 1px solid #737373;
  background: rgba(0, 0, 0, 0.23);
  color: #dededecb;
  cursor: pointer;
  font-family: 'Manrope', sans-serif;
  font-size: 14px;
  transition: all 0.3s ease;
}

.tab-button:hover {
  transform: translateY(-1px);
}

/* Стили для активных вкладок */
.tab-button.active[data-tab="pending"] {
  background: rgba(255, 193, 7, 0.2);
  border-color: #ffc107;
  color: #ffc107;
}

.tab-button.active[data-tab="completed"] {
  background: rgba(66, 185, 131, 0.2);
  border-color: #42b983;
  color: #42b983;
}

.tab-button.active[data-tab="cancelled"] {
  background: rgba(255, 77, 79, 0.2);
  border-color: #ff4d4f;
  color: #ff4d4f;
}

/* Стили при наведении для неактивных вкладок */
.tab-button:not(.active):hover[data-tab="pending"] {
  background: rgba(255, 193, 7, 0.1);
  border-color: rgba(255, 193, 7, 0.5);
}

.tab-button:not(.active):hover[data-tab="completed"] {
  background: rgba(66, 185, 131, 0.1);
  border-color: rgba(66, 185, 131, 0.5);
}

.tab-button:not(.active):hover[data-tab="cancelled"] {
  background: rgba(255, 77, 79, 0.1);
  border-color: rgba(255, 77, 79, 0.5);
}

@media (max-width: 768px) {
  .orders-tabs {
    justify-content: center;
  }
  
  .tab-button {
    font-size: 13px;
    padding: 6px 12px;
  }
}

/* Обновляем стили для списка заказов */
.orders-list {
  opacity: 0;
  transform: translateY(10px);
  animation: slideIn 0.3s ease-out forwards;
}

@keyframes slideIn {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Стили для причины отмены */
.cancel-reason {
  margin: 15px 0;
  padding: 15px;
  background: rgba(255, 77, 79, 0.1);
  border: 1px solid rgba(255, 77, 79, 0.3);
  border-radius: 8px;
}

.cancel-reason h4 {
  color: #ff4d4f;
  margin-bottom: 8px;
  font-weight: 500;
  font-family: 'Manrope', sans-serif;
}

.cancel-reason p {
  color: #dededecb;
  font-family: 'Manrope', sans-serif;
  margin: 0;
  line-height: 1.5;
}

.profile-container h1,
.profile-container h2,
.profile-container h3 {
  color: #ffffff;
  font-family: 'Manrope', sans-serif;
}

.profile-section {
  background: rgba(0, 0, 0, 0.23);
  border: 1px solid #737373;
  border-radius: 16px;
  padding: 20px;
  margin-bottom: 20px;
}

.form-group label {
  color: #dededecb;
  margin-bottom: 8px;
  display: block;
  font-family: 'Manrope', sans-serif;
}

.form-input {
  width: 100%;
  padding: 12px;
  background: rgba(0, 0, 0, 0.23);
  border: 1px solid #737373;
  border-radius: 8px;
  color: #ffffff;
  font-size: 16px;
  font-family: 'Manrope', sans-serif;
}

.save-button {
  background: #474747;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  font-family: 'Manrope', sans-serif;
}
</style>