# Imagen base
FROM python

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo
WORKDIR /app

# Copiar requirements
COPY requirements.txt .

# Actualizar pip e instalar dependencias reales
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copiar el código
COPY . .



# Comando por defecto: iniciar nodo
CMD ["python", "main.py"]
