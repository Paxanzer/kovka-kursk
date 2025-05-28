<template>
  <div class="login-container" :class="{ 'fade-in': show }">
    <transition name="fade">
      <div v-if="authStore.logoutMessage" class="logout-message">
        {{ authStore.logoutMessage }}
      </div>
    </transition>

    <h2>Вход в систему</h2>
    <form @submit.prevent="handleLogin">
      <div class="form-group">
        <input
          id="username"
          v-model="form.username"
          type="text"
          required
          placeholder="Введите имя пользователя"
          class="input-field"
        />
      </div>
      
      <div class="form-group">
        <input
          id="password"
          v-model="form.password"
          type="password"
          required
          placeholder="Введите пароль"
          class="input-field"
        />
      </div>
      
      <button type="submit" :disabled="loading" class="submit-btn">
        <span v-if="loading" class="btn-content">
          <span class="spinner"></span>
          <span>Вход...</span>
        </span>
        <span v-else class="btn-content">Войти</span>
      </button>
      
      <transition name="fade">
        <div v-if="error" class="error-message">
          {{ error }}
        </div>
      </transition>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue' // <-- 1. Импортируем onUnmounted
import { useAuthStore } from '@/store/auth.js'

const authStore = useAuthStore()
const form = ref({
  username: '',
  password: ''
})

const loading = ref(false)
const error = ref(null)
const show = ref(false)

onMounted(() => {
  setTimeout(() => {
    show.value = true
  }, 100)
})

// 2. ДОБАВЛЕН ХУК ЖИЗНЕННОГО ЦИКЛА ДЛЯ ОЧИСТКИ СООБЩЕНИЯ
// Он сработает, когда пользователь покинет страницу входа
onUnmounted(() => {
  if (authStore.logoutMessage) {
    authStore.clearLogoutMessage()
  }
})

const handleLogin = async () => {
  try {
    loading.value = true
    error.value = null
    await authStore.login(form.value)
  } catch (err) {
    error.value = 'Логин или пароль введен неправильно'
    setTimeout(() => {
      error.value = null
    }, 3000)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
/* Анимация появления */
.fade-in {
  animation: fadeIn 0.8s ease-out forwards;
}

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

/* Анимация ошибки */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.login-container {
  max-width: 223px;
  margin: 0 auto;
  padding: 1px 50px 40px;
  background: rgba(0, 0, 0, 0.23);
  border: 1px solid #737373;
  border-radius: 32px;
  margin-top: 67px;
  opacity: 0; /* Начальное состояние для анимации */
  transform: translateY(20px);
  transition: transform 0.5s ease-out, box-shadow 0.5s ease-out;
}

.login-container:hover {
  transform: scale(1.005) translateY(0);
  box-shadow: 0 8px 24px rgba(222, 222, 222, 0.11);
}

.form-group {
  margin-bottom: 15px;
}

h2 {
  text-align: center;
  font-family: 'Manrope', sans-serif;
  font-weight: 400;
  color: #dededecb;
  margin-bottom: 25px;
}

.input-field {
  width: 88.5%;
  padding: 12px;
  border: 1px solid #737373;
  border-radius: 8px;
  background: rgba(0, 0, 0, 0.23);
  color: #ccccccbf;
  margin-bottom: 15px;
  transition: all 0.3s ease;
  font-size: 14px;
}

.input-field:focus {
  outline: none;
  border-color: #474747;
  box-shadow: 0 0 0 2px rgba(177, 177, 177, 0.2);
}

.input-field:hover {
  border: 1px solid #ffffffc2;
}

.submit-btn {
  width: 100%;
  padding: 12px;
  background-color: #474747;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  transition: all 0.3s ease;
  margin-top: 10px;
}

.submit-btn:hover:not(:disabled) {
  background-color: #474747;
  transform: translateY(-1px);
}

.submit-btn:active:not(:disabled) {
  transform: translateY(0);
}

.submit-btn:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
  opacity: 0.7;
}

.btn-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.error-message {
  margin-top: 25px;
  color: #ff4d4f;
  text-align: center;
  font-size: 14px;
  padding: 8px;
  background: rgba(255, 77, 79, 0.1);
  border-radius: 4px;
  animation: shake 0.5s ease;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  20%, 60% { transform: translateX(-5px); }
  40%, 80% { transform: translateX(5px); }
}

/* 3. ДОБАВЛЕНЫ СТИЛИ ДЛЯ НОВОГО СООБЩЕНИЯ */
.logout-message {
  margin-bottom: 20px;
  color: #a6c5e4; /* приглушенный синий/белый цвет */
  text-align: center;
  font-size: 14px;
  padding: 12px;
  background: rgba(77, 137, 255, 0.1);
  border: 1px solid rgba(77, 137, 255, 0.2);
  border-radius: 8px;
}
</style>