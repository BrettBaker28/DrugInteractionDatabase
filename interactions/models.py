from django.db import models

# Create your models here.

class Drug(models.Model):
    ddinter_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class DrugInteraction(models.Model):
    ddinter_id_a = models.CharField(max_length=50)
    drug_a = models.CharField(max_length=255)
    ddinter_id_b = models.CharField(max_length=50)
    drug_b = models.CharField(max_length=255)
    level = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.drug_a} + {self.drug_b}"