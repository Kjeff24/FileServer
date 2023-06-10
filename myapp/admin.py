from django.contrib import admin
from .models import User, File, UserActivities
# Register your models here.

admin.site.register(User)
admin.site.register(File)
admin.site.register(UserActivities)