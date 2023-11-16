from django.contrib import admin
from users import models
# Register your models here.


@admin.register(models.UserProfile)
class PostAdmin(admin.ModelAdmin):
    pass

