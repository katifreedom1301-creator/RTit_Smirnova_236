import datetime
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By

print("=" * 50)
print("ТЕСТ 1: ОТКРЫТИЕ САЙТА РОСТЕЛЕКОМ")
print("=" * 50)

project_root = os.path.dirname(os.path.abspath(__file__))  # Папка, где лежит этот файл
screenshots_dir = os.path.join(project_root, "screenshots")  # Полный путь к screenshots/


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

print("\n3. Открываем сайт Ростелеком...")
url = "https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth?client_id=account_b2c&redirect_uri=https://b2c.passport.rt.ru/account_b2c/login&response_type=code&scope=openid&state=686d7744-c37c-4272-a461-80090fecb52f"
driver.get(url)
print("   Сайт открыт")

time.sleep(3)

print(f"\n4. Заголовок страницы: {driver.title}")

print("\n5. Делаем скриншот...")
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
filename = os.path.join(screenshots_dir, f"test_01_{timestamp}.png")
driver.save_screenshot(filename)
print(f"   Скриншот сохранен: {filename}")

print("\n6. Закрываем браузер...")
driver.quit()
print("   Браузер закрыт")

print("\n" + "=" * 50)
print("ТЕСТ 1 ЗАВЕРШЕН УСПЕШНО!")
print("=" * 50)

input("\nНажмите Enter для выхода...")