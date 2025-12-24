import datetime
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By

print("=" * 50)
print("ТЕСТ 11: ВХОД ПО НЕВЕРНОМУ ТЕЛЕФОНУ НО ВЕРНОМУ ПАРОЛЮ")
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
    from config import TEST_ACCOUNTS, TEST_DATA
    print("✓ Конфигурационный файл загружен")
    
    # Берем неверный телефон из TEST_DATA
    wrong_phone = TEST_DATA["invalid"]["wrong_phone"]
    
    # Берем верный пароль из аккаунта acc1
    valid_password = TEST_ACCOUNTS["acc1"]["password"]
    
    print(f"✓ Используем данные:")
    print(f"  Телефон: {wrong_phone} (неверный)")
    print(f"  Пароль: {valid_password} (верный)")
    
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
    login_field = driver.find_element(By.CSS_SELECTOR, "input[name='username'], input#username, input[type='text']")
    print("   ✓ Поле для логина найдено")
    
    password_field = driver.find_element(By.CSS_SELECTOR, "input[name='password'], input#password, input[type='password']")
    print("   ✓ Поле для пароля найдено")
    
    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit'], button#kc-login, button[name='login']")
    print("   ✓ Кнопка 'Войти' найдена")
    
except Exception as e:
    print(f"   ✗ Ошибка при поиске элементов формы: {e}")
    print("   Делаем скриншот для отладки...")
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    debug_screenshot = os.path.join(screenshots_dir, f"test_11_debug_{timestamp}.png")
    driver.save_screenshot(debug_screenshot)
    print(f"   Скриншот сохранен: test_11_debug_{timestamp}.png")
    driver.quit()
    exit()

print("\n6. Заполняем форму входа с неверным телефоном...")

try:
    # Вводим НЕВЕРНЫЙ телефон
    login_field.clear()
    login_field.send_keys(wrong_phone)
    print(f"   ✓ Введен неверный телефон: {wrong_phone}")
    time.sleep(0.5)
    
    # Вводим верный пароль
    password_field.clear()
    password_field.send_keys(valid_password)
    print(f"   ✓ Введен верный пароль")
    time.sleep(0.5)
    
    print("\n7. Делаем скриншот заполненной формы...")
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    before_login_screenshot = os.path.join(screenshots_dir, f"test_11_before_login_{timestamp}.png")
    driver.save_screenshot(before_login_screenshot)
    print(f"   Скриншот сохранен: test_11_before_login_{timestamp}.png")
    
    print("\n8. Нажимаем кнопку 'Войти'...")
    login_button.click()
    print("   ✓ Нажата кнопка 'Войти'")
    
    print("   Ждем обработки (7 секунд)...")
    time.sleep(7)
    
    print("\n9. Анализируем результат входа...")
    
    current_url = driver.current_url
    print(f"   Текущий URL: {current_url}")
    
    page_title = driver.title
    print(f"   Заголовок страницы: {page_title}")
    
    login_failed = False
    failure_indicators = []
    
    # Проверяем наличие сообщений об ошибке
    error_elements = driver.find_elements(By.CSS_SELECTOR, ".card-container__error, .rt-input-container__error, .alert-error, .text-danger")
    visible_errors = []
    for error in error_elements:
        if error.is_displayed() and error.text.strip():
            visible_errors.append(error.text.strip())
    
    if visible_errors:
        login_failed = True
        failure_indicators.append(f"Найдены ошибки: {visible_errors[0][:50]}...")
    
    # Проверяем, остались ли мы на странице входа
    if "auth/realms/b2c" in current_url or "login" in current_url:
        login_failed = True
        failure_indicators.append("Остались на странице входа")
    
    # Проверяем отсутствие признаков успешного входа
    try:
        welcome_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Добро пожаловать') or contains(text(), 'Привет') or contains(text(), 'Кабинет')]")
        welcome_found = False
        for elem in welcome_elements:
            if elem.is_displayed():
                welcome_found = True
                break
        
        if not welcome_found:
            login_failed = True
            failure_indicators.append("Отсутствуют приветствия")
            
    except:
        pass
    
    print("\n10. Делаем скриншот результата...")
    after_login_screenshot = os.path.join(screenshots_dir, f"test_11_after_login_{timestamp}.png")
    driver.save_screenshot(after_login_screenshot)
    print(f"   Скриншот сохранен: test_11_after_login_{timestamp}.png")
    
    # Выводим итог
    print("\n" + "=" * 40)
    print("РЕЗУЛЬТАТ ТЕСТА 11:")
    print("=" * 40)
    
    if login_failed:
        print("✓ ТЕСТ ПРОЙДЕН УСПЕШНО!")
        print("  Вход не выполнился (как и ожидалось)")
        if failure_indicators:
            print("  Признаки неуспешного входа:")
            for indicator in failure_indicators:
                print(f"  - {indicator}")
    else:
        print("✗ ТЕСТ ПРОВАЛЕН!")
        print("  Вход выполнился (хотя не должен был)")
        
except Exception as e:
    print(f"   ✗ Ошибка при выполнении теста: {e}")
    
    error_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    error_screenshot = os.path.join(screenshots_dir, f"test_11_error_{error_timestamp}.png")
    driver.save_screenshot(error_screenshot)
    print(f"   Скриншот ошибки сохранен: test_11_error_{error_timestamp}.png")

print("\n11. Закрываем браузер...")
driver.quit()
print("   Браузер закрыт")

print("\n" + "=" * 50)
print("ИТОГИ ТЕСТА 11:")
print("=" * 50)

print("\nВыполнено:")
print("✓ Загружены данные из config.py")
print("✓ Открыта страница входа")
print("✓ Найдены элементы формы")
print("✓ Заполнена форма (неверный телефон + верный пароль)")
print(f"✓ Сделано 2 скриншота:")
print(f"  - test_11_before_login_{timestamp}.png (перед входом)")
print(f"  - test_11_after_login_{timestamp}.png (после попытки входа)")
print("✓ Нажата кнопка 'Войти'")
print("✓ Проанализирован результат")

if 'login_failed' in locals():
    if login_failed:
        print("\n✓ РЕЗУЛЬТАТ: ТЕСТ ПРОЙДЕН (вход не выполнился)")
    else:
        print("\n✗ РЕЗУЛЬТАТ: ТЕСТ ПРОВАЛЕН (вход выполнился)")

print("\n" + "=" * 50)
print("ТЕСТ 11 ЗАВЕРШЕН!")
print("=" * 50)

input("\nНажмите Enter для выхода...")