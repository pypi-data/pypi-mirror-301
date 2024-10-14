from django.db import models

class EmotionAnalysis(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images/')
    emotion = models.CharField(max_length=50)
    message = models.TextField()

    def __str__(self):
        return f"{self.timestamp} - {self.emotion}"