from django.urls import path
from . import views

# Маршрут приложения
urlpatterns = [
    path('', views.main, name='main'), # маршрут, функция(вью) отвечающая за него, имя для ориентации в приложении
    path('cash/', views.cash, name='cash'),
    path('mail/', views.mail, name='mail'),
    path('package/', views.package, name='package'),
    path('notifications/', views.notifications, name='notifications'),
    path('sign_in/', views.sign_in, name='sign_in'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('logout/', views.logout_page, name='logout'),
    path('post_queue/', views.post_queue, name='post_queue'),
]
