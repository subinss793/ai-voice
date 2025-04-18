from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    standard = models.CharField(max_length=50, null=True, blank=True)

class PronunciationRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Reference the custom User model
    word = models.CharField(max_length=100)
    spoken_word = models.CharField(max_length=100)
    accuracy = models.FloatField(default=100.0)
    timestamp = models.DateTimeField(auto_now_add=True)


from django.db import models

class TestProgress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    progress = models.IntegerField(default=0)
    level = models.CharField(max_length=50, default="Beginner")

    def __str__(self):
        return f'{self.user.username} - {self.progress}%'


from django.db import models
from .models import User

class Question(models.Model):
    LEVEL_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ]
    
    question = models.TextField()
    answer_key = models.CharField(max_length=100)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='Beginner')
    hint = models.TextField(blank=True, null=True)  # New column for hints


    def __str__(self):
        return f'{self.level} - {self.question[:50]}'