from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.IndexPageView.as_view(), name='index'),
    path('continent/create/', views.ContinentCreateView.as_view(), name='continent_create'),
    path('subcontinent/create/', views.SubContinentCreateView.as_view(), name='subcontinent_create'),
    path('country/create/', views.CountryCreateView.as_view(), name='country_create'),    
    path('state/create/', views.StateCreateView.as_view(), name='state_create'),
    path('city/create/', views.CityCreateView.as_view(), name='city_create'),
    path('timezone/create/', views.TimeZoneCreateView.as_view(), name='timezone_create'),


    path('continent/<int:pk>/subcontinent/', views.ContinentSubContinentListView.as_view(), name='continentsubcontinent_list'),
    path('subcontinent/<int:pk>/country/', views.SubContinentCountryListView.as_view(), name='subcontinentcountry_list'),
    path('country/<int:pk>/state/', views.CountryStateListView.as_view(), name='countrystate_list'),
    path('state/<int:pk>/city/', views.StateCityListView.as_view(), name='statecity_list'),
    path('countrycity/list/<int:pk>/', views.CountryCityListView.as_view(), name='countrycity_list'),


    path('continent/index/', views.ContinentIndexView.as_view(), name='continent_index'),
    path('subcontinent/index/', views.SubContinentIndexView.as_view(), name='subcontinent_index'),
    path('country/index/', views.CountryIndexView.as_view(), name='country_index'),
    #path('countrycity/index/', views.CountryCityIndexView.as_view(), name='countrycity_index'),
    path('state/index/', views.StateIndexView.as_view(), name='state_index'),
    path('city/index/', views.CityIndexView.as_view(), name='city_index'),
    path('timezone/index/', views.TimeZoneIndexView.as_view(), name='timezone_index'),

    
    path('continent/import/', views.continent_import, name='continent_import'),
    path('subcontinent/import/', views.subcontinent_import, name='subcontinent_import'),
    path('country/import/', views.country_import, name='country_import'),
    path('state/import/', views.state_import, name='state_import'),
    path('city/import/', views.city_import, name='city_import'),
    path('timezone/import/', views.timezone_import, name='timezone_import'),


    path('continent/<int:pk>/delete/', views.ContinentDeleteView.as_view(), name='continent_confirm_delete'),
    path('subcontinent/<int:pk>/delete/', views.SubContinentDeleteView.as_view(), name='subcontinent_confirm_delete'),
    path('country/<int:pk>/delete/', views.CountryDeleteView.as_view(), name='country_confirm_delete'),
    path('state/<int:pk>/delete/', views.StateDeleteView.as_view(), name='state_confirm_delete'),
    path('city/<int:pk>/delete/', views.CityDeleteView.as_view(), name='city_confirm_delete'),
    path('timezone/<int:pk>/delete/', views.TimeZoneDeleteView.as_view(), name='timezone_confirm_delete'),


    path('timezone/<int:pk>/update/', views.TimeZoneUpdateView.as_view(), name='timezone_update'),
    path('continent/<int:pk>/update/', views.ContinentUpdateView.as_view(), name='continent_update'),
    path('subcontinent/<int:pk>/update/', views.SubContinentUpdateView.as_view(), name='subcontinent_update'),
    path('country/<int:pk>/update/', views.CountryUpdateView.as_view(), name='country_update'),
    path('state/<int:pk>/update/', views.StateUpdateView.as_view(), name='state_update'),
    path('city/<int:pk>/update/', views.CityUpdateView.as_view(), name='city_update'),

    path('continent/<int:pk>/detail/', views.ContinentDetailView.as_view(), name='continent_detail'),
    path('subcontinent/<int:pk>/detail/', views.SubContinentDetailView.as_view(), name='subcontinent_detail'),
    path('country/<int:pk>/detail/', views.CountryDetailView.as_view(), name='country_detail'),
    path('state/<int:pk>/detail/', views.StateDetailView.as_view(), name='state_detail'),
    path('city/<int:pk>/detail/', views.CityDetailView.as_view(), name='city_detail'),
    
    path('city/<int:pk>/location/', views.CityLocationView.as_view(), name='city_location'),
    path('city/<int:pk>/showlocation/', views.city_location, name='city_location'),

    path('ajax/load-subcontinents/', views.load_subcontinents, name='ajax_load_subcontinents'),
    path('ajax/load-countries/', views.load_countries, name='ajax_load_countries'),
    path('ajax/load-states/', views.load_states, name='ajax_load_states'),
    path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'),


]
