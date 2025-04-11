from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import CustomUser
from django.conf import settings
from django.contrib.auth.models import User

class CropCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Crop Category')
        verbose_name_plural = _('Crop Categories')
        ordering = ['name']

    def __str__(self):
        return self.name

class Crop(models.Model):
    UNIT_CHOICES = (
        ('kg', _('Kilogram')),
        ('quintal', _('Quintal')),
        ('ton', _('Ton')),
        ('bag', _('Bag')),
    )
    
    STATUS_CHOICES = (
        ('available', _('Available')),
        ('pending', _('Pending')),
        ('sold', _('Sold')),
    )

    SOIL_TYPE_CHOICES = [
        ('clay', 'Clay'),
        ('sandy', 'Sandy'),
        ('loamy', 'Loamy'),
        ('black', 'Black'),
        ('red', 'Red'),
    ]

    CLIMATE_ZONE_CHOICES = [
        ('tropical', 'Tropical'),
        ('subtropical', 'Subtropical'),
        ('temperate', 'Temperate'),
        ('arid', 'Arid'),
    ]

    IRRIGATION_METHOD_CHOICES = [
        ('drip', 'Drip Irrigation'),
        ('sprinkler', 'Sprinkler'),
        ('flood', 'Flood Irrigation'),
        ('furrow', 'Furrow Irrigation'),
    ]

    GROWING_SEASON_CHOICES = [
        ('kharif', 'Kharif (Monsoon)'),
        ('rabi', 'Rabi (Winter)'),
        ('zaid', 'Zaid (Summer)'),
        ('year_round', 'Year Round'),
    ]

    MARKET_PREFERENCE_CHOICES = [
        ('local', 'Local Market'),
        ('export', 'Export Market'),
        ('processing', 'Processing Industry'),
    ]

    farmer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='crops')
    category = models.ForeignKey(CropCategory, on_delete=models.SET_NULL, null=True, related_name='crops')
    name = models.CharField(max_length=100, verbose_name=_('Crop Name'))
    description = models.TextField(verbose_name=_('Description'))
    quantity = models.PositiveIntegerField(verbose_name=_('Quantity'))
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES, verbose_name=_('Unit'))
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Price per Unit'))
    image = models.ImageField(upload_to='crops/', null=True, blank=True, verbose_name=_('Image'))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available', verbose_name=_('Status'))
    is_available = models.BooleanField(default=True, verbose_name=_('Is Available'))

    # Recommendation fields with default values
    soil_type = models.CharField(max_length=20, choices=SOIL_TYPE_CHOICES, default='loamy', verbose_name=_('Soil Type'))
    climate_zone = models.CharField(max_length=20, choices=CLIMATE_ZONE_CHOICES, default='tropical', verbose_name=_('Climate Zone'))
    min_ph = models.FloatField(default=6.0, verbose_name=_('Minimum pH'))
    max_ph = models.FloatField(default=7.5, verbose_name=_('Maximum pH'))
    min_rainfall = models.FloatField(default=500, verbose_name=_('Minimum Rainfall (mm/year)'))
    max_rainfall = models.FloatField(default=2000, verbose_name=_('Maximum Rainfall (mm/year)'))
    irrigation_method = models.CharField(max_length=20, choices=IRRIGATION_METHOD_CHOICES, default='rainfed', verbose_name=_('Irrigation Method'))
    growing_season = models.CharField(max_length=20, choices=GROWING_SEASON_CHOICES, default='all', verbose_name=_('Growing Season'))
    market_preference = models.CharField(max_length=20, choices=MARKET_PREFERENCE_CHOICES, default='both', verbose_name=_('Market Preference'))

    # Market analysis fields with default values
    yield_potential = models.DecimalField(max_digits=5, decimal_places=2, default=50.0, verbose_name=_('Yield Potential'))
    market_demand = models.DecimalField(max_digits=5, decimal_places=2, default=50.0, verbose_name=_('Market Demand'))
    price_stability = models.DecimalField(max_digits=5, decimal_places=2, default=50.0, verbose_name=_('Price Stability'))
    growth_period = models.DecimalField(max_digits=5, decimal_places=2, default=50.0, verbose_name=_('Growth Period'))
    water_requirement = models.DecimalField(max_digits=5, decimal_places=2, default=50.0, verbose_name=_('Water Requirement'))

    # Yield and market analysis fields
    yield_per_acre = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.0,
        verbose_name=_('Yield per Acre (tons)')
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Crop')
        verbose_name_plural = _('Crops')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.farmer.get_full_name()} ({self.quantity} {self.unit})"

    @property
    def total_price(self):
        return self.quantity * self.price_per_unit

    def save(self, *args, **kwargs):
        # Update is_available based on status
        self.is_available = self.status == 'available'
        super().save(*args, **kwargs)

class CropRecommendation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recommendations')
    soil_type = models.CharField(max_length=20, choices=Crop.SOIL_TYPE_CHOICES)
    climate_zone = models.CharField(max_length=20, choices=Crop.CLIMATE_ZONE_CHOICES)
    field_area = models.FloatField()
    soil_ph = models.FloatField()
    rainfall = models.IntegerField()
    irrigation_method = models.CharField(max_length=20, choices=Crop.IRRIGATION_METHOD_CHOICES)
    growing_season = models.CharField(max_length=20, choices=Crop.GROWING_SEASON_CHOICES)
    market_preference = models.CharField(max_length=20, choices=Crop.MARKET_PREFERENCE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Store the recommended crops as JSON
    recommendations = models.JSONField(default=list)
    
    def __str__(self):
        return f"Recommendation for {self.user.username} - {self.created_at}"

    class Meta:
        ordering = ['-created_at']
