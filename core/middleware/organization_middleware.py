from django.utils.deprecation import MiddlewareMixin
from ..tenant_context import set_current_organization, clear_current_organization


class OrganizationMiddleware(MiddlewareMixin):
    """
    Attach the current organization to the request object.

    After this middleware:
        request.organization
    will be available across the project.
    """

    def process_request(self, request):
        request.organization = None

        if hasattr(request, "user") and request.user.is_authenticated:
            request.organization = getattr(request.user, "organization", None)

        set_current_organization(request.organization)


    def process_response(self, request, response):
        clear_current_organization()
        return response


    def process_exception(self, request, exception):
        clear_current_organization()
        return None


