FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

WORKDIR /src

# Como temos apenas a pasta src, deixaremos os arquivos na pasta src do container
COPY src/ .

RUN useradd --create-home user
USER user

CMD ["python", "-m", "main"]