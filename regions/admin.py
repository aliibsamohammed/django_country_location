from django.contrib import admin
from django import forms
from .models import Continent, SubContinent, Country, State, City, Person, TimeZone
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin
from import_export import fields, resources
from import_export.admin import ExportActionMixin
from import_export.widgets import ForeignKeyWidget


@admin.register(Person)
class PersonAdmin(ImportExportModelAdmin):
    pass


class ContinentResource(resources.ModelResource):
    class Meta:
        model = Continent
        fields = ('name', 'code', 'id', )


class SubContinentResource(resources.ModelResource):
    continent = fields.Field(
            column_name='continent',
            attribute='continent',
            widget=ForeignKeyWidget(Continent, 'code'))

    class Meta:
        model = SubContinent
        fields = ('continent', 'name', 'id', )


class CountryResource(resources.ModelResource):
    continent = fields.Field(
            column_name='continent',
            attribute='continent',
            widget=ForeignKeyWidget(Continent, 'code'))

    subcontinent = fields.Field(
            column_name='subcontinent',
            attribute='subcontinent',
            widget=ForeignKeyWidget(SubContinent, 'name'))

    class Meta:
        model = Country
        fields = ('continent', 'country_code', 'country_name', 'id',)
    



class StateResource(resources.ModelResource):
    country = fields.Field(
            column_name='country',
            attribute='country',
            widget=ForeignKeyWidget(Country, 'country_code'))
    class Meta:
        model = State
        #import_id_fields = ('cont_Id',)
        fields = ('country', 'name', 'id')
#        widgets = {
#                'cont_StartDate': {'format': '%d.%m.%Y'},
#                'cont_CompletionDate': {'format': '%d.%m.%Y'},
#                }

class CityResource(resources.ModelResource):
    class Meta:
        model = City
        #import_id_fields = ('cont_Id',)
        fields = ('country', 'name')


class TimeZoneResource(resources.ModelResource):
    class Meta:
        model = TimeZone
        #import_id_fields = ('cont_Id',)
        fields = ('zoneName', 'gmtOffset', 'gmtOffsetName', 'abbreviation', 'tzName', 'id')

class TimeZoneAdmin(ImportExportModelAdmin):
    resource_class = ContinentResource

class ContinentAdmin(ImportExportModelAdmin):
    resource_class = ContinentResource

class SubContinentAdmin(ImportExportModelAdmin):
    resource_class = SubContinentResource

class CountryAdmin(ImportExportModelAdmin):
    resource_class = CountryResource


class StateAdmin(ImportExportModelAdmin):
    resource_class = StateResource

class CityAdmin(ImportExportModelAdmin):
    resource_class = CityResource

admin.site.register(TimeZone, TimeZoneAdmin)
admin.site.register(Continent, ContinentAdmin)
admin.site.register(SubContinent, SubContinentAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(City, CityAdmin)


"""
from django.core import serializers
from django.http import HttpResponse

def export_as_json(modeladmin, request, queryset):
    response = HttpResponse(content_type="application/json")
    serializers.serialize("json", queryset, stream=response)
    return response


from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect

def export_selected_objects(modeladmin, request, queryset):
    selected = queryset.values_list('pk', flat=True)
    ct = ContentType.objects.get_for_model(queryset.model)
    return HttpResponseRedirect('/export/?ct=%s&ids=%s' % (
        ct.pk,
        ','.join(str(pk) for pk in selected),
    ))


from django.contrib import admin

admin.site.add_action(export_selected_objects)


class LocationAdmin(admin.ModelAdmin):
    form = LocationForm
    class Media:
        js = ('http://ajax.googleapis.com/ajax/libs/jquery/1.4.0/jquery.min.js',
                '/site_media/js/municipality.js')

admin.site.register(Location, LocationAdmin)
"""