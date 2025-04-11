from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Crop, CropCategory

class CropCategoryForm(forms.ModelForm):
    class Meta:
        model = CropCategory
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500',
                'rows': 3,
                'placeholder': _('Describe the category')
            }),
        }
        labels = {
            'name': _('Category Name'),
            'description': _('Description'),
        }

class CropForm(forms.ModelForm):
    class Meta:
        model = Crop
        fields = ['category', 'name', 'description', 'quantity', 'unit', 'price_per_unit', 'image']
        widgets = {
            'category': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500'
            }),
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500',
                'rows': 4,
                'placeholder': _('Describe your crop')
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500',
                'step': '0.01',
                'min': '0'
            }),
            'unit': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500'
            }),
            'price_per_unit': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500',
                'step': '0.01',
                'min': '0'
            }),
            'image': forms.FileInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500'
            }),
        }
        labels = {
            'category': _('Category'),
            'name': _('Crop Name'),
            'description': _('Description'),
            'quantity': _('Quantity'),
            'unit': _('Unit'),
            'price_per_unit': _('Price per Unit'),
            'image': _('Crop Image'),
        }

class CropRecommendationForm(forms.Form):
    soil_type = forms.ChoiceField(
        choices=Crop.SOIL_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    climate_zone = forms.ChoiceField(
        choices=Crop.CLIMATE_ZONE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    field_area = forms.FloatField(
        min_value=0.1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'placeholder': 'Enter field area in acres'
        })
    )
    
    soil_ph = forms.FloatField(
        min_value=0,
        max_value=14,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'placeholder': 'Enter soil pH (0-14)'
        })
    )
    
    rainfall = forms.IntegerField(
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter average rainfall in mm'
        })
    )
    
    irrigation_method = forms.ChoiceField(
        choices=Crop.IRRIGATION_METHOD_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    growing_season = forms.ChoiceField(
        choices=Crop.GROWING_SEASON_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    market_preference = forms.ChoiceField(
        choices=Crop.MARKET_PREFERENCE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    ) 