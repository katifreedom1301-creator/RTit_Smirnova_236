import datetime
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

print("=" * 50)
print("ТЕСТ 7: ВХОД ПО ВАЛИДНОЙ ПОЧТЕ И ПАРОЛЮ")
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
    
    # Берем данные второго аккаунта (только почта)
    account = TEST_ACCOUNTS["acc2"]
    email = account["email"]
    password = account["password"]
    
    print(f"✓ Используем данные аккаунта acc2:")
    print(f"  Почта: {email}")
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
    # Ищем поле для логина
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
    debug_screenshot = os.path.join(screenshots_dir, f"test_07_debug_{timestamp}.png")
    driver.save_screenshot(debug_screenshot)
    print(f"   Скриншот сохранен: test_07_debug_{timestamp}.png")
    driver.quit()
    exit()

print("\n6. Заполняем форму входа...")

try:
    # Вводим email (система сама определит что это почта)
    login_field.clear()
    login_field.send_keys(email)
    print(f"   ✓ Введена почта: {email}")
    time.sleep(0.5)
    
    # Вводим пароль
    password_field.clear()
    password_field.send_keys(password)
    print(f"   ✓ Введен пароль")
    time.sleep(0.5)
    
    print("\n7. Делаем скриншот заполненной формы...")
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    before_login_screenshot = os.path.join(screenshots_dir, f"test_07_before_login_{timestamp}.png")
    driver.save_screenshot(before_login_screenshot)
    print(f"   Скриншот сохранен: test_07_before_login_{timestamp}.png")
    
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
    # 1. URL изменился
    if "auth/realms/b2c" not in current_url:
        login_successful = True
        success_indicators.append("URL изменился (не страница входа)")
    
    # 2. Проверяем есть ли приветствие
    try:
        welcome_texts = ["Добро пожаловать", "Привет", "Кабинет", "Личный кабинет", "Учётная запись"]
        for text in welcome_texts:
            try:
                elements = driver.find_elements(By.XPATH, f"//*[contains(text(), '{text}')]")
                for elem in elements:
                    if elem.is_displayed():
                        login_successful = True
                        success_indicators.append(f"Найдено: {elem.text[:30]}...")
                        break
                if login_successful:
                    break
            except:
                continue
    except:
        pass
    
    # 3. Проверяем наличие кнопки "Выйти"
    try:
        logout_texts = ["Выйти", "Выход", "Logout", "Выйти из аккаунта"]
        for text in logout_texts:
            try:
                elements = driver.find_elements(By.XPATH, f"//*[contains(text(), '{text}')]")
                for elem in elements:
                    if elem.is_displayed():
                        login_successful = True
                        success_indicators.append(f"Найдена кнопка: {text}")
                        break
                if login_successful:
                    break
            except:
                continue
    except:
        pass
    
    # 4. Проверяем отсутствие ошибок
    error_elements = driver.find_elements(By.CSS_SELECTOR, ".alert-error, .rt-input-container__error, .text-danger, [class*='error']")
    visible_errors = []
    for error in error_elements:
        if error.is_displayed() and error.text.strip():
            visible_errors.append(error.text.strip())
    
    if visible_errors:
        login_successful = False
        print(f"   Обнаружены ошибки:")
        for error in visible_errors[:2]:  # Показываем первые 2 ошибки
            print(f"   - {error[:60]}...")
    
    # 5. Проверяем остались ли мы на странице входа (дополнительная проверка)
    try:
        still_on_login_page = driver.find_elements(By.CSS_SELECTOR, "input[name='username'], button[type='submit']")
        if len(still_on_login_page) >= 2 and not login_successful:
            # Есть и поле логина и кнопка входа - вероятно остались на странице входа
            print("   ⚠ Возможно остались на странице входа")
    except:
        pass
    
    print("\n10. Делаем скриншот результата...")
    after_login_screenshot = os.path.join(screenshots_dir, f"test_07_after_login_{timestamp}.png")
    driver.save_screenshot(after_login_screenshot)
    print(f"   Скриншот сохранен: test_07_after_login_{timestamp}.png")
    
    # Выводим итог
    print("\n" + "=" * 40)
    print("РЕЗУЛЬТАТ ТЕСТА 7:")
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
            for error in visible_errors[:2]:
                print(f"   - {error}")
        else:
            print("   Не удалось определить причину")
            print("   Проверьте скриншот для анализа")
        
except Exception as e:
    print(f"   ✗ Ошибка при выполнении входа: {e}")
    
    # Делаем скриншот ошибки
    error_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    error_screenshot = os.path.join(screenshots_dir, f"test_07_error_{error_timestamp}.png")
    driver.save_screenshot(error_screenshot)
    print(f"   Скриншот ошибки сохранен: test_07_error_{error_timestamp}.png")

print("\n11. Закрываем браузер...")
driver.quit()
print("   Браузер закрыт")

print("\n" + "=" * 50)
print("ИТОГИ ТЕСТА 7:")
print("=" * 50)

print("\nВыполнено:")
print("✓ Загружены данные из config.py (acc2)")
print("✓ Открыта страница входа")
print("✓ Найдены элементы формы")
print("✓ Заполнена форма (почта + пароль)")
print(f"✓ Сделано 2 скриншота:")
print(f"  - test_07_before_login_{timestamp}.png (перед входом)")
print(f"  - test_07_after_login_{timestamp}.png (после входа)")
print("✓ Нажата кнопка 'Войти'")
print("✓ Проанализирован результат")

if 'login_successful' in locals():
    if login_successful:
        print("\n✓ РЕЗУЛЬТАТ: ВХОД УСПЕШЕН")
    else:
        print("\n✗ РЕЗУЛЬТАТ: ВХОД НЕ УДАЛСЯ")

print("\n" + "=" * 50)
print("ТЕСТ 7 ЗАВЕРШЕН!")
print("=" * 50)

input("\nНажмите Enter для выхода...")