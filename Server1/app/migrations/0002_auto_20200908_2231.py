# Generated by Django 3.1.1 on 2020-09-08 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='backtest',
            name='Initial_Capital',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='backtest',
            name='Quantity',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='backtest',
            name='Time_frame',
            field=models.CharField(default='1min', max_length=200),
            preserve_default=False,
        ),
    ]