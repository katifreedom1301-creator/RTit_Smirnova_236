import datetime
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

print("=" * 50)
print("ТЕСТ 6: ВХОД ПО ВАЛИДНОМУ ТЕЛЕФОНУ И ПАРОЛЮ")
print("=" * 50)

# Определяем пути
project_root = os.path.dirname(os.path.abspath(__file__))
screenshots_dir = os.path.join(project_root, "screenshots")

# Создаем папку для скриншотов если её нет
if not os.path.exists(screenshots_dir):
    os.makedirs(screenshots_dir)
    print(f"Создана папка: {screenshots_dir}")
else:
    print(f"Папка {screenshots_dir} уже существует")

print("\n1. Загружаем данные из config.py...")
try:
    from config import TEST_ACCOUNTS
    print("✓ Конфигурационный файл загружен")
    
    # Берем данные первого аккаунта (с номером телефона)
    account = TEST_ACCOUNTS["acc1"]
    phone = account["phone"]
    password = account["password"]
    
    print(f"✓ Используем данные аккаунта acc1:")
    print(f"  Телефон: {phone}")
    print(f"  Пароль: {password}")
    
except ImportError:
    print("✗ Ошибка: файл config.py не найден!")
    print("   Создайте файл config.py в папке tests/")
    exit()
except KeyError as e:
    print(f"✗ Ошибка: ключ {e} не найден в config.py")
    exit()

print("\n2. Запускаем браузер...")
driver = webdriver.Chrome()
driver.maximize_window()
print("   Браузер открыт (на весь экран)")

print("\n3. Открываем страницу входа Ростелеком...")
url = "https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth?client_id=account_b2c&redirect_uri=https://b2c.passport.rt.ru/account_b2c/login&response_type=code&scope=openid&state=686d7744-c37c-4272-a461-80090fecb52f"
driver.get(url)
print("   Страница входа открыта")

time.sleep(3)

print(f"\n4. Заголовок страницы: {driver.title}")

print("\n5. Находим поля формы входа...")
try:
    # Ищем поле для логина (система сама определит телефон или почта)
    login_field = driver.find_element(By.CSS_SELECTOR, "input[name='username'], input#username, input[type='text']")
    print("   ✓ Поле для логина найдено")
    
    # Ищем поле для пароля
    password_field = driver.find_element(By.CSS_SELECTOR, "input[name='password'], input#password, input[type='password']")
    print("   ✓ Поле для пароля найдено")
    
    # Ищем кнопку "Войти"
    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit'], button#kc-login, button[name='login']")
    print("   ✓ Кнопка 'Войти' найдена")
    
except Exception as e:
    print(f"   ✗ Ошибка при поиске элементов формы: {e}")
    print("   Делаем скриншот для отладки...")
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    debug_screenshot = os.path.join(screenshots_dir, f"test_06_debug_{timestamp}.png")
    driver.save_screenshot(debug_screenshot)
    print(f"   Скриншот сохранен: test_06_debug_{timestamp}.png")
    driver.quit()
    exit()

print("\n6. Заполняем форму входа...")

try:
    # Вводим номер телефона
    login_field.clear()
    login_field.send_keys(phone)
    print(f"   ✓ Введен телефон: {phone}")
    time.sleep(0.5)
    
    # Вводим пароль
    password_field.clear()
    password_field.send_keys(password)
    print(f"   ✓ Введен пароль")
    time.sleep(0.5)
    
    print("\n7. Делаем скриншот заполненной формы...")
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    before_login_screenshot = os.path.join(screenshots_dir, f"test_06_before_login_{timestamp}.png")
    driver.save_screenshot(before_login_screenshot)
    print(f"   Скриншот сохранен: test_06_before_login_{timestamp}.png")
    
    print("\n8. Нажимаем кнопку 'Войти'...")
    login_button.click()
    print("   ✓ Нажата кнопка 'Войти'")
    
    # Ждем обработки входа
    print("   Ждем обработки входа (5 секунд)...")
    time.sleep(5)
    
    print("\n9. Анализируем результат входа...")
    
    # Получаем текущий URL
    current_url = driver.current_url
    print(f"   Текущий URL: {current_url}")
    
    # Получаем новый заголовок
    new_title = driver.title
    print(f"   Новый заголовок: {new_title}")
    
    # Проверяем успешность входа
    login_successful = False
    success_indicators = []
    
    # Индикаторы успешного входа
    # 1. URL изменился (не остались на странице входа)
    if "auth/realms/b2c" not in current_url:
        login_successful = True
        success_indicators.append("URL изменился")
    
    # 2. Проверяем есть ли приветствие или имя пользователя
    try:
        welcome_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Добро пожаловать') or contains(text(), 'Привет') or contains(text(), 'Кабинет')]")
        for elem in welcome_elements:
            if elem.is_displayed():
                login_successful = True
                success_indicators.append(f"Найдено приветствие: {elem.text[:30]}...")
                break
    except:
        pass
    
    # 3. Проверяем есть ли имя/фамилия из аккаунта
    try:
        name_elements = driver.find_elements(By.XPATH, f"//*[contains(text(), '{account.get('first_name', '')}') or contains(text(), '{account.get('last_name', '')}')]")
        for elem in name_elements:
            if elem.is_displayed():
                login_successful = True
                success_indicators.append(f"Найдено имя пользователя: {elem.text[:30]}...")
                break
    except:
        pass
    
    # 4. Проверяем наличие кнопки "Выйти" или личного кабинета
    try:
        logout_buttons = driver.find_elements(By.XPATH, "//*[contains(text(), 'Выйти') or contains(text(), 'Выход')]")
        for btn in logout_buttons:
            if btn.is_displayed():
                login_successful = True
                success_indicators.append("Найдена кнопка 'Выйти'")
                break
    except:
        pass
    
    # 5. Проверяем отсутствие ошибок
    error_elements = driver.find_elements(By.CSS_SELECTOR, ".alert-error, .rt-input-container__error, .text-danger")
    visible_errors = []
    for error in error_elements:
        if error.is_displayed() and error.text.strip():
            visible_errors.append(error.text.strip())
    
    if visible_errors:
        login_successful = False
        print(f"   Обнаружены ошибки: {visible_errors[0][:50]}...")
    
    print("\n10. Делаем скриншот результата...")
    after_login_screenshot = os.path.join(screenshots_dir, f"test_06_after_login_{timestamp}.png")
    driver.save_screenshot(after_login_screenshot)
    print(f"   Скриншот сохранен: test_06_after_login_{timestamp}.png")
    
    # Выводим итог
    print("\n" + "=" * 40)
    print("РЕЗУЛЬТАТ ТЕСТА 6:")
    print("=" * 40)
    
    if login_successful:
        print("✓ УСПЕШНЫЙ ВХОД!")
        if success_indicators:
            print("   Признаки успеха:")
            for indicator in success_indicators:
                print(f"   - {indicator}")
    else:
        print("✗ ВХОД НЕ УДАЛСЯ")
        if visible_errors:
            print("   Причины:")
            for error in visible_errors[:2]:  # Показываем первые 2 ошибки
                print(f"   - {error}")
        else:
            print("   Не удалось определить причину")
        
except Exception as e:
    print(f"   ✗ Ошибка при выполнении входа: {e}")
    
    # Делаем скриншот ошибки
    error_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    error_screenshot = os.path.join(screenshots_dir, f"test_06_error_{error_timestamp}.png")
    driver.save_screenshot(error_screenshot)
    print(f"   Скриншот ошибки сохранен: test_06_error_{error_timestamp}.png")

print("\n11. Закрываем браузер...")
driver.quit()
print("   Браузер закрыт")

print("\n" + "=" * 50)
print("ИТОГИ ТЕСТА 6:")
print("=" * 50)

print("\nВыполнено:")
print("✓ Загружены данные из config.py (acc1)")
print("✓ Открыта страница входа")
print("✓ Найдены элементы формы")
print("✓ Заполнена форма (телефон + пароль)")
print(f"✓ Сделано 2 скриншота:")
print(f"  - test_06_before_login_{timestamp}.png (перед входом)")
print(f"  - test_06_after_login_{timestamp}.png (после входа)")
print("✓ Нажата кнопка 'Войти'")
print("✓ Проанализирован результат")

if 'login_successful' in locals():
    if login_successful:
        print("\n✓ РЕЗУЛЬТАТ: ВХОД УСПЕШЕН")
    else:
        print("\n✗ РЕЗУЛЬТАТ: ВХОД НЕ УДАЛСЯ")

print("\n" + "=" * 50)
print("ТЕСТ 6 ЗАВЕРШЕН!")
print("=" * 50)

input("\nНажмите Enter для выхода...")