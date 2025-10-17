from django.shortcuts import render, redirect, get_object_or_404
from .models import MenuItem, Barista, Cafe, Resena, Proveedor
from .forms import ResenaForm, CambiarGrupoForm, EditarUsuarioForm, CafeForm, BaristaForm, ProveedorForm
from django.http import JsonResponse
from .mixins import PermissionProtectedTemplateView
from sesion.models import CustomUser
from django.core.paginator import Paginator
from django.contrib.auth.models import Group
from django.contrib import messages
from django.db.models import Q

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
    search_fields = ['username','first_name', 'last_name', 'email']  # Campos para buscar

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_query = self.request.GET.get('q', '')

        if search_query:
            q_objects = Q()
            for field in self.search_fields:
                q_objects |= Q(**{f"{field}__icontains": search_query})
            usuarios_list = self.model.objects.filter(q_objects).order_by('username')
        else:
            usuarios_list = self.model.objects.all().order_by('username')

        # Paginación
        paginator = Paginator(usuarios_list, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['usuarios'] = page_obj  # En lugar de usuarios_list
        context['search_query'] = search_query
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

        return redirect('admin_usuarios')

class CafeAdminView(PermissionProtectedTemplateView):
    template_name = 'admin_cafe.html'
    group_required = 'Administrador'
    permission_required = 'cafeteria.can_edit_menu'
    model = Cafe
    form_class = CafeForm
    context_object_name = 'cafes'
    paginate_by = 10
    search_fields = ['nombre', 'descripcion']  # Campos para buscar

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_query = self.request.GET.get('q', '')

        if search_query:
            q_objects = Q()
            for field in self.search_fields:
                q_objects |= Q(**{f"{field}__icontains": search_query})
            cafes_list = self.model.objects.filter(q_objects).order_by('nombre')
        else:
            cafes_list = self.model.objects.all().order_by('nombre')

        # Paginación
        paginator = Paginator(cafes_list, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['cafes'] = page_obj  # En lugar de cafes_list
        context['search_query'] = search_query
        context['form'] = self.form_class()

        # Si hay un ID, cargar el café para edición
        cafe_id = self.kwargs.get('id')
        if cafe_id:
            context['cafe'] = get_object_or_404(self.model, id=cafe_id)
            context['form'] = self.form_class(instance=context['cafe'])

        return context

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        cafe_id = request.POST.get('id')

        if action == 'create':
            return self.create(request)
        elif action == 'update':
            return self.update(request, cafe_id)
        elif action == 'delete':
            return self.delete(request, cafe_id)
        else:
            messages.error(request, "Acción no válida.")
            return redirect('cafe_admin')

    def create(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Café creado correctamente.")
        else:
            messages.error(request, "Error al crear el café.")
        return redirect('cafe_admin')

    def update(self, request, cafe_id):
        cafe = get_object_or_404(self.model, id=cafe_id)
        form = self.form_class(request.POST, instance=cafe)
        if form.is_valid():
            form.save()
            messages.success(request, "Café actualizado correctamente.")
        else:
            messages.error(request, "Error al actualizar el café.")
        return redirect('cafe_admin')

    def delete(self, request, cafe_id):
        cafe = get_object_or_404(self.model, id=cafe_id)
        cafe.delete()
        messages.success(request, "Café eliminado correctamente.")
        return redirect('cafe_admin')
    
class BaristaAdminView(PermissionProtectedTemplateView):
    template_name = 'admin_barista.html'
    group_required = 'Administrador'
    permission_required = 'cafeteria.can_edit_menu'
    model = Barista
    form_class = BaristaForm
    context_object_name = 'baristas'
    paginate_by = 10
    search_fields = ['nombre']  # Campos para buscar

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_query = self.request.GET.get('q', '')

        if search_query:
            q_objects = Q()
            for field in self.search_fields:
                q_objects |= Q(**{f"{field}__icontains": search_query})
            baristas_list = self.model.objects.filter(q_objects).order_by('nombre')
        else:
            baristas_list = self.model.objects.all().order_by('nombre')

        # Paginación
        paginator = Paginator(baristas_list, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['baristas'] = page_obj  # En lugar de cafes_list
        context['search_query'] = search_query
        context['form'] = self.form_class()

        # Si hay un ID, cargar el café para edición
        barista_id = self.kwargs.get('id')
        if barista_id:
            context['barista'] = get_object_or_404(self.model, id=barista_id)
            context['form'] = self.form_class(instance=context['barista'])

        return context

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        barista_id = request.POST.get('id')

        if action == 'create':
            return self.create(request)
        elif action == 'update':
            return self.update(request, barista_id)
        elif action == 'delete':
            return self.delete(request, barista_id)
        else:
            messages.error(request, "Acción no válida.")
            return redirect('barista_admin')

    def create(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Barista creado correctamente.")
        else:
            messages.error(request, "Error al crear el Barista.")
        return redirect('barista_admin')

    def update(self, request, cafe_id):
        cafe = get_object_or_404(self.model, id=cafe_id)
        form = self.form_class(request.POST, instance=cafe)
        if form.is_valid():
            form.save()
            messages.success(request, "Barista actualizado correctamente.")
        else:
            messages.error(request, "Error al actualizar el café.")
        return redirect('barista_admin')

    def delete(self, request, cafe_id):
        cafe = get_object_or_404(self.model, id=cafe_id)
        cafe.delete()
        messages.success(request, "Barista eliminado correctamente.")
        return redirect('barista_admin')

class ProveedorAdminView(PermissionProtectedTemplateView):
    template_name = 'admin_proveedores.html'
    group_required = 'Administrador'
    permission_required = 'cafeteria.can_edit_menu'
    model = Proveedor
    form_class = ProveedorForm
    context_object_name = 'proveedores'
    paginate_by = 10
    search_fields = ['nombre']  # Campos para buscar

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_query = self.request.GET.get('q', '')

        if search_query:
            q_objects = Q()
            for field in self.search_fields:
                q_objects |= Q(**{f"{field}__icontains": search_query})
            proveedores_list = self.model.objects.filter(q_objects).order_by('nombre')
        else:
            proveedores_list = self.model.objects.all().order_by('nombre')

        # Paginación
        paginator = Paginator(proveedores_list, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['proveedores'] = page_obj  # En lugar de cafes_list
        context['search_query'] = search_query
        context['form'] = self.form_class()

        # Si hay un ID, cargar el café para edición
        proveedor_id = self.kwargs.get('id')
        if proveedor_id:
            context['proveedor'] = get_object_or_404(self.model, id=proveedor_id)
            context['form'] = self.form_class(instance=context['proveedor'])

        return context

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        barista_id = request.POST.get('id')

        if action == 'create':
            return self.create(request)
        elif action == 'update':
            return self.update(request, barista_id)
        elif action == 'delete':
            return self.delete(request, barista_id)
        else:
            messages.error(request, "Acción no válida.")
            return redirect('proveedor_admin')

    def create(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "proveedor creado correctamente.")
        else:
            messages.error(request, "Error al crear el Proveedor.")
        return redirect('proveedor_admin')

    def update(self, request, proveedor_id):
        proveedor = get_object_or_404(self.model, id=proveedor_id)
        form = self.form_class(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            messages.success(request, "Proveedor actualizado correctamente.")
        else:
            messages.error(request, "Error al actualizar el Proveedor.")
        return redirect('proveedor_admin')

    def delete(self, request, cafe_id):
        cafe = get_object_or_404(self.model, id=cafe_id)
        cafe.delete()
        messages.success(request, "Proveedor eliminado correctamente.")
        return redirect('proveedor_admin')
    
class ResenaAdminView(PermissionProtectedTemplateView):
    template_name = 'admin_resenas.html'
    group_required = 'Administrador'
    permission_required = 'cafeteria.can_edit_menu'
    model = Resena
    form_class = ResenaForm
    context_object_name = 'resenas'
    paginate_by = 10
    search_fields = ['nombre_cliente']  # Campos para buscar

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_query = self.request.GET.get('q', '')

        if search_query:
            q_objects = Q()
            for field in self.search_fields:
                q_objects |= Q(**{f"{field}__icontains": search_query})
            resenas_list = self.model.objects.filter(q_objects).order_by('nombre_cliente')
        else:
            resenas_list = self.model.objects.all().order_by('nombre_cliente')

        # Paginación
        paginator = Paginator(resenas_list, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['resenas'] = page_obj  # En lugar de cafes_list
        context['search_query'] = search_query
        context['form'] = self.form_class()

        # Si hay un ID, cargar el café para edición
        proveedor_id = self.kwargs.get('id')
        if proveedor_id:
            context['resena'] = get_object_or_404(self.model, id=proveedor_id)
            context['form'] = self.form_class(instance=context['resena'])

        return context

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        resena_id = request.POST.get('id')

        if action == 'create':
            return self.create(request)
        elif action == 'update':
            return self.update(request, resena_id)
        elif action == 'delete':
            return self.delete(request, resena_id)
        else:
            messages.error(request, "Acción no válida.")
            return redirect('resena_admin')

    def create(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Reseña creada correctamente.")
        else:
            messages.error(request, "Error al crear el Proveedor.")
        return redirect('resena_admin')

    def update(self, request, proveedor_id):
        proveedor = get_object_or_404(self.model, id=proveedor_id)
        form = self.form_class(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            messages.success(request, "Reseña actualizada correctamente.")
        else:
            messages.error(request, "Error al actualizar la Reseña.")
        return redirect('resena_admin')

    def delete(self, request, cafe_id):
        cafe = get_object_or_404(self.model, id=cafe_id)
        cafe.delete()
        messages.success(request, "Proveedor eliminado correctamente.")
        return redirect('proveedor_admin')
    
def handler403(request, exception=None):
    """Manejador personalizado para errores 403 (Permiso denegado)"""
    return render(request, '403.html', status=403)


def handler404(request, exception=None):
    """Manejador personalizado para errores 404 (Página no encontrada)"""
    return render(request, '404.html', status=404)
