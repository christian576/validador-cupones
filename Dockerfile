# Usa una imagen base oficial de Python
FROM python:3.9-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de requisitos y luego instala las dependencias
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia el contenido de la aplicación
COPY . .

# Comando por defecto para ejecutar la aplicación
CMD ["python", "app.py"]


