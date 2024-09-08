from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_delete
from django.dispatch import receiver

# Модель пользователя, наследующая от AbstractUser
class User(AbstractUser):
    # Дополнительные поля пользователя
    username = models.CharField(max_length=256, null=True, verbose_name='Имя')
    email = models.EmailField(unique=True, null=True, verbose_name='Почта')
    login = models.CharField(max_length=256, null=True, verbose_name='Логин')
    avatar = models.ImageField(
        null=True, blank=True,
        upload_to='avatars',
        default="assets/img/icons/avatar.svg",
        verbose_name='Аватар'
    )

    # Поля даты создания и обновления
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    # Настройки отображения, поиска и фильтрации в админке
    DisplayFields = ['username', 'login', 'email', 'avatar', 'created', 'updated', 'id']
    SearchableFields = ['id', 'username', 'login', 'email', 'avatar', 'created', 'updated']
    FilterFields = ['created', 'updated']

    # Установка поля email как основного идентификатора пользователя
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # Метакласс и свод правил отображения в Админке по умолчанию
    class Meta:
        ordering = ['-id', '-updated']
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    # Представление модели в Админке
    def __str__(self):
        return self.username or self.email


# Модель окна
class Windows(models.Model):
    # Поля окна
    number = models.CharField(max_length=250, blank=True, null=True, verbose_name='Номер')

    # Поля даты создания и обновления
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    # Настройки отображения, поиска и фильтрации в админке
    DisplayFields = ['id', 'number', 'created', 'updated']
    SearchableFields = DisplayFields
    FilterFields = ['created', 'updated']

    # Метакласс и свод правил отображения в Админке по умолчанию
    class Meta:
        ordering = ['id', '-updated']
        verbose_name = 'окно'
        verbose_name_plural = 'окна'

    # Представление модели в Админке
    def __str__(self):
        return f'Окно {self.number}'


# Модель очереди
class Queue(models.Model):
    # Поля очереди
    number = models.CharField(max_length=250, blank=True, null=True, verbose_name='Номер')
    window = models.ForeignKey(Windows, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Окно')
    type = models.CharField(max_length=250, blank=True, null=True, verbose_name='Тип посылки')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Клиент')

    # Поля даты создания и обновления
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    # Настройки отображения, поиска и фильтрации в админке
    DisplayFields = ['id', 'number', 'window', 'type', 'user', 'created', 'updated']
    SearchableFields = DisplayFields
    FilterFields = ['created', 'updated']

    # Метакласс и свод правил отображения в Админке по умолчанию
    class Meta:
        ordering = ['id', '-created']
        verbose_name = 'очередь'
        verbose_name_plural = 'очереди'

    # Представление модели в Админке
    def __str__(self):
        return f'Очередь №{self.number}'


# Модель уведомления
class Notification(models.Model):
    # Поля уведомления
    number = models.CharField(max_length=250, blank=True, null=True, verbose_name='Номер')

    window = models.ForeignKey(Windows, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Окно')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Клиент')

    # Поля даты создания и обновления
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    # Настройки отображения, поиска и фильтрации в админке
    DisplayFields = ['id', 'number', 'window', 'user', 'created', 'updated']
    SearchableFields = DisplayFields
    FilterFields = ['created', 'updated']

    # Метакласс и свод правил отображения в Админке по умолчанию
    class Meta:
        ordering = ['-id', '-created']
        verbose_name = 'уведомление'
        verbose_name_plural = 'уведомления'

    # Представление модели в Админке
    def __str__(self):
        return f'Уведомление №{self.number}'


# Сигнал для создания уведомления при удалении очереди
@receiver(post_delete, sender=Queue)
def create_notification_on_queue_delete(sender, instance, **kwargs):
    # При удалении записи из модели Queue, создается новая запись в модели Notification
    Notification.objects.create(
        window=instance.window,
        user=instance.user,
        number=instance.number
    )
