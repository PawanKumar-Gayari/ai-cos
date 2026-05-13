from django.db import models


class APIRequestLog(models.Model):

    request_id = models.CharField(
        max_length=255,
        unique=True
    )

    method = models.CharField(
        max_length=20
    )

    path = models.TextField()

    status_code = models.IntegerField()

    execution_time = models.FloatField(
        default=0
    )

    ip_address = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    user_agent = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        ordering = [
            "-created_at"
        ]

    def __str__(self):

        return (
            f"{self.method} {self.path}"
        )