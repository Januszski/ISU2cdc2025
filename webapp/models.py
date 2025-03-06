import uuid
from django.db import models

class DownloadLink(models.Model):
    email = models.EmailField()
    token = models.CharField(max_length=255, unique=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.email} - {'Used' if self.used else 'Unused'}"


class SoftwareVersion(models.Model):
    version_number = models.CharField(max_length=10)
    release_date = models.DateField()
    description = models.TextField()

    def __str__(self):
        return f"Version {self.version_number} - Released {self.release_date}"