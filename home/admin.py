from django.contrib import admin 
from .models import Comment,Post
from django.db import models


class postadmin(admin.ModelAdmin):
    list_display=('user','created','slug')
    search_fields=('slug','body')




admin.site.register(Comment)
admin.site.register(Post,postadmin)

# Register your models here.
