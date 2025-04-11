from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Bid, Demand, DemandResponse

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['price', 'quantity', 'message']
        widgets = {
            'price': forms.NumberInput(attrs={
                'class': 'form-input',
                'step': '0.01',
                'min': '0'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-input',
                'step': '0.01',
                'min': '0'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-input',
                'rows': 4,
                'placeholder': _('Add any additional information about your bid')
            })
        }
        labels = {
            'price': _('Bid Price (per unit)'),
            'quantity': _('Quantity'),
            'message': _('Message')
        }

class DemandForm(forms.ModelForm):
    class Meta:
        model = Demand
        fields = [
            'crop_name', 'description', 'quantity', 'unit',
            'max_price', 'location', 'state', 'district'
        ]
        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'form-input',
                'rows': 4
            }),
            'crop_name': forms.TextInput(attrs={'class': 'form-input'}),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-input',
                'step': '0.01',
                'min': '0'
            }),
            'unit': forms.TextInput(attrs={'class': 'form-input'}),
            'max_price': forms.NumberInput(attrs={
                'class': 'form-input',
                'step': '0.01',
                'min': '0'
            }),
            'location': forms.TextInput(attrs={'class': 'form-input'}),
            'state': forms.TextInput(attrs={'class': 'form-input'}),
            'district': forms.TextInput(attrs={'class': 'form-input'}),
        }
        labels = {
            'crop_name': _('Crop Name'),
            'description': _('Description'),
            'quantity': _('Required Quantity'),
            'unit': _('Unit'),
            'max_price': _('Maximum Price (per unit)'),
            'location': _('Location'),
            'state': _('State'),
            'district': _('District'),
        }

class DemandResponseForm(forms.ModelForm):
    class Meta:
        model = DemandResponse
        fields = ['price', 'quantity', 'message']
        widgets = {
            'price': forms.NumberInput(attrs={
                'class': 'form-input',
                'step': '0.01',
                'min': '0'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-input',
                'step': '0.01',
                'min': '0'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-input',
                'rows': 4,
                'placeholder': _('Add any additional information about your response')
            })
        }
        labels = {
            'price': _('Price (per unit)'),
            'quantity': _('Available Quantity'),
            'message': _('Message')
        } 