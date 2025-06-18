<template>
  <div class="admin-container">
    <!-- Проверка прав администратора -->
    <div v-if="!authStore.isAdmin" class="access-denied">
      <h2>Доступ запрещен</h2>
      <p>У вас недостаточно прав для просмотра этой страницы</p>
      <p>Текущая роль: {{ authStore.userRole || 'не определена' }}</p>
    </div>

    <!-- Админ-панель -->
    <div v-else>
      <div class="tabs">
        <button
          v-for="tab in tabs"
          :key="tab"
          @click="currentTab = tab"
          :class="{ active: currentTab === tab }"
        >
          {{ tab }}
        </button>
      </div>

      <!-- Индикатор загрузки -->
      <div v-if="isLoading" class="loading-indicator">
        <div class="spinner"></div>
        <span>Загрузка данных...</span>
      </div>

      <!-- Контент вкладок -->
      <div class="tab-content">
        <!-- Пользователи -->
        <div v-if="currentTab === 'Пользователи'" class="users-section">
          <button @click="openUserModal(null)" class="add-button">
    + Добавить пользователя
  </button>
          
          <table class="data-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Имя</th>
                <th>Email</th>
                <th>Телефон</th>
                <th>Роль</th>
                <th>Действия</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="user in users" :key="user.id">
                <td>{{ user.id }}</td>
                <td>{{ user.username }}</td>
                <td>{{ user.email }}</td>
                <td>{{ user.phone }}</td>
                <td>{{ user.role }}</td>
                <td>
                  <button @click="openUserModal(user)" class="edit-btn">✏️</button>
                  <button @click="deleteUser(user.id)" class="delete-btn">🗑️</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Товары -->
        <div v-if="currentTab === 'Товары'" class="products-section">
          <button @click="openProductModal(null)" class="add-button">
            + Добавить товар
          </button>
          
          <table class="data-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Название</th>
                <th>Категория</th>
                <th>Цена</th>
                <th>Артикул</th>
                <th>Действия</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="product in products" :key="product.id">
                <td>{{ product.id }}</td>
                <td>{{ product.name }}</td>
                <td>{{ product.category ? product.category.name : 'Не указана' }}</td>
                <td>{{ product.price }} ₽</td>
                <td>{{ product.article }}</td>
                <td>
                  <button @click="openProductModal(product)" class="edit-btn">✏️</button>
                  <button @click="deleteProduct(product.id)" class="delete-btn">🗑️</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Категории -->
        <div v-if="currentTab === 'Категории'" class="categories-section">
          <button @click="openCategoryModal(null)" class="add-button">
            + Добавить категорию
          </button>
          
          <table class="data-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Название</th>
                <th>Действия</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="category in categories" :key="category.id">
                <td>{{ category.id }}</td>
                <td>{{ category.name }}</td>
                <td>
                  <button @click="openCategoryModal(category)" class="edit-btn">✏️</button>
                  <button @click="deleteCategory(category.id)" class="delete-btn">🗑️</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Модальные окна -->
      <Teleport to="body">
  <UserModal
    v-if="showUserModal"
    :user="selectedUser"
    @save="saveUser"
    @close="showUserModal = false"
  />
  
  <ProductModal
    v-if="showProductModal"
    :product="selectedProduct"
    :categories="categories"
    @save="saveProduct"
    @close="showProductModal = false"
  />
  
  <CategoryModal
    v-if="showCategoryModal"
    :category="selectedCategory"
    @save="saveCategory"
    @close="showCategoryModal = false"
  />
</Teleport>

      <!-- Сообщения об ошибках -->
      <div v-if="error" class="error-message">
        {{ error }}
        <button @click="error = null" class="close-error">×</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/store/auth'
import UserModal from '@/components/admin/UserModal.vue'
import ProductModal from '@/components/admin/ProductModal.vue'
import CategoryModal from '@/components/admin/CategoryModal.vue'

const authStore = useAuthStore()
const tabs = ['Пользователи', 'Товары', 'Категории']
const currentTab = ref('Пользователи')

// Данные
const users = ref([])
const products = ref([])
const categories = ref([])

// Состояние
const isLoading = ref(false)
const error = ref(null)

// Модальные окна
const showUserModal = ref(false)
const showProductModal = ref(false)
const showCategoryModal = ref(false)

const selectedUser = ref(null)
const selectedProduct = ref(null)
const selectedCategory = ref(null)



// Загрузка данных
const fetchData = async () => {
  try {
    isLoading.value = true
    error.value = null
    
    const api = authStore.getApiClient()
    
    const [usersRes, productsRes, categoriesRes] = await Promise.all([
      api.get('users/'),
      api.get('products/'),
      api.get('categories/')
    ])

    users.value = usersRes.data
    products.value = productsRes.data
    categories.value = categoriesRes.data

  } catch (err) {
    console.error('Ошибка загрузки данных:', err)
    error.value = err.response?.data?.message || 'Ошибка при загрузке данных'

    if (err.response?.status === 401) {
      authStore.logout()
    }
  } finally {
    isLoading.value = false
  }
}

// Методы для пользователей
const openUserModal = (user) => {
  selectedUser.value = user ? { ...user } : {
    username: '',
    email: '',
    phone: '',
    role: 'customer'
  }
  showUserModal.value = true
}

const saveUser = async (userData) => {
  try {
    const api = authStore.getApiClient();

    if (userData.id) {
      // РЕЖИM РЕДАКТИРОВАНИЯ (отправляем только роль)
      await api.patch(`users/${userData.id}/`, {
        role: userData.role
      });
    } else {
      // РЕЖИМ СОЗДАНИЯ (отправляем все данные для регистрации)
      await api.post('users/', userData);
    }

    await fetchData(); // Обновляем данные в таблице
    showUserModal.value = false; // Закрываем модальное окно
  } catch (err) {
    console.error('Ошибка сохранения пользователя:', err.response?.data);
    const errorData = err.response?.data;
    // Формируем более читаемое сообщение об ошибке
    let errorMessage = 'Ошибка при сохранении пользователя.';
    if (typeof errorData === 'object' && errorData !== null) {
      errorMessage = Object.entries(errorData)
        .map(([key, value]) => `${key}: ${Array.isArray(value) ? value.join(', ') : value}`)
        .join(' ');
    }
    error.value = errorMessage;
    // Окно не закрываем, чтобы пользователь видел ошибку
  }
};

const deleteUser = async (id) => {
  if (!confirm('Вы уверены, что хотите удалить этого пользователя?')) return
  
  try {
    const api = authStore.getApiClient()
    await api.delete(`users/${id}/`)
    await fetchData()
  } catch (err) {
    console.error('Ошибка удаления пользователя:', err)
    error.value = err.response?.data?.message || 'Ошибка при удалении пользователя'
  }
}

// Методы для товаров 1
const openProductModal = (product) => {
  selectedProduct.value = product ? { 
    ...product,
    category: product.category?.id || null
  } : {
    name: '',
    category: null,
    article: '',
    price: 0,
    specifications: '',
    description: '',
    image: null
  }
  showProductModal.value = true
}

const saveProduct = async (productData) => {
  try {
    const api = authStore.getApiClient()
    const formData = new FormData()
    
    // Обязательные поля
    formData.append('name', productData.name)
    formData.append('category_id', productData.category) // Исправлено на category_id
    formData.append('price', productData.price.toString())
    
    // Необязательные поля
    if (productData.article) formData.append('article', productData.article)
    if (productData.specifications) formData.append('specifications', productData.specifications)
    if (productData.description) formData.append('description', productData.description)
    
    // Изображение
    if (productData.image instanceof File) {
      formData.append('image', productData.image)
    }

    // Логирование данных перед отправкой
    for (let [key, value] of formData.entries()) {
      console.log(key, value)
    }

    const method = productData.id ? 'put' : 'post'
    const url = productData.id ? `products/${productData.id}/` : 'products/'
    
    const response = await api[method](url, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    
    await fetchData()
    showProductModal.value = false
    return response.data
  } catch (err) {
    console.error('Ошибка сохранения товара:', err.response?.data || err.message)
    error.value = err.response?.data || 'Ошибка при сохранении товара'
    throw err
  }
}

const deleteProduct = async (id) => {
  if (!confirm('Вы уверены, что хотите удалить этот товар?')) return
  
  try {
    const api = authStore.getApiClient()
    await api.delete(`products/${id}/`)
    await fetchData()
  } catch (err) {
    console.error('Ошибка удаления товара:', err)
    error.value = err.response?.data?.message || 'Ошибка при удалении товара'
  }
}

// Методы для категорий
const openCategoryModal = (category) => {
  selectedCategory.value = category ? { ...category } : {
    name: '',
    image: null
  }
  showCategoryModal.value = true
}

const saveCategory = async (categoryData) => {
  try {
    const api = authStore.getApiClient()
    const formData = new FormData()
    formData.append('name', categoryData.name)
    if (categoryData.image instanceof File) {
      formData.append('image', categoryData.image)
    }

    const method = categoryData.id ? 'put' : 'post'
    const url = categoryData.id ? `categories/${categoryData.id}/` : 'categories/'
    
    await api[method](url, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    
    await fetchData()
    showCategoryModal.value = false
  } catch (err) {
    console.error('Ошибка сохранения категории:', err)
    error.value = err.response?.data?.message || 'Ошибка при сохранении категории'
    throw err
  }
}

const deleteCategory = async (id) => {
  if (!confirm('Вы уверены, что хотите удалить эту категорию?')) return
  
  try {
    const api = authStore.getApiClient()
    await api.delete(`categories/${id}/`)
    await fetchData()
  } catch (err) {
    console.error('Ошибка удаления категории:', err)
    error.value = err.response?.data?.message || 'Ошибка при удалении категории'
  }
}

// Загрузка данных при монтировании и смене вкладки
onMounted(() => {
  if (authStore.isAdmin) {
    fetchData()
  }
})


</script>

<style scoped>
/* Основные стили контейнера */
.admin-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 30px;
  animation: fadeIn 0.8s ease-out forwards;
  opacity: 0;
  transform: translateY(20px);
}

@keyframes fadeIn {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Стили для сообщения "Доступ запрещен" */
.access-denied {
  text-align: center;
  padding: 50px;
  background: rgba(0, 0, 0, 0.23);
  border: 1px solid #737373;
  border-radius: 16px;
  color: #dededecb;
  margin-top: 50px;
  font-family: 'Manrope', sans-serif;
}

.access-denied h2 {
  color: #ff4d4f;
  margin-bottom: 15px;
}

/* Стили вкладок */
.tabs {
  display: flex;
  margin: 30px 0;
  border-bottom: 1px solid #737373;
  gap: 5px;
}

.tabs button {
  padding: 12px 25px;
  background: rgba(0, 0, 0, 0.23);
  border: 1px solid transparent;
  border-radius: 8px 8px 0 0;
  cursor: pointer;
  font-size: 14px;
  font-family: 'Manrope', sans-serif;
  color: #ccccccbf;
  transition: all 0.3s ease;
}

.tabs button:hover {
  background: rgba(71, 71, 71, 0.5);
}

.tabs button.active {
  background: rgba(71, 71, 71, 0.7);
  border-color: #737373;
  border-bottom-color: transparent;
  color: #dededecb;
  font-weight: 500;
}

/* Индикатор загрузки */
.loading-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 30px;
  color: #ccccccbf;
  font-family: 'Manrope', sans-serif;
}

.spinner {
  width: 20px;
  height: 20px;
  border: 3px solid rgba(222, 222, 222, 0.1);
  border-radius: 50%;
  border-top-color: #dededecb;
  animation: spin 1s ease-in-out infinite;
  margin-right: 10px;
}

/* Кнопки */
.add-button {
  background-color: #474747;
  color: #dededecb;
  border: none;
  padding: 12px 20px;
  border-radius: 8px;
  cursor: pointer;
  margin-bottom: 20px;
  font-family: 'Manrope', sans-serif;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
}

.add-button:hover {
  background-color: #5a5a5a;
  transform: translateY(-1px);
}

/* Таблицы */
.data-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  margin-bottom: 30px;
  background: rgba(0, 0, 0, 0.23);
  border: 1px solid #737373;
  border-radius: 8px;
  overflow: hidden;
}

.data-table th,
.data-table td {
  padding: 15px;
  text-align: left;
  border-bottom: 1px solid #737373;
  color: #ccccccbf;
  font-family: 'Manrope', sans-serif;
}

.data-table th {
  background: rgba(71, 71, 71, 0.5);
  font-weight: 500;
  color: #dededecb;
}

.data-table tr:last-child td {
  border-bottom: none;
}

.data-table tr:hover td {
  background: rgba(71, 71, 71, 0.2);
}

/* Кнопки действий */
.edit-btn, .delete-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 16px;
  padding: 8px;
  margin: 0 5px;
  transition: transform 0.2s ease;
}

.edit-btn {
  color: #42b983;
}

.delete-btn {
  color: #ff4d4f;
}

.edit-btn:hover, .delete-btn:hover {
  transform: scale(1.2);
}

/* Сообщения об ошибках */
.error-message {
  position: fixed;
  bottom: 30px;
  right: 30px;
  background: rgba(255, 77, 79, 0.2);
  color: #ff4d4f;
  padding: 15px 20px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  max-width: 400px;
  border: 1px solid #ff4d4f;
  font-family: 'Manrope', sans-serif;
  animation: fadeIn 0.3s ease-out, shake 0.5s ease;
}

.close-error {
  background: none;
  border: none;
  color: #ff4d4f;
  font-size: 20px;
  cursor: pointer;
  margin-left: 15px;
  opacity: 0.7;
  transition: opacity 0.2s ease;
}

.close-error:hover {
  opacity: 1;
}

/* Анимация встряски для ошибок */
@keyframes shake {
  0%, 100% { transform: translateX(0); }
  20%, 60% { transform: translateX(-5px); }
  40%, 80% { transform: translateX(5px); }
}

/* Адаптивность */
@media (max-width: 768px) {
  .admin-container {
    padding: 15px;
  }
  
  .tabs {
    flex-wrap: wrap;
  }
  
  .tabs button {
    padding: 10px 15px;
    font-size: 13px;
  }
  
  .data-table th,
  .data-table td {
    padding: 10px;
    font-size: 13px;
  }
}
</style>