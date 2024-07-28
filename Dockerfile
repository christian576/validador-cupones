FROM python:3.9-slim

WORKDIR /app

# Instala las dependencias
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia el contenido del directorio actual al directorio de trabajo en la imagen
COPY . .

# Establece las variables de entorno
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Exponer el puerto en el que correrá la app
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]

