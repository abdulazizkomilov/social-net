from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField

class User(AbstractUser):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, blank=True)
    avatar = models.ImageField(null=True, blank=True)
    follower = models.ManyToManyField('User', blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    summary = models.CharField(max_length=300)
    image = models.ImageField(upload_to='room/', blank=True, null=True)
    description = RichTextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    like = models.ManyToManyField(User, related_name='like', blank=True)
    views = models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']


    def __str__(self):
        return self.name


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField(blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        ordering = ['-updated', '-created']

    
    @property
    def getReplies(self):
        return Comment.objects.filter(parent=self).reverse()
    

    @property
    def is_parent(self):
        if self.parent is None:
            return True

    def __str__(self):
        return self.body
