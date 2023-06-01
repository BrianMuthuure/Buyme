from django.db import models


class EmailMessage(models.Model):
    email = models.EmailField()
    subject = models.CharField(max_length=250)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return f'{self.email} - {self.subject}'
