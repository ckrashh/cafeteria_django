from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator


class CustomLoginRequiredMixin(LoginRequiredMixin):
    """Mixin personalizado para requerir autenticación"""
    login_url = '/login/'
    redirect_field_name = 'next'


class CustomPermissionRequiredMixin(PermissionRequiredMixin):
    """Mixin personalizado para requerir permisos específicos"""
    login_url = '/login/'
    redirect_field_name = 'next'
    raise_exception = True  # Lanza excepción para que Django use el handler403 personalizado


class ProtectedTemplateView(CustomLoginRequiredMixin, TemplateView):
    """Vista base protegida que requiere autenticación"""
    pass


class PermissionProtectedTemplateView(CustomLoginRequiredMixin, CustomPermissionRequiredMixin, TemplateView):
    """Vista base protegida que requiere autenticación y permisos específicos"""
    pass

class CRUDMixin:
    """
    Mixin para vistas CRUD con búsqueda, paginación y operaciones básicas.
    Requiere:
    - model: Modelo de Django.
    - form_class: Formulario para el modelo.
    - search_fields: Lista de campos para la búsqueda.
    - paginate_by: Número de elementos por página.
    - template_name: Nombre del template.
    - context_object_name: Nombre del objeto en el contexto (opcional).
    - success_url: URL de redirección después de una acción exitosa.
    - order_by: Campo de ordenamiento (opcional).
    """
    model = None
    form_class = None
    search_fields = []
    paginate_by = 10
    context_object_name = 'objects'
    success_url = None
    order_by = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_query = self.request.GET.get('q', '')

        # Filtrar registros según la búsqueda
        if search_query:
            q_objects = Q()
            for field in self.search_fields:
                q_objects |= Q(**{f"{field}__icontains": search_query})
            object_list = self.model.objects.filter(q_objects).order_by(self.order_by)
        else:
            object_list = self.model.objects.all().order_by(self.order_by)

        # Paginación
        paginator = Paginator(object_list, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context[self.context_object_name] = page_obj
        context['search_query'] = search_query
        context['form'] = self.form_class()
        context['model_verbose_name'] = self.model._meta.verbose_name_plural.title()

        # Si hay un ID en los kwargs, cargar el objeto para edición
        obj_id = self.kwargs.get('id')
        if obj_id:
            context['object'] = get_object_or_404(self.model, id=obj_id)
            context['form'] = self.form_class(instance=context['object'])

        return context

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        obj_id = request.POST.get('id')

        if action == 'create':
            return self.create(request)
        elif action == 'update':
            return self.update(request, obj_id)
        elif action == 'delete':
            return self.delete(request, obj_id)
        else:
            messages.error(request, "Acción no válida.")
            return redirect(self.success_url)

    def create(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"{self.model._meta.verbose_name} creado correctamente.")
        else:
            messages.error(request, f"Error al crear el {self.model._meta.verbose_name}.")
        return redirect(self.success_url)

    def update(self, request, obj_id):
        obj = get_object_or_404(self.model, id=obj_id)
        form = self.form_class(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, f"{self.model._meta.verbose_name} actualizado correctamente.")
        else:
            messages.error(request, f"Error al actualizar el {self.model._meta.verbose_name}.")
        return redirect(self.success_url)

    def delete(self, request, obj_id):
        obj = get_object_or_404(self.model, id=obj_id)
        obj.delete()
        messages.success(request, f"{self.model._meta.verbose_name} eliminado correctamente.")
        return redirect(self.success_url)