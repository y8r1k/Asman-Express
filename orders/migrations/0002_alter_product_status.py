# Generated by Django 5.1.4 on 2024-12-08 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='status',
            field=models.CharField(choices=[('issued', 'Выдан'), ('not_issued', 'Не выдан')], default='not_issued', max_length=20),
        ),
    ]