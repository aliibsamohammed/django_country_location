from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.views.generic import TemplateView, DetailView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from .models import Continent, SubContinent, Country, State, City, TimeZone
from .forms import StateCreateForm, CityCreateForm, RegionCreateForm, TimeZoneCreateForm
from .forms import ContinentCreateForm, SubContinentCreateForm, CountryCreateForm
from .forms import ContinentUpdateForm, SubContinentUpdateForm, CountryUpdateForm
from .forms import StateUpdateForm, CityUpdateForm, RegionUpdateForm, TimeZoneUpdateForm
from .resources import PersonResource, ContinentResource, SubContinentResource
from .resources import CountryResource, StateResource, CityResource, TimeZoneResource
import requests
import csv
from django.views.generic import ListView

from tablib import Dataset

class IndexPageView(TemplateView):

    def get(self, request, *args, **kwargs):
        #user = self.request.user
        try:
            num_continents = Continent.objects.all().count()
            num_subcontinents = SubContinent.objects.all().count() 
            num_countries = Country.objects.all().count() 
            num_states = State.objects.all().count()
            num_cities = City.objects.all().count()
            #num_contractors = ProjectContractor.objects.filter(company__role='mc').count()
            #num_consults = ProjectConsultant.objects.filter(company__role='ce').count()
            #num_emps = ProjectTeam.objects.all().count() 

            # Number of visits to this view, as counted in the session variable.
            num_visits = request.session.get('num_visits', 1)
            request.session['num_visits'] = num_visits+1
            
            context = {
                'num_continents': num_continents,
                'num_subcontinents': num_subcontinents,
                'num_countries': num_countries,
                'num_states': num_states,
                'num_cities': num_cities,
                'num_visits': num_visits,

            }

            return render(self.request, 'index.html', context)
        except ObjectDoesNotExist:
            messages.info(self.request, 'You do not have list of countries')
            return redirect('country_index')


class TimeZoneCreateView(SuccessMessageMixin, CreateView):
    model = TimeZone
    form_class = TimeZoneCreateForm
    template_name = 'regions/create/timezone_create.html'
    success_url = reverse_lazy('timezone_create')
    success_message = 'TimeZone created successfully.'


class ContinentCreateView(SuccessMessageMixin, CreateView):
    model = Continent
    form_class = ContinentCreateForm
    template_name = 'regions/create/continent_create.html'
    success_url = reverse_lazy('continent_create')
    success_message = 'Continent created successfully.'


class SubContinentCreateView(SuccessMessageMixin, CreateView):
    model = SubContinent
    form_class = SubContinentCreateForm
    template_name = 'regions/create/subcontinent_create.html'
    success_url = reverse_lazy('subcontinent_create')
    success_message = 'SubContinent created successfully.'


class CountryCreateView(SuccessMessageMixin, CreateView):
    model = Country
    form_class = CountryCreateForm
    template_name = 'regions/create/country_create.html'
    success_url = reverse_lazy('country_create')
    success_message = 'Country created successfully.'


class StateCreateView(SuccessMessageMixin, CreateView):
    model = State
    form_class = StateCreateForm
    template_name = 'regions/create/state_create.html'
    success_url = reverse_lazy('state_create')
    success_message = 'State created successfully.'


class CityCreateView(SuccessMessageMixin, CreateView):
    model = City
    form_class = CityCreateForm
    template_name = 'regions/create/city_create.html'
    success_url = reverse_lazy('city_create')
    success_message = 'City created successfully.'


def load_subcontinents(request):
    continent_id = request.GET.get('continent')
    subcontinents = SubContinent.objects.filter(continent_id=continent_id).order_by('name')
    return render(request, 'regions/ajax/subcontinent_dropdown_list_options.html', {'subcontinents': subcontinents})


def load_countries(request):
    subcontinent_id = request.GET.get('subcontinent')
    countries = Country.objects.filter(subcontinent_id=subcontinent_id).order_by('name')
    return render(request, 'regions/ajax/country_dropdown_list_options.html', {'countries': countries})


def load_states(request):
    country_id = request.GET.get('country')
    states = State.objects.filter(country_id=country_id).order_by('state_name')
    return render(request, 'regions/ajax/state_dropdown_list_options.html', {'states': states})


def load_cities(request):
    state_id = request.GET.get('state')
    cities = City.objects.filter(state_id=state_id).order_by('city_name')
    return render(request, 'regions/ajax/city_dropdown_list_options.html', {'cities': cities})


class TimeZoneUpdateView(SuccessMessageMixin, UpdateView):
    model = TimeZone
    form_class = TimeZoneUpdateForm
    template_name = 'regions/update/timezone_update.html'
    success_url = reverse_lazy('timezone_index')
    success_message = 'TimeZone updated successfully.'


class ContinentUpdateView(SuccessMessageMixin, UpdateView):
    model = Continent
    form_class = ContinentUpdateForm
    template_name = 'regions/update/continent_update.html'    
    success_url = reverse_lazy('continent_index')
    success_message = 'Continent updated successfully.'


class SubContinentUpdateView(SuccessMessageMixin, UpdateView):
    model = SubContinent
    form_class = SubContinentUpdateForm
    template_name = 'regions/update/subcontinent_update.html'
    success_url = reverse_lazy('subcontinent_index')
    success_message = 'SubContinent updated successfully.'


class CountryUpdateView(SuccessMessageMixin, UpdateView):
    model = Country
    form_class = CountryUpdateForm
    template_name = 'regions/update/country_update.html'
    success_url = reverse_lazy('country_index')
    success_message = 'Country updated successfully.'


class StateUpdateView(SuccessMessageMixin, UpdateView):
    model = State
    form_class = StateUpdateForm
    template_name = 'regions/update/state_update.html'
    success_url = reverse_lazy('state_index')
    success_message = 'State updated successfully.'


class CityUpdateView(SuccessMessageMixin, UpdateView):
    model = City
    form_class = CityUpdateForm
    template_name = 'regions/update/city_update.html'
    success_url = reverse_lazy('city_index')
    success_message = 'City updated successfully.'


def states_list_view(request, pk):
    country = Country.objects.get(id=pk)
    states = State.objects.filter(country_id=pk).order_by('name')
    num_states = State.objects.filter(country_id=pk).count()
        
    return render(request, 'addresses/state_list.html', {'country': country, 'states': states})


#------ListView---------------
class TimeZoneIndexView(ListView):
    model = TimeZone
    template_name = 'regions/index/timezone_index.html'
    context_object_name = 'timezones'
    paginate_by = 20


class ContinentIndexView(ListView):
    model = Continent
    template_name = 'regions/index/continent_index.html'
    context_object_name = 'continents'
    

class SubContinentIndexView(ListView):
    model = SubContinent
    template_name = 'regions/index/subcontinent_index.html'    
    context_object_name = 'subcontinents'
    #paginate_by = 20


class CountryIndexView(ListView):
    model = Country
    template_name = 'regions/index/country_index.html'
    context_object_name = 'countries'
    paginate_by = 20
    

class StateIndexView(ListView):
    model = State
    template_name = 'regions/index/state_index.html'
    context_object_name = 'states'
    paginate_by = 20
    

class CityIndexView(ListView):
    model = City
    template_name = 'regions/index/city_index.html'
    context_object_name = 'cities'
    paginate_by = 20
    

#------ListView---------------
class ContinentSubContinentListView(ListView):

    def get(self, request, pk, *args, **kwargs):
        try:
            continent = Continent.objects.get(id=pk)
            subcontinents = SubContinent.objects.filter(continent_id=pk)
            num_subcontinents = SubContinent.objects.filter(continent_id=pk).count()

            context = {
                'continent': continent,
                'subcontinents': subcontinents,
                'num_subcontinents': num_subcontinents,
            }

            return render(self.request, 'regions/list/continentsubcontinent_list.html', context)
        except ObjectDoesNotExist:
            messages.info(self.request, 'You do not have list of subcontinents')
            return redirect('continentsubcontinent_list')


class SubContinentCountryListView(ListView):

    def get(self, request, pk, *args, **kwargs):
        try:
            subcontinent = SubContinent.objects.get(id=pk)
            countries = Country.objects.filter(subcontinent_id=pk)
            num_countries = Country.objects.filter(subcontinent_id=pk).count()

            context = {
                'subcontinent': subcontinent,
                'countries': countries,
                'num_countries': num_countries,
            }

            return render(self.request, 'regions/list/subcontinentcountry_list.html', context)
        except ObjectDoesNotExist:
            messages.info(self.request, 'You do not have list of countries')
            return redirect('subcontinentcountry_list')  


class CountryStateListView(ListView):
    paginate_by = 20
    def get(self, request, pk, *args, **kwargs):
        try:
            country = Country.objects.get(id=pk)
            states = State.objects.filter(country_id=pk)
            num_states = State.objects.filter(country_id=pk).count()

            context = {
                'country': country,
                'states': states,
                'num_states': num_states,
            }

            return render(self.request, 'regions/list/countrystate_list.html', context)
        except ObjectDoesNotExist:
            messages.info(self.request, 'You do not have list of states')
            return redirect('countrystate_list')


class StateCityListView(ListView):
    paginate_by = 20
    def get(self, request, pk, *args, **kwargs):
        try:
            state = State.objects.get(id=pk)
            cities = City.objects.filter(state_id=pk)
            num_cities = City.objects.filter(state_id=pk).count()

            context = {
                'state': state,
                'cities': cities,
                'num_cities': num_cities,
            }

            return render(self.request, 'regions/list/statecity_list.html', context)
        except ObjectDoesNotExist:
            messages.info(self.request, 'You do not have list of cities')
            return redirect('statecity_list')


class CountryCityListView(ListView):
    paginate_by = 20
    def get(self, request, pk, *args, **kwargs):
        try:
            country = Country.objects.get(id=pk)
            cities = City.objects.filter(country_id=pk)
            cities_count = City.objects.filter(country_id=pk).count()

            context = {
                'country': country,
                'cities': cities,
                'cities_count': cities_count,
            }

            return render(self.request, 'regions/list/countrycity_list.html', context)
        except ObjectDoesNotExist:
            messages.info(self.request, 'You do not have list of citie in country')
            return redirect('countrycity_list')


#------DetailView---------------
class TimeZoneDetailView(DetailView):
    model = TimeZone
    template_name = 'regions/detail/timezone_detail.html'
    context_object_name = 'timezones'

    def get_queryset(self, pk):
        try:
            timezone = TimeZone.objects.get(id=pk)
            context = {
                'timezone': timezone,
            }
            return render(self.request, 'regions/detail/timezone_detail.html', context)
        except ObjectDoesNotExist:
            messages.info(self.request, 'You do not have details for this time zone to view')
            return redirect('timezone_detail')


class ContinentDetailView(DetailView):
    def get(self, request, pk, *args, **kwargs):
        try:
            continent = Continent.objects.get(id=pk)
            subcontinents_count = SubContinent.objects.filter(continent_id=pk).count()
            countries_count = Country.objects.filter(continent_id=pk).count()
            states_count = State.objects.filter(country__continent_id=pk).count()
            cities_count = City.objects.filter(country__continent_id=pk).count()

            context = {
                'continent': continent,
                'subcontinents_count': subcontinents_count,
                'countries_count': countries_count,
                'states_count': states_count,
                'cities_count': cities_count,
            }

            return render(self.request, 'regions/detail/continent_detail.html', context)
        except ObjectDoesNotExist:
            messages.info(self.request, 'You do not have details for this continent to view')
            return redirect('continent_index')
    

class SubContinentDetailView(DetailView):
    def get(self, request, pk, *args, **kwargs):
        try:
            subcontinent = SubContinent.objects.get(id=pk)
            countries_count = Country.objects.filter(subcontinent_id=pk).count()
            states_count = State.objects.filter(country__subcontinent_id=pk).count()
            cities_count = City.objects.filter(country__subcontinent_id=pk).count()

            context = {
                'subcontinent': subcontinent,
                'countries_count': countries_count,
                'states_count': states_count,
                'cities_count': cities_count,
            }

            return render(self.request, 'regions/detail/subcontinent_detail.html', context)
        except ObjectDoesNotExist:
            messages.info(self.request, 'You do not have details for this sub continent to view')
            return redirect('subcontinent_index')


class CountryDetailView(DetailView):
    def get(self, request, pk, *args, **kwargs):
        try:
            country = Country.objects.get(id=pk)
            timezones = country.timezones.all()
            time_zones = list(country.timezones.all().values_list('zoneName',).get())
            states_count = State.objects.filter(country_id=pk).count()
            cities_count = City.objects.filter(country_id=pk).count()

            context = {
                'country': country,
                'timezones': timezones,
                'time_zones': time_zones,
                'states_count': states_count,
                'cities_count': cities_count,
            }

            return render(self.request, 'regions/detail/country_detail.html', context)
        except ObjectDoesNotExist:
            messages.info(self.request, 'You do not have details for this country to view')
            return redirect('country_index')


class StateDetailView(DetailView):
    def get(self, request, pk, *args, **kwargs):
        try:
            state = State.objects.get(id=pk)
            cities_count = City.objects.filter(state_id=pk).count()

            context = {
                'state': state,
                'cities_count': cities_count,
            }

            return render(self.request, 'regions/detail/state_detail.html', context)
        except ObjectDoesNotExist:
            messages.info(self.request, 'You do not have details for this state to view')
            return redirect('state_index')


class CityDetailView(DetailView):
    model = City
    template_name = 'regions/detail/city_detail.html'
    context_object_name = 'city'


#------locatiionView--------

class CityLocationView(DetailView):
    model = City
    template_name = 'regions/location/city_location.html'
    #paginate_by = 20
    context_object_name = 'city'


#---------DeleteView----------------

class TimeZoneDeleteView(DeleteView):
    model = TimeZone
    template_name = 'regions/delete/timezone_confirm_delete.html'
    
    def get_success_url(self):
        return reverse('timezone_index')


class ContinentDeleteView(DeleteView):
    model = Continent
    template_name = 'regions/delete/continent_confirm_delete.html'
    
    def get_success_url(self):
        return reverse('continent_index')


class SubContinentDeleteView(DeleteView):
    model = SubContinent
    template_name = 'regions/delete/subcontinent_confirm_delete.html'
    
    def get_success_url(self):
        return reverse('subcontinent_index')


class CountryDeleteView(DeleteView):
    model = Country
    template_name = 'regions/delete/country_confirm_delete.html'

    def get_success_url(self):
        return reverse('country_index')


class StateDeleteView(DeleteView):
    model = State
    template_name = 'regions/delete/state_confirm_delete.html'
    
    def get_success_url(self):
        return reverse('state_index')


class CityDeleteView(DeleteView):
    model = City
    template_name = 'regions/delete/city_confirm_delete.html'
    
    def get_success_url(self):
        return reverse('city_index')


def simple_upload(request):
    if request.method == 'POST':
        person_resource = PersonResource()
        dataset = Dataset()
        new_persons = request.FILES['myfile']
        imported_data = dataset.load(new_persons.read().decode("utf-8"), format='csv', headers=True)
        result = person_resource.import_data(dataset, dry_run=True) 

        if not result.has_errors():
            person_resource.import_data(dataset, dry_run=False)
            return HttpResponseRedirect(reverse('simple_upload') )
        else:
            return HttpResponse("""your form is wrong, reload on <a href = "{{ url 'simple_upload' }}">reload</a>""")
    
    return render(request, 'regions/simple_upload.html')


def continent_import(request):
    if request.method == 'POST':
        continent_resource = ContinentResource()
        dataset = Dataset()
        new_continents = request.FILES['myfile']
        imported_data = dataset.load(new_continents.read().decode("utf-8"), format='csv', headers=True)
        result = continent_resource.import_data(dataset, dry_run=True)

        if not result.has_errors():
            continent_resource.import_data(dataset, dry_run=False)
            messages.success(request, f'Your continents data has been imported successfully!') 
            return HttpResponseRedirect(reverse('continent_index') )
        else:
            return HttpResponse("""your form is wrong, reload on <a href = "{{ url 'continent_import' }}">reload</a>""")
    
    return render(request, 'regions/import/continent_import.html')


def subcontinent_import(request):
    if request.method == 'POST':
        subcontinent_resource = SubContinentResource()
        dataset = Dataset()
        new_subcontinents = request.FILES['myfile']
        imported_data = dataset.load(new_subcontinents.read().decode("utf-8"), format='csv', headers=True)
        result = subcontinent_resource.import_data(dataset, dry_run=True) 

        if not result.has_errors():
            subcontinent_resource.import_data(dataset, dry_run=False) 
            messages.success(request, f'Your subcontinents data has been imported successfully!') 
            return HttpResponseRedirect(reverse('subcontinent_index') )
        else:
            return HttpResponse("""your form is wrong, reload on <a href = "{{ url : 'subcontinent_import'}}">reload</a>""")
    
    return render(request, 'regions/import/subcontinent_import.html')



def country_import(request):
    if request.method == 'POST':
        country_resource = CountryResource()
        dataset = Dataset()
        new_countries = request.FILES['myfile']
        imported_data = dataset.load(new_countries.read().decode("utf-8"), format='csv', headers=True)
        result = country_resource.import_data(dataset, dry_run=True, raise_errors=True) 

        if not result.has_errors():
            country_resource.import_data(dataset, dry_run=False) 
            messages.success(request, f'Your countries data has been imported successfully!') 
            return HttpResponseRedirect(reverse('country_index') )
        else:
            return HttpResponse("""your form is wrong, reload on <a href = "{{ url 'country_import' }}">reload</a>""")
    
    return render(request, 'regions/import/country_import.html')



def state_import(request):
    if request.method == 'POST':
        state_resource = StateResource()
        dataset = Dataset()
        new_states = request.FILES['myfile']
        imported_data = dataset.load(new_states.read().decode("utf-8"), format='csv', headers=True)
        result = state_resource.import_data(dataset, dry_run=True, raise_errors=True)

        if not result.has_errors():
            state_resource.import_data(dataset, dry_run=False)
            messages.success(request, f'Your states data has been imported successfully!')  
            return HttpResponseRedirect(reverse('state_index') )
        else:
            return HttpResponse("""your form is wrong, reload on <a href = "{{ url 'state_import' }}">reload</a>""")
    
    return render(request, 'regions/import/state_import.html')



def city_import(request):
    if request.method == 'POST':
        city_resource = CityResource()
        dataset = Dataset()
        new_cities = request.FILES['myfile']
        imported_data = dataset.load(new_cities.read().decode("utf-8"), format='csv', headers=True)
        result = city_resource.import_data(dataset, dry_run=True, raise_errors=True)  # Test the data import

        if not result.has_errors():
            city_resource.import_data(dataset, dry_run=False) 
            messages.success(request, f'Your cities data has been imported successfully!')
            return HttpResponseRedirect(reverse('city_index') )
        else:
            return HttpResponse("""your form is wrong, reload on <a href = "{{ url 'city_import' }}">reload</a>""")
    
    return render(request, 'regions/import/city_import.html')



def timezone_import(request):
    if request.method == 'POST':
        timezone_resource = TimeZoneResource()
        dataset = Dataset()
        new_timezones = request.FILES['myfile']
        imported_data = dataset.load(new_timezones.read().decode("utf-8"), format='csv', headers=True)
        result = timezone_resource.import_data(dataset, dry_run=True) 

        if not result.has_errors():
            timezone_resource.import_data(dataset, dry_run=False) 
            messages.success(request, f'Your timezones data has been imported successfully!') 
            return HttpResponseRedirect(reverse('timezone_index') )
        else:
            return HttpResponse("""your form is wrong, reload on <a href = "{{ url 'timezone_import' }}">reload</a>""")
    
    return render(request, 'regions/import/timezone_import.html')



def city_location(request, pk):
    api_key = "your-api-key"
    url = "https://maps.googleapis.com/maps/api/staticmap?"
    city = City.objects.get(id=pk)
    lat = city.latitude
    lon = city.longitude
    center = str(lat) + "," + str(lon)
    zoom = 10
    r = requests.get(url + "center=" + center + "&zoom=" + str(zoom) + "&size=400x400&key=api_key")
    context = {'r': r}

    return render(request, 'regions/location/city_location.html', context,)


def show_location(request):
    api_key = "your-api-key"
    url = "https://maps.googleapis.com/maps/api/staticmap?"
    user = request.user
    address = Address.objects.get(user_id=user.id)
    center = address.city
    zoom = 10
    r = requests.get(url + "center =" + center + "&zoom =" + str(zoom) + "&size=400x400&key =api_key")# + "sensor = false")
    context = {'r': r}

    return render(request, 'addresses/show_location.html', context,)



def delete_country(request, country_id):
    country_id = int(country_id)
    try:
        country_sel = Country.objects.get(id = country_id)
    except Country.DoesNotExist:
         return redirect('addresses:country_list')
    country_sel.delete()
    return redirect('addresses:country_list')


class AboutView(TemplateView):
    template_name = 'about.html'