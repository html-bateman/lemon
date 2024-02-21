from rest_framework import serializers
from django.contrib.auth.models import User
from .models import MenuItem, Cart, Order, OrderItem, CapstoneMenuItem


class MenuItemSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=255)
    price = serializers.DecimalField(max_digits=6, decimal_places=2)
    featured = serializers.BooleanField()
    category = serializers.StringRelatedField()
    category_id = serializers.IntegerField()

    class Meta:
        model = MenuItem
        fields = ['title', 'price', 'featured', 'category', 'category_id']


class CapstoneMenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CapstoneMenuItem
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['user', 'menuitem', 'quantity', 'unit_price', 'price']


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'


class OrderStatusSerializer(serializers.ModelSerializer):
    def validate(self, data):
        if 'status' not in data:
            raise serializers.ValidationError(
                "Status field is required.")

    class Meta:
        model = Order
        fields = ['status']
