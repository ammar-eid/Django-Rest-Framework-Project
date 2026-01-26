from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions
from rest_framework.views import APIView

from .models import Post, Follow
from .serializers import PostSerializer
from .permissions import IsAuthorOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Post,Like
from django.contrib.auth.models import User
# Create your views here.

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer

    #to allow performing like on a post of a non-follower user
    def get_permissions(self):
        if self.action in ['like', 'feed', 'list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthorOrReadOnly]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    #for like or unlike for someone
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user

        like_queryset = Like.objects.filter(user=user,post=post)

        if like_queryset.exists():
            like_queryset.delete()
            return Response({'message': 'Unliked'}, status=200)
        else:
            Like.objects.create(user=user,post=post)
            return Response({'message': 'Liked'}, status=201)



    @action(detail=False, methods=['get'])
    def feed(self, request):

        followed_users=request.user.following.values_list("followed_user",flat=True)

        posts=Post.objects.filter(author__id__in=followed_users).order_by('-created_at')

        serializer = self.get_serializer(posts,many=True)

        return Response(serializer.data)


class FollowUserAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,user_id):
        user_to_follow = get_object_or_404(User,id=user_id)
        #user cannot follow himself
        if user_to_follow==request.user:
            return Response({'message': 'You cannot follow yourself'}, status=400)

        #create object from the follow table
        follow_obj,created = Follow.objects.get_or_create(
            follower=request.user,
            followed_user=user_to_follow
        )

        if not created:
            follow_obj.delete()
            return Response({'message': 'Unfollowed Successfully'}, status=200)

        return Response({'message': f'you are now following {user_to_follow.username}'}, status=201)






