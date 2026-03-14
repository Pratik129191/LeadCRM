from django.contrib import admin
from .models import Deal


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):

    list_display = (
        "lead",
        "value",
        "closed_by",
        "closed_at",
    )

    list_filter = (
        "closed_at",
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if request.user.is_superuser:
            return qs

        return qs.filter(organization=request.organization)