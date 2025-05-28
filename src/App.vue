<template>
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  
  <body>
    
    

    <div class="body3"> 
      <div class="navbar">
        <img 
            class="catalog_img"
            src="@/assets/catalog.png" 
            alt="Каталог"
          >
          <router-link class="nav-link home-link" to="/">Главная</router-link>
      <router-link class="nav-link catalog-link" to="/catalog">Каталог</router-link>
        <div class="search_fr">
          <div class="search_button">
            <p class="search_Btxt">поиск</p>
          </div>
          <input 
    class="search_input1" 
    placeholder="поиск" 
    type="text"
    v-model="searchQuery"
    @focus="redirectToSearch"
    @keyup.enter="performSearch"
  >
        </div>

        <div class="catalog-container">
          

          <nav>
        <router-link class="nav-link register-button" v-if="!authStore.isAuthenticated" to="/register">Регистрация</router-link>
        <router-link class="nav-link login-button" v-if="!authStore.isAuthenticated" to="/login">Войти</router-link>
        
        <router-link class="nav-link admin-button"
      v-if="authStore.isAuthenticated && authStore.isAdmin" 
      to="/admin-panel"
    >
      Админ-панель
    </router-link>
    <router-link class="nav-link admin-button"
      v-if="authStore.isAuthenticated && authStore.isAdmin" 
      to="/admin/orders"
    > Заказы </router-link>
      
      <router-link class="nav-link profile-link" v-if="authStore.isAuthenticated" to="/profile">Профиль</router-link>
      
      <!-- Добавляем кнопку корзины -->
      <router-link 
        v-if="authStore.isAuthenticated" 
        to="/cart" 
        class="nav-link cart-button"
      >
        <div class="cart-icon-wrapper">
          <svg 
            class="cart-icon" 
            viewBox="0 0 24 24" 
            fill="none" 
            stroke="currentColor" 
            stroke-width="2"
          >
            <path d="M9 22a1 1 0 100-2 1 1 0 000 2zM20 22a1 1 0 100-2 1 1 0 000 2z" />
            <path d="M1 1h4l2.68 13.39a2 2 0 002 1.61h9.72a2 2 0 002-1.61L23 6H6" />
          </svg>
          <span v-if="cartItemsCount > 0" class="cart-counter">
            {{ cartItemsCount }}
          </span>
        </div>
        <span class="cart-text">Корзина</span>
      </router-link>
    </nav>

         


        </div>
      </div>
    </div>

    <router-view></router-view>
    
  </body>
</template>
<script>
import { computed, ref, watch } from 'vue'
import { useAuthStore } from '@/store/auth.js'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'

export default {
  name: 'App',
  setup() {
    const router = useRouter()
    const store = useStore()
    const searchQuery = ref('')
    const authStore = useAuthStore()

    const isAuthenticated = computed(() => {
      return !!localStorage.getItem('access_token')
    })

    // Добавляем вычисляемое свойство для количества товаров в корзине
    const cartItemsCount = computed(() => {
      return store.getters['cart/itemCount']
    })

    const redirectToSearch = () => {
      router.push('/catalogs')
    }
    
    const performSearch = () => {
      if (searchQuery.value.trim()) {
        router.push({ path: '/catalogs', query: { q: searchQuery.value } })
        searchQuery.value = ''
      }
    }

    watch(searchQuery, (newVal) => {
      if (newVal.trim()) {
        router.push({ path: '/catalogs', query: { q: newVal } })
      }
    })

    return {
      isAuthenticated,
      authStore,
      searchQuery,
      redirectToSearch,
      performSearch,
      cartItemsCount
    }
  }
}
</script>
<style>

/* Стили для навигационных кнопок */
/* Общие стили для всех ссылок навигации */
.nav-link {
  text-decoration: none;
  color: #dededecb;
  transition: all 0.3s ease;
  font-family: 'Manrope', sans-serif;
  font-size: 16px;
  padding: 0 16px;
  border-radius: 20px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  white-space: nowrap;
  height: 100%;
  box-sizing: border-box;
}

/* Кнопка регистрации */
.register-button {
  background-color: rgba(71, 71, 71, 0.5);
  border: 1px solid #737373;
}

.register-button:hover {
  background-color: rgba(71, 71, 71, 0.8);
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(222, 222, 222, 0.1);
}

/* Кнопка регистрации */
.admin-button {
  background-color: rgb(147 53 53 / 50%);
  border: 1px solid #f16666;
  margin: 0 5px;
  min-height: 40px;
}

.admin-button:hover {
  background-color: rgba(218, 74, 74, 0.5);
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(255, 0, 0, 0.1);
}


/* Кнопка входа */
.login-button {
  background-color: rgba(66, 185, 131, 0.3);
  border: 1px solid rgba(66, 185, 131, 0.5);
}

.login-button:hover {
  background-color: rgba(66, 185, 131, 0.5);
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(66, 185, 131, 0.2);
}

/* Ссылка профиля */
.profile-link {
  background-color: rgba(0, 0, 0, 0.23);
  border: 1px solid #737373;
  margin: 0 5px;
  min-height: 40px;
}

.profile-link:hover {
  background-color: rgba(71, 71, 71, 0.5);
  transform: translateY(-1px);
}

/* Основные навигационные ссылки */
.home-link,
.about-link,
.catalog-link {
  position: relative;
  padding: 8px 0;
  margin: 0 15px;
  border: none;
  background: none;
}

.home-link::after,
.about-link::after,
.catalog-link::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 1px;
  background-color: #dededecb;
  transition: width 0.3s ease;
}

.home-link:hover::after,
.about-link:hover::after,
.catalog-link:hover::after {
  width: 100%;
}

/* Активное состояние */
.router-link-active {
  color: #ffffffe8;
}

.home-link.router-link-active::after,
.about-link.router-link-active::after,
.catalog-link.router-link-active::after {
  width: 100%;
  background-color: #ffffffd7;
}



/* Адаптация для мобильных */
@media (max-width: 768px) {
  .nav-link {
    font-size: 14px;
    padding: 0 12px;
    margin: 2px;
    min-height: 36px; /* Немного меньше на мобильных */
  }
  
  .register-button,
  .login-button {
    display: block;
    width: 100%;
    margin: 5px 0;
    text-align: center;
  }

  .admin-button,
  .cart-button,
  .profile-link {
    min-height: 36px;
  }
}

.body3 {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 0;
    width: 100%; /* Занимает всю доступную ширину */
    background: #1C1A1C;
    box-sizing: border-box; /* Важно, чтобы padding не ломал ширину */
}
body {
  background: #1C1A1C;
}
.navbar {
    width: 100%; /* Занимает всю ширину контейнера body3 */
    height: auto; /* Автоматическая высота */
    min-height: 77px; /* Минимальная высота, как у вас было */
    border-bottom: 1px solid rgba(189, 189, 189, 0.32);
    display: flex;
    justify-content: space-between; /* Размещает элементы по краям */
    align-items: center; /* Вертикальное выравнивание */
    padding: 10px 20px; /* Отступы слева и справа */
    box-sizing: border-box;
    flex-wrap: wrap; /* Позволяет элементам переноситься на новую строку */
}

.search_fr {
    position: relative;
    width: auto; /* Автоматическая ширина, чтобы не вылезать */
    max-width: 571px; /* Максимальная ширина, как у вас было */
    height: 40px;
    /*left: 459px;  Удалено, позиционирование обрабатывается flexbox */
    /*top: 19px;  Удалено, позиционирование обрабатывается flexbox */
    flex-grow: 1; /* Занимает доступное пространство */
    margin-right: 10px; /* Небольшой отступ справа */

}

.search_input1 {
    box-sizing: border-box;
    width: 100%; /* Занимает всю ширину контейнера search_fr */
    height: 40px;
    background: #1C1A1C;
    border: 2px solid #737373;
    border-radius: 6px;
    color: #DEDEDE;
    font-size: 16px; /* Меньше на мобильных */
    font-family: 'Manrope', sans-serif;
    padding: 8px 12px;
    outline: none;
    transition: border-color 0.3s ease;
    position: relative; /* Убираем absolute */
    margin-left: 20px;
}

.search_input1::placeholder {
    color: #737373;
    opacity: 1;
}

.search_input1:focus {
    border-color: #dededeb2;
}

.search_input1:hover {
    border-color: #dededeb2;
}

.search_button {
    box-sizing: border-box;
    position: absolute; /* Оставляем absolute */
    width: 104px;
    height: 40px;
    right: 0; /* Прижимаем к правому краю search_fr */
    top: 0;
    background: #737373;
    border: 1px solid #737373;
    border-radius: 7px;
    cursor: pointer;
}

.search_Btxt {
    position: absolute;
    width: auto; /* Автоматическая ширина */
    height: 25px;
    left: 21px;
    top: 4px;
    font-family: 'Manrope', sans-serif;
    font-style: normal;
    font-weight: 700;
    font-size: 16px; /* Меньше на мобильных */
    line-height: 20px;
    color: #1C1A1C;
    cursor: pointer;
    margin: 0;
    white-space: nowrap; /* Предотвращает перенос текста */
}


.catalog-container {
    display: flex; /* Используем flexbox для выравнивания */
    align-items: center; /* Вертикальное выравнивание по центру */
    position: relative; /* Для позиционирования текста */
    margin-left: auto; /* Прижимаем к правому краю, если search_fr не занимает все место */
}

.catalog_img {
    width: 30px;
    height: 30px;
    opacity: 0.4;
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.2sease;
    margin-right: 24px;
    position: relative;
}

.catalog_img:hover {
    opacity: 0.75;
}

.catalog_txt {
    position: relative;
    width: auto; /* Автоматическая ширина */
    height: auto; /* Автоматическая высота */
    /*left: 370px; Удалено, позиционирование обрабатывается flexbox */
    /*top: 20px; Удалено, позиционирование обрабатывается flexbox */
    font-family: 'Manrope', sans-serif;
    font-style: normal;
    font-weight: 400;
    font-size: 14px; /* Меньше на мобильных */
    line-height: 20px;
    color: #FFFFFF;
    opacity: 1; /* Всегда виден */
    transform: translateX(0); /* Без сдвига */
    transition: none; /* Без анимации */
    margin: 0;
    white-space: nowrap; /* Предотвращает перенос текста */
}

/* Медиа-запрос для небольших экранов (например, мобильных) */
@media (max-width: 768px) {
    .search_fr {
        max-width: 100%; /* Занимает всю ширину на мобильных */
        margin-bottom: 10px; /* Отступ снизу */
    }

    .search_button {
        position: absolute; /* Оставляем absolute */
        width: 80px;
        height: 30px;
        right: 0; /* Прижимаем к правому краю search_fr */
        top: 5px;
    }
    .search_Btxt {
        font-size: 12px;
        left: auto;
        right: 5px;
    }
    .catalog-container {
        margin-left: 0; /* Убираем отступ, чтобы был слева */
    }

    .catalog_txt {
        font-size: 12px;
    }
}

/* Стили для кнопки корзины */
.cart-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  background-color: rgba(71, 71, 71, 0.5);
  border: 1px solid #737373;
  margin: 0 5px;
  min-height: 40px;
}

.cart-button:hover {
  background-color: rgba(71, 71, 71, 0.8);
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(222, 222, 222, 0.1);
}

.cart-icon-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.cart-icon {
  width: 24px;
  height: 24px;
  opacity: 0.8;
}

.cart-counter {
  position: absolute;
  top: -8px;
  right: -8px;
  background: #e53e3e;
  color: white;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  font-size: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  border: 2px solid #1C1A1C;
}

.cart-text {
  font-size: 16px;
  font-weight: 500;
}

/* Адаптивность для мобильных устройств */
@media (max-width: 768px) {
  .cart-button {
    padding: 6px 12px;
  }

  .cart-icon {
    width: 20px;
    height: 20px;
  }

  .cart-counter {
    width: 18px;
    height: 18px;
    font-size: 11px;
  }

  .cart-text {
    font-size: 14px;
  }
}

nav {
    display: flex;
    align-items: stretch; /* Растягиваем элементы по высоте */
    gap: 10px;
    margin-left: auto;
    height: 40px; /* Фиксированная высота для навигации */
}

@media (max-width: 768px) {
    nav {
        height: auto;
        justify-content: center;
        flex-wrap: wrap;
        gap: 5px;
    }
}

</style>
