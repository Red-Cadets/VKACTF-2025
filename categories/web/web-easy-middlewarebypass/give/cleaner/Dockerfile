FROM postgres:16-alpine

COPY clean.sh /clean.sh
RUN chmod +x /clean.sh

# Запускаем скрипт каждые 30 секунд
CMD ["sh", "-c", "while true; do /clean.sh; sleep 30; done"]
