# Указывает Docker использовать официальный образ python 3 с dockerhub в качестве базового образа
FROM python:3.9.15-slim
# Устанавливает переменную окружения, которая гарантирует, что вывод из python будет отправлен прямо в терминал без предварительной буферизации
ENV PYTHONUNBUFFERED 1
# Устанавливает рабочий каталог контейнера — "app"
WORKDIR /app
EXPOSE 8000
COPY requirements.txt ./
# Запускает команду pip install для всех библиотек, перечисленных в requirements.txt
RUN pip install -r requirements.txt
# Копирует все файлы из нашего локального проекта в контейнер
COPY . .
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]