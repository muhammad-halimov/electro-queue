const sendButtons = document.querySelectorAll('.send'); // Получение кнопок на страницах

let pass1 = document.getElementById('id_password1'); // Поля для паролей во время регистрации
let pass2 = document.getElementById('id_password2');

if (window.location.pathname === '/sign_up/'){
  pass1.placeholder = 'Ваш пароль'; // Установление плейсхолдеров на странице регистрации
  pass2.placeholder = 'Подтвердите пароль';
}

function generateQueueNumber() {
  return Math.random().toString(16).slice(-4); // Метод для генерации очереди
}

sendButtons.forEach((sendButton) => { // При нажатии одной из кнопок на странице
  sendButton.addEventListener('click', async (event) => {
    event.preventDefault(); // Остановка действия по умолчанию

    const queueNumber = generateQueueNumber();

    try {
      const response = await fetch('/post_queue/', { // Страница в которую идет запрос
        method: 'POST',
        body: JSON.stringify({ queue_number: queueNumber, mail_type: sendButton.value }),
        // То что будет отправлено на сервер в БД
        headers: {
          'X-CSRFToken': getCookie('csrftoken'),
          'Content-Type': 'application/json',
        },
      }); // Отправка запроса добавление очереди в БД

      if (response.ok) { // Получение ответа от сервера
        const data = await response.json();
        alert(`Очередь ${data.queue_number} успешно добавлена в базу данных. Окно ${data.window_number}`);
      } else {
        alert('Ошибка при добавлении очереди в базу данных. Либо вы не авторизованы');
      }
    } catch (error) { // Обработка исключений и ошибок
      console.error('Ошибка при отправке запроса:', error);
      alert('Произошла ошибка. Пожалуйста, попробуйте еще раз. Либо вы не авторизованы');
    }

    window.location.reload(); // Перезагрузка страницы
  });
});

function getCookie(name) { // Получения куки-токена для авторизации сессии на сервере
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }

  return cookieValue;
}
