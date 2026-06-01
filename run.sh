#!/bin/bash
if [ ! -d 'inbox' ]; then
    echo "ОШИБКА: Не найдена папка 'inbox'. Пожалуйста, создайте его и поместите туда файлы для обработки."
    exit 1
fi

mkdir -p logs

python3 main.py "$@" | tee logs/run.log

status=$?
if [ $status -eq 0 ]; then
    echo "Скрипт выполнен успешно."
else
    echo "Скрипт завершился с ошибкой. Код ошибки: $status"
fi