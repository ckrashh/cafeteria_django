# Cafetería Django

**Autor:** Gerald Carrillo  
**Licencia:** MIT  
**Repositorio:** [ckrashh/cafeteria_django](https://github.com/ckrashh/cafeteria_django)

---

## 📖 Descripción

**Cafetería Django** es una aplicación web desarrollada con el framework **Django**, diseñada para gestionar los procesos básicos de una cafetería, incluyendo la administración de productos, categorías y pedidos.  
Este proyecto fue creado con fines educativos como parte de un proceso de aprendizaje en desarrollo web con Python y Django.

---

## 🧩 Estructura del Proyecto

cafeteria_django/
├── cafeteria/ # Aplicación principal
│ ├── migrations/ # Archivos de migración de la base de datos
│ ├── templates/ # Archivos HTML para las vistas
│ ├── static/ # Archivos estáticos (CSS, JS, imágenes)
│ ├── models.py # Modelos de base de datos
│ ├── views.py # Lógica de negocio y vistas
│ ├── urls.py # Enrutamiento interno
│ └── admin.py # Configuración del panel de administración
├── manage.py # Script principal de gestión de Django
├── requerimientos.txt # Dependencias del proyecto
└── pasos_para_crear_un_proyecto.txt # Documentación auxiliar


---

## 🛠️ Tecnologías Utilizadas

- **Lenguaje:** Python 3.x  
- **Framework:** Django  
- **Base de datos:** SQLite (por defecto)  
- **Frontend:** HTML5, CSS3, Django Templates  
- **Control de versiones:** Git y GitHub

---

## ⚙️ Instalación y Ejecución

Siga los siguientes pasos para ejecutar el proyecto en un entorno local:

```bash
# 1. Clonar el repositorio
git clone https://github.com/ckrashh/cafeteria_django.git
cd cafeteria_django

# 2. Crear un entorno virtual (recomendado)
python -m venv venv

# 3. Activar el entorno virtual
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Aplicar migraciones
python manage.py migrate

# 6. Crear un superusuario (opcional)
python manage.py createsuperuser

# 7. Ejecutar el servidor de desarrollo
python manage.py runserver
```
Una vez iniciado el servidor, acceder a la aplicación en:
👉 http://127.0.0.1:8000/

🧪 Funcionalidades Principales

Panel administrativo de Django para control de datos.

Plantillas HTML integradas con el sistema de vistas.

📋 Requisitos

Python 3.8 o superior.

Django (versión especificada en requerimientos.txt).

Git (para control de versiones).

📌 Estado del Proyecto

Proyecto funcional en fase de desarrollo educativo.
Puede ser ampliado con funcionalidades adicionales como autenticación de usuarios, integración de bases de datos externas o sistemas de pedidos en línea.


