# Generated by Django 4.2.7 on 2024-04-23 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slth', '0003_rename_photo_profile_alter_profile_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='Foto'),
        ),
    ]
