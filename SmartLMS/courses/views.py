from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Course, Enrollment

from .permissions import IsEnrolled,IsInstructorOrReadOnly
from .serializers import CourseSerializer,LessonSerializer


# Create your views here.
class CourseViewSet(viewsets.ModelViewSet):
    queryset=Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsInstructorOrReadOnly,permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)

    @action(detail=True, methods=['post'])
    def enroll(self, request, pk=None):
        course = self.get_object()
        enrollment,created = Enrollment.objects.get_or_create(course=course,student=request.user)

        if not created:
            return Response({'detail': 'You are already enrolled.'}, status=400)
        else:
            return Response({'detail': 'Enrolled Successfully'}, status=201)


class LessonViewSet(viewsets.ModelViewSet):
    queryset=Course.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):

        if self.action == 'retrieve':
            self.permission_classes = [permissions.IsAuthenticated, IsEnrolled]
        else:
            self.permission_classes = [permissions.IsAuthenticated, IsInstructorOrReadOnly]

        return super().get_permissions()
