# Generated by Django 5.1.2 on 2024-10-18 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='password',
            field=models.CharField(max_length=128, verbose_name='password'),
        ),
    ]
