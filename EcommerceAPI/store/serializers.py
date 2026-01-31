from rest_framework import serializers

from .models import Cart, CartItem, Product, Order, Review


class ReviewSerializer(serializers.ModelSerializer):
    user=serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    reviews=ReviewSerializer(many=True,read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'category', 'reviews']


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True) #for presenting all data
    subtotal = serializers.ReadOnlyField()  #for reading the method in the models.py
    class Meta:
        model = CartItem
        fields = ['id','quantity','product','subtotal']


class CartSerializer(serializers.ModelSerializer):
    items=CartItemSerializer(many=True,read_only=True)
    total_price=serializers.ReadOnlyField()
    class Meta:
        model = Cart
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
