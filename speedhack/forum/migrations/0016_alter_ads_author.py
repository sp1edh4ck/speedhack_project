# Generated by Django 3.2.18 on 2023-11-29 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0015_alter_ads_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ads',
            name='author',
            field=models.CharField(default=123, max_length=15, verbose_name='Автор'),
            preserve_default=False,
        ),
    ]
