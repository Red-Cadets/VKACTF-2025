import os
from selenium import webdriver
import time
import psycopg2
from psycopg2 import sql
import logging
from datetime import datetime
import redis

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

db_user = os.environ.get("POSTGRES_USER")
db_pass = os.environ.get("POSTGRES_PASSWORD")
db_name = os.environ.get("POSTGRES_DB")

host = os.environ.get("SERVICE_HOST")
port = os.environ.get("SERVICE_PORT")

redis_port = int(os.environ.get("REDIS_PORT"))
queue_key = os.environ.get("REDIS_QUEUE_KEY")

CONFIG = {
    'db': {
        'host': "web-m-hawk-postgres",
        'database': db_name,
        'user': db_user,
        'password': db_pass
    },
    'web': {
        'base_url': f"http://{host}:{port}/vote/",
        'check_interval': 10 
    },
    'redis':{
        'host': "web-m-hawk-redis",
        'port': redis_port,
        'db': 0
    }
}

class URLTracker:
    def __init__(self):
        self.redis=redis.Redis(
            host=CONFIG['redis']['host'],
            port=CONFIG['redis']['port'],
            db=CONFIG['redis']['db'],
            decode_responses=True
        )
        self.key_prefix="visited:"
    
    def _format_key(self, url):
        return f"{self.key_prefix}{url}"

    def add_url(self, url):
        self.redis.set(self._format_key(url), 1)
    
    def is_visited(self, url):
        return self.redis.exists(self._format_key(url))

def get_all_pool_uuids(conn):
    try:
        with conn.cursor() as cur:
            query = sql.SQL("SELECT uuid FROM pools")
            cur.execute(query)
            return [row[0] for row in cur.fetchall()]
    except Exception as e:
        logging.error(f"Ошибка при запросе к БД: {e}")
        return []

def visit_url(url):
    with open("./flag/flag", "r") as f:
        flag = f.read().strip()
    
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-extensions')

    driver = None
    try:
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        driver.add_cookie({
            'name': 'flag',
            'value': flag,
            'path': '/',
            'domain': host
        })
        driver.get(url)
        logging.info(f"Успешно посещён URL: {url}")
        time.sleep(3) 
        return True
    except Exception as e:
        logging.error(f"Ошибка при посещении {url}: {e}")
        return False
    finally:
        if driver is not None:
            driver.quit()

def main():
    tracker = URLTracker()
    logging.info("Бот запущен")
    
    r = redis.Redis(
        host=CONFIG['redis']['host'],
        port=CONFIG['redis']['port'],
        db=CONFIG['redis']['db'],
        decode_responses=True
    )

    try:
        while True:
            try:
                uuid = r.rpop(queue_key)
                if uuid:
                    url = CONFIG['web']['base_url'] + uuid
                    if not tracker.is_visited(url):
                        visit_url(url)
                    else:
                        logging.info(f"URL уже был посещён: {url}")
                else:
                    logging.info("Очередь пуста")
            except Exception as e:
                logging.error("Ощибка в одсновном цикле")    
            time.sleep(CONFIG['web']['check_interval'])
    
    except KeyboardInterrupt:
        logging.info("Бот остановлен по запросу пользователя")
    except Exception as e:
        logging.error(f"Критическая ошибка: {e}")
    finally:
        logging.info("Работа бота завершена")

if __name__ == "__main__":
    main()

# qazWSX123@