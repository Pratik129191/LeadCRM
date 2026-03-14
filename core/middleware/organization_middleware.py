from django.utils.deprecation import MiddlewareMixin
from ..tenant_context import set_current_organization


class OrganizationMiddleware(MiddlewareMixin):
    """
    Attach the current organization to the request object.

    After this middleware:
        request.organization
    will be available across the project.
    """

    def process_request(self, request):
        request.organization = None

        if not hasattr(request, 'user'):
            return

        if request.user.is_authenticated:
            request.organization = getattr(request.user, "organization", None)
        set_current_organization(request.organization)

