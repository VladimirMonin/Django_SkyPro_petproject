# Указывает Docker использовать официальный образ python:3.9.15-slim с dockerhub в качестве базового образа
FROM python:3.9.15-slim
# Устанавливает переменную окружения, которая гарантирует, что вывод из python будет отправлен прямо в терминал без предварительной буферизации
ENV PYTHONUNBUFFERED 1
# Устанавливает рабочий каталог контейнера — "app"
WORKDIR /app
# Говорим другим разработчикам, порт, на котором будет наше приложение
EXPOSE 8000
COPY requirements.txt ./
# Запускает команду pip install для всех библиотек, перечисленных в requirements.txt
RUN pip install -r requirements.txt
# Копирует все файлы из нашего локального проекта в контейнер
COPY . .
# Выполняет миграции и накатывает их (это так не работает, увы)
#CMD ["python", "manage.py", "makemigrations"]
#CMD ["python", "manage.py", "migrate"]
# Запускает скрипт в файле entrypoint.sh - который проведет миграции
ENTRYPOINT ["bash", "entrypoint.sh"]
# Запускает проект Django на порт 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]