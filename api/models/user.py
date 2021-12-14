from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin,BaseUserManager, User


class UserManager(BaseUserManager):
    def create_user(self,email, password=None, **extra_fields):
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(email = self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return(user)

    
    def create_superuser(self, email , password):
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length= 255, unique=True)
    is_actice = models.BooleanField(default=True)
    is_staff= models.BooleanField(default=False)
    object = UserManager()
    USERNAME_FIELD = 'email'
    
    def __str__(self):
        """Return string representation of the user"""""
        return self.email