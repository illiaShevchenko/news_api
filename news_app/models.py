from django.db.models import QuerySet
from django.db.models.manager import BaseManager
from phone_field import PhoneField
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


def company_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/company_<id>/<filename>
    return f'company_{instance.name}/{filename}'


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<surname>_<name>/<filename>
    return f'user_{instance.last_name}_{instance.first_name}/{filename}'


class MyUserManager(UserManager):
    use_in_migrations = True

    def create_user(self, username, email=None, password=None, **extra_fields):
        #raise Exception(extra_fields)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, email, password, **extra_fields)

    create = create_user

    def create_superuser(self, email, password):
        user = self.model(
            email=self.normalize_email(email)
        )

        user.last_name = email
        user.username = email
        user.set_password(password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)
        return user

    # class Meta:
    #     model = User


class User(AbstractUser):
    objects = MyUserManager()
    USER_TYPE_CHOICES = [
        ('client', 'client'),
        ('admin', 'admin'),
    ]
    email = models.EmailField('email address', blank=True, unique=True)
    company = models.ForeignKey("Company", on_delete=models.SET_NULL, null=True)
    user_type = models.TextField(choices=USER_TYPE_CHOICES, null=True, default='client')
    avatar = models.ImageField(upload_to=user_directory_path, null=True)
    telephone_number = PhoneField(blank=True, help_text='Contact phone number', null=True)
    #username = 'user_'+str(id)

    # The following fields are required for every custom User model

    is_active = models.BooleanField(default=True)

#    USERNAME_KEY = 'id'
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

    class Meta:
        unique_together = ('last_name', 'first_name')
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return True

    def soft_delete(self):
        self.company_id = None
        self.email = 'deleted'
        self.password = None
        self.first_name = None
        self.last_name = None
        self.user_type = None
        self.avatar = None
        self.telephone_number = None
        self.save()


class Company(models.Model):
    name = models.TextField()
    url = models.URLField(default=f'{name}_company.com')
    address = models.EmailField(default=f'{name}@default.com')          # EmailField/ ?
    date_created = models.DateField(null=True)
    logo = models.ImageField(upload_to=company_directory_path, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'


class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.SET_NULL, null=True)
    title = models.TextField()
    text = models.TextField()
    topic = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
