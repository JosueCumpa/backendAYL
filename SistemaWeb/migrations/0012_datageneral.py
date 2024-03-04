# Generated by Django 4.2.7 on 2024-01-24 23:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SistemaWeb', '0011_camion_fecha_actualizacion_alter_camion_conductor'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataGeneral',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_creacion', models.DateTimeField()),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True)),
                ('galones', models.DecimalField(decimal_places=3, max_digits=10)),
                ('documento', models.TextField(blank=True, null=True)),
                ('precio', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('total', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('kilometraje', models.DecimalField(decimal_places=1, max_digits=10)),
                ('conductor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SistemaWeb.conductor')),
                ('grifo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SistemaWeb.grifo')),
                ('placa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SistemaWeb.camion')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SistemaWeb.producto')),
            ],
        ),
    ]
