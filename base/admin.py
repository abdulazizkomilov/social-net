from django.contrib import admin
from .models import Topic, Room, Comment, User

admin.site.register(User)
admin.site.register(Topic)
admin.site.register(Room)
admin.site.register(Comment)