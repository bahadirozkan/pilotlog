from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportMixin
from .models import User, Aircraft, AircraftMeta


class UserResource(resources.ModelResource):
    class Meta:
        model = User


class AircraftResource(resources.ModelResource):
    class Meta:
        model = Aircraft


class AircraftMetaResource(resources.ModelResource):
    class Meta:
        model = AircraftMeta


class UserAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = UserResource
    list_display = ('user_id', )


class AircraftAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = AircraftResource
    list_display = ('guid', 'user', 'table', 'platform', '_modified')
    search_fields = ['guid', 'user__user_id', 'table']


class AircraftMetaAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = AircraftMetaResource
    list_display = ('aircraft', 'fin', 'sea', 'tmg', 'efis')
    search_fields = ['aircraft__guid']


admin.site.register(User, UserAdmin)
admin.site.register(Aircraft, AircraftAdmin)
admin.site.register(AircraftMeta, AircraftMetaAdmin)