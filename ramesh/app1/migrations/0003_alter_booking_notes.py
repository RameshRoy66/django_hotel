# Generated by Django 5.2.2 on 2025-06-07 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0002_booking'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='notes',
            field=models.TextField(),
        ),
    ]
