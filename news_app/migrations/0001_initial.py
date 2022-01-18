from django.conf import settings
import django.contrib.auth.validators
from django.contrib.auth.hashers import make_password
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import news_app.models
import phone_field.models

from news_app.models import *


def forwards(apps, schema_editor):
    companies = apps.get_model('news_app', 'Company')
    number = 10
    for i in range(number):
        company = {'name': f'company{i}',
                   'url': f'company{i}.com',
                   'address': f'company{i}@gmail.com',
                   }
        this_company = Company(**company)
        this_company.save()

    users = apps.get_model('news_app', 'User')
    number = 200
    for i in range(number):
        user = {'email': f'email{i}@gmail.com',
                'company_id': str(i % 10 + 1),
                'username': f'username{i}',
                'password': make_password(str(i)),
                'first_name': f'first_name{i}',
                'last_name': f'last_name{i}',
                }
        this_user = User(**user)
        this_user.save()

    posts = apps.get_model('news_app', 'User')
    number = 200 * 30
    for i in range(number):
        post = {'user_id': str((i % 30) + 1),
                'title': f'title{i}',
                'text': f'text{i}',
                'topic': f'topic{i}',
                }
        this_post = Post(**post)
        this_post.save()



class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(blank=True, max_length=254, unique=True, verbose_name='email address')),
                ('user_type', models.TextField(choices=[('client', 'client'), ('admin', 'admin')], default='client', null=True)),
                ('avatar', models.ImageField(null=True, upload_to=news_app.models.user_directory_path)),
                ('telephone_number', phone_field.models.PhoneField(blank=True, help_text='Contact phone number', max_length=31, null=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
            managers=[
                ('objects', news_app.models.MyUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('url', models.URLField(default='<django.db.models.fields.TextField>_company.com')),
                ('address', models.EmailField(default='<django.db.models.fields.TextField>@default.com', max_length=254)),
                ('date_created', models.DateField(null=True)),
                ('logo', models.ImageField(null=True, upload_to=news_app.models.company_directory_path)),
            ],
            options={
                'verbose_name': 'Company',
                'verbose_name_plural': 'Companies',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('text', models.TextField()),
                ('topic', models.TextField()),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Post',
                'verbose_name_plural': 'Posts',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='news_app.company'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.AlterUniqueTogether(
            name='user',
            unique_together={('last_name', 'first_name')},
        ),
        migrations.RunPython(forwards),
    ]
