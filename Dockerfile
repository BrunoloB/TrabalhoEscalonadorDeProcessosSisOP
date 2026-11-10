FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

WORKDIR /src

COPY src/ ./src/

RUN useradd --create-home user
USER user

CMD ["python", "-m", "src.main"]