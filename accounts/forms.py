from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field, Div
from django.utils.translation import gettext_lazy as _
from .models import Profile, CustomUser

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-md-6'),
                Column('last_name', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            'email',
            'password1',
            'password2',
            Submit('submit', _('Sign Up'), css_class='btn btn-primary w-full')
        )

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'address', 'state', 'district', 'pincode')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-md-6 mb-0'),
                Column('last_name', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'email',
            Row(
                Column('phone_number', css_class='form-group col-md-6 mb-0'),
                Column('pincode', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('state', css_class='form-group col-md-6 mb-0'),
                Column('district', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'address',
            Submit('submit', _('Save Changes'), css_class='btn btn-primary')
        )

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'phone_number', 'address', 'state', 'district', 'pincode']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-input'}),
            'address': forms.Textarea(attrs={
                'class': 'form-input',
                'rows': 3
            }),
            'state': forms.TextInput(attrs={'class': 'form-input'}),
            'district': forms.TextInput(attrs={'class': 'form-input'}),
            'pincode': forms.TextInput(attrs={'class': 'form-input'}),
        }
        labels = {
            'first_name': _('First Name'),
            'last_name': _('Last Name'),
            'phone_number': _('Phone Number'),
            'address': _('Address'),
            'state': _('State'),
            'district': _('District'),
            'pincode': _('Pincode'),
        }

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input'}),
        label=_('Your Name')
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-input'}),
        label=_('Your Email')
    )
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-input'}),
        label=_('Subject')
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-input',
            'rows': 5,
            'placeholder': _('Your message here...')
        }),
        label=_('Message')
    ) 