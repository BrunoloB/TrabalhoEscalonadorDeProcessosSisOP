FROM python:3.14-slim

# Evita criar __pycache__ e garante saída imediata no terminal
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

WORKDIR /src

# O código-fonte fica apenas na pasta src, que vira /src dentro do container
COPY src/ .

# Executa como usuário comum (sem privilégios de root)
RUN useradd --create-home user
USER user

CMD ["python", "-m", "main"]