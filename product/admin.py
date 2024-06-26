from django.contrib import admin
from .models import Producto

# Register your models here.
@admin.register(Producto)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["nombre", "precio1", "onlinePrice", "codigo", "existenciaMakita"]
    search_fields = ["nombre", "codigo"]