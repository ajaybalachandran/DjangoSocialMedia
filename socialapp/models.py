from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Myuser(AbstractUser):
  profile_pic = models.ImageField(upload_to='profile', default='default/pro_pic.png')


class UserProfile(models.Model):
  user = models.OneToOneField(Myuser, on_delete=models.CASCADE, related_name='user_profile')
  bio = models.CharField(max_length=120, null=True, blank=True)
  mobile = models.CharField(max_length=12, null=True, blank=True)
  dob = models.DateField(null=True, blank=True)
  GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Others', 'Others')
  )
  gender = models.CharField(max_length=12, choices=GENDER_CHOICES, null=True, blank=True)
  following = models.ManyToManyField(Myuser, related_name='followinglist', blank=True)
  followers = models.ManyToManyField(Myuser, related_name='followerslist', blank=True)

  @property
  def get_followers(self):
    return self.followers.all()
    
  @property
  def get_followings(self):
    return self.following.all()


class Posts(models.Model):
  user = models.ForeignKey(Myuser, on_delete=models.CASCADE, related_name='my_post')
  title = models.CharField(max_length=120)
  description = models.CharField(max_length=200)
  post_image = models.ImageField(upload_to='post-images')
  posted_date = models.DateField(auto_now_add=True)
  liked_by = models.ManyToManyField(Myuser)


  def __str__(self):
    return self.title


class Comments(models.Model):
  post = models.ForeignKey(Posts, on_delete=models.CASCADE)
  user = models.ForeignKey(Myuser, on_delete=models.CASCADE)
  comment = models.CharField(max_length=120)
  commented_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.comment

