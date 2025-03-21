from django.db import models
import uuid
# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Customers(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="Customers")
    name = models.CharField(max_length=255)
    email = models.EmailField()
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, null=True)

    STATUS_CHOICES = [
        ('pending', 'Ожидание'),
        ('attended', 'Пришел'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    def __str__(self):
        return f"{self.name} - {self.event.title}"