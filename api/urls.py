from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ProductViewSet, ProductCategoryViewSet, AuthViewSet, OrderViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'products', ProductViewSet)
router.register(r'categories', ProductCategoryViewSet)
router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'orders', OrderViewSet, basename='orders')

urlpatterns = [
    path('', include(router.urls)),
    path('api/auth/logout/', AuthViewSet.as_view({'post': 'logout'})),
    path('api/auth/user/', AuthViewSet.as_view({'get': 'user'})),  # Добавьте эту строку
]