from django.contrib import admin
from .models import User

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
     list_display = [field.name for field in User._meta.get_fields()]

     
