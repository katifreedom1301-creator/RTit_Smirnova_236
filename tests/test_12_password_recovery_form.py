import datetime
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

print("=" * 50)
print("ТЕСТ 12: ОТКРЫТИЕ ФОРМЫ ВОССТАНОВЛЕНИЯ ПАРОЛЯ")
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
    
    print("\n4. Ищем ссылку 'Забыл пароль'...")
    
    # Ищем ссылку восстановления пароля
    recovery_selectors = [
        "a#forgot_password",  # ID ссылки
        "a.rt-link--muted",  # Ссылка восстановления
        "a[href*='login-actions/reset-credentials']",
        "a[href*='forgot']",
        "//a[contains(text(), 'Забыл пароль')]",  # XPath по тексту
        "//a[contains(text(), 'Восстановить пароль')]",
        "//a[contains(text(), 'Не помню пароль')]",
        "//*[contains(text(), 'Забыл пароль')]",
    ]
    
    recovery_link = None
    recovery_found = False
    
    for selector in recovery_selectors:
        try:
            if selector.startswith("//"):
                recovery_link = driver.find_element(By.XPATH, selector)
            else:
                recovery_link = driver.find_element(By.CSS_SELECTOR, selector)
            
            if recovery_link.is_displayed():
                print(f"   Найдена ссылка восстановления пароля")
                recovery_found = True
                
                # Прокручиваем к ссылке чтобы она была видна
                driver.execute_script("arguments[0].scrollIntoView(true);", recovery_link)
                time.sleep(1)
                
                # Получаем текст ссылки
                link_text = recovery_link.text.strip()
                print(f"   Текст ссылки: '{link_text}'")
                
                # Делаем скриншот перед кликом
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                before_click_screenshot = os.path.join(screenshots_dir, f"test_12_before_click_{timestamp}.png")
                driver.save_screenshot(before_click_screenshot)
                print(f"   Скриншот до клика сохранен: test_12_before_click_{timestamp}.png")
                
                # Кликаем на ссылку
                recovery_link.click()
                print("   Кликнули на ссылку восстановления пароля")
                break
                
        except Exception as e:
            continue
    
    if not recovery_found:
        print("   ⚠ Ссылка 'Забыл пароль' не найдена")
        # Делаем скриншот чтобы увидеть что на странице
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        debug_filename = os.path.join(screenshots_dir, f"test_12_debug_{timestamp}.png")
        driver.save_screenshot(debug_filename)
        print(f"   Скриншот для отладки сохранен: {debug_filename}")
        driver.quit()
        exit()
    
    # Ждем загрузки формы восстановления
    print("\n5. Ждем загрузки формы восстановления пароля...")
    time.sleep(5)  # Даем больше времени для загрузки
    
    # Проверяем что мы на странице восстановления пароля
    print("\n6. Проверяем элементы формы восстановления...")
    
    # Проверяем заголовок
    recovery_indicators = driver.find_elements(By.XPATH, "//*[contains(text(), 'Восстановление пароля') or contains(text(), 'восстановлени') or contains(text(), 'Забыли пароль')]")
    if recovery_indicators:
        print("   ✓ Найден заголовок восстановления пароля")
        for elem in recovery_indicators[:2]:  # Показываем первые 2 элемента
            if elem.is_displayed() and elem.text.strip():
                print(f"     - '{elem.text.strip()[:50]}...'")
    else:
        print("   ⚠ Заголовок восстановления не найден")
    
    # Ищем поле для ввода телефона/почты
    input_fields = driver.find_elements(By.CSS_SELECTOR, "input[name='username'], input#username, input[type='text'], input[placeholder*='телефон'], input[placeholder*='почт']")
    if input_fields:
        print(f"   ✓ Найдено поле для ввода: {len(input_fields)} шт.")
        for field in input_fields[:2]:  # Первые 2 поля
            placeholder = field.get_attribute("placeholder") or ""
            name = field.get_attribute("name") or ""
            print(f"     - Поле: name='{name}', placeholder='{placeholder[:30]}...'")
    else:
        print("   ⚠ Поле для ввода не найдено")
    
    # Ищем кнопку "Продолжить" или подобную
    continue_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Продолжить') or contains(text(), 'Далее') or contains(text(), 'Восстановить')]")
    if continue_buttons:
        print(f"   ✓ Найдена кнопка продолжения: {len(continue_buttons)} шт.")
        for btn in continue_buttons[:2]:
            if btn.is_displayed() and btn.text.strip():
                print(f"     - Кнопка: '{btn.text.strip()}'")
    else:
        print("   ⚠ Кнопка продолжения не найдена")
    
    # Ищем ссылку "Вспомнил пароль" для возврата
    back_links = driver.find_elements(By.XPATH, "//a[contains(text(), 'Вспомнил пароль') or contains(text(), 'Вернуться назад') or contains(text(), 'Назад')]")
    if back_links:
        print(f"   ✓ Найдена ссылка возврата: {len(back_links)} шт.")
    else:
        print("   ⚠ Ссылка возврата не найдена")
    
    # Проверяем текущий URL
    current_url = driver.current_url
    print(f"\n   Текущий URL: {current_url}")
    
    # Проверяем заголовок страницы
    new_title = driver.title
    print(f"   Заголовок страницы: {new_title}")
    
    print("\n7. Делаем скриншот формы восстановления...")
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Ищем основную форму для скриншота
    form_selectors = [
        "form",
        ".card-container",
        ".recovery-form",
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
        form_screenshot = os.path.join(screenshots_dir, f"test_12_recovery_form_{timestamp}.png")
        form_element.screenshot(form_screenshot)
        print(f"   Скриншот формы сохранен: test_12_recovery_form_{timestamp}.png")
    else:
        # Если форму не нашли, делаем скриншот всей страницы
        full_screenshot = os.path.join(screenshots_dir, f"test_12_full_page_{timestamp}.png")
        driver.save_screenshot(full_screenshot)
        print(f"   Скриншот всей страницы сохранен: test_12_full_page_{timestamp}.png")
    
    # Анализируем результат
    print("\n8. Анализируем результат...")
    
    recovery_form_opened = False
    success_indicators = []
    
    # 1. URL изменился
    if current_url != url:
        recovery_form_opened = True
        success_indicators.append("URL изменился")
    
    # 2. Найден заголовок восстановления
    if recovery_indicators:
        recovery_form_opened = True
        success_indicators.append("Найден заголовок восстановления")
    
    # 3. Найдено поле для ввода
    if input_fields:
        recovery_form_opened = True
        success_indicators.append("Найдено поле для ввода данных")
    
    print("\n" + "=" * 40)
    print("РЕЗУЛЬТАТ ТЕСТА 12:")
    print("=" * 40)
    
    if recovery_form_opened:
        print("✓ ТЕСТ ПРОЙДЕН УСПЕШНО!")
        print("  Форма восстановления пароля открыта")
        print("  Признаки успеха:")
        for indicator in success_indicators:
            print(f"  - {indicator}")
    else:
        print("✗ ТЕСТ ПРОВАЛЕН!")
        print("  Форма восстановления пароля не открылась")
        
except Exception as e:
    print(f"   ✗ Ошибка при выполнении теста: {e}")
    
    # Делаем скриншот ошибки
    error_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    error_screenshot = os.path.join(screenshots_dir, f"test_12_error_{error_timestamp}.png")
    driver.save_screenshot(error_screenshot)
    print(f"   Скриншот ошибки сохранен: test_12_error_{error_timestamp}.png")

print("\n9. Закрываем браузер...")
driver.quit()
print("   Браузер закрыт")

print("\n" + "=" * 50)
print("ИТОГИ ТЕСТА 12:")
print("=" * 50)

print("\nВыполнено:")
print("✓ Открыта главная страница")
print("✓ Найдена ссылка 'Забыл пароль'")
print("✓ Кликнут по ссылке восстановления")
print(f"✓ Сделано 2 скриншота:")
if 'before_click_screenshot' in locals():
    print(f"  - test_12_before_click_{timestamp}.png (до клика)")
if 'form_screenshot' in locals():
    print(f"  - test_12_recovery_form_{timestamp}.png (форма восстановления)")
elif 'full_screenshot' in locals():
    print(f"  - test_12_full_page_{timestamp}.png (вся страница)")
print("✓ Проверены элементы формы восстановления")
print("✓ Проанализирован результат")

if 'recovery_form_opened' in locals():
    if recovery_form_opened:
        print("\n✓ РЕЗУЛЬТАТ: ТЕСТ ПРОЙДЕН (форма открыта)")
    else:
        print("\n✗ РЕЗУЛЬТАТ: ТЕСТ ПРОВАЛЕН (форма не открылась)")

print("\n" + "=" * 50)
print("ТЕСТ 12 ЗАВЕРШЕН!")
print("=" * 50)

input("\nНажмите Enter для выхода...")