import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AboutView from '../views/AboutView.vue'


import CatalogView from '../components/CatalogView.vue'
import LoginView from '../views/LoginView.vue' // Создайте этот компонент
import RegisterView from '../views/RegisterView.vue' // Создайте этот компонент

import { useAuthStore } from '@/store/auth'
import SearchVue from '../components/SearchView.vue' // Компонент для ошибки доступа


const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
    meta: { title: 'Главная' }
  },
  {
    path: '/catalog',
    name: 'categories2',
    component: AboutView,
    meta: { title: 'Каталог' }
  },
  {
    path: '/about',
    name: 'categories',
    component: AboutView,
    meta: { title: 'Каталог' }
  },
  {
    path: '/product/:productId',
    name: 'ProductDetail',
    component: () => import('../views/DetailView.vue')
  },
  {
  path: '/catalogs',
  name: 'catalogs',
  component: SearchVue,
  props: route => ({ query: route.query.q })
},
  {
    path: '/catalog/:categoryId',
    name: 'catalog',
    component: CatalogView,
    props: true,
    meta: { title: 'Категория'}
  },
  {
    path: '/profile',
  name: 'profile',
  component: () => import('../views/ProfileView.vue'),
  meta: { 
    title: 'Профиль',
    requiresAuth: true 
  }
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    meta: { 
      title: 'Вход',
      hideForAuth: true 
    }
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterView,
    meta: { 
      title: 'Регистрация',
      hideForAuth: true 
    }
  },
  {
    path: '/admin-panel',
    name: 'admin-panel',
    component: () => import('../views/AdminPanelView.vue'),
    meta: { 
      title: 'Админ-панель',
      requiresAuth: true,
      requiresAdmin: true
    }
  },
  {
    path: '/cart',
    name: 'cart',
    component: () => import('../components/CartView.vue')
  },
  {
    path: '/orders',
    name: 'orders',
    component: () => import('../views/OrdersView.vue')
  },
  {
    path: '/admin/orders',
    name: 'admin-orders',
    component: () => import('../views/AdminOrdersView.vue'),
    meta: { 
      title: 'Управление заказами',
      requiresAuth: true,
      requiresAdmin: true
    }
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  const isAuthenticated = authStore.isAuthenticated
  
  // Если маршрут требует авторизации, а пользователь не авторизован
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!isAuthenticated) {
      next('/login')
      return
    }
    
    // Если требуется админ, но пользователь не админ
    if (to.matched.some(record => record.meta.requiresAdmin)) {
      if (!authStore.isAdmin) {
        next('/')
        return
      }
    }
  }
  
  // Если маршрут скрыт для авторизованных, а пользователь авторизован
  if (to.matched.some(record => record.meta.hideForAuth) && isAuthenticated) {
    next('/profile')
    return
  }
  
  next()
})

export default router