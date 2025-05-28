<template>
  <div class="cart-container">
    <h2>Корзина</h2>
    
    <!-- Список товаров -->
    <div v-if="cartItems.length > 0" class="cart-items">
      <div v-for="item in cartItems" :key="item.id" class="cart-item">
        <img :src="getImageUrl(item.image)" :alt="item.name" class="item-image">
        <div class="item-details">
          <h3>{{ item.name }}</h3>
          <p class="item-price">{{ item.price }} ₽</p>
          <div class="quantity-controls">
            <button @click="decreaseQuantity(item)">-</button>
            <span>{{ item.quantity }}</span>
            <button @click="increaseQuantity(item)">+</button>
          </div>
        </div>
        <button class="remove-item" @click="removeItem(item)">×</button>
      </div>
      
      <div class="cart-summary">
        <div class="total">
          <span>Итого:</span>
          <span>{{ totalPrice }} ₽</span>
        </div>
        <button class="checkout-button" @click="createOrder">
          Оформить заказ
        </button>
      </div>
    </div>
    
    <!-- Пустая корзина -->
    <div v-else class="empty-cart">
      <p>Ваша корзина пуста</p>
      <router-link to="/catalog" class="continue-shopping">
        Перейти к покупкам
      </router-link>
    </div>

    <!-- Модальное окно с кодом заказа -->
    <div v-if="showOrderCode" class="order-modal">
      <div class="order-modal-content">
        <h3>Ваш заказ успешно создан!</h3>
        <div class="order-code">
          <p>Код для получения заказа:</p>
          <span class="code">{{ orderCode }}</span>
        </div>
        <p class="order-info">
          Покажите этот код при получении заказа в нашей точке выдачи.
          Оплата производится при получении.
        </p>
        <button @click="closeOrderModal" class="close-button">Закрыть</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useStore } from 'vuex'
import axios from 'axios'

const store = useStore()
const showOrderCode = ref(false)
const orderCode = ref('')
const baseUrl = 'http://localhost:8000'

const cartItems = computed(() => store.state.cart.items)
const totalPrice = computed(() => store.getters['cart/totalPrice'])

const getImageUrl = (imagePath) => {
  if (!imagePath) return require('@/assets/img/no-image.webp')
  if (imagePath.startsWith('http')) return imagePath
  return `${baseUrl}${imagePath}`
}

const increaseQuantity = (item) => {
  store.commit('cart/updateItemQuantity', {
    id: item.id,
    quantity: item.quantity + 1
  })
}

const decreaseQuantity = (item) => {
  if (item.quantity > 1) {
    store.commit('cart/updateItemQuantity', {
      id: item.id,
      quantity: item.quantity - 1
    })
  }
}

const removeItem = (item) => {
  store.commit('cart/removeItem', item.id)
}

const createOrder = async () => {
  try {
    const response = await axios.post(`${baseUrl}/api/orders/`, {
      items: cartItems.value.map(item => ({
        product_id: item.id,
        quantity: item.quantity
      }))
    })
    
    orderCode.value = response.data.code
    showOrderCode.value = true
    store.commit('cart/clearCart')
  } catch (error) {
    console.error('Error creating order:', error)
    // Здесь можно добавить обработку ошибок
  }
}

const closeOrderModal = () => {
  showOrderCode.value = false
  orderCode.value = ''
}
</script>

<style scoped>
.cart-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.cart-container h2 {
  color: #ffffff;
  margin-bottom: 30px;
  font-family: 'Manrope', sans-serif;
}

.cart-items {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.cart-item {
  display: flex;
  align-items: center;
  padding: 20px;
  background: rgba(0, 0, 0, 0.23);
  border: 1px solid #737373;
  border-radius: 16px;
  gap: 20px;
}

.item-image {
  width: 100px;
  height: 100px;
  object-fit: cover;
  border-radius: 8px;
}

.item-details {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.item-details h3 {
  margin: 0;
  color: #ffffff;
  font-family: 'Manrope', sans-serif;
}

.item-price {
  color: #dededecb;
  font-weight: bold;
  margin: 0;
  font-family: 'Manrope', sans-serif;
}

.quantity-controls {
  display: flex;
  align-items: center;
  gap: 10px;
}

.quantity-controls button {
  background: #474747;
  border: none;
  color: white;
  width: 30px;
  height: 30px;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.3s;
}

.quantity-controls button:hover {
  background: #5a5a5a;
}

.quantity-controls span {
  color: #dededecb;
  min-width: 30px;
  text-align: center;
  font-family: 'Manrope', sans-serif;
}

.remove-item {
  background: none;
  border: none;
  color: #8d8d8d;
  font-size: 24px;
  cursor: pointer;
  padding: 0 10px;
  transition: color 0.3s;
}

.remove-item:hover {
  color: #ff5252;
}

.cart-summary {
  margin-top: 30px;
  padding: 20px;
  background: rgba(0, 0, 0, 0.23);
  border: 1px solid #737373;
  border-radius: 16px;
}

.total {
  display: flex;
  justify-content: space-between;
  color: #ffffff;
  font-size: 20px;
  margin-bottom: 20px;
  font-family: 'Manrope', sans-serif;
}

.checkout-button {
  width: 100%;
  padding: 15px;
  background: #474747;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s;
  font-family: 'Manrope', sans-serif;
}

.checkout-button:hover {
  background: #5a5a5a;
  transform: translateY(-1px);
}

.empty-cart {
  text-align: center;
  color: #dededecb;
  padding: 40px;
  font-family: 'Manrope', sans-serif;
}

.continue-shopping {
  display: inline-block;
  margin-top: 20px;
  padding: 10px 20px;
  background: #474747;
  color: white;
  text-decoration: none;
  border-radius: 8px;
  transition: background 0.3s;
  font-family: 'Manrope', sans-serif;
}

.continue-shopping:hover {
  background: #5a5a5a;
}

/* Стили для модального окна */
.order-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.order-modal-content {
  background: #1a1a1a;
  padding: 30px;
  border-radius: 16px;
  max-width: 400px;
  width: 90%;
  text-align: center;
  border: 1px solid #737373;
}

.order-modal-content h3 {
  color: #ffffff;
  margin-bottom: 20px;
  font-family: 'Manrope', sans-serif;
}

.order-code {
  margin: 20px 0;
}

.code {
  display: block;
  font-size: 32px;
  font-weight: bold;
  color: #ffffff;
  padding: 20px;
  background: rgba(71, 71, 71, 0.3);
  border-radius: 8px;
  margin: 10px 0;
  font-family: 'Manrope', sans-serif;
}

.order-info {
  color: #dededecb;
  margin: 20px 0;
  line-height: 1.5;
  font-family: 'Manrope', sans-serif;
}

.close-button {
  padding: 10px 20px;
  background: #474747;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.3s;
  font-family: 'Manrope', sans-serif;
}

.close-button:hover {
  background: #5a5a5a;
}

@media (max-width: 768px) {
  .cart-item {
    flex-direction: column;
    text-align: center;
  }

  .item-image {
    width: 150px;
    height: 150px;
  }

  .quantity-controls {
    justify-content: center;
  }

  .remove-item {
    align-self: flex-end;
  }
}

.order-id {
  font-family: 'Manrope', sans-serif;
}
</style> 