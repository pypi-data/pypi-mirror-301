# Generated by Django 4.2.6 on 2024-09-09 07:10

from django.db import migrations
import slth.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('slth', '0007_deletion_log'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deletion',
            name='datetime',
            field=slth.db.models.DateTimeField(null=True, verbose_name='Data/Hora'),
        ),
        migrations.AlterField(
            model_name='log',
            name='datetime',
            field=slth.db.models.DateTimeField(null=True, verbose_name='Data/Hora'),
        ),
    ]
