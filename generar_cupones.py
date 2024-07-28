import qrcode
import psycopg2
import qrcode
import psycopg2
import os
from urllib.parse import urlparse
from PIL import Image, ImageDraw, ImageFont
import uuid

def generar_cupones(cantidad):
    # Obtener la URL de la base de datos desde las variables de entorno
    DATABASE_URL = os.environ['DATABASE_URL']
    result = urlparse(DATABASE_URL)
    username = result.username
    password = result.password
    database = result.path[1:]
    hostname = result.hostname
    port = result.port

    # Conectar a la base de datos
    conn = psycopg2.connect(
        database=database,
        user=username,
        password=password,
        host=hostname,
        port=port
    )
    cursor = conn.cursor()

    # Crear la tabla de vouchers si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vouchers (
            code TEXT PRIMARY KEY,
            used INTEGER DEFAULT 0
        );
    ''')
    conn.commit()

    # Cargar la imagen de la marca
    logo = Image.open("logo.png").convert("RGBA")

    # Cargar la nueva fuente estilizada
    font_path = "fonts/Microstyle Bold Extended ATT.ttf"
    font_large = ImageFont.truetype(font_path, 14)  # Reducir tamaño de fuente
    font_small = ImageFont.truetype(font_path, 12)  # Reducir tamaño de fuente

    # Definir el color del texto para que coincida con el del logo
    text_color = (128, 0, 0)  # Usar un color marrón oscuro similar al del logo

    # Generar códigos QR y guardarlos en la base de datos y como imágenes
    os.makedirs("qrcodes", exist_ok=True)
    for _ in range(cantidad):
        code = str(uuid.uuid4())
        qr = qrcode.make(code)
        
        # Crear una nueva imagen para el cupón
        coupon = Image.new("RGB", (400, 600), "white")
        draw = ImageDraw.Draw(coupon)
        
        # Pegar el logo en la parte superior del cupón
        logo.thumbnail((300, 100))
        coupon.paste(logo, (50, 20), logo)

        # Pegar el QR code en el centro del cupón
        qr.thumbnail((200, 200))
        coupon.paste(qr, (100, 150))

        # Agregar el código alfanumérico centrado
        code_bbox = draw.textbbox((0, 0), code, font=font_small)
        code_width = code_bbox[2] - code_bbox[0]
        code_x = (coupon.width - code_width) // 2
        draw.text((code_x, 370), code, fill=text_color, font=font_small)

        # Agregar el mensaje de invitación con estilo y centrado
        mensaje = "Te invitamos a disfrutar\nde una cena gratis en nuestro local.\nEste descuento es de $100000."
        lines = mensaje.split('\n')
        y_text = 450
        for line in lines:
            line_bbox = draw.textbbox((0, 0), line, font=font_large)
            line_width = line_bbox[2] - line_bbox[0]
            line_x = (coupon.width - line_width) // 2
            draw.text((line_x, y_text), line, fill=text_color, font=font_large)
            y_text += line_bbox[3] - line_bbox[1]
        
        # Agregar un recuadro alrededor de toda la imagen
        draw.rectangle([(0, 0), (coupon.width - 1, coupon.height - 1)], outline=text_color, width=5)
        
        # Guardar la imagen del cupón
        coupon.save(f"qrcodes/{code}.png")
        
        cursor.execute('INSERT INTO vouchers (code, used) VALUES (%s, %s) ON CONFLICT (code) DO NOTHING', (code, False))
        conn.commit()

    cursor.close()
    conn.close()

    print(f"{cantidad} códigos QR generados, guardados en la base de datos y como imágenes en la carpeta 'qrcodes'.")
