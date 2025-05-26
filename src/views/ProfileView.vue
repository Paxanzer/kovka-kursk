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
        
        <div class="profile-field">
          <span class="field-label">Роль:</span>
          <span class="field-value">{{ user.role_display }}</span>
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
  import { ref, onMounted } from 'vue'
  import axios from 'axios'
  import { useAuthStore } from '@/store/auth.js'
  
  const authStore = useAuthStore()
  const user = ref(null)
  const isLoading = ref(false)
  const showLogoutConfirm = ref(false)

  const confirmLogout = () => {
  showLogoutConfirm.value = false
  authStore.logout()
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
  transition: transform 0.5s ease-out, box-shadow 0.5s ease-out;
}

.profile-card:hover {
  transform: scale(1.005);
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
</style>