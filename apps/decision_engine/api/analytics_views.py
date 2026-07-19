"""
Decision analytics API views.
"""

from django.db.models import (
    Avg,
    Count,
)

from rest_framework.views import (
    APIView,
)

from rest_framework.response import (
    Response,
)

from rest_framework import status

from drf_spectacular.utils import (
    extend_schema,
)

from apps.decision_engine.models import (
    DecisionLog,
)


class DecisionAnalyticsAPIView(
    APIView
):

    """
    Enterprise decision analytics endpoint.
    """

    @extend_schema(
        tags=["Decision Analytics"]
    )
    def get(
        self,
        request,
    ):

        # ==========================================
        # TOTALS
        # ==========================================

        total_decisions = (
            DecisionLog.objects.count()
        )

        successful = (

            DecisionLog.objects.filter(
                status="success"
            ).count()
        )

        failed = (

            DecisionLog.objects.filter(
                status="failed"
            ).count()
        )

        rewrite_required = (

            DecisionLog.objects.filter(
                rewrite_required=True
            ).count()
        )

        publish_ready = (

            DecisionLog.objects.filter(
                should_generate=True
            ).count()
        )

        # ==========================================
        # SUCCESS RATE
        # ==========================================

        success_rate = 0

        if total_decisions > 0:

            success_rate = round(

                (
                    successful
                    / total_decisions
                ) * 100,

                2,
            )

        # ==========================================
        # GLOBAL AVERAGES
        # ==========================================

        averages = (

            DecisionLog.objects.aggregate(

                avg_seo_score=(
                    Avg("seo_score")
                ),

                avg_quality_score=(
                    Avg("quality_score")
                ),

                avg_publish_score=(
                    Avg("publish_score")
                ),

                avg_ai_quality_score=(
                    Avg("ai_quality_score")
                ),

                avg_execution_time=(
                    Avg("execution_time")
                ),

                avg_response_time=(
                    Avg("response_time")
                ),

                avg_provider_latency=(
                    Avg("provider_latency")
                ),

                avg_token_usage=(
                    Avg("token_usage")
                ),

                avg_estimated_cost=(
                    Avg("estimated_cost")
                ),
            )
        )

        # ==========================================
        # PROVIDER BENCHMARKS
        # ==========================================

        provider_benchmarks = (

            DecisionLog.objects.values(
                "provider"
            )

            .annotate(

                total_requests=(
                    Count("id")
                ),

                avg_publish_score=(
                    Avg("publish_score")
                ),

                avg_ai_quality_score=(
                    Avg("ai_quality_score")
                ),

                avg_execution_time=(
                    Avg("execution_time")
                ),

                avg_response_time=(
                    Avg("response_time")
                ),

                avg_provider_latency=(
                    Avg("provider_latency")
                ),

                avg_token_usage=(
                    Avg("token_usage")
                ),

                avg_estimated_cost=(
                    Avg("estimated_cost")
                ),
            )

            .order_by(
                "-avg_publish_score"
            )
        )

        # ==========================================
        # PROVIDER USAGE
        # ==========================================

        provider_usage = (

            DecisionLog.objects.values(
                "provider"
            )

            .annotate(
                total=Count("id")
            )

            .order_by(
                "-total"
            )
        )

        # ==========================================
        # TOP KEYWORDS
        # ==========================================

        top_keywords = (

            DecisionLog.objects.values(
                "keyword"
            )

            .annotate(
                total=Count("id")
            )

            .order_by(
                "-total"
            )[:10]
        )

        # ==========================================
        # FASTEST PROVIDER
        # ==========================================

        fastest_provider = None

        if provider_benchmarks:

            fastest_provider = min(

                provider_benchmarks,

                key=lambda x:
                x.get(
                    "avg_response_time"
                ) or 9999
            )

        # ==========================================
        # CHEAPEST PROVIDER
        # ==========================================

        cheapest_provider = None

        if provider_benchmarks:

            cheapest_provider = min(

                provider_benchmarks,

                key=lambda x:
                x.get(
                    "avg_estimated_cost"
                ) or 9999
            )

        # ==========================================
        # BEST QUALITY PROVIDER
        # ==========================================

        best_quality_provider = None

        if provider_benchmarks:

            best_quality_provider = max(

                provider_benchmarks,

                key=lambda x:
                x.get(
                    "avg_ai_quality_score"
                ) or 0
            )

        # ==========================================
        # FINAL RESPONSE
        # ==========================================

        return Response(

            {

                "success": True,

                "analytics": {

                    # ======================
                    # CORE
                    # ======================

                    "total_decisions": (
                        total_decisions
                    ),

                    "successful": (
                        successful
                    ),

                    "failed": (
                        failed
                    ),

                    "success_rate": (
                        success_rate
                    ),

                    "rewrite_required": (
                        rewrite_required
                    ),

                    "publish_ready": (
                        publish_ready
                    ),

                    # ======================
                    # AVERAGES
                    # ======================

                    "average_scores": (
                        averages
                    ),

                    # ======================
                    # PROVIDERS
                    # ======================

                    "provider_usage": list(
                        provider_usage
                    ),

                    "provider_benchmarks": list(
                        provider_benchmarks
                    ),

                    "fastest_provider": (
                        fastest_provider
                    ),

                    "cheapest_provider": (
                        cheapest_provider
                    ),

                    "best_quality_provider": (
                        best_quality_provider
                    ),

                    # ======================
                    # KEYWORDS
                    # ======================

                    "top_keywords": list(
                        top_keywords
                    ),
                },
            },

            status=status.HTTP_200_OK,
        )