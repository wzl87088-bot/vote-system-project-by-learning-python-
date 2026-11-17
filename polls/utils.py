import secrets
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont


def generate_captcha():
    chars = '23456789ABCDEFGHJKLMNPQRSTUVWXYZ'
    code = ''.join(secrets.choice(chars) for _ in range(4))

    image = Image.new('RGB', (160, 60), 'white')
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default(size=32)
    draw.text((20, 10), code, font=font, fill='darkblue')

    buffer = BytesIO()
    image.save(buffer, format='PNG')
    return code, buffer.getvalue()
