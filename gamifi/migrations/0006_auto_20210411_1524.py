# Generated by Django 3.1.7 on 2021-04-11 19:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gamifi', '0005_exercise_exp'),
    ]

    operations = [
        migrations.CreateModel(
            name='AerobicExercise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('finished', models.BooleanField(default=False)),
                ('duration', models.PositiveSmallIntegerField()),
                ('name', models.CharField(choices=[('Running', 'RUNNING'), ('Swimming', 'SWIMMING'), ('Biking', 'BIKING'), ('Walking', 'WALKING')], max_length=50)),
                ('exp', models.IntegerField(default=100)),
                ('duration_suffix', models.CharField(choices=[('Repetitions', 'repetitions'), ('Minutes', 'minutes'), ('Hours', 'hours'), ('Laps', 'laps')], max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FlexibilityExercise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('finished', models.BooleanField(default=False)),
                ('duration', models.PositiveSmallIntegerField()),
                ('name', models.CharField(choices=[('Lunges', 'LUNGES'), ('Butterfly Stretch', 'BUTTERFLY STRETCH'), ('Yoga', 'YOGA')], max_length=50)),
                ('exp', models.IntegerField(default=50)),
                ('duration_suffix', models.CharField(choices=[('Repetitions', 'repetitions'), ('Sets', 'sets'), ('Minutes', 'minutes')], max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StrengthExercise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('finished', models.BooleanField(default=False)),
                ('duration', models.PositiveSmallIntegerField()),
                ('name', models.CharField(choices=[('Push-Ups', 'PUSH-UPS'), ('Deadlift', 'DEADLIFT'), ('Pull-ups', 'PULL-UPS')], max_length=50)),
                ('exp', models.IntegerField(default=217)),
                ('duration_suffix', models.CharField(choices=[('Repetitions', 'repetitions'), ('Sets', 'sets'), ('Minutes', 'minutes')], max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='Exercise',
        ),
    ]
