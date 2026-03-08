from .views import CourseViewSet,LessonViewSet
from rest_framework.routers import DefaultRouter
from django.urls import path, include

router = DefaultRouter()
router.register('lesson',LessonViewSet,basename='lesson')
router.register('course',CourseViewSet,basename='course')

urlpatterns = [
path('', include(router.urls)),
]