# Generated by Django 3.1.7 on 2021-04-18 22:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gamifi', '0013_auto_20210418_0012'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('finished', models.BooleanField(default=False)),
                ('duration', models.PositiveSmallIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('category', models.CharField(max_length=20)),
                ('name', models.CharField(choices=[('Running', 'RUNNING'), ('Swimming', 'SWIMMING'), ('Biking', 'BIKING'), ('Walking', 'WALKING')], max_length=50)),
                ('exp', models.IntegerField(default=100)),
                ('duration_suffix', models.CharField(choices=[('Repetitions', 'repetitions'), ('Minutes', 'minutes'), ('Hours', 'hours'), ('Laps', 'laps')], max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ExerciseChoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('image_url', models.CharField(max_length=100)),
                ('category', models.CharField(max_length=20)),
            ],
        ),
        migrations.RemoveField(
            model_name='flexibilityexercise',
            name='user',
        ),
        migrations.RemoveField(
            model_name='strengthexercise',
            name='user',
        ),
        migrations.DeleteModel(
            name='AerobicExercise',
        ),
        migrations.DeleteModel(
            name='FlexibilityExercise',
        ),
        migrations.DeleteModel(
            name='StrengthExercise',
        ),
    ]
