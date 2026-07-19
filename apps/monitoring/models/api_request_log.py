from django.db import models


class APIRequestLog(
    models.Model
):

    METHOD_CHOICES = [

        ("GET", "GET"),

        ("POST", "POST"),

        ("PUT", "PUT"),

        ("PATCH", "PATCH"),

        ("DELETE", "DELETE"),
    ]

    # ==========================================
    # REQUEST INFO
    # ==========================================

    request_id = models.CharField(

        max_length=255,

        unique=True,
    )

    method = models.CharField(

        max_length=20,

        choices=METHOD_CHOICES,
    )

    path = models.TextField()

    query_params = models.TextField(

        blank=True,

        null=True,
    )

    # ==========================================
    # RESPONSE
    # ==========================================

    status_code = models.IntegerField()

    execution_time = models.FloatField(
        default=0
    )

    response_size_kb = models.FloatField(
        default=0
    )

    # ==========================================
    # CLIENT INFO
    # ==========================================

    ip_address = models.CharField(

        max_length=255,

        blank=True,

        null=True,
    )

    user_agent = models.TextField(

        blank=True,

        null=True,
    )

    # ==========================================
    # REQUEST STATUS
    # ==========================================

    successful = models.BooleanField(
        default=True
    )

    error_message = models.TextField(

        blank=True,

        null=True,
    )

    # ==========================================
    # TIMESTAMPS
    # ==========================================

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        ordering = [
            "-created_at"
        ]

       