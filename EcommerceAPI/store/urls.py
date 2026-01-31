from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CartViewSet, ProductViewSet, OrderViewSet

router = DefaultRouter()

router.register("cart",CartViewSet,basename="cart")
router.register("products",ProductViewSet,basename="products")
router.register("orders",OrderViewSet,basename="orders")

urlpatterns = router.urls