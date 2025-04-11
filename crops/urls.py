from django.urls import path
from . import views

app_name = 'crops'

urlpatterns = [
    path('', views.crop_list, name='list'),
    path('search/', views.crop_search, name='search'),
    path('my-crops/', views.my_crops, name='my_crops'),
    path('add/', views.crop_create, name='create'),
    path('recommendation/', views.crop_recommendation, name='recommendation'),
    path('<int:crop_id>/', views.crop_detail, name='detail'),
    path('<int:crop_id>/edit/', views.crop_update, name='update'),
    path('<int:crop_id>/delete/', views.crop_delete, name='delete'),
] 