from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import User, Product, ProductCategory, Order
from .serializers import (
    UserSerializer, ProductSerializer, ProductCategorySerializer, 
    ProductImage, UserRegisterSerializer, UserLoginSerializer,
    OrderSerializer, CreateOrderSerializer, UserProfileSerializer
)
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class AuthViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': serializer.data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'role': user.role
                })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
    @action(detail=False, methods=['post'])
    def logout(self, request):
        # Здесь можно добавить логику недействительности токена
        return Response({"detail": "Successfully logged out."})
    

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def user(self, request):
        """Получение данных профиля пользователя со всеми заказами"""
        user = request.user
        if not user.is_authenticated:
            return Response({'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        if self.action in ['create']:
            permission_classes = []
        else:
            permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_classes]
    
    def create(self, request, *args, **kwargs):
        """Создание нового пользователя (доступно без авторизации)"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def update(self, request, *args, **kwargs):
        """Полное обновление пользователя (требует админских прав)"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        """Удаление пользователя (требует админских прав)"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)



class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    parser_classes = (MultiPartParser, FormParser)
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def create(self, request, *args, **kwargs):
        """Создание новой категории (требует авторизации)"""
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        """Обновление категории (требует авторизации)"""
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """Удаление категории (требует авторизации)"""
        return super().destroy(request, *args, **kwargs)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    parser_classes = (MultiPartParser, FormParser)
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = []
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def create(self, request, *args, **kwargs):
        """Создание нового товара (требует авторизации)"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def update(self, request, *args, **kwargs):
        """Обновление товара (требует авторизации)"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    def partial_update(self, request, *args, **kwargs):
        """Частичное обновление товара (требует авторизации)"""
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """Удаление товара (требует авторизации)"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def perform_create(self, serializer):
        product = serializer.save()
        images_data = self.request.FILES.getlist('images')
        for image_data in images_data:
            ProductImage.objects.create(product=product, image=image_data)

    @action(detail=True, methods=['delete'], url_path='delete-image')
    def delete_image(self, request, pk=None):
        product = self.get_object()
        if not product.image:
            return Response({'detail': 'No image to delete'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Удаляем файл изображения
        file_path = product.image.path
        if default_storage.exists(file_path):
            default_storage.delete(file_path)
        
        # Обновляем поле изображения в модели
        product.image.delete(save=True)
        
        return Response({'detail': 'Image deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'code'
    lookup_url_kwarg = 'pk'

    def get_queryset(self):
        """
        Возвращает заказы текущего пользователя.
        Для администраторов возвращает все заказы.
        """
        user = self.request.user
        if user.is_staff:
            return Order.objects.all().prefetch_related('items', 'items__product', 'user')
        return Order.objects.filter(user=user).prefetch_related('items', 'items__product', 'user')

    def get_serializer_class(self):
        """Использует разные сериализаторы для создания и получения заказов"""
        if self.action == 'create':
            return CreateOrderSerializer
        return OrderSerializer

    @action(detail=False, methods=['get'], url_path='search/(?P<code>[^/.]+)')
    def search_by_code(self, request, code=None):
        """
        Поиск заказа по коду.
        Только для администраторов.
        """
        if not request.user.is_staff:
            return Response(
                {"detail": "У вас нет прав для выполнения этого действия."},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            order = Order.objects.select_related('user').prefetch_related('items', 'items__product').get(code=code)
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        except Order.DoesNotExist:
            return Response(
                {"detail": "Заказ с таким кодом не найден."},
                status=status.HTTP_404_NOT_FOUND
            )

    def partial_update(self, request, *args, **kwargs):
        """
        Частичное обновление заказа (PATCH).
        Только для администраторов.
        """
        if not request.user.is_staff:
            return Response(
                {"detail": "У вас нет прав для выполнения этого действия."},
                status=status.HTTP_403_FORBIDDEN
            )

        instance = self.get_object()
        
        # Проверяем, что обновляются только разрешенные поля
        allowed_fields = {'status', 'cancel_reason'}
        if not set(request.data.keys()).issubset(allowed_fields):
            return Response(
                {"detail": "Можно обновлять только статус и причину отмены заказа."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Проверяем валидность статуса
        new_status = request.data.get('status')
        if new_status and new_status not in dict(Order.STATUS_CHOICES):
            return Response(
                {"detail": "Недопустимый статус заказа."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Если статус меняется на "cancelled", требуем указать причину отмены
        if new_status == 'cancelled' and not request.data.get('cancel_reason'):
            return Response(
                {"detail": "При отмене заказа необходимо указать причину."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Создает новый заказ"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        
        # Возвращаем данные созданного заказа через основной сериализатор
        response_serializer = OrderSerializer(order)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)