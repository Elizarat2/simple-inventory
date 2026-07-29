# Utiliza una imagen oficial y ligera de Python en versión slim
FROM python:3.10-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Instala dependencias del sistema necesarias si alguna librería lo requiere
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copia e instala los requerimientos de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código del proyecto al contenedor
COPY . .

# Expone el puerto en el que correrá Flask
EXPOSE 5000

# Define el comando para ejecutar la aplicación usando Gunicorn para producción o run.py
CMD ["python", "run.py"]