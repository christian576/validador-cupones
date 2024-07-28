# Utiliza una imagen base oficial de Python
FROM python:3.9-slim

# Establece la variable de entorno para que las salidas de python no sean almacenadas en búfer
ENV PYTHONUNBUFFERED=1

# Establece el directorio de trabajo
WORKDIR /app

# Copia los requisitos del archivo
COPY requirements.txt /app/

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el contenido del directorio actual en el contenedor
COPY . /app/

# Establece las variables de entorno
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Expone el puerto en el que correrá la aplicación
EXPOSE 8000

# Comando para correr la aplicación
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]


