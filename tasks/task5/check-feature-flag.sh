#!/bin/bash

set -e

echo "▶️ Проверка Feature Flag (X-Feature-Enabled: true)..."

echo "Сначала отправляем запросы без заголовка, чтобы убедиться, что маршрутизация идёт согласно весам"
for i in {1..10}
do
    curl -s http://localhost:9090/index
    echo ''
done

echo "\nТеперь отправляем заголовок, чтобы маршрутизация отправляла запрос на v2"
for i in {1..10}
do
    curl -H "X-Feature-Enabled: true" http://localhost:9090/index
    echo ''
done


