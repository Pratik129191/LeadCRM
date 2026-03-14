from django.utils.deprecation import MiddlewareMixin


class OrganizationMiddleware(MiddlewareMixin):
    """
    Attach the current organization to the request object.

    After this middleware:
        request.organization
    will be available across the project.
    """

    def process_request(self, request):
        request.organization = None

        if request.user.is_authenticated:
            request.organization = getattr(request.user, "organization", None)

