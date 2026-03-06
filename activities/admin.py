from django.contrib import admin
from .models import Activity

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = (
        'lead',
        'activity_type',
        'user',
        'next_follow_up',
        'created_at'
    )

    list_filter = (
        'activity_type',
        'created_at'
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if request.user.is_superuser:
            return qs

        return qs.filter(organization=request.user.organization)