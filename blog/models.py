from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    category = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now = True)
    
    #--모델 확장 --#
    image = models.ImageField(upload_to ='posts/', blank=True, null=True)
    views = models.PositiveIntegerField(default=0)


    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post_detail', kwarge={'pk':self.pk})
    
    #--프로필 --# 
    class Profile(models.Model):
        user = models.OneToOneField(User, on_delete=models.CASCADE)
        nickname = models.CharField(max_length=50, blank=True)
        bio= models.TextField(max_length=500, blank=True)
        profile_image = models.ImageField(upload_to = 'profriles/', blank=True, null=True)

        def __str__(self):
            return f"{self.user.username}'s profile"
        

    #--댓글 --# 
    class Comment(models.Model):
        post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')  # 이제 Post가 위에 정의되어 있음
        author = models.ForeignKey(User, on_delete=models.CASCADE)
        content = models.TextField()
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)
        parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

        class Meta:
            ordering = ['created_at']

        def __str__(self):
            return f'Comment by {self.author.username} on {self.post.title}'


