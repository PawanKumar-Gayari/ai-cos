from django.contrib.auth.decorators import (
    login_required,
)

from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)

from apps.dashboard.models import (
    SystemFeature,
)

from apps.dashboard.services.feature_service import (
    FeatureService,
)

from apps.monitoring.services.system_monitor import (
    SystemMonitor,
)

from apps.keywords.models import (
    KeywordResearchJob,
)

from apps.keywords.tasks import (
    run_keyword_pipeline,
)


# =========================================================
# DASHBOARD HOME
# =========================================================

@login_required
def index(
    request
):

    stats = (
        SystemMonitor.get_system_stats()
    )

    report = (
        SystemMonitor().full_report()
    )

    features = (
        FeatureService.get_features()
    )

    system_status = (
        FeatureService.system_status()
    )

    return render(

        request,

        "dashboard/index.html",

        {

            "stats": stats,

            "report": report,

            "features": features,

            "system_status": (
                system_status
            ),
        }
    )


# =========================================================
# MONITORING PAGE
# =========================================================

@login_required
def monitoring(
    request
):

    stats = (
        SystemMonitor.get_system_stats()
    )

    report = (
        SystemMonitor().full_report()
    )

    return render(

        request,

        "dashboard/monitoring.html",

        {

            "stats": stats,

            "report": report,
        }
    )


# =========================================================
# GENERATOR PAGE
# =========================================================

@login_required
def generator(
    request
):

    features = (
        FeatureService.get_features()
    )

    system_status = (
        FeatureService.system_status()
    )

    return render(

        request,

        "dashboard/generator.html",

        {

            "features": features,

            "system_status": (
                system_status
            ),
        }
    )


# =========================================================
# FEATURE TOGGLE
# =========================================================

@login_required
def toggle_feature(
    request,
    pk,
):

    feature = get_object_or_404(

        SystemFeature,

        pk=pk,
    )

    FeatureService.toggle(
        feature.key
    )

    return redirect(
        "dashboard-home"
    )


# =========================================================
# KEYWORDS DASHBOARD
# =========================================================

@login_required
def keywords_dashboard(
    request
):

    error_message = None

    latest_jobs = (

        KeywordResearchJob.objects
        .order_by(
            "-created_at"
        )[:10]
    )

    if request.method == "POST":

        keyword = (
            request.POST.get(
                "keyword"
            )
        )

        try:

            # =========================================
            # CREATE JOB
            # =========================================

            job = (

                KeywordResearchJob.objects
                .create(
                    keyword=keyword
                )
            )

            # =========================================
            # RUN CELERY TASK
            # =========================================

            task = (
                run_keyword_pipeline.delay(
                    job.id
                )
            )

            # =========================================
            # STORE TASK ID
            # =========================================

            job.celery_task_id = (
                task.id
            )

            job.save()

            # =========================================
            # REDIRECT RESULTS
            # =========================================

            return redirect(

                "keyword-results",

                job_id=job.id,
            )

        except Exception as error:

            error_message = str(
                error
            )

    return render(

        request,

        "dashboard/keywords.html",

        {

            "latest_jobs": (
                latest_jobs
            ),

            "error_message": (
                error_message
            ),
        },
    )


# =========================================================
# JOB RESULTS PAGE
# =========================================================

@login_required
def keyword_results(
    request,
    job_id,
):

    job = get_object_or_404(

        KeywordResearchJob,

        id=job_id,
    )

    return render(

        request,

        "dashboard/keyword_results.html",

        {

            "job": job,

            "result": (
                job.result
            ),

            "status": (
                job.status
            ),

            "progress": (
                job.progress
            ),
        },
    )