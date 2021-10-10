from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget
from .models import Continent, SubContinent, Country, State, City, TimeZone

from .models import Person

class PersonResource(resources.ModelResource):
    class Meta:
        model = Person
        #import_id_fields = ('id',)
        fields = ('name', 'email', 'birth_date', 'location', 'id', )
        widgets = {
                'birth_date': {'format': '%d/%m/%Y'},
                }


class TimeZoneResource(resources.ModelResource):
    class Meta:
        model = TimeZone
        #import_id_fields = ('id',)
        fields = ('zoneName', 'gmtOffset', 'gmtOffsetName', 'abbreviation', 'tzName', 'id', )


class ContinentResource(resources.ModelResource):
    class Meta:
        model = Continent
        #import_id_fields = ('id',)
        fields = ('name', 'code', 'id', )


class SubContinentResource(resources.ModelResource):
    continent = fields.Field(
            column_name='continent',
            attribute='continent',
            widget=ForeignKeyWidget(Continent, 'code'))
    
    class Meta:
        model = SubContinent
        #import_id_fields = ('id',)
        fields = ('continent', 'name', 'id', )


class CountryResource(resources.ModelResource):
    continent = fields.Field(
            column_name='continent',
            attribute='continent',
            widget=ForeignKeyWidget(Continent, 'name'))

    subcontinent = fields.Field(
            column_name='subcontinent',
            attribute='subcontinent',
            widget=ForeignKeyWidget(SubContinent, 'name'))
    
    timezones = fields.Field(
            column_name='timezones',
            attribute='timezones',
            saves_null_values=True,
            widget=ManyToManyWidget(TimeZone, separator=',', field='zoneName'))


    class Meta:
        model = Country
        #import_id_fields = ('id',)
        fields = ('name', 'iso3', 'iso2', 'numeric_code', 'phone_code', 'capital', 'currency', 
                    'currency_symbol', 'tld', 'native', 'continent' 'subcontinent', 'timezones', 'latitude', 'longitude', 
                    'emoji', 'emojiU', 'flag_image', 'map_image', 'area', 'population', 'id')


class StateResource(resources.ModelResource):
    country = fields.Field(
            column_name='country',
            attribute='country',
            widget=ForeignKeyWidget(Country, 'iso2'))

    class Meta:
        model = State
        #import_id_fields = ('id',)
        fields = ('country', 'state_name', 'state_code', 'latitude', 'longitude', 'id', )


class CityResource(resources.ModelResource):
    country = fields.Field(
            column_name='country',
            attribute='country',
            widget=ForeignKeyWidget(Country, 'iso2'))

    state = fields.Field(
            column_name='state',
            attribute='state',
            widget=ForeignKeyWidget(State, 'state_code'))

    class Meta:
        model = City
        #import_id_fields = ('id',)
        fields = ('country', 'state', 'district', 'city_name', 'latitude', 'longitude', 'id', )

"""
class FullNameForeignKeyWidget(ForeignKeyWidget):
    def get_queryset(self, value, row):
        return self.model.objects.filter(
            first_name__iexact=row["first_name"],
            last_name__iexact=row["last_name"]
        )
"""