TEST_ACCOUNTS = {
    "acc1": {  # account_1 - с номером
        "email": "katifreedom1301@gmail.com",
        "phone": "+79093683573", 
        "password": "QWyn31)(",
        "first_name": "Екатерина",
        "last_name": "Смирнова",
    },
    "acc2": {  # account_2 - с почтй
        "email": "ekosmirnova@kpfu.ru",
        "phone": "",
        "password": "ASgh48^^",
        "first_name": "Анна",
        "last_name": "Козлинкина",
    }
}

# Дополнительные данные для тестов
TEST_DATA = {
    # Неверные данные для тестов 08-11
    "invalid": {
        "wrong_password": "WrongPass123!",      # Неверный пароль
        "wrong_email": "wrong_email@example.com",  # Неверный email
        "wrong_phone": "+79999999999",          # Неверный номер
    },
    
    # Сообщения об ошибках (для проверки)
    "error_messages": {
        "invalid_credentials": "Неверный логин или пароль",
        "account_not_found": "Учетная запись не найдена",
        "empty_fields": "Заполните все поля",
    }
}