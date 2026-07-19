"""
Dashboard authentication middleware.
"""

from django.shortcuts import redirect


class DashboardLoginRequiredMiddleware:

    """
    Protect dashboard pages only.
    """

    def __init__(

        self,

        get_response,
    ):

        self.get_response = (
            get_response
        )

    def __call__(

        self,

        request,
    ):

        # ======================================
        # PROTECTED DASHBOARD ROUTES
        # ======================================

        protected_paths = [

            "/dashboard/",
        ]

        # ======================================
        # CHECK AUTH
        # ======================================

        for path in protected_paths:

            if request.path.startswith(

                path

            ):

                if (

                    not request.user.is_authenticated
                ):

                    return redirect(
                        "/login/"
                    )

        return self.get_response(
            request
        )