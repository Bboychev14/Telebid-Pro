import base64
import random
import string
from PIL import Image, ImageDraw, ImageFont


class CaptchaGenerator:

    @staticmethod
    def generate_captcha_text(length=6):
        """
        Generate random CAPTCHA text.
        """
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

    @staticmethod
    def generate_captcha_image(captcha_text, image_width=200, image_height=80):
        """
        Generate CAPTCHA image.
        """
        # Generate image
        image = Image.new('RGB', (image_width, image_height), color='white')
        draw = ImageDraw.Draw(image)

        # Load font
        font = ImageFont.truetype('arial.ttf', size=40)

        # Write CAPTCHA text on the image
        text_width, text_height = draw.textsize(captcha_text, font=font)
        draw.text(((image_width - text_width) // 2, (image_height - text_height) // 2),
                  captcha_text, fill='black', font=font)

        # Add noise to the image (e.g., random points or lines)
        for _ in range(50):
            draw.point((random.randint(0, image_width), random.randint(0, image_height)), fill='gray')
            draw.line([(random.randint(0, image_width), random.randint(0, image_height)),
                       (random.randint(0, image_width), random.randint(0, image_height))], fill='gray')

        # Save the image in PNG format
        image.save('captcha.png')

        # Return the image data as base64-encoded string
        with open('captcha.png', 'rb') as img_file:
            image_data = img_file.read()
            base64_image = base64.b64encode(image_data).decode('utf-8')

        return base64_image
