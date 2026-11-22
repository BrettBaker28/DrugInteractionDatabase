from django.db import models

# Create your models here.

class Drug(models.Model):
    ddinter_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
