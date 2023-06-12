from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser,PermissionsMixin


class UserManager(BaseUserManager):

    def create_user(self, username=None, password=None,*args,**kwargs):
        if not username:
            raise ValueError("Users must have a username")
        if not password:
            raise ValueError("Users must have a password")
        user= self.model(
            username=username,
            *args,
            **kwargs)
        user.set_password(password)
        user.is_active=True
        user.save()
        return user

    def create_superuser(self, username, password,email):
        user = self.create_user(
            username=username,
            password=password,
            email=email,
            role=1, 
            is_staff=True,
        )
        user.is_superuser = True
        user.save()
        return user

ROLE_CHOICES = [
    (1, 'Admin'),
    (2, 'Users')
]

class CustomUser(AbstractBaseUser,PermissionsMixin):

    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    role = models.IntegerField(choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def _str_(self):
        return self.username

class UserProfile(models.Model):

    fk_user=models.OneToOneField(CustomUser,on_delete=models.CASCADE) 
    firstname=models.CharField(max_length=100)
    lastname=models.CharField(max_length=100)
    course=models.CharField(max_length=100)
    user_status=models.BooleanField(default=False)

class Task(models.Model):
    question=models.CharField(max_length=250)
    option1=models.CharField(max_length=200)
    option2=models.CharField(max_length=200)
    option3=models.CharField(max_length=200)
    option4=models.CharField(max_length=200)
    answer=models.CharField(max_length=200)

class Exam(models.Model):
    fk_task=models.ForeignKey(Task,on_delete=models.CASCADE)
    fk_user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    answer=models.CharField(max_length=250)
