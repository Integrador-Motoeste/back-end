# Generated by Django 4.2.11 on 2024-04-18 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Motorcycle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=100, verbose_name='Modelo')),
                ('brand', models.CharField(max_length=100, verbose_name='Marca')),
                ('color', models.CharField(max_length=100, verbose_name='Cor')),
                ('year', models.IntegerField(verbose_name='Ano')),
                ('plate', models.CharField(max_length=10, verbose_name='Placa')),
                ('crlv', models.CharField(max_length=20)),
                ('picture_moto', models.ImageField(upload_to='uploads', verbose_name='Imagem')),
            ],
            options={
                'verbose_name': 'Moto',
                'verbose_name_plural': 'Motos',
                'ordering': ['model'],
            },
        ),
    ]
