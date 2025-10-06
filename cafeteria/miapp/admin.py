from django.contrib import admin
from .models import MenuItem, Barista, Cafe, Resena, Proveedor

# Registrar modelos básicos
@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio')
    search_fields = ('nombre', 'descripcion')
    list_filter = ('categoria',)

@admin.register(Barista)
class BaristaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(Cafe)
class CafeAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'origen', 'nivel_tostado', 'precio')
    list_filter = ('nivel_tostado', 'origen')
    search_fields = ('nombre', 'descripcion')

@admin.register(Resena)
class ResenaAdmin(admin.ModelAdmin):
    list_display = ('nombre_cliente', 'calificacion', 'fecha_creacion')
    list_filter = ('calificacion', 'fecha_creacion')
    search_fields = ('nombre_cliente', 'comentario')

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'contacto', 'direccion')
    search_fields = ('nombre', 'contacto')

# Opcional: Si no usas el decorador @admin.register, puedes registrar así:
# admin.site.register(MenuItem, MenuItemAdmin)
# admin.site.register(Barista, BaristaAdmin)
# admin.site.register(Cafe, CafeAdmin)
# admin.site.register(Resena, ResenaAdmin)
# admin.site.register(Proveedor, ProveedorAdmin)