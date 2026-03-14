from django.db import models
from .tenant_context import get_current_organization, is_system_mode
from .exceptions import TenantIsolationError

class OrganizationQuerySet(models.QuerySet):
    def for_org(self, organization):
        return self.filter(organization=organization)

    def active(self):
        return self.filter(is_deleted=False)

    def deleted(self):
        return self.filter(is_deleted=True)


class OrganizationManager(models.Manager):
    def get_queryset(self):
        query_set = OrganizationQuerySet(self.model, using=self._db)

        if is_system_mode():
            return query_set

        organization = get_current_organization()
        if organization is None:
            raise TenantIsolationError(
                f"{self.model.__name__} accessed without organization context"
            )
        return query_set.filter(organization=organization)

    def for_org(self, organization):
        return OrganizationQuerySet(self.model, using=self._db).filter(
            organization=organization
        )

    def active(self):
        return self.get_queryset().active()

    def deleted(self):
        return self.get_queryset().deleted()


