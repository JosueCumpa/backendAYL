# Generated by Django 4.2.7 on 2023-11-23 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('SistemaWeb', '0004_delete_group'),
    ]

    operations = [
        migrations.CreateModel(
            name='MaquinaInyeccion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=150, unique=True)),
                ('estado', models.CharField(max_length=1)),
            ],
        ),
    ]