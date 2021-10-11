from django.db import models
from django.conf import settings
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from datetime import date
from django.utils import timezone

class TimeZone(models.Model):
    
    zoneName = models.CharField(max_length=15, 
        verbose_name=_("Zone Name"), 
        help_text=_("Zone official name description (e.g. Asia/Kabul)."))

    gmtOffset = models.IntegerField(
        verbose_name=_("GMT offset"), 
        help_text=_("Number of hours or minutes a time zone is ahead of or behind GMT."))

    gmtOffsetName = models.CharField(max_length=10, 
        verbose_name=_("GMT offset name"), 
        help_text=_("GMT offset name description (e.g. UTC+04:30)."))

    abbreviation = models.CharField(max_length=6, 
        verbose_name=_("GMT offset abbreviation"), 
        help_text=_("GMT offset name abbreviation (e.g. AFT)."))

    tzName = models.CharField(max_length=55, 
        verbose_name=_("Time Zone Name"), 
        help_text=_("Time Zone Name description (e.g. Afghanistan Time)."))

    date_created = models.DateTimeField(auto_now_add=True,)
    date_mod = models.DateField(default=timezone.now, verbose_name='Date Modified')
    
    class Meta:
        #unique_together = ['name', 'code', ],
        ordering = ['zoneName']
        verbose_name_plural = 'TimeZones'

    def get_absolute_url(self):
        return reverse('timezone_detail', args=[str(self.id)])

    def __str__(self):
        return str('%s' ' (%s)' % (self.zoneName, self.gmtOffsetName))


class Continent(models.Model):

    name = models.CharField(max_length=15, 
        verbose_name=_("Continent Name"), 
        help_text=_("Continent official name description."))

    code = models.CharField(max_length=2, 
        verbose_name=_("Continent Code"), 
        help_text=_("Continent ISO3166-2 description."))

    date_created = models.DateTimeField(auto_now_add=True,)
    date_mod = models.DateField(default=timezone.now, verbose_name='Date Modified')

    class Meta:
        #unique_together = ['name', 'code', ],
        ordering = ['name']
        verbose_name_plural = 'Continents'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('continent-detail', kwargs={'pk': self.pk})

    


class SubContinent(models.Model):
    
    continent = models.ForeignKey(Continent, on_delete=models.CASCADE, 
        related_name='continent_subcontinents', 
        verbose_name=_("Continent"), help_text=_("The continent description."))

    name = models.CharField(max_length=30, 
        verbose_name=_("SubContinent Name"), 
        help_text=_("SubContinent official name description."))

    date_created = models.DateTimeField(auto_now_add=True,)
    date_mod = models.DateField(default=timezone.now, verbose_name='Date Modified')

    class Meta:
        #unique_together = ['name', 'code', ],
        ordering = ['continent']
        verbose_name_plural = 'SubContinents'

    def __str__(self):
        return self.name


    def get_absolute_url(self):
        return reverse('subcontinent_detail', kwargs={'pk': self.pk})

    


class Country(models.Model):    
    name = models.CharField(max_length=50,
        verbose_name=_("Country Name"), 
        help_text=_("Country official name description."))

    iso3 = models.CharField(max_length=3,
        verbose_name=_("ISO3166-3 Code"), 
        help_text=_("Country ISO3166-3 code description."))
    
    iso2 = models.CharField(max_length=3,
        verbose_name=_("ISO3166-2 Code"), 
        help_text=_("Country ISO3166-2 code description."))

    numeric_code = models.IntegerField(
        verbose_name=_("ISO3166-3 numeric_code"), 
        help_text=_("Country ISO3166-32 numeric_code description."))

    phone_code = models.CharField(max_length=10,
        verbose_name=_("Phone Area Calling Code"), 
        help_text=_("Country Phone Area Calling Code (+) description."))

    capital = models.CharField(max_length=30,
        verbose_name=_("Capital City"), 
        help_text=_("Country capital city name description."))

    currency = models.CharField(max_length=30,
        verbose_name=_("Country Currency"), 
        help_text=_("Country currency name description."))

    currency_symbol = models.CharField(max_length=30,
        verbose_name=_("Country Currency Symbol"), 
        help_text=_("Country currency symbol description."))

    tld = models.CharField(max_length=30,
        verbose_name=_("Country TLD"), 
        help_text=_("Country top level domain description."))

    native = models.CharField(max_length=30,
        verbose_name=_("Country native name"), 
        help_text=_("Country native name description."))

    continent = models.ForeignKey(Continent, on_delete=models.CASCADE, 
        related_name='region_countries', 
        verbose_name=_("Continent"), help_text=_("The country continent description."))

    subcontinent = models.ForeignKey(SubContinent, on_delete=models.CASCADE, 
        related_name='subregion_countries', 
        verbose_name=_("SubContinent"), help_text=_("The country subcontinent description."))

    timezones = models.ManyToManyField(TimeZone,
        verbose_name=_("Country timezones"), 
        help_text=_("Country timezones descriptions."))

    latitude = models.DecimalField(max_digits=12, decimal_places=8,
        verbose_name=_("Latitude"), help_text=_("The Latitude Coordinate."))
    
    longitude = models.DecimalField(max_digits=12, decimal_places=8,
        verbose_name=_("Longitude"), help_text=_("The Longitude Coordinate."))
    
    emoji = models.CharField(max_length=2,
        verbose_name=_("Country emoji"), 
        help_text=_("Country emoji name description."))

    emojiU = models.CharField(max_length=20,
        verbose_name=_("Country emoji unicode"), 
        help_text=_("Country emoji unicode character description."))

    flag_image = models.ImageField(upload_to='flags/', blank=True, null=True, 
        verbose_name=_("Flag Image"), help_text=_("Official flag of country"))

    map_image = models.ImageField(upload_to='maps/', blank=True, null=True, 
        verbose_name=_("Map Image"), help_text=_("Political map image of country"))

    area = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True,
        verbose_name=_("Area square km"), help_text=_("The Area in square km.")) 

    population = models.PositiveIntegerField(blank=True, null=True,
        verbose_name=_("Population"), help_text=_("The population at time of data entry.")) 

    date_created = models.DateTimeField(auto_now_add=True,)
    date_mod = models.DateField(default=timezone.now, verbose_name='Date Modified')

    class Meta:
        #unique_together = ['continent', 'country_name', 'country_code', ],
        ordering = ['name',]
        verbose_name_plural = 'Countries'

    def get_absolute_url(self):
        return reverse('country-detail', args=[str(self.id)])

    def __str__(self):
        return self.name



class State(models.Model):

    country = models.ForeignKey(Country, on_delete=models.CASCADE, 
        related_name='country_state', 
        verbose_name=_("Country"), help_text=_("The country of the state."))

    state_name = models.CharField(max_length=30,
        verbose_name=_("State / Province / Subdivision Name"), 
        help_text=_("Country higher level sub-division (State / Province / Subdivision) description."))

    state_code = models.CharField(max_length=6, blank=True, null=True,
        verbose_name=_("State / Province / Subdivision Code"), 
        help_text=_("State / province / subdivision code description."))

    latitude = models.DecimalField(max_digits=12, decimal_places=8, blank=True, null=True,
        verbose_name=_("Latitude"), help_text=_("The Latitude Coordinate."))
    
    longitude = models.DecimalField(max_digits=12, decimal_places=8, blank=True, null=True,
        verbose_name=_("Longitude"), help_text=_("The Longitude Coordinate."))

    date_created = models.DateTimeField(auto_now_add=True,)
    date_mod = models.DateField(default=timezone.now, verbose_name='Date Modified')

    class Meta:
        #unique_together = ['country', 'name']
        ordering = ['country', 'state_name']


    def get_absolute_url(self):
        return reverse('state-detail', args=[str(self.id)])
        
    def __str__(self):
        return self.state_name


class City(models.Model):
    
    country = models.ForeignKey(Country, on_delete=models.CASCADE, 
        related_name='country_cities', 
        verbose_name=_("Country"), help_text=_("The country."))

    state = models.ForeignKey(State, on_delete=models.CASCADE, 
        related_name='state_cities', 
        verbose_name=_("State/Province"), help_text=_("The state sub-country description."))
    
    district = models.CharField(max_length=30, blank=True, null=True,
        verbose_name=_("Sub-State / County / District"),
        help_text=_("Country substates/county or sub-province description."))

    city_name = models.CharField(max_length=30,
        verbose_name=_("City or Town"),
        help_text=_("City or Town name description."))
    
    latitude = models.DecimalField(max_digits=12, decimal_places=8,
        verbose_name=_("Latitude"), help_text=_("The Latitude Coordinate."))
    
    longitude = models.DecimalField(max_digits=12, decimal_places=8,
        verbose_name=_("Longitude"), help_text=_("The Longitude Coordinate."))

    date_created = models.DateTimeField(auto_now_add=True,)
    date_mod = models.DateField(default=timezone.now, verbose_name='Date Modified')

    class Meta:
        ordering = ['country', 'state', 'city_name']
        verbose_name_plural = 'Cities'

    def get_absolute_url(self):
        return reverse('city-detail', args=[str(self.id)])

    def __str__(self):
        return self.city_name


class Region(models.Model):
    
    continent = models.ForeignKey(Continent, on_delete=models.CASCADE, 
        related_name='continent_regions', 
        verbose_name=_("Continent"), help_text=_("The country continent description."))

    subcontinent = models.ForeignKey(SubContinent, on_delete=models.CASCADE, 
        related_name='subcontinent_regions', 
        verbose_name=_("SubContinent"), help_text=_("The country subcontinent description."))

    country = models.ForeignKey(Country, on_delete=models.CASCADE, 
        related_name='country_regions', 
        verbose_name=_("Country"), help_text=_("The country."))

    state = models.ForeignKey(State, on_delete=models.CASCADE, 
        related_name='state_regions', 
        verbose_name=_("State/Province"), help_text=_("The state sub-country description."))
    
    city = models.ForeignKey(City, on_delete=models.CASCADE, 
        related_name='city_regions', 
        verbose_name=_("City/Town"), help_text=_("The City / Town description."))

    subcity = models.CharField(max_length=30, blank=True, null=True,
        verbose_name=_("SubCity / Village / Ward / Kebele"),
        help_text=_("Subcity/village or ward description."))
    
    latitude = models.DecimalField(max_digits=12, decimal_places=8,
        verbose_name=_("Latitude"), help_text=_("The Latitude Coordinate."))
    
    longitude = models.DecimalField(max_digits=12, decimal_places=8,
        verbose_name=_("Longitude"), help_text=_("The Longitude Coordinate."))

    date_created = models.DateTimeField(auto_now_add=True,)
    date_mod = models.DateField(default=timezone.now, verbose_name='Date Modified')

    class Meta:
        #unique_together = ['country', 'name']
        ordering = ['subcity']
        verbose_name_plural = 'Regions'

    def get_absolute_url(self):
        return reverse('country-detail', args=[str(self.id)])

    def __str__(self):
        return self.name


class Address(models.Model):
      
    name = models.CharField(max_length=30,
        verbose_name=_("Address"), help_text=_("Address user person name."))
    
    address_01 = models.CharField(
        verbose_name=_("Apartment / House No."), max_length=50,
        help_text=_("Apartment / House No. Address."))
    
    address_02 = models.CharField(
        verbose_name=_("Address 2"), max_length=50, null=True, blank=True,
        help_text=_("Address line two."))
    
    postal_code = models.CharField(max_length=15, 
        verbose_name=_("Postal / ZIP Code"), 
        help_text=_("The postal / zip code of the user."))

    country = models.ForeignKey(Country, on_delete=models.CASCADE,
        verbose_name=_("Country"),)
        
    state = models.ForeignKey(State, on_delete=models.CASCADE,
        verbose_name=_("State / Province / Zone"),)

    city = models.ForeignKey(City, on_delete=models.CASCADE,
        verbose_name=_("City"),)
    
    sub_city = models.CharField(max_length=30,
        verbose_name=_("Sub City / Town"),
        help_text=_("The sub city or town address."))


    date_created = models.DateTimeField(auto_now_add=True,)
    date_mod = models.DateField(default=timezone.now, verbose_name='Date Modified')
       
    
    class Meta:
        ordering = ['name']

    def get_absolute_url(self):
        return reverse('address-detail', args=[str(self.id)])

    def show_location(self, request):
        api_key = "your-api-key"
        url = "https://maps.googleapis.com/maps/api/staticmap?"
        
        center = self.city
        zoom = 15
        r = requests.get(url + "center =" + center + "&zoom =" + str(zoom) + "&size=400x400&key =your-api-key")# + "sensor = false")
        context = {'r': r}
        return render(request, 'addresses/show_location.html', context,)

    def __str__(self):
        return "{} : {}".format('Address of', self.name)


class Person(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(blank=True)
    birth_date = models.DateField()
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Persons'

