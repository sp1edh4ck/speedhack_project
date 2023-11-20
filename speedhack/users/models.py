from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.cache import cache
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

GENDER = [
    ("Не выбрано", 'Не выбрано'),
    ("Мужской", 'Мужской'),
    ("Женский", 'Женский'),
]

MAIN_POST = [
    ("пользователь", "пользователь"),
    ("заблокирован", "заблокирован"),
    ("дизайнер", "дизайнер"),
    ("главный дизайнер", "главный дизайнер"),
    ("куратор", "куратор"),
    ("арбитр", "арбитр"),
    ("главный арбитр", "главный арбитр"),
    ("бот", "бот"),
    ("администратор", "администратор"),
    ("разработчик", "разработчик"),
    ("гл. администратор", "гл. администратор"),
    ("владелец", "владелец"),
]

RANK_LVL = [
    ("1", "1"),
    ("0", "0"),
    ("2", "2"),
    ("3", "3"),
    ("4", "4"),
    ("5", "5"),
    ("6", "6"),
    ("7", "7"),
    ("8", "8"),
    ("9", "9"),
]

PRIVILEGE = [
    ("нет привилегий", "нет привилегий"),
    ("местный", "местный"),
    ("постоялец", "постоялец"),
    ("эксперт", "эксперт"),
    ("гуру", "гуру"),
    ("искусственный интелект", "искусственный интелект"),
]

MARKET_PRIVILEGE = [
    ("нет привилегий", "нет привилегий"),
    ("продавец", "продавец"),
    ("доверенный продавец", "доверенный продавец"),
    ("партнёр", "партнёр"),
]

BUY_PRIVILEGE = [
    ("нет привилегий", "нет привилегий"),
    ("легенда", "легенда"),
    ("суприм", "суприм"),
    ("уник", "уник"),
]

USERNAME_STYLE = [
    ("gray-un", ".gray-un"),
    ("white-shadow-un", ".white-shadow-un"),
    ("purple-white-un", ".purple-white-un"),
    ("grad-wb-un", ".grad-wb-un"),
    ("red-shadow-un", ".red-shadow-un"),
    ("grad-pwv-un", ".grad-pwv-un"),
    ("grad-bvr-un", ".grad-bvr-un"),
    ("grad-p-double-un", ".grad-p-double-un"),
    ("pink-shadow-un", ".pink-shadow-un"),
    ("purple-shadow-un", ".purple-shadow-un"),
    ("light-green-shadow-un", ".light-green-shadow-un"),
    ("grad-wp-un", ".grad-wp-un"),
    ("grad-wy-un", ".grad-wy-un"),
    ("grad-pp-un", ".grad-pp-un"),
    ("light-red-shadow-un", ".light-red-shadow-un"),
    ("blue-shadow-un", ".blue-shadow-un"),
    ("white-double-shadow-un", ".white-double-shadow-un"),
    ("blue-light-shadow-un", ".blue-light-shadow-un"),
    ("dark-green-shadow-un", ".dark-green-shadow-un"),
    ("blue-p-shadow-un", ".blue-p-shadow-un"),
    ("black-shadow-un", ".black-shadow-un"),
    ("red-orange-shadow-un", ".red-orange-shadow-un"),
    ("light-blue-double-shadow-un", ".light-blue-double-shadow-un"),
    ("aquamarine-shadow-un", ".aquamarine-shadow-un"),
    ("green-so-beautifull-un", ".green-so-beautifull-un"),
]

RANK_STYLE = [
    ("gray-role", ".gray-role"),
    ("green-yellow-role", ".green-yellow-role"),
    ("milk-pink-role", ".milk-pink-role"),
    ("purple-aquamarine-role", ".purple-aquamarine-role"),
    ("red-purple-role", ".red-purple-role"),
    ("yellow-green-role", ".yellow-green-role"),
    ("blue-pink-role", ".blue-pink-role"),
]


class CustomUser(AbstractUser):
    activation_code = models.CharField(max_length=6, blank=True)
    likes = models.IntegerField(verbose_name='Симпатии', default=0)
    balance = models.IntegerField(verbose_name='Баланс', default=0)
    save_deposit = models.IntegerField(verbose_name='Страховой депозит', default=0)
    gender = models.TextField(verbose_name='Пол', choices=GENDER, default=GENDER[0][0])
    username_style = models.TextField(verbose_name='Стиль имени', choices=USERNAME_STYLE, default=USERNAME_STYLE[0][0])
    banner = models.TextField(verbose_name='', choices=RANK_STYLE, default=RANK_STYLE[0][0])
    brt_day = models.CharField(verbose_name='День', max_length=2, blank=True, null=True)
    brt_month = models.CharField(verbose_name='Месяц', max_length=10, blank=True, null=True)
    brt_year = models.CharField(verbose_name='Год', max_length=4, blank=True, null=True)
    occupation = models.CharField(verbose_name='Род занятий', max_length=200, default='')
    interests = models.CharField(verbose_name='Интересы', max_length=200, default='')
    description = models.CharField(verbose_name='Описание', max_length=200, default='')
    rank = models.TextField(verbose_name='Должность', choices=MAIN_POST, default=MAIN_POST[0][0])
    rank_lvl = models.TextField(verbose_name='Уровень доступа', choices=RANK_LVL, default=RANK_LVL[0][0])
    save_rank = models.TextField(verbose_name='Сохранённый ранг', default='')
    privilege = models.TextField(verbose_name='Ранг', choices=PRIVILEGE, default=PRIVILEGE[0][0])
    market_privilege = models.TextField(verbose_name='Привилегия на маркете', choices=MARKET_PRIVILEGE, default=MARKET_PRIVILEGE[0][0])
    buy_privilege = models.TextField(verbose_name='Платные привилегии', choices=BUY_PRIVILEGE, default=BUY_PRIVILEGE[0][0])
    time_buy_privilege = models.DateField(verbose_name='Дата покупки привилегии', default=timezone.now())
    time_buy_profile_sub = models.DateField(verbose_name='Дата покупки фона профиля', default=timezone.now())
    time_buy_market_privilege = models.DateField(verbose_name='Дата покупки доступа к маркету', default=timezone.now())
    profile_sub = models.BooleanField(verbose_name='Доступ к фону профиля', default=False)
    messages = models.IntegerField(verbose_name='Сообщения', default=0)
    tg_link = models.CharField(verbose_name='Ссылка на телеграм', max_length=70, default='', blank=True)
    subscriber = models.IntegerField(verbose_name='Подписчики', default=0)
    scam = models.BooleanField(verbose_name='Скам', default=False)
    avatar = models.ImageField(
        verbose_name='Аватар',
        upload_to='avatars/',
        default='default.png',
        null=True,
        blank=True,
    )
    profile_background = models.ImageField(
        verbose_name='Фон профиля',
        upload_to='backgrounds/',
        null=True,
        blank=True,
    )

    def is_online(self):
        last_seen = cache.get(f'last-seen-{self.id}')
        if last_seen is not None and timezone.now() < last_seen + timezone.timedelta(seconds=60):
            return True
        return False

    # last_online = models.DateTimeField(default=timezone.now, blank=True, null=True)

    # def is_online(self):
    #     if self.last_online:
    #         return (timezone.now() - self.last_online) < timezone.timedelta(minutes=1)
    #     return False

    # def get_online_info(self):
    #     if self.is_online():
    #         return _('В сети')
    #     if self.last_online:
    #         return _('В сети {}').format(naturaltime(self.last_online))
    #     return _('Неизвестно')

    def __str__(self):
        return self.username


class IpUser(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='ip_user',
    )
    ip_address = models.CharField(max_length=19, verbose_name='Ip-адресс пользователя')
    banned = models.BooleanField(default=False, verbose_name='Блокировка ip-адресса')

    def __str__(self):
        return self.ip_address
