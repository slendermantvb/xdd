# Imagen base
FROM python:3.11-slim

# Evita archivos .pyc y buffers raros
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo
WORKDIR /

# Instalar dependencias
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install --upgrade pip

# Copiar el código
COPY . .

# Comando por defecto
CMD ["python", "main.py"]
