# Generated by Django 3.2.18 on 2023-11-24 18:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forum', '0008_auto_20231124_1345'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='helpforum',
            options={'ordering': ('-open', '-priority_lvl'), 'verbose_name': 'Тикет', 'verbose_name_plural': 'Тикеты'},
        ),
        migrations.AlterField(
            model_name='helpanswer',
            name='ticket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answer', to='forum.helpforum', verbose_name='Тикет'),
        ),
        migrations.AlterField(
            model_name='helpforum',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='helpforum',
            name='description',
            field=models.TextField(max_length=2000, verbose_name='Описание вопроса'),
        ),
    ]
