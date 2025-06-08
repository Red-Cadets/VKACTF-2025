#!/bin/bash

echo "[CRON] Удаление приказов, кроме ID 1-8..."

psql "$DATABASE_URL" <<EOF
DELETE FROM "Order" WHERE id NOT IN (1,2,3,4,5,6,7,8);
DELETE FROM "Model" WHERE id NOT IN (1,2,3,4);
EOF

echo "[CRON] Готово."
