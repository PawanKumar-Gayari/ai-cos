from django.db import models


class EngineExecution(models.Model):

    engine_name = models.CharField(
        max_length=255
    )

    keyword = models.CharField(
        max_length=255
    )

    execution_time = models.FloatField(
        default=0
    )

    status = models.CharField(
        max_length=50,
        default="success"
    )

    score = models.FloatField(
        default=0
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
            f"{self.engine_name}"
        )