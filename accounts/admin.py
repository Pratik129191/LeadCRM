from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Organization


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'owner',
        'created_at',
    )

    search_fields = (
        'name',
    )


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(organization=request.organization)

    fieldsets = (
        ("Organization Info", {
            "fields": ('organization', 'role'),
        }),
    )

    list_display = (
        'username',
        'email',
        'role',
        'organization',
        'is_staff',
    )

    list_filter = (
        'role',
        'organization',
    )




