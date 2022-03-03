import os
import requests
import shutil
from PIL import Image, ImageDraw, ImageFilter, ImageFont

img = Image.open('img/welcome-card.png')

res = requests.get('https://cdn.discordapp.com/avatars/796358028664242208/11f860a0c7d9ac923d485d08857587a2.png?size=1024', stream=True)
with open('img/avatar.png', 'wb') as out_file:
    shutil.copyfileobj(res.raw, out_file)
del res

img_sec = Image.open('img/avatar.png')


def crop_center(pil_img, crop_width, crop_height):
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))


def crop_max_square(pil_img):
    return crop_center(pil_img, min(pil_img.size), min(pil_img.size))


def mask_circle_trans(pil_img, blur_radius, offset=0):
    offset = blur_radius * 2 + offset
    mask = Image.new('L', pil_img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((offset, offset, pil_img.size[0] - offset, pil_img.size[1] - offset), fill=255, outline='black')
    mask = mask.filter((ImageFilter.GaussianBlur(0)))

    result = pil_img.copy()
    result.putalpha(mask)

    return result


def create_text(pil_img, text, color, offset=250):
    w, h = pil_img.size
    draw = ImageDraw.Draw(pil_img)
    fnt = ImageFont.truetype('font/Roboto-Bold.ttf', 25)

    W, H = draw.textsize(text, font=fnt)
    draw.text(((W-w) / -2, offset), text, fill=color, font=fnt)

    return pil_img


im_square = crop_max_square(img_sec).resize((186, 186), Image.LANCZOS)
img_cutted = mask_circle_trans(im_square, 0.1, 2)

w, h = img.size
W, H = img_cutted.size

img = create_text(img, "HV | exersalza[>'-']> Joined the Server", (255, 0, 0))
img = create_text(img, '#69420', (255, 0, 0), 290)
img.paste(img_cutted, (((W-w) // -2), ((H-h) // -3) - 53), img_cutted)
img.show()
img.save('img.png', save_all=True)
