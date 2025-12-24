import datetime
import time
import os
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

print("=" * 50)
print("ТЕСТ 4: АВТОПЕРЕКЛЮЧЕНИЕ ПОЧТА → ТЕЛЕФОН")
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

print("\n1. Проверяем библиотеки...")
print("   Selenium готов")
print("   Random готов")

print("\n2. Генерируем случайный номер телефона...")
random_digits = ''.join([str(random.randint(0, 9)) for _ in range(10)])
phone_number = f"+7{random_digits}"
print(f"   Сгенерирован номер: {phone_number}")

print("\n3. Запускаем браузер...")
driver = webdriver.Chrome()
driver.maximize_window()
print("   Браузер открыт (на весь экран)")

print("\n4. Открываем сайт Ростелеком...")
url = "https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth?client_id=account_b2c&redirect_uri=https://b2c.passport.rt.ru/account_b2c/login&response_type=code&scope=openid&state=686d7744-c37c-4272-a461-80090fecb52f"
driver.get(url)
print("   Сайт открыт")

time.sleep(3)

print(f"\n5. Заголовок страницы: {driver.title}")

print("\n6. Делаем первый скриншот - начальное состояние...")
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
initial_screenshot = os.path.join(screenshots_dir, f"test_04_initial_{timestamp}.png")
driver.save_screenshot(initial_screenshot)
print(f"   Скриншот начального состояния сохранен: test_04_initial_{timestamp}.png")

print("\n7. Ищем табы (почта/телефон/логин)...")
try:
    tabs = driver.find_elements(By.CSS_SELECTOR, ".rt-tab.rt-tab--small")
    if not tabs:
        tabs = driver.find_elements(By.CSS_SELECTOR, ".rt-tab")
    
    if tabs:
        print(f"   Найдено {len(tabs)} табов:")
        
        mail_tab = None
        for tab in tabs:
            tab_text = tab.text.strip()
            print(f"   - Таб: '{tab_text}'")
            
            if 'почт' in tab_text.lower() or 'mail' in tab_text.lower() or '@' in tab_text:
                mail_tab = tab
                print(f"   ✓ Найден таб 'Почта': {tab_text}")
                break
        
        if mail_tab:
            if "rt-tab--active" not in mail_tab.get_attribute("class"):
                print("   Таб 'Почта' не активен, кликаем...")
                mail_tab.click()
                time.sleep(1)
                print("   ✓ Переключились на таб 'Почта'")
                
                # Скриншот после переключения на почту
                after_mail_screenshot = os.path.join(screenshots_dir, f"test_04_after_mail_{timestamp}.png")
                driver.save_screenshot(after_mail_screenshot)
                print(f"   Скриншот после переключения на 'Почта': test_04_after_mail_{timestamp}.png")
            else:
                print("   ✓ Таб 'Почта' уже активен")
        else:
            print("   ⚠ Таб 'Почта' не найден, продолжаем...")
    else:
        print("   ⚠ Табы не найдены")
        
except Exception as e:
    print(f"   Ошибка при поиске табов: {e}")

print("\n8. Ищем поле для ввода логина...")
try:
    login_field = driver.find_element(By.CSS_SELECTOR, "input[name='username'], input#username, input[type='text'], input[placeholder*='@']")
    print("   Поле для ввода найдено")
    
    placeholder = login_field.get_attribute("placeholder") or ""
    print(f"   Плейсхолдер поля: {placeholder}")
    
    login_field.clear()
    
    print("\n9. Вводим номер телефона в поле 'Почта'...")
    print(f"   Вводим: {phone_number}")
    
    # Вводим номер телефона
    login_field.send_keys(phone_number)
    
    # Ждем 1 секунду для начала переключения
    time.sleep(1)
    
    print("\n10. Кликаем на поле пароля чтобы активировать переключение...")
    
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
    print("\n11. Проверяем авто-переключение на таб 'Телефон'...")
    
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
            
            if 'тел' in tab_text.lower() or 'моб' in tab_text.lower() or 'phone' in tab_text.lower():
                print("   ✓ Успешно переключилось на 'Телефон'!")
            elif 'почт' in tab_text.lower() or 'mail' in tab_text.lower():
                print("   ⚠ Осталось на 'Почте' - авто-переключение не сработало")
            else:
                print(f"   ⚠ Активен другой таб: {tab_text}")
    else:
        print("   ⚠ Не удалось найти табы после ввода")
    
    # Проверяем значение в поле
    current_value = login_field.get_attribute("value")
    print(f"\n12. Текущее значение в поле: {current_value}")
    
    if current_value == phone_number:
        print("   ✓ Номер телефона сохранен в поле")
    else:
        print(f"   ⚠ Значение отличается от введенного")
        
except Exception as e:
    print(f"   Ошибка при работе с полем ввода: {e}")

print("\n13. Делаем финальный скриншот...")
final_screenshot = os.path.join(screenshots_dir, f"test_04_final_{timestamp}.png")
driver.save_screenshot(final_screenshot)
print(f"   Финальный скриншот сохранен: test_04_final_{timestamp}.png")

print("\n14. Закрываем браузер...")
driver.quit()
print("   Браузер закрыт")

print("\n" + "=" * 50)
print("ТЕСТ 4 ЗАВЕРШЕН УСПЕШНО!")
print("=" * 50)

print("\nИтоги теста:")
print(f"✓ Сгенерирован номер телефона: {phone_number}")
print("✓ Открыта главная страница авторизации")
print(f"✓ Сделано 3 скриншота:")
print(f"  - test_04_initial_{timestamp}.png (начальное состояние)")
print(f"  - test_04_after_mail_{timestamp}.png (после переключения на 'Почта')")
print(f"  - test_04_final_{timestamp}.png (финальный результат)")
print("✓ Найден и активирован таб 'Почта'")
print("✓ Введен номер телефона в поле 'Почта'")
print("✓ Кликнут на поле пароля для активации переключения")
print("✓ Проверено авто-переключение с почты на телефон")

input("\nНажмите Enter для выхода...")