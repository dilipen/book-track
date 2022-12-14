# Generated by Django 3.2.15 on 2022-09-24 04:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import myapp.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatars/')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='superuser')),
                ('is_staff', models.BooleanField(default=False, verbose_name='staff')),
                ('is_publisher', models.BooleanField(default=False, verbose_name='publisher')),
                ('is_buyer', models.BooleanField(default=False, verbose_name='buyer')),
                ('is_transporter', models.BooleanField(default=False, verbose_name='transporter')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', myapp.managers.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_at', models.DateTimeField(auto_now=True, null=True)),
                ('ebook_rate', models.IntegerField(blank=True, default=0)),
                ('paperbook_rate', models.IntegerField(blank=True, default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_at', models.DateTimeField(auto_now=True, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('book_type', models.CharField(choices=[('ebook', 'EBOOK'), ('paper', 'PAPERBOOK')], max_length=20)),
                ('rate', models.IntegerField(blank=True, default=0)),
                ('is_cancelled', models.BooleanField(default=False)),
                ('cancelled_reason', models.TextField(blank=True, default=None, null=True)),
                ('cancelled_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.book')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.order')),
            ],
        ),
        migrations.CreateModel(
            name='PaperBookOrder',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('is_preparing', models.BooleanField(default=False)),
                ('is_dispatched', models.BooleanField(default=False)),
                ('dispatched_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('order_detail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.orderdetail')),
            ],
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_at', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Transporter',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_at', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UploadFile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('file', models.FileField(blank=True, max_length=250, null=True, upload_to='')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_at', models.DateTimeField(auto_now=True, null=True)),
                ('deleted', models.BooleanField(blank=True, default=False)),
            ],
        ),
        migrations.CreateModel(
            name='UserAddress',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('address_line1', models.TextField(blank=True, default=None, null=True)),
                ('address_line2', models.TextField(blank=True, default=None, null=True)),
                ('address_line3', models.TextField(blank=True, default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PaperBookOrderTrack',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('tracker', models.CharField(choices=[('moving', 'MOVING'), ('station', 'STATION'), ('delivered', 'DELIVERED'), ('outofdelivery', 'OUT_OF_DELIVERY')], max_length=20)),
                ('notes', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_at', models.DateTimeField(auto_now=True, null=True)),
                ('paper_book_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.paperbookorder')),
            ],
        ),
        migrations.AddField(
            model_name='paperbookorder',
            name='publisher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.publisher'),
        ),
        migrations.AddField(
            model_name='paperbookorder',
            name='transporter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.transporter'),
        ),
        migrations.AddField(
            model_name='paperbookorder',
            name='user_address',
            field=models.ForeignKey(blank=None, default=None, null=None, on_delete=django.db.models.deletion.CASCADE, to='myapp.useraddress'),
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_at', models.DateTimeField(auto_now=True, null=True)),
                ('book_type', models.CharField(choices=[('ebook', 'EBOOK'), ('paper', 'PAPERBOOK')], max_length=20)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.book')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='publisher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.publisher'),
        ),
        migrations.AddField(
            model_name='user',
            name='publisher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.publisher'),
        ),
        migrations.AddField(
            model_name='user',
            name='transporter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.transporter'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
