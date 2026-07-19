from django.shortcuts import redirect


class APILoginRequiredMiddleware:

    """
    Protect dashboard and APIs.
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

        protected_prefixes = [

            "/api/",

            "/dashboard/",
        ]

        public_paths = [

            "/login/",

            "/logout/",

            "/password-reset/",

            "/reset/",

            "/admin/login/",
        ]

        path = request.path

        protected = any(

            path.startswith(prefix)

            for prefix in protected_prefixes
        )

        public = any(

            path.startswith(public_path)

            for public_path in public_paths
        )

        if (

            protected

            and not public

            and not request.user.is_authenticated
        ):

            return redirect(
                "/login/"
            )

        return self.get_response(
            request
        )