# Generated by Django 2.2.5 on 2019-09-09 06:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_auto_20190908_1252'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='seats_available',
        ),
    ]
