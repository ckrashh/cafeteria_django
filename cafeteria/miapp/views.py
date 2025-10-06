from django.shortcuts import render
from .models import MenuItem, Barista, Cafe, Resena, Proveedor
from .forms import ResenaForm
from django.http import JsonResponse
from .mixins import PermissionProtectedTemplateView
from sesion.models import CustomUser
def index(request):
    resenas_destacadas = Resena.objects.all().order_by('-calificacion')[:3]
    return render(request, 'index.html', {'resenas_destacadas': resenas_destacadas})

def menu(request):
    menu_items = MenuItem.objects.all()
    return render(request, 'menu.html', {'menu_items': menu_items})

def baristas(request):
    baristas = Barista.objects.all()
    return render(request, 'baristas.html', {'baristas': baristas})

def resenas(request):
    resenas = Resena.objects.all().order_by('-fecha_creacion')
    form = ResenaForm()
    return render(request, 'resenas.html', {'form': form, 'resenas': resenas})

def proveedores(request):
    proveedores = Proveedor.objects.all()
    return render(request, 'proveedores.html', {'proveedores': proveedores})

def cafes(request):
    cafes = Cafe.objects.all()
    return render(request, 'cafes.html', {'cafes': cafes})

def form_resena(request):
    if request.method == 'POST':
        form = ResenaForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'nombre_cliente': form.cleaned_data['nombre_cliente']})  # Respuesta JSON para AJAX
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = ResenaForm()
    return render(request, 'form_resena.html', {'form': form})

class AdminView(PermissionProtectedTemplateView):
    template_name = 'admin_ususarios.html'    
    group_required = 'Administrador'
    permission_required = 'cafeteria.can_edit_menu'
    model = CustomUser
    context_object_name = 'usuarios'
    paginate_by = 10

def handler403(request, exception=None):
    """Manejador personalizado para errores 403 (Permiso denegado)"""
    return render(request, '403.html', status=403)


def handler404(request, exception=None):
    """Manejador personalizado para errores 404 (Página no encontrada)"""
    return render(request, '404.html', status=404)
