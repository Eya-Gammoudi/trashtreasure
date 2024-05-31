from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from django.forms import widgets
from django.contrib.gis.db import models
from .models import Greener, Offer

class ReadOnlyLeafletWidget(widgets.Widget):
    def render(self, name, value, attrs=None, renderer=None):
        return f'<div id="map" style="width: 100%; height: 400px;">{value}</div>'

class GreenerAdmin(LeafletGeoAdmin):
    list_display = ('FirstName', 'LastName', 'Email', 'PhoneNumber', 'is_active', 'is_approved')
    search_fields = ('FirstName', 'LastName', 'Email', 'PhoneNumber')
    list_filter = ('is_active', 'is_approved')
    readonly_fields = ('Location_map', 'FirstName', 'LastName', 'Email', 'PhoneNumber')
    formfield_overrides = {
        models.PointField: {'widget': ReadOnlyLeafletWidget},
    }

    def has_add_permission(self, request):
        return False  # Disable adding new greener users through admin

    def has_delete_permission(self, request, obj=None):
        return False  # Disable deleting greener users through admin
    

    def save_model(self, request, obj, form, change):
        # Only allow admin to modify is_approved, is_staff, and is_active fields
        obj.is_approved = form.cleaned_data['is_approved']
        obj.is_staff = form.cleaned_data['is_staff']
        obj.is_active = form.cleaned_data['is_active']
        obj.save()

    def Location_map(self, instance):
        # Return HTML for displaying the map
        if instance.Location:
            return f'<div id="map" style="width: 100%; height: 400px;">{instance.Location}</div>'
        else:
            return "No location provided."

    Location_map.short_description = "Location Map"

admin.site.register(Greener, GreenerAdmin)


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'manure', 'brown_material', 'green_material', 'date_range_start', 'date_range_end', 'Status')