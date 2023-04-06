from django.contrib.auth.models import AbstractUser
from django.db import models


GENDER = [
	("Не выбранно", 'Не выбранно'),
	("Мужской", 'Мужской'),
	("Женский", 'Женский'),
]


class CustomUser(AbstractUser):
	likes = models.IntegerField(verbose_name='Лайки', default=0)
	balance = models.IntegerField(verbose_name='Баланс', default=0)
	gender = models.TextField(verbose_name='Пол', default='Не выбранно', choices=GENDER)
	birthday = models.DateField(verbose_name='День рождения', default=0, null=True)
	occupation = models.CharField(verbose_name='Род занятий', max_length=200, default='')
	interests = models.CharField(verbose_name='Интересы', max_length=200, default='')
	description = models.CharField(verbose_name='Описание', max_length=200, default='')
	rank = models.TextField(verbose_name='Ранг', default='пользователь')
	messages = models.IntegerField(verbose_name='Сообщения', default=0)
	tg_link = models.CharField(verbose_name='Ссылка на телеграм', max_length=70, default='', blank=True)
	subscriber = models.IntegerField(verbose_name='Подписчики', default=0)
	avatar = models.ImageField(
		verbose_name='Аватар',
		upload_to='avatars/',
		default='default.png',
		null=True,
		blank=True,
	)

	def __str__(self):
		return self.username
