from django.db import models
from django.contrib.auth.models import User
# Create your models here.

#post table
class Post(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='posts')
    content = models.TextField()
    image = models.ImageField(upload_to='post_images/',null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username}'s Post"

#Like table
class Like(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        #prevent accepting more than one like for the same post by the same user
        unique_together = ('user','post')

#follow table
class Follow(models.Model):
    follower = models.ForeignKey(User,on_delete=models.CASCADE,related_name='following')
    followed_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower','followed_user')

    def __str__(self):
        return f"{self.follower} follows {self.followed_user}"