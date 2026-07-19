from django.conf import settings

from django.contrib import messages

from django.core.mail import send_mail

from django.shortcuts import (

    redirect,

    render,
)


def home(request):

    """
    Landing page.
    """

    return render(

        request,

        "home.html",
    )


def about(request):

    """
    About page.
    """

    return render(

        request,

        "about.html",
    )


def privacy_policy(request):

    """
    Privacy policy page.
    """

    return render(

        request,

        "privacy_policy.html",
    )


def contact(request):

    """
    Contact page.
    """

    if request.method == "POST":

        name = request.POST.get(
            "name"
        )

        email = request.POST.get(
            "email"
        )

        subject = request.POST.get(
            "subject"
        )

        message = request.POST.get(
            "message"
        )

        full_message = f"""

Name: {name}

Email: {email}

Subject: {subject}

Message:
{message}
"""

        try:

            send_mail(

                subject=(
                    f"AI COS Contact: {subject}"
                ),

                message=(
                    full_message
                ),

                from_email=(
                    settings.DEFAULT_FROM_EMAIL
                ),

                recipient_list=[

                    settings.CONTACT_EMAIL
                ],

                fail_silently=False,
            )

            messages.success(

                request,

                "Message sent successfully."
            )

        except Exception:

            messages.error(

                request,

                "Failed to send message."
            )

        return redirect(
            "/contact/"
        )

    return render(

        request,

        "contact.html",
    )