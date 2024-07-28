# Usa una imagen base oficial de Python
FROM python:3.11-slim

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia los archivos de requirements.txt al directorio de trabajo
COPY requirements.txt .

# Actualiza pip y luego instala las dependencias
RUN python -m pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copia el contenido del directorio actual al directorio de trabajo en la imagen
COPY . .

# Expone el puerto en el que se ejecutará la aplicación
EXPOSE 8000

# Define el comando para ejecutar la aplicación
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8000"]


