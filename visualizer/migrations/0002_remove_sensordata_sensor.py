# Generated by Django 3.1.14 on 2022-01-15 06:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visualizer', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sensordata',
            name='sensor',
        ),
    ]
