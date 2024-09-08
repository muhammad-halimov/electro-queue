import json
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from . import models
from . import forms

# Функция для отображения главной страницы
def main(request):
    # Получение 5 последних записей из модели Queue
    queues = models.Queue.objects.all()[:5]

    # Если пользователь авторизован, получение 5 последних записей из его очереди
    if request.user.is_authenticated:
        uqueues = request.user.queue_set.all()[:5]
    else:
        uqueues = []

    # Передача данных в контекст для рендеринга шаблона
    context = {'queues': queues, 'uqueues': uqueues}
    return render(request, template_name='base/main.htm', context=context)


# Функция для отображения страницы входа в систему
def sign_in(request):
    # Если пользователь уже авторизован, перенаправление на главную страницу
    if request.user.is_authenticated:
        return redirect('main')

    # Обработка POST-запроса формы входа
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        # Проверка существования пользователя с указанным email-адресом
        # noinspection PyBroadException
        try:
            models.User.objects.get(email=email)
        except BaseException:
            messages.error(request, 'User does not exist')

        # Аутентификация пользователя
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('main')
        else:
            messages.error(request, 'Username OR password does not exist')

    # Получение 5 последних записей из модели Queue
    queues = models.Queue.objects.all()[:5]

    # Если пользователь авторизован, получение 5 последних записей из его очереди
    if request.user.is_authenticated:
        uqueues = request.user.queue_set.all()[:5]
    else:
        uqueues = []

    # Передача данных в контекст для рендеринга шаблона
    context = {'queues': queues, 'uqueues': uqueues}
    return render(request, template_name='base/sign_in.htm', context=context)


# Функция для отображения страницы регистрации
def sign_up(request):
    # Если пользователь уже авторизован, перенаправление на главную страницу
    if request.user.is_authenticated:
        return redirect('main')

    # Создание экземпляра формы регистрации
    form = forms.CustomUserCreationForm

    # Обработка POST-запроса формы регистрации
    if request.method == 'POST':
        form = forms.CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            form.save()
            login(request, user)
            return redirect('main')
        else:
            messages.error(request, 'Возникла ошибка в процессе регистрации')
            messages.error(request, 'Либо пароль слабый')

    # Получение 5 последних записей из модели Queue
    queues = models.Queue.objects.all()[:5]

    # Если пользователь авторизован, получение 5 последних записей из его очереди
    if request.user.is_authenticated:
        uqueues = request.user.queue_set.all()[:5]
    else:
        uqueues = []

    # Передача данных и формы в контекст для рендеринга шаблона
    context = {'queues': queues, 'uqueues': uqueues, 'form': form}

    return render(request, template_name='base/sign_up.htm', context=context)


# Функция для выхода пользователя из системы
def logout_page(request):
    logout(request)
    return redirect('main')


# Функция для отображения страницы кассы
def cash(request):
    # Получение 5 последних записей из модели Queue
    queues = models.Queue.objects.all()[:5]

    # Если пользователь авторизован, получение 5 последних записей из его очереди
    if request.user.is_authenticated:
        uqueues = request.user.queue_set.all()[:5]
    else:
        uqueues = []

    # Передача данных в контекст для рендеринга шаблона
    context = {'queues': queues, 'uqueues': uqueues}
    return render(request, template_name='base/cash.htm', context=context)


# Функция для отображения страницы почты
def mail(request):
    # Получение 5 последних записей из модели Queue
    queues = models.Queue.objects.all()[:5]

    # Если пользователь авторизован, получение 5 последних записей из его очереди
    if request.user.is_authenticated:
        uqueues = request.user.queue_set.all()[:5]
    else:
        uqueues = []

    # Передача данных в контекст для рендеринга шаблона
    context = {'queues': queues, 'uqueues': uqueues}
    return render(request, template_name='base/mail.htm', context=context)


# Функция для отображения страницы посылок
def package(request):
    # Получение 5 последних записей из модели Queue
    queues = models.Queue.objects.all()[:5]

    # Если пользователь авторизован, получение 5 последних записей из его очереди
    if request.user.is_authenticated:
        uqueues = request.user.queue_set.all()[:5]
    else:
        uqueues = []

    # Передача данных в контекст для рендеринга шаблона
    context = {'queues': queues, 'uqueues': uqueues}
    return render(request, template_name='base/package.htm', context=context)


# Функция для отображения страницы уведомлений
@login_required(login_url='sign_in')
def notifications(request):
    # Получение 5 последних записей из модели Queue
    queues = models.Queue.objects.all()[:5]

    # Получение всех уведомлений, связанных с текущим пользователем
    notifications_query = models.Notification.objects.filter(user=request.user)

    # Если пользователь авторизован, получение 5 последних записей из его очереди
    if request.user.is_authenticated:
        uqueues = request.user.queue_set.all()[:5]
    else:
        uqueues = []

    # Передача данных в контекст для рендеринга шаблона
    context = {'queues': queues, 'uqueues': uqueues, 'notifications': notifications_query}
    return render(request, template_name='base/notifications.htm', context=context)



@login_required(login_url='sign_in') # Требование для регистрации
@csrf_exempt # Игнорирование csrf_token
def post_queue(request): # Добавление очереди
    if request.method == 'POST':
        try:
            data = json.loads(request.body) # Берем данные из POST
            queue_number = data.get('queue_number')
            mail_type = data.get('mail_type')
            window = models.Windows.objects.order_by('?').first()

            queue = models.Queue.objects.create( # Создаем очередь с полученными данными
                number=queue_number,
                window=window,
                type=mail_type,
                user=request.user
            )

            queue.save() # Сохраняем очередь
            # Возвращаем promise в JS
            return JsonResponse({'success': True, 'queue_number': queue.number, 'window_number': queue.window.number})
        except (ValueError, KeyError): # Разного рода ошибки и исключение
            return JsonResponse({'error': 'Invalid request data'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=400)
