<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal">
      <h2>{{ isEditMode ? 'Редактирование роли пользователя' : 'Добавить нового пользователя' }}</h2>
      
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label>Имя пользователя:</label>
          <input v-model="formData.username" :disabled="isEditMode" required>
        </div>
        
        <div class="form-group">
          <label>Email:</label>
          <input v-model="formData.email" type="email" :disabled="isEditMode" required>
        </div>
        
        <template v-if="!isEditMode">
          <div class="form-group">
            <label>Пароль:</label>
            <input v-model="formData.password" type="password" required @input="validatePassword">
          </div>
          <div class="form-group">
            <label>Подтвердите пароль:</label>
            <input v-model="formData.confirmPassword" type="password" required @input="validatePassword">
          </div>
        </template>
        
        <div class="form-group">
          <label>Телефон:</label>
          <input v-model="formData.phone" :disabled="isEditMode">
        </div>
        
        <div class="form-group">
          <label>Роль:</label>
          <select v-model="formData.role" required>
            <option value="admin">Администратор</option>
            <option value="customer">Покупатель</option>
          </select>
        </div>
        
        <div v-if="passwordError" class="error-message">{{ passwordError }}</div>

        <div class="form-actions">
          <button type="button" @click="$emit('close')">Отмена</button>
          <button type="submit" :disabled="!!passwordError">Сохранить</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue';
import { defineProps, defineEmits } from 'vue';

const props = defineProps({
  user: {
    type: Object,
    // Теперь не required, может быть null для создания
    default: null 
  }
});

const emit = defineEmits(['close', 'save']);

// Определяем режим работы
const isEditMode = computed(() => props.user && props.user.id);

const formData = ref({});
const passwordError = ref('');

// Эта функция-наблюдатель - "мозг" компонента.
// Она настраивает форму в нужный режим при открытии окна.
watch(() => props.user, (newUser) => {
  if (isEditMode.value) {
    // РЕЖИМ РЕДАКТИРОВАНИЯ: Копируем данные пользователя
    formData.value = { ...newUser };
  } else {
    // РЕЖИМ СОЗДАНИЯ: Сбрасываем форму до пустого состояния
    formData.value = {
      username: '',
      email: '',
      password: '',
      confirmPassword: '',
      phone: '',
      role: 'customer' // Роль по умолчанию
    };
  }
  passwordError.value = ''; // Сбрасываем ошибку пароля
}, { immediate: true, deep: true });


// Валидация пароля (взята из вашего RegisterView)
const validatePassword = () => {
  if (!isEditMode.value) { // Проверяем пароль только в режиме создания
    if (formData.value.password.length > 0 && formData.value.password.length < 8) {
      passwordError.value = 'Пароль должен содержать минимум 8 символов';
    } else if (formData.value.password !== formData.value.confirmPassword) {
      passwordError.value = 'Пароли не совпадают';
    } else {
      passwordError.value = '';
    }
  }
};

// Отправка данных
const handleSubmit = () => {
  validatePassword();
  if (passwordError.value) return;

  if (isEditMode.value) {
    emit('save', {
      id: props.user.id,
      role: formData.value.role
    });
  } else {
    // --- НАЧАЛО ИЗМЕНЕНИЙ ---

    // 1. Создаем копию всех данных формы
    const payload = { ...formData.value };

    // 2. Удаляем из копии ненужное поле подтверждения пароля
    delete payload.confirmPassword;

    // 3. Отправляем очищенный объект
    emit('save', payload);

    // --- КОНЕЦ ИЗМЕНЕНИЙ ---
  }
};
</script>

<style>
/* Здесь ваши стили для модального окна */
.error-message {
  color: #ff4d4f;
  font-size: 14px;
  margin-bottom: 1rem;
  text-align: center;
}
/* ...остальные стили... */
</style>
  
<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  backdrop-filter: blur(5px);
  animation: fadeIn 0.3s ease-out forwards;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.modal {
  background: rgba(30, 30, 30, 0.95);
  padding: 30px;
  border-radius: 16px;
  width: 500px;
  max-width: 90%;
  border: 1px solid #4a4a4a;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  animation: modalSlideIn 0.4s cubic-bezier(0.22, 1, 0.36, 1) forwards;
  transform: translateY(20px);
  opacity: 0;
}

@keyframes modalSlideIn {
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
}

h2 {
  margin: 0;
  color: #e0e0e0;
  font-family: 'Manrope', sans-serif;
  font-weight: 500;
  font-size: 1.5rem;
}

.close-btn {
  background: none;
  border: none;
  color: #a0a0a0;
  font-size: 1.5rem;
  cursor: pointer;
  transition: color 0.2s;
}

.close-btn:hover {
  color: #e0e0e0;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 8px;
  color: #b0b0b0;
  font-family: 'Manrope', sans-serif;
  font-size: 0.9rem;
}

input, 
select,
textarea {
  width: 93%;
  padding: 12px 15px;
  background: rgba(50, 50, 50, 0.5);
  border: 1px solid #4a4a4a;
  border-radius: 8px;
  color: #e0e0e0;
  font-family: 'Manrope', sans-serif;
  transition: all 0.3s ease;
}

input:focus,
select:focus,
textarea:focus {
  outline: none;
  border-color: #636363;
  box-shadow: 0 0 0 2px rgba(100, 100, 100, 0.2);
}

textarea {
  min-height: 100px;
  resize: vertical;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 30px;
}

button {
  padding: 12px 24px;
  border-radius: 8px;
  font-family: 'Manrope', sans-serif;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.cancel-btn {
  background: rgba(70, 70, 70, 0.5);
  border: 1px solid #5a5a5a;
  color: #d0d0d0;
}

.cancel-btn:hover {
  background: rgba(90, 90, 90, 0.5);
  transform: translateY(-1px);
}

.submit-btn {
  background: #474747;
  border: 1px solid #5a5a5a;
  color: #f0f0f0;
}

.submit-btn:hover {
  background: #5a5a5a;
  transform: translateY(-1px);
}

.image-preview {
  max-width: 100%;
  max-height: 200px;
  margin-top: 15px;
  border-radius: 8px;
  border: 1px solid #4a4a4a;
}

.file-input {
  padding: 10px;
  background: rgba(50, 50, 50, 0.5);
  border-radius: 8px;
  margin-top: 5px;
}

/* Анимация ошибки */
.error-message {
  color: #ff6b6b;
  font-size: 0.85rem;
  margin-top: 5px;
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-5px); }
  to { opacity: 1; transform: translateY(0); }
}

@media (max-width: 600px) {
  .modal {
    padding: 20px;
  }
  
  .form-actions {
    flex-direction: column-reverse;
    gap: 10px;
  }
  
  button {
    width: 100%;
  }
}
</style>