# Generated by Django 5.1.1 on 2024-09-27 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_flash_sale',
            field=models.BooleanField(default=True),
        ),
    ]