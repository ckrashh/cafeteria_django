from django.shortcuts import render, redirect
from .models import MenuItem, Barista, Cafe, Resena, Proveedor
from .forms import ResenaForm, CambiarGrupoForm, EditarUsuarioForm
from django.http import JsonResponse
from .mixins import PermissionProtectedTemplateView
from sesion.models import CustomUser
from django.core.paginator import Paginator
from django.contrib.auth.models import Group
from django.contrib import messages

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
    template_name = 'admin.html'
    group_required = 'Administrador'
    permission_required = 'cafeteria.can_edit_menu'
    

class AdminUsuariosView(PermissionProtectedTemplateView):
    template_name = 'admin_usuarios.html'    
    group_required = 'Administrador'
    permission_required = 'cafeteria.can_edit_menu'
    model = CustomUser
    context_object_name = 'usuarios'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtener todos los usuarios
        usuarios_list = CustomUser.objects.all().order_by('username')

        # Aplicar paginación
        paginator = Paginator(usuarios_list, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Agregar al contexto
        context['usuarios'] = page_obj

        context['grupos'] = Group.objects.all().order_by('name')

        # Formulario para cambiar grupo
        context['cambiar_grupo_form'] = CambiarGrupoForm()

        # Formulario para editar usuario
        context['editar_usuario_form'] = EditarUsuarioForm()

        return context
    
    def post(self, request, *args, **kwargs):
        usuario_id = request.POST.get('usuario_id')
        usuario = CustomUser.objects.get(id=usuario_id)
        action = request.POST.get('action')

        #Accion para cambiar el grupo de un usuario
        if action == 'editar_grupo':
            form = CambiarGrupoForm(request.POST)
            if form.is_valid():
                grupo = form.cleaned_data['grupo']
                if grupo:  # Si se seleccionó un grupo
                    usuario.groups.clear()
                    usuario.groups.add(grupo)
                    messages.success(request, f"Grupo de {usuario.username} actualizado a {grupo.name}.")
                else:  # Si no se seleccionó ningún grupo (opción en blanco)
                    usuario.groups.clear()
                    messages.success(request, f"Todos los grupos fueron removidos de {usuario.username}.")
            else:
                messages.error(request, "Error al actualizar el grupo.")
        elif action == 'eliminar':
            usuario.delete()
            messages.success(request, f"Usuario {usuario.username} eliminado correctamente.")
        elif action == 'editar':
            usuario.first_name = request.POST.get('first_name')
            usuario.last_name = request.POST.get('last_name')
            usuario.email = request.POST.get('email')
            usuario.save()
            messages.success(request, f"Usuario {usuario.username} editado correctamente.")
        else:
            messages.error(request, "Acción no reconocida.")

        return redirect('admin_ususarios')
    
def handler403(request, exception=None):
    """Manejador personalizado para errores 403 (Permiso denegado)"""
    return render(request, '403.html', status=403)


def handler404(request, exception=None):
    """Manejador personalizado para errores 404 (Página no encontrada)"""
    return render(request, '404.html', status=404)
