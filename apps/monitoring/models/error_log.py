from django.db import models


class ErrorLog(models.Model):

    request_id = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    error_type = models.CharField(
        max_length=255
    )

    message = models.TextField()

    traceback = models.TextField()

    path = models.TextField(
        blank=True,
        null=True
    )

    severity = models.CharField(
        max_length=50,
        default="error"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        ordering = [
            "-created_at"
        ]

    def __str__(self):

        return self.error_type