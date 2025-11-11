from django.db import models
from django.contrib.auth.models import AbstractUser
class CustomUser(AbstractUser):
    class Meta:
        permissions = [
            ("can_view_reports", "Can view reports"),
            ("can_edit_menu", "Can edit menu"),
        ]



