# Generated by Django 3.1.7 on 2021-04-12 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamifi', '0006_auto_20210411_1524'),
    ]

    operations = [
        migrations.AddField(
            model_name='aerobicexercise',
            name='created_at',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='flexibilityexercise',
            name='created_at',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='strengthexercise',
            name='created_at',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]