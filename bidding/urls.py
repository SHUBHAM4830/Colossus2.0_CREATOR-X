from django.urls import path
from . import views

app_name = 'bidding'

urlpatterns = [
    path('bids/my/', views.my_bids, name='my_bids'),
    path('bids/<int:crop_id>/place/', views.place_bid, name='place_bid'),
    path('bids/<int:bid_id>/accept/', views.accept_bid, name='accept_bid'),
    path('bids/<int:bid_id>/reject/', views.reject_bid, name='reject_bid'),
    
    path('demands/', views.demand_list, name='demand_list'),
    path('demands/my/', views.my_demands, name='my_demands'),
    path('demands/create/', views.create_demand, name='create_demand'),
    path('demands/<int:pk>/', views.demand_detail, name='demand_detail'),
    path('demands/<int:pk>/update/', views.update_demand, name='update_demand'),
    path('demands/<int:pk>/delete/', views.delete_demand, name='delete_demand'),
    path('demands/<int:pk>/bid/', views.create_bid, name='create_bid'),
    path('demands/<int:demand_id>/respond/', views.respond_demand, name='respond_demand'),
    path('demands/responses/<int:response_id>/accept/', views.accept_response, name='accept_response'),
] 