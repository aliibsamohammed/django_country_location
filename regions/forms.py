from django import forms
from .models import Continent, SubContinent, Country, State, City, Region, TimeZone 

class TimeZoneCreateForm(forms.ModelForm):
    class Meta:
        model = TimeZone
        fields = '__all__'


class ContinentCreateForm(forms.ModelForm):
    class Meta:
        model = Continent
        fields = '__all__'


class SubContinentCreateForm(forms.ModelForm):
    class Meta:
        model = SubContinent
        fields = '__all__'


class CountryCreateForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = '__all__'


class StateCreateForm(forms.ModelForm):
    class Meta:
        model = State
        fields = '__all__'


class CityCreateForm(forms.ModelForm):
    class Meta:
        model = City
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['state'].queryset = State.objects.none()

        if 'country' in self.data:
            try:
                country_id = int(self.data.get('country'))
                self.fields['state'].queryset = State.objects.filter(country_id=country_id).order_by('state_name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['state'].queryset = self.instance.country.state_set.order_by('state_name')


class RegionCreateForm(forms.ModelForm):
    class Meta:
        model = Region
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sub_continent'].queryset = SubContinent.objects.none()
        self.fields['country'].queryset = Country.objects.none()
        self.fields['state'].queryset = State.objects.none()
        self.fields['city'].queryset = City.objects.none()

        if 'continent' in self.data:
            try:
                continent_id = int(self.data.get('continent'))
                self.fields['subcontinent'].queryset = SubContinent.objects.filter(continent_id=continent_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['subcontinent'].queryset = self.instance.continent.subcontinent_set.order_by('name')


        if 'subcontinent' in self.data:
            try:
                subcontinent_id = int(self.data.get('subcontinent'))
                self.fields['country'].queryset = Country.objects.filter(subcontinent_id=subcontinent_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['country'].queryset = self.instance.subcontinent.country_set.order_by('name')


        if 'country' in self.data:
            try:
                country_id = int(self.data.get('country'))
                self.fields['state'].queryset = State.objects.filter(country_id=country_id).order_by('state_name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['state'].queryset = self.instance.country.state_set.order_by('state_name')


        if 'state' in self.data:
            try:
                state_id = int(self.data.get('state'))
                self.fields['city'].queryset = City.objects.filter(state_id=state_id).order_by('city_name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['city'].queryset = self.instance.state.city_set.order_by('city_name')


class TimeZoneUpdateForm(forms.ModelForm):
    class Meta:
        model = TimeZone
        fields = '__all__'


class ContinentUpdateForm(forms.ModelForm):
    class Meta:
        model = Continent
        fields = '__all__'

class SubContinentUpdateForm(forms.ModelForm):
    class Meta:
        model = SubContinent
        fields = '__all__'

class CountryUpdateForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = '__all__'

class StateUpdateForm(forms.ModelForm):
    class Meta:
        model = State
        fields = '__all__'

class CityUpdateForm(forms.ModelForm):
    class Meta:
        model = City
        fields = '__all__'

"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['state'].queryset = State.objects.none()

        if 'country' in self.data:
            try:
                country_id = int(self.data.get('country'))
                self.fields['state'].queryset = State.objects.filter(country_id=country_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['state'].queryset = self.instance.country.state_set.order_by('name')
"""

class RegionUpdateForm(forms.ModelForm):
    class Meta:
        model = Region
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sub_continent'].queryset = SubContinent.objects.none()
        self.fields['country'].queryset = Country.objects.none()
        self.fields['state'].queryset = State.objects.none()
        self.fields['city'].queryset = City.objects.none()

        if 'continent' in self.data:
            try:
                continent_id = int(self.data.get('continent'))
                self.fields['subcontinent'].queryset = SubContinent.objects.filter(continent_id=continent_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['subcontinent'].queryset = self.instance.continent.subcontinent_set.order_by('name')


        if 'subcontinent' in self.data:
            try:
                subcontinent_id = int(self.data.get('subcontinent'))
                self.fields['country'].queryset = Country.objects.filter(subcontinent_id=subcontinent_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['country'].queryset = self.instance.subcontinent.country_set.order_by('name')


        if 'country' in self.data:
            try:
                country_id = int(self.data.get('country'))
                self.fields['state'].queryset = State.objects.filter(country_id=country_id).order_by('state_name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['state'].queryset = self.instance.country.state_set.order_by('state_name')


        if 'state' in self.data:
            try:
                state_id = int(self.data.get('state'))
                self.fields['city'].queryset = City.objects.filter(state_id=state_id).order_by('city_name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['city'].queryset = self.instance.state.city_set.order_by('city_name')

