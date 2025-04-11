from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm, ProfileForm

def home(request):
    return render(request, 'home.html')

class CustomLoginView(LoginView):
    template_name = 'account/login.html'
    
    def get_success_url(self):
        user = self.request.user
        if user.is_farmer:
            return '/crops/dashboard/'
        elif user.is_buyer:
            return '/bidding/dashboard/'
        return '/'

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        login(self.request, form.get_user())
        return redirect(self.get_success_url())

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            # Handle farmer role selection
            is_farmer = request.POST.get('is_farmer') == 'on'
            user.is_farmer = is_farmer
            user.save()
            
            messages.success(request, _('Profile updated successfully.'))
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=request.user)
    
    return render(request, 'accounts/profile.html', {
        'form': form,
        'is_farmer': request.user.is_farmer
    })

@login_required
def dashboard(request):
    context = {}
    if request.user.is_farmer:
        context['crops'] = request.user.crops.all()
        context['demand_responses'] = request.user.demand_responses.all()
        return render(request, 'accounts/farmer_dashboard.html', context)
    elif request.user.is_buyer:
        context['bids'] = request.user.bids.all()
        context['demands'] = request.user.demands.all()
        return render(request, 'accounts/buyer_dashboard.html', context)
    return redirect('home')

def contact_view(request):
    if request.method == 'POST':
        # Handle contact form submission
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Here you would typically send an email
        # For now, we'll just show a success message
        messages.success(request, _('Thank you for your message. We will get back to you soon.'))
        return redirect('accounts:contact')
    
    return render(request, 'accounts/contact.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, _('Registration successful. Welcome to KrishiBazaar!'))
            # Redirect based on role
            if user.is_farmer:
                return redirect('crops:dashboard')
            elif user.is_buyer:
                return redirect('bidding:dashboard')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})
