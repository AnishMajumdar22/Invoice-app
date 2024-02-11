from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Create your models here.


class Invoice(models.Model):
    invoice_id = models.IntegerField()
    client_name = models.CharField(max_length=200)
    date = models.DateTimeField()


class ItemList(models.Model):
    # item_id = models.IntegerField()
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="items")
    # here parent is Invoice, if you delete the parent, the Itemlist will be deleted. Parents, goes into child
    desc = models.TextField()
    rate = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.IntegerField()


class UserManager(BaseUserManager):
    def create_user(self, name, password, **extra_fields):
        if not name:
            raise ValueError("Username must be provided!")
        user = self.model(name=name, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, name, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(name, password, **extra_fields)


class User(AbstractBaseUser):
    name = models.CharField(
        max_length=100, validators=[MinLengthValidator(3)], unique=True
    )
    email = models.EmailField(max_length=200)
    password = models.CharField(max_length=200, validators=[MinLengthValidator(6)])
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = "name"
    objects = UserManager()

    def has_perm(self, prem, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
