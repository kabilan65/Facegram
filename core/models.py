from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    userid = models.IntegerField()
    bio = models.CharField(blank=True, max_length=100)
    pfp_image = models.ImageField(upload_to="profile_images", default="blank-profile-picture.png")
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="post_images")
    caption = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    no_of_likes = models.IntegerField(default=0)

    # def __str__(self):
    #     return self.post_id 
    
    class Meta:
        ordering = ["-created_at"]

class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=500)

    def __str__(self):
        return self.username

class Follow(models.Model):
    follower = models.CharField(max_length=500)
    author = models.CharField(max_length=500)

    def __str__(self):
        return self.author

class Comment(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.user.username
    
    class Meta:
        ordering = ["-created_at"]