import io
from PIL import Image
from django.db import models
from django.core.files.base import ContentFile
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    is_trainer = models.BooleanField(
        default=False,
        verbose_name='Trainer status',
        help_text='Designates whether this user is a trainer.'
    )
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='profiles/avatars/', null=True, blank=True)

    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        if self.avatar:
            # Process image if it exists
            image = Image.open(self.avatar)
            image = self.crop_to_square(image)
            
            # Save processed image to a temporary file
            temp_file = io.BytesIO()
            image.save(temp_file, format='JPEG')
            temp_file.seek(0)
            self.avatar.save(self.avatar.name, ContentFile(temp_file.read()), save=False)
        
        # Continue with the normal save method
        super(CustomUser, self).save(*args, **kwargs)

    def crop_to_square(self, image):
        # Calc short for calulator
        width, height = image.size
        min_side = min(width, height)
        
        # Calculate the coordinates for cropping the center square
        left = (width - min_side) / 2
        top = (height - min_side) / 2
        right = (width + min_side) / 2
        bottom = (height + min_side) / 2
        
        # Crop the image to the calculated square
        image = image.crop((left, top, right, bottom))

        # Resize the image to 250x250 pixels
        image = image.resize((250, 250), Image.Resampling.LANCZOS)
        
        # Convert image to RGB if it's not already in that mode
        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")
        
        return image

class Avatar(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='profiles/avatars/')

    def __str__(self):
        return self.name
    
class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    level = models.IntegerField(default=1)
    xp = models.IntegerField(default=0)
    avatar = models.ForeignKey(Avatar, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username

    def add_xp(self, points):
        self.xp += points
        self.check_level_up()
        self.save()

    def check_level_up(self):
    	# Simple example: increase level for every 1000 XP
        while self.xp >= self.level * 1000:
            self.level += 1

class SupportTicket(models.Model):
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject