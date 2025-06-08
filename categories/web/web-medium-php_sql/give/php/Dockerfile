FROM php:7.4.30-fpm

RUN apt-get update && apt-get install -y \
    wget build-essential libreadline-dev libssl-dev \
    libz-dev libxml2-dev libsqlite3-dev \
    python3 python3-pip supervisor cron && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

ENV SQLITE_VERSION=3390200

RUN cd /tmp && \
    wget https://www.sqlite.org/2022/sqlite-autoconf-${SQLITE_VERSION}.tar.gz && \
    tar xzf sqlite-autoconf-${SQLITE_VERSION}.tar.gz && \
    cd sqlite-autoconf-${SQLITE_VERSION} && \
    ./configure --prefix=/usr/local && \
    make -j"$(nproc)" && \
    make install && \
    cd / && rm -rf /tmp/sqlite-autoconf*

RUN docker-php-ext-configure pdo_sqlite --with-pdo-sqlite=/usr/local && \
    docker-php-ext-install pdo pdo_sqlite

COPY php.ini /usr/local/etc/php/php.ini

COPY cleanup.py /usr/local/bin/cleanup.py
RUN chmod +x /usr/local/bin/cleanup.py

COPY crontab /etc/cron.d/db-cleaner
RUN chmod 0644 /etc/cron.d/db-cleaner && crontab /etc/cron.d/db-cleaner

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

WORKDIR /var/www/html

CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
