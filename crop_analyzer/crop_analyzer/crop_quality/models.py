from django.db import models
from django.core.validators import FileExtensionValidator

# Create your models here.

class CropImage(models.Model):
    QUALITY_CHOICES = [
        ('high', 'High Quality'),
        ('intermediate', 'Intermediate Quality'),
        ('low', 'Low Quality'),
    ]
    
    image = models.ImageField(
        upload_to='crop_images/',
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])]
    )
    quality = models.CharField(
        max_length=20,
        choices=QUALITY_CHOICES,
        blank=True
    )
    remarks = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Crop Image {self.id} - {self.quality}"
