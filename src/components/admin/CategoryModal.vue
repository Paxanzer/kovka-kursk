<template>
    <div class="modal-overlay">
      <div class="modal">
        <h2>{{ category.id ? 'Редактировать категорию' : 'Добавить категорию' }}</h2>
        
        <form @submit.prevent="handleSubmit">
          <div class="form-group">
            <label>Название:</label>
            <input v-model="formData.name" required>
          </div>
          
          <div class="form-group">
            <label>Изображе=ние:</label>
            <input type="file" @change="handleImageUpload">
            <img v-if="formData.image && typeof formData.image === 'string'" :src="formData.image" class="preview-image">
          </div>
          
          <div class="form-actions">
            <button type="button" @click="$emit('close')">Отмена</button>
            <button type="submit">Сохранить</button>
          </div>
        </form>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, watch } from 'vue'
  import { defineProps, defineEmits } from 'vue'
  
  const props = defineProps({
    category: {
      type: Object,
      required: true
    }
  })
  
  const emit = defineEmits(['close', 'save'])
  
  const formData = ref({
    name: '',
    image: null
  })
  
  watch(() => props.category, (newVal) => {
    formData.value = { ...newVal }
  }, { immediate: true })
  
  const handleImageUpload = (e) => {
    formData.value.image = e.target.files[0]
  }
  
  const handleSubmit = () => {
    emit('save', formData.value)
  }
  </script>
  
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