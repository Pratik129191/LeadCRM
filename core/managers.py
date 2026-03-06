from django.db import models


class OrganizationQuerySet(models.QuerySet):
    def for_org(self, organization):
        return self.filter(organization=organization)


class OrganizationManager(models.Manager):
    def get_queryset(self):
        return OrganizationQuerySet(self.model, using=self._db)

    def for_org(self, organization):
        return self.get_queryset().for_org(organization)

