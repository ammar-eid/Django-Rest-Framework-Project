from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet,FollowUserAPIView


router = DefaultRouter()
router.register('posts', PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('follow/<int:user_id>/', FollowUserAPIView.as_view(), name='follow-user'),]