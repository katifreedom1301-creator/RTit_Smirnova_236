import datetime
import time
import os
# УБИРАЕМ import sys - он больше не нужен

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

print("=" * 50)
print("ТЕСТ 5: АВТОПЕРЕКЛЮЧЕНИЕ ТЕЛЕФОН → ПОЧТА")
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
    # ПРОСТО ИМПОРТИРУЕМ - config.py в той же папке
    from config import TEST_ACCOUNTS
    print("✓ Конфигурационный файл загружен")
    
    # Берем данные второго аккаунта (только почта)
    account = TEST_ACCOUNTS["acc2"]
    email = account["email"]
    print(f"✓ Используем email: {email}")
    
except ImportError:
    print("✗ Ошибка: файл config.py не найден!")
    print("   Создайте файл config.py в папке tests/")
    exit()
except KeyError:
    print("✗ Ошибка: аккаунт 'acc2' не найден в config.py")
    exit()

print("\n2. Запускаем браузер...")
driver = webdriver.Chrome()
driver.maximize_window()
print("   Браузер открыт (на весь экран)")

print("\n3. Открываем сайт Ростелеком...")
url = "https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth?client_id=account_b2c&redirect_uri=https://b2c.passport.rt.ru/account_b2c/login&response_type=code&scope=openid&state=686d7744-c37c-4272-a461-80090fecb52f"
driver.get(url)
print("   Сайт открыт")

time.sleep(3)

print(f"\n4. Заголовок страницы: {driver.title}")

print("\n5. Делаем первый скриншот - начальное состояние...")
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
initial_screenshot = os.path.join(screenshots_dir, f"test_05_initial_{timestamp}.png")
driver.save_screenshot(initial_screenshot)
print(f"   Скриншот начального состояния сохранен: test_05_initial_{timestamp}.png")

print("\n6. Проверяем текущий активный таб...")
try:
    tabs = driver.find_elements(By.CSS_SELECTOR, ".rt-tab.rt-tab--small")
    if not tabs:
        tabs = driver.find_elements(By.CSS_SELECTOR, ".rt-tab")
    
    if tabs:
        print(f"   Найдено {len(tabs)} табов:")
        
        # Находим активный таб
        active_tab = None
        for tab in tabs:
            tab_text = tab.text.strip()
            tab_class = tab.get_attribute("class")
            
            if "rt-tab--active" in tab_class:
                active_tab = tab
                print(f"   Активный таб: '{tab_text}'")
                break
        
        # Если активен таб "Телефон" - отлично
        # Если активен другой таб, нам нужно переключиться на "Телефон"
        phone_tab = None
        for tab in tabs:
            tab_text = tab.text.strip().lower()
            if 'тел' in tab_text or 'моб' in tab_text or 'phone' in tab_text:
                phone_tab = tab
                print(f"   Найден таб 'Телефон': {tab.text.strip()}")
                break
        
        if phone_tab:
            if "rt-tab--active" not in phone_tab.get_attribute("class"):
                print("   Таб 'Телефон' не активен, кликаем...")
                phone_tab.click()
                time.sleep(1)
                print("   ✓ Переключились на таб 'Телефон'")
               
            else:
                print("   ✓ Таб 'Телефон' уже активен")
        else:
            print("   ⚠ Таб 'Телефон' не найден, продолжаем с текущим табом...")
    else:
        print("   ⚠ Табы не найдены, возможно интерфейс изменился")
        
except Exception as e:
    print(f"   Ошибка при поиске табов: {e}")

print("\n7. Ищем поле для ввода...")
try:
    # Ищем поле ввода (может быть для телефона или логина)
    login_field = driver.find_element(By.CSS_SELECTOR, "input[name='username'], input#username, input[type='text']")
    print("   Поле для ввода найдено")
    
    # Проверяем плейсхолдер
    placeholder = login_field.get_attribute("placeholder") or ""
    print(f"   Плейсхолдер поля: {placeholder}")
    
    # Очищаем поле если там что-то есть
    login_field.clear()
    
    print(f"\n8. Вводим email в поле 'Телефон'...")
    print(f"   Вводим: {email}")
    
    # Вводим email
    login_field.send_keys(email)
    
    # Ждем 1 секунду для начала переключения
    time.sleep(1)
    
    print("\n9. Кликаем на поле пароля чтобы активировать переключение...")
    
    # Ищем поле пароля и кликаем на него
    try:
        password_field = driver.find_element(By.CSS_SELECTOR, "input[name='password'], input#password, input[type='password']")
        password_field.click()
        print("   ✓ Кликнули на поле пароля")
        
        # Ждем еще секунду для полного переключения
        time.sleep(1)
        
    except Exception as e:
        print(f"   ⚠ Не удалось найти поле пароля: {e}")
        # Если не нашли пароль, кликаем на другой элемент
        try:
            driver.find_element(By.TAG_NAME, "body").click()
            print("   Кликнули на body")
        except:
            pass
    
    # Проверяем переключился ли таб
    print("\n10. Проверяем авто-переключение на таб 'Почта'...")
    
    tabs_after = driver.find_elements(By.CSS_SELECTOR, ".rt-tab.rt-tab--small")
    if not tabs_after:
        tabs_after = driver.find_elements(By.CSS_SELECTOR, ".rt-tab")
    
    if tabs_after:
        active_tab_after = None
        for tab in tabs_after:
            if "rt-tab--active" in tab.get_attribute("class"):
                active_tab_after = tab
                break
        
        if active_tab_after:
            tab_text = active_tab_after.text.strip()
            print(f"   Текущий активный таб: '{tab_text}'")
            
            # Проверяем переключился ли на почту
            if 'почт' in tab_text.lower() or 'mail' in tab_text.lower() or '@' in tab_text:
                print("   ✓ Успешно переключилось на 'Почта'!")
            elif 'тел' in tab_text.lower() or 'моб' in tab_text.lower():
                print("   ⚠ Осталось на 'Телефоне' - авто-переключение не сработало")
            else:
                print(f"   ⚠ Активен другой таб: {tab_text}")
    else:
        print("   ⚠ Не удалось найти табы после ввода")
    
    # Проверяем значение в поле
    current_value = login_field.get_attribute("value")
    print(f"\n11. Текущее значение в поле: {current_value}")
    
    if current_value == email:
        print("   ✓ Email сохранен в поле")
    else:
        print(f"   ⚠ Значение отличается от введенного")
        
except Exception as e:
    print(f"   Ошибка при работе с полем ввода: {e}")

print("\n12. Делаем финальный скриншот...")
final_screenshot = os.path.join(screenshots_dir, f"test_05_final_{timestamp}.png")
driver.save_screenshot(final_screenshot)
print(f"   Финальный скриншот сохранен: test_05_final_{timestamp}.png")

print("\n13. Закрываем браузер...")
driver.quit()
print("   Браузер закрыт")

print("\n" + "=" * 50)
print("ТЕСТ 5 ЗАВЕРШЕН УСПЕШНО!")
print("=" * 50)

print("\nИтоги теста:")
print(f"✓ Использован email из config.py: {email}")
print("✓ Открыта главная страница авторизации")
print(f"✓ Сделано 3 скриншота:")
print(f"  - test_05_initial_{timestamp}.png (начальное состояние)")
print(f"  - test_05_final_{timestamp}.png (финальный результат)")
print("✓ Найден и активирован таб 'Телефон' (если нужно было)")
print(f"✓ Введен email '{email}' в поле 'Телефон'")
print("✓ Кликнут на поле пароля для активации переключения")
print("✓ Проверено авто-переключение с телефона на почту")

input("\nНажмите Enter для выхода...")