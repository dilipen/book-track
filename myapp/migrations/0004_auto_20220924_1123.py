# Generated by Django 3.2.15 on 2022-09-24 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_alter_book_publisher'),
    ]

    operations = [
        migrations.AddField(
            model_name='paperbookorder',
            name='dispatched_at',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='paperbookorder',
            name='is_dispatched',
            field=models.BooleanField(default=False),
        ),
    ]
