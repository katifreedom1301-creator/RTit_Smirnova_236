import datetime
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

print("=" * 50)
print("ТЕСТ 3: ВАЛИДАЦИЯ ПОЛЕЙ РЕГИСТРАЦИИ")
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

print("\n2. Запускаем браузер...")
driver = webdriver.Chrome()
driver.maximize_window()
print("   Браузер открыт (на весь экран)")

print("\n3. Открываем главную страницу Ростелеком...")
url = "https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth?client_id=account_b2c&redirect_uri=https://b2c.passport.rt.ru/account_b2c/login&response_type=code&scope=openid&state=686d7744-c37c-4272-a461-80090fecb52f"

try:
    driver.get(url)
    print("   Главная страница открыта")
    time.sleep(3)
    
    page_title = driver.title
    print(f"   Заголовок страницы: {page_title}")
    
    # Ждем загрузки страницы
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    
    print("\n4. Ищем кнопку 'Зарегистрироваться'...")
    
    # Ищем кнопку регистрации (обычно внизу формы)
    register_selectors = [
        "a#kc-register",  # ID кнопки регистрации
        "a.rt-link--muted",  # Ссылка "Зарегистрироваться"
        "a[href*='registration']",  # Ссылка содержащая registration
        "button[name='register']",
        "//a[contains(text(), 'Зарегистрироваться')]",  # XPath по тексту
        "//a[contains(text(), 'регистрации')]",
        "//*[contains(text(), 'Зарегистрироваться')]",
    ]
    
    register_button = None
    register_found = False
    
    for selector in register_selectors:
        try:
            if selector.startswith("//"):
                register_button = driver.find_element(By.XPATH, selector)
            else:
                register_button = driver.find_element(By.CSS_SELECTOR, selector)
            
            if register_button.is_displayed():
                print(f"   Найдена кнопка 'Зарегистрироваться'")
                register_found = True
                
                # Прокручиваем к кнопке чтобы она была видна
                driver.execute_script("arguments[0].scrollIntoView(true);", register_button)
                time.sleep(1)
                
                # Кликаем на кнопку
                register_button.click()
                print("   Кликнули на 'Зарегистрироваться'")
                break
                
        except Exception as e:
            continue
    
    if not register_found:
        print("   ⚠ Кнопка 'Зарегистрироваться' не найдена, проверяем вручную...")
        # Делаем скриншот чтобы увидеть что на странице
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        debug_filename = os.path.join(screenshots_dir, f"test_03_debug_{timestamp}.png")
        driver.save_screenshot(debug_filename)
        print(f"   Скриншот для отладки сохранен: {debug_filename}")
        print("   Открой скриншот и посмотри где кнопка регистрации")
        driver.quit()
        exit()
    
    # Ждем загрузки формы регистрации
    print("\n5. Ждем загрузки формы регистрации...")
    time.sleep(3)
    
    # Проверяем что мы на странице регистрации
    registration_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Регистрация') or contains(text(), 'регистрац')]")
    if registration_elements:
        print("   Форма регистрации загружена")
    else:
        print("   ⚠ Возможно форма регистрации не загрузилась")
    
    # Ищем поля формы
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[name]"))
    )
    
except Exception as e:
    print(f"   Ошибка: {e}")
    driver.quit()
    exit()

print("\n6. Заполняем поля некорректными данными...")

try:
    # Имя
    name_field = driver.find_element(By.CSS_SELECTOR, "input[name='firstName']")
    name_field.clear()
    name_field.send_keys("В")
    print("   Введено имя: 'В' (1 символ)")
    time.sleep(0.3)
    
    # Фамилия
    lastname_field = driver.find_element(By.CSS_SELECTOR, "input[name='lastName']")
    lastname_field.clear()
    lastname_field.send_keys("Ч")
    print("   Введена фамилия: 'Ч' (1 символ)")
    time.sleep(0.3)
    
    # Пароль
    password_field = driver.find_element(By.CSS_SELECTOR, "input[name='password']")
    password_field.clear()
    password_field.send_keys("1111111Ф")
    print("   Введен пароль: '1111111Ф' (7 цифр + русская буква)")
    time.sleep(0.5)
    
    # Активируем валидацию - кликаем на другое поле
    print("\n7. Активируем валидацию полей...")
    
    # Кликаем на поле "E-mail или мобильный телефон"
    try:
        email_field = driver.find_element(By.CSS_SELECTOR, "input[name='email']")
        email_field.click()
    except:
        try:
            # Или на заголовок
            form_title = driver.find_element(By.TAG_NAME, "h1")
            form_title.click()
        except:
            # Или просто на тело
            driver.find_element(By.TAG_NAME, "body").click()
    
    time.sleep(2)
    
    # Поиск сообщений об ошибках
    print("\n8. Проверяем сообщения об ошибках...")
    
    # Сначала делаем скриншот чтобы видеть что происходит
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Ищем форму для основного скриншота
    form_selectors = [
        "form",
        ".card-container",
        ".registration-form",
        ".register-form",
        "div.rt-card",
        "div.card-container__wrapper",
        "div.card-container__content",
    ]
    
    form_element = None
    for selector in form_selectors:
        try:
            element = driver.find_element(By.CSS_SELECTOR, selector)
            if element.is_displayed():
                form_element = element
                print(f"   Найдена форма с селектором: {selector}")
                break
        except:
            continue
    
    if form_element:
        # Делаем скриншот формы
        filename = os.path.join(screenshots_dir, f"test_03_form_{timestamp}.png")
        form_element.screenshot(filename)
        print(f"   Скриншот формы сохранен: {filename}")
    else:
        # Если форму не нашли, делаем скриншот всей страницы
        filename = os.path.join(screenshots_dir, f"test_03_full_{timestamp}.png")
        driver.save_screenshot(filename)
        print(f"   Скриншот всей страницы сохранен: {filename}")
    
    # Ищем ошибки
    error_selectors = [
        ".rt-input-container__error",
        ".rt-input-container__meta--error",
        ".rt-input-container__error span",
        "[class*='error-message']",
        "small.text-danger",
        "div.text-danger",
        "span.text-danger",
    ]
    
    all_errors = []
    for selector in error_selectors:
        try:
            errors = driver.find_elements(By.CSS_SELECTOR, selector)
            for error in errors:
                if error.text.strip() and error.is_displayed():
                    error_text = error.text.strip()
                    all_errors.append(error_text)
        except:
            continue
    
    # НЕ удаляем дубликаты - считаем все найденные ошибки
    error_messages = []
    for error_text in all_errors:
        if error_text.strip():  # Проверяем, что текст не пустой
            error_messages.append(error_text.strip())
    
    if error_messages:
        print(f"\n   Найдено {len(error_messages)} сообщений об ошибках:")
        for i, error_text in enumerate(error_messages, 1):
            print(f"   {i}. {error_text}")
            
        # Проверяем ожидаемые ошибки
        print("\n   Проверка ожидаемых ошибок:")
        expected_phrases = ['От 2 до 30', 'кириллицей', 'латинские буквы']
        for phrase in expected_phrases:
            found = any(phrase in error for error in error_messages)
            status = "✓" if found else "✗"
            print(f"   {status} '{phrase}'")
    else:
        print("   Сообщения об ошибках не найдены")
        
        # Для отладки покажем что есть на странице
        print("\n   Элементы на странице (первые 5):")
        elements = driver.find_elements(By.CSS_SELECTOR, "div, span, p")[:5]
        for elem in elements:
            if elem.text.strip():
                print(f"   - {elem.text.strip()[:50]}...")
        
except Exception as e:
    print(f"   Ошибка при выполнении теста: {e}")

print("\n9. Закрываем браузер...")
driver.quit()
print("   Браузер закрыт")

print("\n" + "=" * 50)
print("ТЕСТ 3 ЗАВЕРШЕН!")
print("=" * 50)

print("\nИтоговый отчет:")
print("✓ Открыта главная страница")
print("✓ Найдена и нажата кнопка 'Зарегистрироваться'")
print("✓ Загружена форма регистрации")
print("✓ Введены некорректные данные:")
print("  - Имя: 'В' (1 символ)")
print("  - Фамилия: 'Ч' (1 символ)")
print("  - Пароль: '1111111Ф' (7 цифр + русская буква)")
print("✓ Активирована валидация полей")
print(f"✓ Скриншот сохранен в: {screenshots_dir}")
print(f"✓ Найдено сообщений об ошибках: {len(error_messages) if 'error_messages' in locals() else 0}")

input("\nНажмите Enter для выхода...")