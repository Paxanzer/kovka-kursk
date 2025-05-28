<template>
  <Teleport to="body">
    <div v-if="show" class="notification-toast" :class="type">
      <div class="notification-content">
        {{ message }}
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  message: {
    type: String,
    required: true
  },
  duration: {
    type: Number,
    default: 5000
  },
  type: {
    type: String,
    default: 'info'
  }
})

const show = ref(false)

watch(() => props.message, (newMessage) => {
  if (newMessage) {
    show.value = true
    setTimeout(() => {
      show.value = false
    }, props.duration)
  }
})
</script>

<style scoped>
.notification-toast {
  position: fixed;
  top: 20px;
  right: 20px;
  padding: 15px 25px;
  border-radius: 8px;
  color: white;
  z-index: 9999;
  animation: slideIn 0.3s ease-out;
  max-width: 400px;
}

.notification-content {
  display: flex;
  align-items: center;
  gap: 10px;
}

.error {
  background-color: #dc3545;
}

.info {
  background-color: #17a2b8;
}

.warning {
  background-color: #ffc107;
  color: #000;
}

@keyframes slideIn {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}
</style> 