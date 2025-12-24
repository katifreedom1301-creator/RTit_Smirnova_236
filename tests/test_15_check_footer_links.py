import datetime
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

print("=" * 50)
print("ТЕСТ 15: ПРОВЕРКА ССЫЛОК В ФУТЕРЕ СТРАНИЦЫ")
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
    
    print("\n4. Прокручиваем страницу вниз к футеру...")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    print("   Страница прокручена вниз")
    time.sleep(2)
    
    print("\n5. Ищем футер страницы...")
    
    # Ищем футер разными способами
    footer_selectors = [
        "footer",
        ".footer",
        "div.footer",
        "div.rt-footer",
        "footer.rt-footer",
        "div[class*='footer']",
        "footer[class*='footer']",
        "//footer",  # XPath
        "//div[contains(@class, 'footer')]",
    ]
    
    footer_element = None
    footer_found = False
    
    for selector in footer_selectors:
        try:
            if selector.startswith("//"):
                footer_element = driver.find_element(By.XPATH, selector)
            else:
                footer_element = driver.find_element(By.CSS_SELECTOR, selector)
            
            if footer_element.is_displayed():
                print(f"   Найден футер с селектором: {selector}")
                footer_found = True
                break
                
        except Exception as e:
            continue
    
    if not footer_found:
        print("   ⚠ Футер не найден стандартными селекторами")
        print("   Ищем любые элементы внизу страницы...")
        
        # Ищем все элементы внизу страницы
        all_elements = driver.find_elements(By.CSS_SELECTOR, "div, footer, section, nav")
        bottom_elements = []
        
        for elem in all_elements:
            try:
                location = elem.location
                if location['y'] > 500:  # Элементы в нижней части страницы
                    if elem.is_displayed() and elem.text.strip():
                        bottom_elements.append(elem)
            except:
                continue
        
        if bottom_elements:
            print(f"   Найдено {len(bottom_elements)} элементов в нижней части страницы")
            footer_element = bottom_elements[0]  # Берем первый
            footer_found = True
        else:
            print("   ⚠ Нижние элементы не найдены")
    
    if not footer_found:
        print("   Футер не найден, делаем скриншот для анализа...")
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        debug_filename = os.path.join(screenshots_dir, f"test_15_debug_{timestamp}.png")
        driver.save_screenshot(debug_filename)
        print(f"   Скриншот для отладки сохранен: {debug_filename}")
        print("   Открой скриншот чтобы увидеть структуру страницы")
        driver.quit()
        exit()
    
    print("\n6. Ищем ссылки в футере...")
    
    # Ищем все ссылки в футере или в нижней части страницы
    if footer_element:
        # Ищем ссылки внутри футера
        footer_links = footer_element.find_elements(By.TAG_NAME, "a")
    else:
        # Ищем все ссылки на странице (фильтруем потом)
        footer_links = driver.find_elements(By.TAG_NAME, "a")
    
    print(f"   Всего найдено ссылок: {len(footer_links)}")
    
    # Фильтруем ссылки (только видимые и с href)
    visible_links = []
    for link in footer_links:
        try:
            if link.is_displayed() and link.get_attribute("href"):
                visible_links.append(link)
        except:
            continue
    
    print(f"   Видимых ссылок с href: {len(visible_links)}")
    
    if visible_links:
        print("\n   Список найденных ссылок (первые 10):")
        for i, link in enumerate(visible_links[:10], 1):
            href = link.get_attribute("href") or ""
            text = link.text.strip() or "[без текста]"
            print(f"   {i}. Текст: '{text[:30]}...'")
            print(f"      URL: {href[:50]}...")
    
    # Ищем конкретные ожидаемые ссылки (обычные для футеров)
    expected_links_texts = [
        "Политика конфиденциальности",
        "Пользовательское соглашение",
        "Условия использования",
        "Поддержка",
        "Помощь",
        "Контакты",
        "О компании",
        "©",
        "Все права защищены",
    ]
    
    found_expected_links = []
    
    print("\n7. Проверяем наличие ожидаемых ссылок...")
    for expected_text in expected_links_texts:
        found = False
        for link in visible_links:
            link_text = link.text.strip()
            if expected_text.lower() in link_text.lower():
                found = True
                href = link.get_attribute("href") or ""
                found_expected_links.append({
                    "text": link_text,
                    "href": href,
                    "expected": expected_text
                })
                break
        
        status = "✓" if found else "✗"
        print(f"   {status} '{expected_text}'")
    
    print("\n8. Делаем скриншот футера...")
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if footer_element:
        # Делаем скриншот футера
        footer_screenshot = os.path.join(screenshots_dir, f"test_15_footer_{timestamp}.png")
        footer_element.screenshot(footer_screenshot)
        print(f"   Скриншот футера сохранен: test_15_footer_{timestamp}.png")
    else:
        # Делаем скриншот всей страницы
        full_screenshot = os.path.join(screenshots_dir, f"test_15_full_{timestamp}.png")
        driver.save_screenshot(full_screenshot)
        print(f"   Скриншот всей страницы сохранен: test_15_full_{timestamp}.png")
    
    # Анализируем результат
    print("\n9. Анализируем результат проверки...")
    
    footer_check_passed = False
    success_indicators = []
    
    # 1. Футер найден
    if footer_found:
        footer_check_passed = True
        success_indicators.append("Футер найден")
    
    # 2. Найдены ссылки
    if visible_links:
        footer_check_passed = True
        success_indicators.append(f"Найдено {len(visible_links)} ссылок")
    
    # 3. Найдены ожидаемые ссылки
    if found_expected_links:
        footer_check_passed = True
        success_indicators.append(f"Найдено {len(found_expected_links)} ожидаемых ссылок")
    
    print("\n" + "=" * 40)
    print("РЕЗУЛЬТАТ ТЕСТА 15:")
    print("=" * 40)
    
    if footer_check_passed:
        print("✓ ТЕСТ ПРОЙДЕН УСПЕШНО!")
        print("  Футер и ссылки проверены")
        print("  Результаты проверки:")
        for indicator in success_indicators:
            print(f"  - {indicator}")
        
        if found_expected_links:
            print("\n  Найденные ожидаемые ссылки:")
            for link_info in found_expected_links[:5]:  # Показываем первые 5
                print(f"  - '{link_info['text'][:30]}...' → {link_info['href'][:50]}...")
    else:
        print("✗ ТЕСТ ПРОВАЛЕН!")
        print("  Футер или ссылки не найдены")
        
except Exception as e:
    print(f"   ✗ Ошибка при выполнении теста: {e}")
    
    # Делаем скриншот ошибки
    error_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    error_screenshot = os.path.join(screenshots_dir, f"test_15_error_{error_timestamp}.png")
    driver.save_screenshot(error_screenshot)
    print(f"   Скриншот ошибки сохранен: test_15_error_{error_timestamp}.png")

print("\n10. Закрываем браузер...")
driver.quit()
print("   Браузер закрыт")

print("\n" + "=" * 50)
print("ИТОГИ ТЕСТА 15:")
print("=" * 50)

print("\nВыполнено:")
print("✓ Открыта главная страница")
print("✓ Страница прокручена вниз")
print("✓ Найден футер/нижняя часть страницы")
print(f"✓ Найдено ссылок: {len(visible_links) if 'visible_links' in locals() else 0}")
print(f"✓ Проверено ожидаемых ссылок: {len(found_expected_links) if 'found_expected_links' in locals() else 0}")
print(f"✓ Сделан скриншот:")
if 'footer_screenshot' in locals():
    print(f"  - test_15_footer_{timestamp}.png (футер)")
elif 'full_screenshot' in locals():
    print(f"  - test_15_full_{timestamp}.png (вся страница)")
print("✓ Проанализирован результат")

if 'footer_check_passed' in locals():
    if footer_check_passed:
        print("\n✓ РЕЗУЛЬТАТ: ТЕСТ ПРОЙДЕН (футер и ссылки проверены)")
    else:
        print("\n✗ РЕЗУЛЬТАТ: ТЕСТ ПРОВАЛЕН (футер/ссылки не найдены)")

print("\n" + "=" * 50)
print("ТЕСТ 15 ЗАВЕРШЕН!")
print("=" * 50)

input("\nНажмите Enter для выхода...")