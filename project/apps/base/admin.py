from django.contrib import admin
from . import models

# Регистрация моделей для отображения в админке
@admin.register(models.User)
class UserAdmin(admin.ModelAdmin): # Название модели
    list_display = models.User.DisplayFields # Отображаемые поля
    search_fields = models.User.SearchableFields # Поисковые поля
    list_filter = models.User.FilterFields # Фильтрируемые поля


@admin.register(models.Windows)
class WindowsAdmin(admin.ModelAdmin):
    list_display = models.Windows.DisplayFields
    search_fields = models.Windows.SearchableFields
    list_filter = models.Windows.FilterFields


@admin.register(models.Queue)
class QueueAdmin(admin.ModelAdmin):
    list_display = models.Queue.DisplayFields
    search_fields = models.Queue.SearchableFields
    list_filter = models.Queue.FilterFields


@admin.register(models.Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = models.Notification.DisplayFields
    search_fields = models.Notification.SearchableFields
    list_filter = models.Notification.FilterFields
