# Generated by Django 3.2.16 on 2022-11-20 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_available'),
    ]

    operations = [
        migrations.AlterField(
            model_name='available',
            name='storage',
            field=models.FloatField(),
        ),
    ]
