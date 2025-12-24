import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

print("=" * 60)
print("ТЕСТ 2: ПРОВЕРКА ЭЛЕМЕНТОВ ФОРМЫ АВТОРИЗАЦИИ")
print("=" * 60)

print("\n1. Запускаем браузер...")
driver = webdriver.Chrome()
driver.maximize_window()
print("   ✓ Браузер открыт")

print("\n2. Открываем страницу авторизации...")
url = "https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth?client_id=account_b2c&redirect_uri=https://b2c.passport.rt.ru/account_b2c/login&response_type=code&scope=openid&state=25caca26-7024-4f3c-a046-b32ec6adcc9d"
print(f"   URL: {url[:80]}...")
driver.get(url)

time.sleep(3)
print("   ✓ Страница загружена")

print("\n3. Проверяем элементы формы...")
print("-" * 40)

elements_to_check = {
    "Таб 'Телефон'": (By.ID, "t-btn-tab-phone"),
    "Таб 'Почта'": (By.ID, "t-btn-tab-mail"),
    "Таб 'Логин'": (By.ID, "t-btn-tab-login"),
    "Таб 'Лицевой счет'": (By.ID, "t-btn-tab-ls"),
    "Поле 'Мобильный телефон'": (By.ID, "username"),
    "Поле 'Пароль'": (By.ID, "password"),
    "Чекбокс 'Запомнить меня'": (By.XPATH, "//span[contains(@class, 'rt-checkbox__label') and text()='Запомнить меня']"),
    "Кнопка 'Войти'": (By.ID, "kc-login"),
    "Ссылка 'Забыл пароль'": (By.ID, "forgot_password"),
    "Ссылка 'Зарегистрироваться'": (By.ID, "kc-register"),
    "Блок 'Войти другим способом'": (By.CLASS_NAME, "social-providers"),
}

missing_elements = []
all_elements_found = True

for element_name, locator in elements_to_check.items():
    try:
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(locator)
        )
        
        if element.is_displayed():
            print(f"   ✓ {element_name}")
        else:
            print(f"   ⚠ {element_name} (есть, но не виден)")
            missing_elements.append(f"{element_name} - не виден")
            all_elements_found = False
            
    except Exception as e:
        print(f"   ✗ {element_name} - НЕ НАЙДЕН")
        missing_elements.append(element_name)
        all_elements_found = False

print("-" * 40)

print("\n" + "=" * 60)
if all_elements_found:
    print("✅ ТЕСТ ПРОЙДЕН: Все элементы найдены!")
else:
    print(f"❌ ТЕСТ НЕ ПРОЙДЕН: Отсутствуют элементы:")
    for elem in missing_elements:
        print(f"   - {elem}")
print("=" * 60)

print("\n5. Закрываем браузер...")
driver.quit()
print("   ✓ Браузер закрыт")

input("\nНажмите Enter для выхода...")