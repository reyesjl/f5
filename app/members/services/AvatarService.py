import io
from PIL import Image
from django.core.files.base import ContentFile

def process_avatar(image_file):
    image = Image.open(image_file)
    image = crop_to_square(image)
    image = resize_image(image)
    return image

def crop_to_square(image):
    width, height = image.size
    min_side = min(width, height)
    left = (width - min_side) / 2
    top = (height - min_side) / 2
    right = (width + min_side) / 2
    bottom = (height + min_side) / 2
    image = image.crop((left, top, right, bottom))
    return image

def resize_image(image):
    image = image.resize((250, 250), Image.Resampling.LANCZOS)
    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")
    return image

def save_processed_avatar(image, avatar_field):
    temp_file = io.BytesIO()
    image.save(temp_file, format='JPEG')
    temp_file.seek(0)
    avatar_field.save(avatar_field.name, ContentFile(temp_file.read()), save=False)
    
def delete_old_avatar(old_avatar):
    if old_avatar and old_avatar != 'default_avatar.png':
        old_avatar.delete(save=False)