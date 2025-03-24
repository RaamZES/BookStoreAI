from django.db import models
from django.contrib.auth.models import User
from rest_framework import serializers, viewsets, routers
from django.urls import path, include
from django.shortcuts import get_object_or_404

# Модели
class Author(models.Model):
    name = models.CharField(max_length=255)
    bio = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.PositiveIntegerField()
    
    def __str__(self):
        return self.title

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    books = models.ManyToManyField(Book)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Order {self.id} by {self.user.username}'

# Сериализаторы
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    
    class Meta:
        model = Book
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True)
    
    class Meta:
        model = Order
        fields = '__all__'

# ViewSets
class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

# Роутинг
router = routers.DefaultRouter()
router.register(r'authors', AuthorViewSet)
router.register(r'books', BookViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
