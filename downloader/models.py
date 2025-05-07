from django.db import models

# Create your models here.

class Download(models.Model):
    url = models.URLField(max_length=500)
    title = models.CharField(max_length=255, blank=True, null=True)
    format = models.CharField(max_length=10)  # 'video' or 'audio'
    file_path = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or self.url
