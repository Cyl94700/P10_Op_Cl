from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """User model with unique email"""

    email = models.EmailField(unique=True)
