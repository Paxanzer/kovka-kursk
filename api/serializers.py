from rest_framework import serializers
from .models import User, Product, ProductCategory, ProductImage, Order, OrderItem
from django.contrib.auth.hashers import make_password
from django.core.files.storage import default_storage

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'phone']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},  # Делаем email обязательным
            'phone': {'required': False}  # Телефон необязательный
        }

    def validate(self, data):
        # Проверка уникальности username
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("Пользователь с таким именем уже существует.")
        
        # Проверка email
        if User.objects.filter(email=data.get('email', '')).exists():
            raise serializers.ValidationError("Пользователь с таким email уже существует.")
        
        return data

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data.get('email'),
            phone=validated_data.get('phone'),
            role='customer',  # Устанавливаем роль по умолчанию
            is_active=True  # Активируем пользователя
        )
        user.set_password(validated_data['password'])  # Безопасное хеширование
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'role', 'password']
        extra_kwargs = {'password': {'write_only': True},
                        }
    
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().update(instance, validated_data)



class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text']
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = instance.image.url if instance.image else None
        return representation

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id', 'name', 'image']
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = instance.image.url if instance.image else None
        return representation

class ProductSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=ProductCategory.objects.all(),
        source='category',
        write_only=True
    )
    images = ProductImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'category', 'category_id', 'article', 
            'price', 'specifications', 'description', 
            'image', 'images'
        ]
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = instance.image.url if instance.image else None
        return representation
    
    def update(self, instance, validated_data):
        # Удаляем старое изображение при загрузке нового
        if 'image' in validated_data and instance.image:
            default_storage.delete(instance.image.path)

        return super().update(instance, validated_data)

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price']
        read_only_fields = ['price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'code', 'user', 'status', 'status_display', 'created_at', 'total_price', 'items', 'cancel_reason']
        read_only_fields = ['code', 'created_at', 'total_price']

class CreateOrderItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

class CreateOrderSerializer(serializers.Serializer):
    items = CreateOrderItemSerializer(many=True)

    def create(self, validated_data):
        user = self.context['request'].user
        order = Order.objects.create(user=user)
        
        for item_data in validated_data['items']:
            product = Product.objects.get(id=item_data['product_id'])
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item_data['quantity'],
                price=product.price
            )
        
        return order

class UserProfileOrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price']

class UserProfileOrderSerializer(serializers.ModelSerializer):
    items = UserProfileOrderItemSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'code', 'status', 'status_display', 'created_at', 'total_price', 'items', 'cancel_reason']

class UserProfileSerializer(serializers.ModelSerializer):
    orders = UserProfileOrderSerializer(many=True, read_only=True)
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'role', 'role_display', 'orders']
        read_only_fields = ['role']