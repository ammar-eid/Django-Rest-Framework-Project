from django.db import transaction
from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets,status
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
# Create your views here.

class ProductViewSet(viewsets.ModelViewSet):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer

    filter_backends=[DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]

    filterset_fields=['category']

    search_fields=['name','description']
    #'name^' for exactly name
    #'name@' for the name with not case sensitive

    ordering_fields=['price','created_at']


class CartViewSet(viewsets.ModelViewSet):
    queryset=Cart.objects.all()
    serializer_class=CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    @action(methods=['post'],detail=False)
    def add_to_cart(self,request):
        product_id=request.data.get('product_id')
        quantity=int(request.data.get('quantity',1))

        product=Product.objects.get(id=product_id)
        cart,_ = Cart.objects.get_or_create(user=request.user)

        item,created=CartItem.objects.get_or_create(cart=cart,product=product)

        if not created:
            item.quantity+=quantity
        else:
            item.quantity=quantity

        item.save()

        return Response({'message':'Product added to cart!'},status=status.HTTP_201_CREATED)

    @action(methods=['post'],detail=False)
    def checkout_cart(self,request):
        cart=request.user.cart
        cart_items=cart.items.all()

        if not cart_items.exists():
            return Response({'error':'cart is empty'},status=400)

        with transaction.atomic():
            order = Order.objects.create(user=request.user,total_price=cart.total_price())

            for item in cart_items:
                if item.product.stock<item.quantity:
                    raise serializers.ValidationError(
                        f"Not enough stock for {item.product.name}, stock:{item.product.stock} required: {item.quantity}")

                item.product.stock-=item.quantity
                item.product.save()

                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price_at_purchase=item.product.price,
                )

            cart_items.delete()

        return Response({'message':'Order placed Successfully','order_id':order.id},status=201)

class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')
