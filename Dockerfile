# Фаза 1: Сглобяване
FROM python:3.9-slim as builder

# Задаване на работната директория в контейнера
WORKDIR /build

# Копиране на файловете със зависимостите и инсталирането им
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копиране на кода на приложението
COPY . .

# Инсталиране на зависимостите и сглобяване на приложението
RUN pip install --target=/build/dependencies -r requirements.txt

# Фаза 2: Изпълнение
FROM python:3.9-slim

# Задаване на работната директория в контейнера
WORKDIR /app

# Копиране на зависимостите от фазата на сглобяване
COPY --from=builder /build/dependencies /usr/local/lib/python3.9/site-packages

# Копиране на сглобеното приложение от фазата на сглобяване
COPY --from=builder /build .

# Експониране на порт 3000, на който Flask приложението ще слуша
EXPOSE 3000

# Командата, която ще се изпълни при стартиране на контейнера
CMD ["python", "app.py"]

