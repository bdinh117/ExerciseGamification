# Generated by Django 3.1.7 on 2021-04-12 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamifi', '0009_auto_20210412_0140'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='experience',
            field=models.IntegerField(default=0),
        ),
    ]
