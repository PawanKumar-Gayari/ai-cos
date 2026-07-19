from django.db import models


class ErrorLog(
    models.Model
):

    SEVERITY_CHOICES = [

        ("info", "Info"),

        ("warning", "Warning"),

        ("error", "Error"),

        ("critical", "Critical"),
    ]

    # ==========================================
    # REQUEST TRACE
    # ==========================================

    request_id = models.CharField(

        max_length=255,

        blank=True,

        null=True,
    )

    path = models.TextField(

        blank=True,

        null=True,
    )

    method = models.CharField(

        max_length=20,

        blank=True,

        null=True,
    )

    # ==========================================
    # ERROR DETAILS
    # ==========================================

    error_type = models.CharField(
        max_length=255
    )

    message = models.TextField()

    traceback = models.TextField(

        blank=True,

        null=True,
    )

    source = models.CharField(

        max_length=255,

        blank=True,

        null=True,
    )

    # ==========================================
    # SEVERITY
    # ==========================================

    severity = models.CharField(

        max_length=50,

        choices=SEVERITY_CHOICES,

        default="error",
    )

    resolved = models.BooleanField(
        default=False
    )

    resolved_at = models.DateTimeField(

        blank=True,

        null=True,
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

        verbose_name = (
            "Error Log"
        )

        verbose_name_plural = (
            "Error Logs"
        )

    def __str__(
        self
    ):

        return (

            f"{self.error_type} | "

            f"{self.severity}"
        )