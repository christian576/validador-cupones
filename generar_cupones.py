import qrcode
import qrcode
import psycopg2
import os
from urllib.parse import urlparse
from PIL import Image, ImageDraw, ImageFont
import uuid

def generar_cupones(cantidad):
    DATABASE_URL = os.environ['DATABASE_URL']
    result = urlparse(DATABASE_URL)
    username = result.username
    password = result.password
    database = result.path[1:]
    hostname = result.hostname
    port = result.port

    conn = psycopg2.connect(
        database=database,
        user=username,
        password=password,
        host=hostname,
        port=port
    )
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vouchers (
            code TEXT PRIMARY KEY,
            used BOOLEAN DEFAULT FALSE
        );
    ''')
    conn.commit()

    logo = Image.open("static/logo.png").convert("RGBA")

    font_path = "fonts/Microstyle Bold Extended ATT.ttf"
    font_large = ImageFont.truetype(font_path, 14)
    font_small = ImageFont.truetype(font_path, 12)

    text_color = (128, 0, 0)

    os.makedirs("static/qrcodes", exist_ok=True)
    for _ in range(cantidad):
        code = str(uuid.uuid4())
        qr = qrcode.make(code)
        
        coupon = Image.new("RGB", (400, 600), "white")
        draw = ImageDraw.Draw(coupon)
        
        logo.thumbnail((300, 100))
        coupon.paste(logo, (50, 20), logo)

        qr.thumbnail((200, 200))
        coupon.paste(qr, (100, 150))

        code_bbox = draw.textbbox((0, 0), code, font=font_small)
        code_width = code_bbox[2] - code_bbox[0]
        code_x = (coupon.width - code_width) // 2
        draw.text((code_x, 370), code, fill=text_color, font=font_small)

        mensaje = "Te invitamos a disfrutar\nde una cena gratis en nuestro local.\nEste descuento es de $100000."
        lines = mensaje.split('\n')
        y_text = 450
        for line in lines:
            line_bbox = draw.textbbox((0, 0), line, font=font_large)
            line_width = line_bbox[2] - line_bbox[0]
            line_x = (coupon.width - line_width) // 2
            draw.text((line_x, y_text), line, fill=text_color, font=font_large)
            y_text += line_bbox[3] - line_bbox[1]
        
        draw.rectangle([(0, 0), (coupon.width - 1, coupon.height - 1)], outline=text_color, width=5)
        
        coupon.save(f"static/qrcodes/{code}.png")
        
        cursor.execute('INSERT INTO vouchers (code, used) VALUES (%s, %s) ON CONFLICT (code) DO NOTHING', (code, False))
        conn.commit()

    cursor.close()
    conn.close()
    print(f"{cantidad} códigos QR generados, guardados en la base de datos y como imágenes en la carpeta 'static/qrcodes'.")
