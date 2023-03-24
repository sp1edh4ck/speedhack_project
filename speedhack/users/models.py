from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
	likes = models.IntegerField(verbose_name='Лайки', default=0)
	rank = models.TextField(verbose_name='Ранг', default='пользователь')
	messages = models.IntegerField(verbose_name='Сообщения', default=0)
	tg_link = models.TextField(verbose_name='Ссылка на телеграм', default='')
	subscriber = models.IntegerField(verbose_name='Подписчики', default=0)
	avatar = models.ImageField(verbose_name='Аватарка', default='default.png')

	def __str__(self):
		return self.username
