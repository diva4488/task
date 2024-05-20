from django.db import models

class Upload(models.Model):
    csv_file = models.FileField(upload_to='uploads/')
    created_at = models.DateTimeField(auto_now_add=True)

