<template>
  <div class="register-container" :class="{ 'fade-in': show }">
    <h2>Регистрация</h2>
    <form @submit.prevent="handleRegister">
      <div class="form-group">
        <input
          v-model="form.username"
          type="text"
          required
          placeholder="Введите логин"
          class="input-field"
        />
      </div>

      <div class="form-group">
        <input
          v-model="form.password"
          type="password"
          required
          placeholder="Введите пароль (минимум 8 символов)"
          class="input-field"
          @input="validatePassword"
        />
      </div>

      <div class="form-group">
        <input
          v-model="form.confirmPassword"
          type="password"
          required
          placeholder="Подтвердите пароль"
          class="input-field"
          @input="validatePassword"
        />
      </div>

      <div class="form-group">
        <input
          v-model="form.email"
          type="email"
          required
          placeholder="Введите email"
          class="input-field"
        />
      </div>

      <div class="form-group">
        <input
          v-model="form.phone"
          type="tel"
          placeholder="Введите телефон"
          class="input-field"
        />
      </div>

      <button type="submit" :disabled="loading || !isFormValid" class="submit-btn">
        <span v-if="loading" class="btn-content">
          <span class="spinner"></span>
          <span>Регистрация...</span>
        </span>
        <span v-else class="btn-content">Зарегистрироваться</span>
      </button>

      <transition name="fade">
        <div v-if="error" class="error-message">
          {{ error }}
        </div>
      </transition>

      <transition name="fade">
        <div v-if="passwordError" class="error-message">
          {{ passwordError }}
        </div>
      </transition>
    </form>
  </div>
</template>
  
  <script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/store/auth.js'

const authStore = useAuthStore()
const form = ref({
  username: '',
  password: '',
  confirmPassword: '',
  email: '',
  phone: ''
})

const loading = ref(false)
const error = ref(null)
const passwordError = ref('')
const show = ref(false)

onMounted(() => {
  setTimeout(() => {
    show.value = true
  }, 100)
})

const isFormValid = computed(() => {
  return (
    form.value.username &&
    form.value.password &&
    form.value.password.length >= 8 &&
    form.value.password === form.value.confirmPassword &&
    form.value.email &&
    !passwordError.value
  )
})

const validatePassword = () => {
  if (form.value.password.length < 8) {
    passwordError.value = 'Пароль должен содержать минимум 8 символов'
  } else if (form.value.password !== form.value.confirmPassword) {
    passwordError.value = 'Пароли не совпадают'
  } else {
    passwordError.value = ''
  }
}

const handleRegister = async () => {
  try {
    loading.value = true
    error.value = null
    await authStore.register(form.value)
  } catch (err) {
    error.value = err.response?.data || 'Ошибка регистрации'
  } finally {
    loading.value = false
  }
}
  </script>
  
  <style scoped>
.register-container {
  max-width: 223px;
  margin: 0 auto;
  padding: 1px 50px 40px;
  background: rgba(0, 0, 0, 0.23);
  border: 1px solid #737373;
  border-radius: 32px;
  margin-top: 40px;
  opacity: 0;
  transform: translateY(20px);
  transition: transform 0.5s ease-out, box-shadow 0.5s ease-out;
}

.register-container:hover {
  transform: scale(1.005) translateY(0);
  box-shadow: 0 8px 24px rgba(222, 222, 222, 0.11);
}

/* Анимации (те же, что и в Login) */
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

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Стили формы (аналогичные Login) */
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
  font-size: 14pxs;
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
  margin-top: 15px;
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
  </style>