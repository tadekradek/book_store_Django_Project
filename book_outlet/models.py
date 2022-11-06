from django.db import models

# Create your models here. #every time I edit models.py file, I need to make sure that I make migration to sent instruction for Django how to update database

class Book(models.Model): #my class that I just created inherits from Django-specific models.Model class that is useful and provides built-in functionalites
    title = models.CharField(max_length = 50)
    rating = models.IntegerField()