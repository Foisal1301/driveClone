# Generated by Django 3.2.16 on 2022-11-16 07:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_file_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='name',
        ),
    ]
