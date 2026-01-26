from django.urls import path

from . import views

urlpatterns = [
    path('',views.product_list_create_api_view,name='product-list'),
    path('create/', views.product_list_create_api_view),
    path('<int:pk>/update/',views.product_Update_api_view),
    path('<int:pk>/delete/',views.product_destroy_api_view),
    path('<int:pk>/', views.product_detail_view,name='product-detail'),

]