FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

WORKDIR /app

COPY app/ ./app/

RUN useradd --create-home user
USER user

CMD ["python", "-m", "app.main"]