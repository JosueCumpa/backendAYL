# Generated by Django 4.2.7 on 2024-01-25 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SistemaWeb', '0012_datageneral'),
    ]

    operations = [
        migrations.AddField(
            model_name='datageneral',
            name='traspaso_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
