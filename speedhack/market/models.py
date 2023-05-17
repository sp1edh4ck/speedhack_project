from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MaxValueValidator

User = get_user_model()


class AccGroup(models.Model):
    title = models.CharField(unique=True, max_length=50, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='Уникальный адрес')

    class Meta:
        verbose_name = 'Платформа'
        verbose_name_plural = 'Платформы'

    def __str__(self):
        return self.title


class Market(models.Model):
    group = models.ForeignKey(
        AccGroup,
        on_delete=models.SET_NULL,
        null=True,
        related_name='acc',
        verbose_name='Платформа',
    )
    title = models.CharField(verbose_name='Заголовок', max_length=55)
    login = models.CharField(verbose_name='Логин', max_length=50)
    password = models.CharField(verbose_name='Пароль', max_length=100)
    email = models.CharField(verbose_name='Почта', max_length=100)
    email_password = models.CharField(verbose_name='Пароль от почты', max_length=100)
    price = models.IntegerField(verbose_name='Цена', validators=[MaxValueValidator(150000)])
    description = models.TextField(verbose_name='Описание', max_length=1000)
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    view = models.IntegerField(
        default=0,
        verbose_name='Просмотры'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Продавец',
        related_name='seller',
    )
    buyer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='Покупатель',
        related_name='buyer',
    )

    class Meta:
        verbose_name = 'Аккаунт'
        verbose_name_plural = 'Аккаунты'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.title
