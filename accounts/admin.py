from django.contrib import admin
from .models import relation, userprofile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class userprofileInline(admin.StackedInline):
    model= userprofile
    can_delete=False

class Extendeduseradmin(UserAdmin):
    inlines=(userprofileInline,)




admin.site.unregister(User)
admin.site.register(User,Extendeduseradmin)
admin.site.register(relation)

# Register your models here.
