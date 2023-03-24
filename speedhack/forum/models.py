from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
	title = models.CharField(unique=True, max_length=50, verbose_name='Название')
	slug = models.SlugField(unique=True, verbose_name='Уникальный адрес')

	class Meta:
		verbose_name = 'Ранг'
		verbose_name_plural = 'Ранги'

	def __str__(self):
		return self.title


class Forum(models.Model):
	title = models.CharField(verbose_name='Заголовок', max_length=55)
	text = models.TextField(verbose_name='Текст', max_length=10000)
	pub_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
	author = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		verbose_name='Автор',
		related_name='posts'
	)
	image = models.ImageField(
		'Картинка',
		upload_to='posts/',
		blank=True
	)
	
	class Meta:
		verbose_name = 'Пост'
		verbose_name_plural = 'Посты'
		ordering = ('-pub_date',)

	def __str__(self):
		number_of_chars = 15
		return self.text[:number_of_chars]


class Comment(models.Model):
	post = models.ForeignKey(
		Forum,
		on_delete=models.CASCADE,
		related_name='comments',
		verbose_name='Пост',
	)
	author = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='comments',
		verbose_name='Автор',
	)
	text = models.TextField(
		verbose_name='Текст комментария',
		max_length=2000,
	)
	image = models.ImageField(
		'Картинка',
		upload_to='posts/images/',
		blank=True
	)
	created = models.DateTimeField(
		auto_now_add=True,
		verbose_name='Дата публикации',
	)

	class Meta:
		verbose_name = 'Комментарий'
		verbose_name_plural = 'Комментарии'


class ProfileComment(models.Model):
	author = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='profile_comments',
		verbose_name='Автор',
	)
	profile = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='profile_with_comments',
	)
	text = models.TextField(
		verbose_name='Текст комментария',
		max_length=2000,
	)
	image = models.ImageField(
		'Картинка',
		upload_to='posts/images/',
		blank=True
	)
	created = models.DateTimeField(
		auto_now_add=True,
		verbose_name='Дата публикации',
	)

	class Meta:
		verbose_name = 'Комментарий на стене пользователя'
		verbose_name_plural = 'Комментарии на стене пользователя'


class Follow(models.Model):
	user = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='follower',
	)
	author = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='following',
	)
 
	class Meta:
		verbose_name = 'Подписка'
		verbose_name_plural = 'Подписки'
		constraints = [
			models.UniqueConstraint(
				fields=('user', 'author'),
				name='unique_name_in_subsciber',
			)
		]
