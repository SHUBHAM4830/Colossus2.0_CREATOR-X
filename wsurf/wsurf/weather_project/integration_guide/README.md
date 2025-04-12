# Weather App Integration Guide

This guide explains how to integrate the weather app into your existing Django project.

## Step 1: Copy Files
Copy the entire `weather` directory into your Django project's root directory.

## Step 2: Install Dependencies
Add these to your `requirements.txt`:
```
requests==2.31.0
```

## Step 3: Update settings.py
Add 'weather' to your INSTALLED_APPS:
```python
INSTALLED_APPS = [
    ...
    'weather',
]
```

## Step 4: Update Project URLs
Add this to your project's urls.py:
```python
from django.urls import path, include

urlpatterns = [
    ...
    path('weather/', include('weather.urls')),  # You can change 'weather/' to any prefix you want
]
```

## Step 5: Run Migrations
```bash
python manage.py migrate
```

## Step 6: API Key
The app uses OpenWeatherMap API. Make sure to:
1. Keep the API key in your environment variables or settings
2. Update views.py with your API key:
```python
api_key = 'YOUR_API_KEY'  # Replace with your OpenWeatherMap API key
```

## Step 7: Templates
The app includes its own templates in `weather/templates/weather/`. Make sure your project's template settings include app directories:
```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,  # This should be True
        ...
    },
]
```

## Step 8: Static Files
The app uses Font Awesome and Inter font from CDN. No additional static files needed.

## Usage
After integration, the weather app will be available at:
- If mounted at root: `http://your-domain/`
- If mounted at weather/: `http://your-domain/weather/`

## Customization
1. Colors: Edit the CSS variables in `weather/templates/weather/index.html`:
```css
:root {
    --primary-color: #2ecc71;
    --secondary-color: #27ae60;
    --accent-color: #ff7f50;
    ...
}
```

2. Layout: The template uses a responsive design and can be modified in the same file.

3. API Settings: You can modify weather alert thresholds in `weather/views.py`:
```python
if current_temp >= 35:  # Change temperature thresholds
    alerts.append({
        'type': 'danger',
        'icon': 'fas fa-temperature-high',
        'message': 'Extreme heat warning!'
    })
```

## Features
- Current weather display
- 5-day forecast
- Weather alerts for:
  - Extreme temperatures
  - Rain and storms
  - Future weather conditions
- Responsive design
- Modern UI with animations

## Troubleshooting
1. CSRF Issues: Make sure your Django CSRF settings are properly configured
2. API Errors: Verify your OpenWeatherMap API key is valid
3. Template Issues: Ensure 'APP_DIRS' is True in your template settings

## Security Notes
1. Always keep API keys in environment variables in production
2. Enable CSRF protection
3. Use HTTPS in production

## Dependencies
- Django
- requests library
- OpenWeatherMap API account
- Font Awesome (via CDN)
- Inter font (via Google Fonts CDN)
