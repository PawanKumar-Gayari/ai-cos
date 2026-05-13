from django.urls import include, path


urlpatterns = [

    # API Version 1
    path("v1/", include("apps.api.v1.urls")),

]