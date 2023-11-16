from django.contrib import admin
from posts import models
# Register your models here.


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    pass
    # list_display = ("id", "caller", "callee", "callee_trunk")

@admin.register(models.PostRate)
class PostRateAdmin(admin.ModelAdmin):
    pass
    # list_display = ("id", "caller", "callee", "callee_trunk")
