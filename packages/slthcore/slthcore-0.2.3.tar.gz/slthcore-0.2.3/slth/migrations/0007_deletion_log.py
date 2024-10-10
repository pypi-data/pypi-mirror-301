# Generated by Django 4.2.6 on 2024-05-30 11:07

from django.db import migrations, models
import slth
import slth.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('slth', '0006_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Deletion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', slth.db.models.CharField(db_index=True, max_length=50, null=True)),
                ('datetime', models.DateTimeField(null=True, verbose_name='Data/Hora')),
                ('instance', slth.db.models.CharField(db_index=True, max_length=50, null=True, verbose_name='Instância')),
                ('restored', models.BooleanField(default=False, verbose_name='Restaurado')),
                ('backup', slth.db.models.TextField(verbose_name='Backup')),
            ],
            options={
                'verbose_name': 'Exclusão',
                'verbose_name_plural': 'Exclusões',
            },
            bases=(models.Model, slth.ModelMixin),
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', slth.db.models.CharField(db_index=True, max_length=50, null=True)),
                ('endpoint', slth.db.models.CharField(db_index=True, max_length=255, null=True, verbose_name='Nome do Endpoint')),
                ('instance', slth.db.models.CharField(db_index=True, max_length=50, null=True, verbose_name='Instância')),
                ('action', slth.db.models.CharField(db_index=True, max_length=255, null=True, verbose_name='Ação')),
                ('datetime', models.DateTimeField(null=True, verbose_name='Data/Hora')),
                ('url', slth.db.models.CharField(max_length=255, null=True, verbose_name='URL')),
                ('data', slth.db.models.TextField(verbose_name='Dados')),
            ],
            options={
                'verbose_name': 'Log',
                'verbose_name_plural': 'Logs',
            },
            bases=(models.Model, slth.ModelMixin),
        ),
    ]
