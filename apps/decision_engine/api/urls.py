from django.urls import (
    path,
)

from apps.decision_engine.api.decision_views import (
    DecisionAPIView,
)
from apps.decision_engine.api.analytics_views import (
    DecisionAnalyticsAPIView,
)


urlpatterns = [

    path(

        "evaluate/",

        DecisionAPIView.as_view(),

        name="decision-evaluate",
    ),
    path(

    "analytics/",

    DecisionAnalyticsAPIView.as_view(),

    name="decision-analytics",
),
]