from rest_framework.routers import DefaultRouter

from products.viewsets import ProductViewSet,product_detail_view,product_list_view

router = DefaultRouter()
router.register('products', ProductViewSet,basename='products')
#router.register('products', product_detail_view,basename='products')

print(router.urls)
urlpatterns = router.urls