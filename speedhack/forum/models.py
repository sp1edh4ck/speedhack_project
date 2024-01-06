from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

CATEGORY = [
    ("Разблокировка аккаунта", "Разблокировка аккаунта"),
    ("Проблема с пополнением средств", "Проблема с пополнением средств"),
    ("Проблема с выводом средств", "Проблема с выводом средств"),
    ("Разблокировка с причиной 'Вбив/отмыв'", "Разблокировка с причиной 'Вбив/отмыв'"),
    ("Возврат средств за привилегию", "Возврат средств за привилегию"),
    ("Смена почты на аккаунте", "Смена почты на аккаунте"),
    ("Разблокировка с причиной 'Взломан'", "Разблокировка с причиной 'Взломан'"),
    ("Другое", "Другое"),
]

PRIORITY = [
    ("Низкий", "Низкий"),
    ("Средний", "Средний"),
    ("Высокий", "Высокий"),
]

PRIORITY_LVL = [
    ("1", "1"),
    ("2", "2"),
    ("3", "3"),
]

REQUEST = [
    ("Нет", "Нет"),
    ("Да", "Да"),
]


class Group(models.Model):
    title = models.CharField(unique=True, max_length=50, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='Уникальный адрес')

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return self.title


class Helper(models.Model):
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        null=True,
        related_name='groups',
        verbose_name='Группа',
    )
    helper = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='group',
        verbose_name='Куратор',
    )


class Ads(models.Model):
    title = models.CharField(verbose_name='Заголовок', max_length=100)
    post_id = models.CharField(verbose_name='Ссылка', max_length=10)
    weeks = models.IntegerField(verbose_name='Кол-во оплаченных недель')
    author = models.CharField(verbose_name='Автор рекламы', max_length=15)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации', blank=True, null=True)

    class Meta:
        verbose_name = 'Рекламный пост'
        verbose_name_plural = 'Рекламные посты'
        ordering = ('-created',)


class Forum(models.Model):
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        null=True,
        related_name='posts',
        verbose_name='Группа',
    )
    title = models.CharField(verbose_name='Заголовок', max_length=55)
    text = models.TextField(verbose_name='Текст', max_length=5000)
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='posts',
    )
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to='posts/',
        blank=True,
    )
    closed = models.BooleanField(
        default=False,
        verbose_name='Закрытая тема',
    )
    edit = models.BooleanField(
        default=False,
        verbose_name='Пост был отредактирован',
    )
    open_activities = models.BooleanField(
        default=False,
        verbose_name='Активности доступны',
    )

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ('-pub_date',)

    def __str__(self):
        number_of_chars = 15
        return self.text[:number_of_chars]


class HelpForum(models.Model):
    category = models.TextField(verbose_name='Категория', choices=CATEGORY, default=CATEGORY[0][0])
    priority = models.TextField(verbose_name='Приоритет', choices=PRIORITY, default=PRIORITY[0][0])
    priority_lvl = models.TextField(verbose_name='Уровень приоритета', choices=PRIORITY_LVL, default=PRIORITY_LVL[0][0])
    title = models.CharField(verbose_name='Заголовок', max_length=60)
    request = models.TextField(verbose_name='Обращение к админу', choices=REQUEST, default=REQUEST[0][0])
    description = models.TextField(
        verbose_name='Описание вопроса',
        max_length=2000,
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )
    open = models.BooleanField(
        default=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tickets',
        verbose_name='Автор',
    )

    class Meta:
        verbose_name = 'Тикет'
        verbose_name_plural = 'Тикеты'
        ordering = ('-open', '-priority_lvl', 'request', '-created',)


class HelpAnswer(models.Model):
    ticket = models.ForeignKey(
        HelpForum,
        on_delete=models.CASCADE,
        related_name='answer',
        verbose_name='Тикет',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name='Автор',
    )
    text = models.TextField(
        verbose_name='Текст комментария',
        max_length=2000,
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


class Viewer(models.Model):
    post = models.ForeignKey(
        Forum,
        null=True,
        on_delete=models.CASCADE,
        related_name='viewer',
        verbose_name='Пост',
    )
    user = models.ForeignKey(
        User,
        null=True,
        on_delete=models.CASCADE,
        related_name='viewers',
        verbose_name='Пользователь',
    )


class Like(models.Model):
    post = models.ForeignKey(
        Forum,
        on_delete=models.CASCADE,
        related_name='like',
        verbose_name='Пост',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='liker',
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='liking',
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата лайка',
    )

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'


class Symp(models.Model):
    post = models.ForeignKey(
        Forum,
        on_delete=models.CASCADE,
        related_name='symp',
        verbose_name='Пост',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='symper',
        verbose_name='Тот кому поставили',
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='symping',
        verbose_name='Тот кто поставил',
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата симпатии',
    )

    class Meta:
        verbose_name = 'Симпатия'
        verbose_name_plural = 'Симпатии'


class Comment(models.Model):
    post = models.ForeignKey(
        Forum,
        on_delete=models.CASCADE,
        related_name='comment',
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
        blank=True,
    )
    edit = models.BooleanField(
        default=False,
        verbose_name='Комментарий был отредактирован',
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class CommentSymp(models.Model):
    comment = models.ForeignKey(
        Comment,
        null=True,
        on_delete=models.CASCADE,
        related_name='comment_symp',
        verbose_name='Комментарий',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comment_symper',
        verbose_name='Тот кому поставили',
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comment_symping',
        verbose_name='Тот кто поставили',
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата симпатии',
    )

    class Meta:
        verbose_name = 'Симпатия на комментарии'
        verbose_name_plural = 'Симпатии на комментарии'


class ProfileComment(models.Model):
    profile = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Профиль',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author',
        verbose_name='Автор',
    )
    text = models.TextField(
        verbose_name='Текст комментария',
        max_length=2000,
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )

    class Meta:
        verbose_name = 'Комментарий на стене пользователя'
        verbose_name_plural = 'Комментарии на стене пользователя'
        ordering = ('-created',)


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


class Favourites(models.Model):
    post = models.ForeignKey(
        Forum,
        on_delete=models.CASCADE,
        verbose_name='Пост',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор добавления поста в избранное',
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления в избранное',
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        ordering = ('-created',)


# Система личных сообщений
# class Message(models.Model):
#     author = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name='message_author',
#         verbose_name='Автор',
#     )
#     user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name='message_user',
#         verbose_name='Пользователь',
#     )
#     message = models.TextField(verbose_name='Сообщение',)
#     created = models.DateTimeField(
#         auto_now_add=True,
#         verbose_name='Дата отправки сообщения',
#     )
#     is_readed = models.BooleanField(verbose_name='Прочитано', default=False,)
 
#     class Meta:
#         ordering=['created']
 
#     def __str__(self):
#         return self.message


class Maecenas(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Меценат',
    )
    amount = models.IntegerField(
        default=0,
        verbose_name='Сумма',
    )
    date_created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )
    date_until = models.DateTimeField(
        verbose_name='Дата окончания',
    )
    active = models.BooleanField(
        default=False,
        verbose_name='Активный меценат',
    )

    class Meta:
        verbose_name = 'Меценат'
        verbose_name_plural = 'Меценаты'
