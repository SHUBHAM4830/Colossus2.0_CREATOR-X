from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .models import Crop, CropCategory, CropRecommendation
from .forms import CropForm, CropCategoryForm, CropRecommendationForm
from django.http import JsonResponse
import os
import pickle
from django.conf import settings
from django.views.decorators.http import require_http_methods
import random
import json

def crop_list(request):
    crops = Crop.objects.filter(is_available=True)
    categories = CropCategory.objects.all()
    return render(request, 'crops/list.html', {
        'crops': crops,
        'categories': categories
    })

def crop_detail(request, crop_id):
    crop = get_object_or_404(Crop, id=crop_id)
    return render(request, 'crops/detail.html', {'crop': crop})

@login_required
def my_crops(request):
    crops = Crop.objects.filter(farmer=request.user)
    return render(request, 'crops/my_crops.html', {'crops': crops})

@login_required
def crop_create(request):
    if request.method == 'POST':
        form = CropForm(request.POST, request.FILES)
        if form.is_valid():
            crop = form.save(commit=False)
            crop.farmer = request.user
            crop.save()
            messages.success(request, _('Your crop has been listed successfully!'))
            return redirect('crops:my_crops')
    else:
        form = CropForm()
    return render(request, 'crops/form.html', {'form': form})

@login_required
def crop_update(request, crop_id):
    crop = get_object_or_404(Crop, id=crop_id, farmer=request.user)
    if request.method == 'POST':
        form = CropForm(request.POST, request.FILES, instance=crop)
        if form.is_valid():
            form.save()
            messages.success(request, _('Your crop listing has been updated!'))
            return redirect('crops:my_crops')
    else:
        form = CropForm(instance=crop)
    return render(request, 'crops/form.html', {'form': form})

@login_required
def crop_delete(request, crop_id):
    crop = get_object_or_404(Crop, id=crop_id, farmer=request.user)
    if request.method == 'POST':
        crop.delete()
        messages.success(request, _('Your crop listing has been deleted!'))
        return redirect('crops:my_crops')
    return render(request, 'crops/confirm_delete.html', {'crop': crop})

@login_required
def crop_search(request):
    query = request.GET.get('q', '')
    category_id = request.GET.get('category')
    
    crops = Crop.objects.filter(is_available=True)
    
    if query:
        crops = crops.filter(name__icontains=query)
    
    if category_id:
        crops = crops.filter(category_id=category_id)
    
    categories = CropCategory.objects.all()
    
    return render(request, 'crops/search.html', {
        'crops': crops,
        'categories': categories,
        'query': query,
        'selected_category': category_id
    })

@login_required
def crop_recommendation(request):
    if request.method == 'POST':
        form = CropRecommendationForm(request.POST)
        if form.is_valid():
            try:
                # Get form data
                soil_type = form.cleaned_data['soil_type']
                climate_zone = form.cleaned_data['climate_zone']
                field_area = form.cleaned_data['field_area']
                soil_ph = form.cleaned_data['soil_ph']
                rainfall = form.cleaned_data['rainfall']
                irrigation_method = form.cleaned_data['irrigation_method']
                growing_season = form.cleaned_data['growing_season']
                market_preference = form.cleaned_data['market_preference']
                
                # Get all crops
                crops = Crop.objects.all()
                recommended_crops = []
                
                # Calculate suitability score for each crop
                for crop in crops:
                    score = 0
                    total_factors = 0
                    
                    # Soil type match
                    if crop.soil_type == soil_type:
                        score += 20
                    total_factors += 20
                    
                    # Climate zone match
                    if crop.climate_zone == climate_zone:
                        score += 20
                    total_factors += 20
                    
                    # pH range check
                    if crop.min_ph <= soil_ph <= crop.max_ph:
                        score += 15
                    total_factors += 15
                    
                    # Rainfall check
                    if crop.min_rainfall <= rainfall <= crop.max_rainfall:
                        score += 15
                    total_factors += 15
                    
                    # Irrigation method match
                    if crop.irrigation_method == irrigation_method:
                        score += 10
                    total_factors += 10
                    
                    # Growing season match
                    if crop.growing_season == growing_season:
                        score += 10
                    total_factors += 10
                    
                    # Market preference match
                    if crop.market_preference == market_preference:
                        score += 10
                    total_factors += 10
                    
                    # Calculate final suitability score
                    suitability_score = (score / total_factors) * 100
                    
                    # Calculate estimated yield and profit
                    base_yield = float(crop.yield_per_acre) if crop.yield_per_acre else 2.0
                    adjusted_yield = base_yield * (suitability_score / 100)
                    estimated_yield = adjusted_yield * field_area
                    
                    estimated_revenue = estimated_yield * float(crop.price_per_unit)
                    estimated_cost = estimated_yield * 5000  # Assuming ₹5000 per ton as cost
                    estimated_profit = estimated_revenue - estimated_cost
                    profit_margin = (estimated_profit / estimated_revenue) * 100 if estimated_revenue > 0 else 0
                    
                    if suitability_score >= 50:  # Only include crops with at least 50% suitability
                        recommended_crops.append({
                            'id': crop.id,
                            'name': crop.name,
                            'description': crop.description,
                            'image_url': crop.image.url if crop.image else None,
                            'suitability_score': round(suitability_score, 2),
                            'estimated_yield': round(estimated_yield, 2),
                            'estimated_revenue': round(estimated_revenue, 2),
                            'estimated_cost': round(estimated_cost, 2),
                            'estimated_profit': round(estimated_profit, 2),
                            'profit_margin': round(profit_margin, 2)
                        })
                
                # Sort crops by suitability score
                recommended_crops.sort(key=lambda x: x['suitability_score'], reverse=True)
                
                # Save recommendation to database
                CropRecommendation.objects.create(
                    user=request.user,
                    soil_type=soil_type,
                    climate_zone=climate_zone,
                    field_area=field_area,
                    soil_ph=soil_ph,
                    rainfall=rainfall,
                    irrigation_method=irrigation_method,
                    growing_season=growing_season,
                    market_preference=market_preference,
                    recommendations=recommended_crops
                )
                
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': True,
                        'field_area': field_area,
                        'recommended_crops': recommended_crops
                    })
                else:
                    messages.success(request, _('Crop recommendations generated successfully!'))
                    return render(request, 'crops/recommendation.html', {
                        'form': form,
                        'recommended_crops': recommended_crops,
                        'field_area': field_area
                    })
            except Exception as e:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False,
                        'errors': str(e)
                    })
                else:
                    messages.error(request, _('An error occurred while generating recommendations.'))
                    return render(request, 'crops/recommendation.html', {'form': form})
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'errors': form.errors
                })
            else:
                messages.error(request, _('Please correct the errors below.'))
                return render(request, 'crops/recommendation.html', {'form': form})
    else:
        form = CropRecommendationForm()
        return render(request, 'crops/recommendation.html', {'form': form})
