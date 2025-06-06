from django.contrib import admin
from .models import Usuario, Produto
# Register your models here.

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ("nome", "email", "senha")

admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Produto)