from .models import MenuItem
from rest_framework import serializers
from .models import MenuItem, Book, Category, Rating, Booking
from decimal import Decimal
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator
import bleach


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']


class MenuItemSerializer(serializers.HyperlinkedModelSerializer):
    stock = serializers.IntegerField(source='inventory')
    title = serializers.CharField(
        max_length=255,
        validators=[UniqueValidator(queryset=MenuItem.objects.all())]
    )
    # validators = [
    # UniqueTogetherValidator(
    #     queryset=MenuItem.objects.all(),
    #     fields=['title', 'price']
    # ),
    # ]

    def validate_title(self, value):

        return bleach.clean(value)

    def validate_price(self, value):
        if value < 2:
            raise serializers.ValidationError(
                'Price should not be less than 2.0')

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError('Stock cannot be negative')

    def validate(self, attrs):
        attrs['title'] = bleach.clean(attrs['title'])
        if attrs['price'] < 2:
            raise serializers.ValidationError(
                'Price should not be less than 2.0')
        if attrs['inventory'] < 0:
            raise serializers.ValidationError('Stock cannot be negative')
        return super().validate(attrs)

    class Meta:
        model = MenuItem
        # fields = ['title', 'price', 'inventory']
        fields = ['title', 'price', 'stock']
        extra_kwargs = {
            'price': {'min_value': 2},
            # 'inventory': {'min_value': 1},
            'stock': {'source': 'inventory', 'min_value': 0}
        }

    def calculate_tax(self, product: MenuItem):
        return product.price * Decimal(1.1)


class MenuItemSerializerHide(serializers.ModelSerializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    # price = serializers.DecimalField(max_digits=6, decimal_places=2)
    # price = serializers.DecimalField(
    #     max_digits=6, decimal_places=2, min_value=2)
   # inventory = serializers.ImageField()
    stock = serializers.IntegerField(source='inventory')
    price_after_tax = serializers.SerializerMethodField(
        method_name='calculate_tax')
    # category = serializers.StringRelatedField()
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    ''' present the category field as a link'''
    # category = serializers.HyperlinkedRelatedField(
    #     queryset=Category.objects.all(),
    #     view_name='category-detail'
    # )

    class Meta:
        model = MenuItem
       # fields = ['id', 'title', 'price', 'inventory']
        fields = ['id', 'title', 'stock', 'price',
                  'price_after_tax', 'category', 'category_id']
        # depth = 1

    def calculate_tax(self, product: MenuItem):
        return round(product.price * Decimal(1.1), 2)


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'price']


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'


class RatingSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Rating
        fields = ['user', 'menuitem_id', 'rating']
        validators = [UniqueValidator(
            queryset=Rating.objects.all(),
            message="test.....")]
        extra_kwargs = {
            'rating': {'max_value': 5, 'min_value': 0}
        }
