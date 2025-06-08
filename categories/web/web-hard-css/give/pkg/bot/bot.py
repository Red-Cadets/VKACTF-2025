from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

host = os.environ.get("SERVICE_HOST")
port = os.environ.get("SERVICE_PORT")

admin_username = os.environ.get("ADMIN_USERNAME")
admin_pass = os.environ.get("ADMIN_PASSWORD")


BASE_URL = f"http://{host}:{port}"
ADMIN_USERNAME = admin_username
ADMIN_PASSWORD = admin_pass
PROFILE_URL = f"{BASE_URL}/profile/"
REFRESH_INTERVAL = 3

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def login(driver):
    logger.info("Выполняется вход в систему...")
    driver.get(f"{BASE_URL}/login/")
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "Username"))
    )
    
    username_field = driver.find_element(By.NAME, "Username")
    password_field = driver.find_element(By.NAME, "Password")
    
    username_field.clear()
    password_field.clear()
    
    username_field.send_keys(ADMIN_USERNAME)
    password_field.send_keys(ADMIN_PASSWORD)
    
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    
    WebDriverWait(driver, 10).until(
        EC.url_contains("/profile/")
    )
    logger.info("Вход выполнен успешно, перенаправлен в профиль.")

def get_themes(driver):
    themes = []
    try:
        theme_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "theme-item"))
        )
        
        for element in theme_elements:
            try:
                theme_id = element.find_element(By.NAME, "theme_id").get_attribute("value")
                name_element = element.find_element(By.XPATH, ".//a[contains(@onclick, 'switchTheme')]")
                theme_name = name_element.text
                delete_button = element.find_element(By.XPATH, ".//button[@type='submit']")
                themes.append({
                    "id": theme_id,
                    "name": theme_name,
                    "name_element": name_element,
                    "delete_button": delete_button
                })
            except Exception as e:
                logger.warning(f"Ошибка при обработке элемента темы: {e}")
                continue
                
        logger.info(f"Найдено тем: {len(themes)}")
    except Exception as e:
        logger.error(f"Ошибка при получении тем: {e}")
    return themes

def apply_and_delete_theme(driver, theme):
    try:
        logger.info(f"Применяется тема: {theme['name']} (ID: {theme['id']})")
        theme["name_element"].click()
        time.sleep(0.5)
        
        logger.info(f"Удаляется тема: {theme['name']} (ID: {theme['id']})")
        theme["delete_button"].click()
        
        WebDriverWait(driver, 10).until(
            EC.staleness_of(theme["delete_button"])
        )
        logger.info(f"Тема {theme['name']} успешно применена и удалена.")
        return True
    except Exception as e:
        logger.error(f"Ошибка при обработке темы {theme['name']}: {e}")
        return False

def main():
    driver = setup_driver()
    applied_themes = set()
    
    try:
        login(driver)
        
        while True:
            try:
                driver.get(PROFILE_URL)
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Profile')]"))
                )
                logger.info("Страница профиля загружена.")

                themes = get_themes(driver)
                
                for theme in themes:
                    if theme["id"] not in applied_themes:
                        if apply_and_delete_theme(driver, theme):
                            applied_themes.add(theme["id"])
                
                time.sleep(REFRESH_INTERVAL)
                
            except Exception as e:
                logger.error(f"Ошибка в основном цикле: {e}")
                try:
                    login(driver)
                except:
                    logger.error("Не удалось перелогиниться")
    
    except KeyboardInterrupt:
        logger.info("Бот остановлен по запросу пользователя")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
    finally:
        driver.quit()
        logger.info("Браузер закрыт. Работа бота завершена.")

if __name__ == "__main__":
    main()
