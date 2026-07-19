from django.urls import path

from apps.frontend.views import (

    home,

    about,

    privacy_policy,

    contact,
)


urlpatterns = [

    path(
        "",
        home,
        name="home",
    ),

    path(
        "about/",
        about,
        name="about",
    ),

    path(
    "privacy-policy/",
    privacy_policy,
    name="privacy-policy",
    ),

    path(
    "contact/",
    contact,
    name="contact",
    ),
]