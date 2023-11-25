# Generated by Django 3.2.18 on 2023-11-25 18:02

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20231120_2125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='time_buy_market_privilege',
            field=models.DateField(default=datetime.datetime(2023, 11, 25, 18, 2, 28, 495458, tzinfo=utc), verbose_name='Дата покупки доступа к маркету'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='time_buy_privilege',
            field=models.DateField(default=datetime.datetime(2023, 11, 25, 18, 2, 28, 495458, tzinfo=utc), verbose_name='Дата покупки привилегии'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='time_buy_profile_sub',
            field=models.DateField(default=datetime.datetime(2023, 11, 25, 18, 2, 28, 495458, tzinfo=utc), verbose_name='Дата покупки фона профиля'),
        ),
    ]
