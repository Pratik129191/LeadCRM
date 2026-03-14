from django.contrib import admin
from .models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'business_type',
        'phone',
        'status',
        'estimated_value',
        'assigned_to',
        'created_at'
    )

    list_filter = (
        'status',
        'business_type',
    )

    search_fields = (
        'name',
        'phone',
        'email'
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(organization=request.organization)

