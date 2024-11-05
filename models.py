# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Counselor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    def __str__(self):
        return self.user.username

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    counselor = models.ForeignKey(Counselor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled')], default='Pending')

    def __str__(self):
        return f"Appointment with {self.counselor.user.username} on {self.date}"


class CounselingMaterial(models.Model):
    MATERIAL_TYPES = [
        ('PDF', 'PDF'),
        ('Video', 'Video'),
        ('Text', 'Text'),
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    material_type = models.CharField(max_length=10, choices=MATERIAL_TYPES)
    upload_date = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='materials/', null=True, blank=True)  # For PDF and video uploads
    content = models.TextField(null=True, blank=True)  # For text-based content
    image = models.ImageField(upload_to='materials/images/', null=True, blank=True)  # Add this line for images
    video_url = models.URLField(null=True, blank=True)  # For YouTube video links

    def __str__(self):
        return self.title



        
# models.py

class ContactMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contact_messages")
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.user.username} - {self.subject}"
