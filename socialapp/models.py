from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Myuser(AbstractUser):
    profile_pic=models.ImageField(upload_to="profile",blank=True,null=True)
    bio=models.TextField(max_length=200,blank=True)

#userprofile
class Profile(models.Model):
    
    user=models.OneToOneField(Myuser,on_delete=models.CASCADE,related_name="userprofile")
    email=models.EmailField(max_length=100,null=True)
    dob=models.DateTimeField(null=True,blank=True)
    gender_choices={
        ('male','Male'),
        ('female','Female')
    }
    gender=models.CharField(max_length=200,choices=gender_choices,null=True,blank=True)
    followers=models.ManyToManyField(Myuser,related_name="followers")
    following=models.ManyToManyField(Myuser,related_name="following")

    def __str__(self):
        return self.user.username

#model for storing the post

class Posts(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    images = models.ImageField(upload_to="images",null=True,blank=True)
    uploaded_date=models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(Myuser,on_delete=models.CASCADE,related_name='my_post')
    num_likes=models.ManyToManyField(Myuser,related_name="num_likes")

    def __str__(self):
        return self.title

#comments

class Comment(models.Model):
    user=models.ForeignKey(Myuser,on_delete=models.CASCADE)
    post=models.ForeignKey(Posts,on_delete=models.CASCADE)
    comment=models.CharField(max_length=200)
    commented_at=models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.comment
    
# class Followers(models.Model):
#     user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user')
#     followers=models.ForeignKey(Myuser,blank=True,default=True,related_name='followers',on_delete=models.CASCADE)
    
#     class Meta:
#         unique_together = ('user','followers',)

#     def __str__(self):     
#         return self.user


