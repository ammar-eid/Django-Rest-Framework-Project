from rest_framework import serializers
from .models import Post,Like


class PostSerializer(serializers.ModelSerializer):
    author =serializers.ReadOnlyField(source='author.username')
    likes_count=serializers.SerializerMethodField()
    is_liked=serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ['id','author','content','image','created_at','likes_count','is_liked']

    def get_likes_count(self,obj):
        return obj.likes.count()

    def get_is_liked(self,obj):
        user=self.context['request'].user

        if user.is_authenticated:
            return obj.likes.filter(user=user).exists()
        return False

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'