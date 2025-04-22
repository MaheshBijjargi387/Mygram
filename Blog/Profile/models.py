from django.db import models
from Post.models import*


class ProfileImg(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    image=models.ImageField(upload_to="Img/")
    name=models.CharField(max_length=50,null=True,blank=True)


class Following(models.Model):
    follower = models.ForeignKey(User, related_name='following_set', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers_set', on_delete=models.CASCADE)

