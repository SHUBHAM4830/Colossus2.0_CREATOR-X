from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token
import requests

@ensure_csrf_cookie
def index(request):
    # Ensure CSRF token is set
    get_token(request)
    if request.method == 'POST':
        city = request.POST.get('city', '').strip()
        if not city:
            return render(request, 'weather/index.html', {'error': 'Please enter a city name'})

        api_key = '9cfe807537ce733a2f119d9df16b9634'  # OpenWeatherMap API key
        
        try:
            # Get current weather
            current_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
            # Get 5-day forecast
            forecast_url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric'
            
            headers = {
                'User-Agent': 'Mozilla/5.0',
                'Accept': 'application/json'
            }
            
            # Get current weather
            current_response = requests.get(current_url, headers=headers, timeout=10)
            
            if current_response.status_code == 401:
                return render(request, 'weather/index.html', {'error': 'API key error. Please check the API key.'})
            elif current_response.status_code == 404:
                return render(request, 'weather/index.html', {'error': f'City "{city}" not found. Please check the city name.'})
            
            current_response.raise_for_status()
            current_data = current_response.json()

            # Get forecast data
            forecast_response = requests.get(forecast_url, headers=headers, timeout=10)
            forecast_response.raise_for_status()
            forecast_data = forecast_response.json()

            # Map weather codes to Font Awesome icons
            weather_icons = {
                '01d': 'fas fa-sun',  # clear sky
                '01n': 'fas fa-moon',
                '02d': 'fas fa-cloud-sun',  # few clouds
                '02n': 'fas fa-cloud-moon',
                '03d': 'fas fa-cloud',  # scattered clouds
                '03n': 'fas fa-cloud',
                '04d': 'fas fa-cloud',  # broken clouds
                '04n': 'fas fa-cloud',
                '09d': 'fas fa-cloud-rain',  # shower rain
                '09n': 'fas fa-cloud-rain',
                '10d': 'fas fa-cloud-sun-rain',  # rain
                '10n': 'fas fa-cloud-moon-rain',
                '11d': 'fas fa-bolt',  # thunderstorm
                '11n': 'fas fa-bolt',
                '13d': 'fas fa-snowflake',  # snow
                '13n': 'fas fa-snowflake',
                '50d': 'fas fa-smog',  # mist
                '50n': 'fas fa-smog'
            }

            # Process forecast data (every 24 hours)
            forecast_list = []
            seen_dates = set()
            
            for item in forecast_data['list']:
                date = item['dt_txt'].split()[0]
                if date not in seen_dates:
                    icon_code = item['weather'][0]['icon']
                    forecast_list.append({
                        'date': date,
                        'temperature': round(item['main']['temp']),
                        'description': item['weather'][0]['description'],
                        'icon': weather_icons.get(icon_code, 'fas fa-sun'),
                        'humidity': item['main']['humidity'],
                        'wind_speed': round(item['wind']['speed'], 1)
                    })
                    seen_dates.add(date)
                if len(seen_dates) >= 5:  # Only take 5 days
                    break

            # Get icon for current weather
            current_icon_code = current_data['weather'][0]['icon']
            current_icon = weather_icons.get(current_icon_code, 'fas fa-sun')

            # Generate weather alerts
            alerts = []
            current_temp = current_data['main']['temp']
            current_weather_id = current_data['weather'][0]['id']

            # Temperature alerts
            if current_temp >= 35:
                alerts.append({
                    'type': 'danger',
                    'icon': 'fas fa-temperature-high',
                    'message': 'Extreme heat warning! Stay hydrated and avoid outdoor activities.'
                })
            elif current_temp >= 30:
                alerts.append({
                    'type': 'warning',
                    'icon': 'fas fa-temperature-high',
                    'message': 'High temperature alert! Stay hydrated.'
                })
            elif current_temp <= 0:
                alerts.append({
                    'type': 'info',
                    'icon': 'fas fa-temperature-low',
                    'message': 'Freezing conditions! Bundle up and be careful of ice.'
                })

            # Rain and storm alerts
            if 200 <= current_weather_id <= 232:  # Thunderstorm
                alerts.append({
                    'type': 'danger',
                    'icon': 'fas fa-bolt',
                    'message': 'Thunderstorm warning! Seek indoor shelter.'
                })
            elif 300 <= current_weather_id <= 321:  # Drizzle
                alerts.append({
                    'type': 'info',
                    'icon': 'fas fa-cloud-rain',
                    'message': 'Light rain expected. Consider taking an umbrella.'
                })
            elif 500 <= current_weather_id <= 531:  # Rain
                alerts.append({
                    'type': 'warning',
                    'icon': 'fas fa-cloud-showers-heavy',
                    'message': 'Heavy rain alert! Take precautions and carry rain gear.'
                })

            # Check forecast for upcoming severe weather
            for day in forecast_list[:2]:  # Check next 2 days
                if 'rain' in day['description'] or 'storm' in day['description']:
                    alerts.append({
                        'type': 'info',
                        'icon': 'fas fa-cloud-rain',
                        'message': f'Rain or storms expected on {day["date"]}. Plan accordingly!'
                    })

            context = {
                'city': f"{current_data['name']}, {current_data['sys']['country']}",
                'temperature': round(current_data['main']['temp']),
                'description': current_data['weather'][0]['description'],
                'icon': current_icon,
                'humidity': current_data['main']['humidity'],
                'wind_speed': round(current_data['wind']['speed'], 1),
                'forecast': forecast_list,
                'alerts': alerts
            }
            
        except requests.exceptions.Timeout:
            return render(request, 'weather/index.html', {'error': 'Request timed out. Please try again.'})
        except requests.exceptions.ConnectionError:
            return render(request, 'weather/index.html', {'error': 'Network connection error. Please check your internet connection.'})
        except requests.exceptions.RequestException as e:
            return render(request, 'weather/index.html', {'error': f'Error fetching data: {str(e)}'})
        except (KeyError, IndexError) as e:
            return render(request, 'weather/index.html', {'error': 'Error processing weather data. Please try again.'})
        except Exception as e:
            return render(request, 'weather/index.html', {'error': f'An unexpected error occurred: {str(e)}'})
    else:
        context = {}
    
    return render(request, 'weather/index.html', context)
