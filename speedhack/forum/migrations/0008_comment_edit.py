# Generated by Django 3.2.18 on 2023-12-07 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0007_auto_20231207_2015'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='edit',
            field=models.BooleanField(default=False, verbose_name='Комментарий был отредактирован'),
        ),
    ]
