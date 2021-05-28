# Generated by Django 3.0.5 on 2021-04-29 17:44

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfileDB',
            fields=[
                ('username', models.CharField(max_length=25, primary_key=True, serialize=False)),
                ('phonenumber', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None, unique=True)),
                ('country', models.CharField(blank=True, max_length=15)),
                ('address', models.CharField(blank=True, max_length=50)),
                ('state', models.CharField(blank=True, max_length=15)),
                ('description', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.DeleteModel(
            name='Musician',
        ),
    ]
