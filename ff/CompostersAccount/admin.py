from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.gis.db import models
from leaflet.admin import LeafletGeoAdmin
from GreenersAccount.admin import ReadOnlyLeafletWidget
from .models import Composter

class ComposterAdmin(LeafletGeoAdmin):
    list_display = ('Email', 'OrganizationName', 'CommunityName', 'PhoneNumber', 'Location', 'is_staff', 'is_approved')
    search_fields = ('Email', 'OrganizationName', 'CommunityName', 'PhoneNumber')
    ordering = ('Email',)
    filter_horizontal = ()
    list_filter = ('is_approved',)
    readonly_fields = ('Location_map',)
    formfield_overrides = {
        models.PointField: {'widget': ReadOnlyLeafletWidget},
    }
    
    def has_add_permission(self, request):
        return False  # Disable adding new greener users through admin

    def has_delete_permission(self, request, obj=None):
        return False  # Disable deleting greener users through admin

    def save_model(self, request, obj, form, change):
        # Only allow admin to modify is_approved, is_staff, and is_active fields
        obj.is_approved = form.cleaned_data.get('is_approved', obj.is_approved)
        obj.is_staff = form.cleaned_data.get('is_staff', obj.is_staff)
        obj.is_active = form.cleaned_data.get('is_active', obj.is_active)
        obj.save()

    def Location_map(self, instance):
        # Return HTML for displaying the map
        if instance.Location:
            return f'<div id="map" style="width: 100%; height: 400px;" data-lat="{instance.Location.y}" data-lng="{instance.Location.x}"></div>'
        else:
            return "No location provided."

    Location_map.short_description = "Location Map"

    fieldsets = (
        (None, {'fields': ('Email', 'password')}),
        ('Personal Info', {'fields': ('OrganizationName', 'CommunityName', 'PhoneNumber')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_approved', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login',)}),
        ('Location', {'fields': ('Location_map',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('Email', 'OrganizationName', 'CommunityName', 'PhoneNumber', 'password1', 'password2'),
        }),
    )

admin.site.register(Composter, ComposterAdmin)
