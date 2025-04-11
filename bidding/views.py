from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from crops.models import Crop
from .models import Bid, Demand, DemandResponse
from .forms import BidForm, DemandForm, DemandResponseForm
from notifications.models import Notification

@login_required
def place_bid(request, crop_id):
    crop = get_object_or_404(Crop, id=crop_id, is_available=True)
    
    if request.user.is_farmer:
        messages.error(request, _('Only buyers can place bids'))
        return redirect('crops:detail', crop_id=crop_id)
    
    if request.method == 'POST':
        form = BidForm(request.POST)
        if form.is_valid():
            bid = form.save(commit=False)
            bid.buyer = request.user
            bid.crop = crop
            bid.save()
            
            # Create notification for the farmer
            Notification.objects.create(
                user=crop.farmer,
                title=_('New Bid Received'),
                message=_('%(buyer)s has placed a bid of ₹%(price)s per %(unit)s for your %(crop)s') % {
                    'buyer': request.user.get_full_name(),
                    'price': bid.price,
                    'unit': crop.unit,
                    'crop': crop.name
                },
                notification_type='bid',
                related_url=f'/crops/{crop.id}/'
            )
            
            messages.success(request, _('Your bid has been placed successfully!'))
            return redirect('crops:detail', crop_id=crop_id)
    else:
        form = BidForm()
    
    return render(request, 'bidding/place_bid.html', {
        'form': form,
        'crop': crop
    })

@login_required
def my_bids(request):
    bids = Bid.objects.filter(buyer=request.user)
    return render(request, 'bidding/my_bids.html', {'bids': bids})

@login_required
def demand_list(request):
    """View all active demands"""
    demands = Demand.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'bidding/demand_list.html', {
        'demands': demands
    })

@login_required
def my_demands(request):
    """View demands created by the current user"""
    demands = Demand.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'bidding/my_demands.html', {
        'demands': demands
    })

@login_required
def create_demand(request):
    if request.method == 'POST':
        form = DemandForm(request.POST)
        if form.is_valid():
            demand = form.save(commit=False)
            demand.user = request.user
            demand.save()
            messages.success(request, _('Demand created successfully.'))
            return redirect('bidding:demand_detail', pk=demand.id)
    else:
        form = DemandForm()
    
    return render(request, 'bidding/create_demand.html', {'form': form})

@login_required
def demand_detail(request, pk):
    demand = get_object_or_404(Demand, pk=pk)
    return render(request, 'bidding/demand_detail.html', {
        'demand': demand
    })

@login_required
def respond_demand(request, demand_id):
    demand = get_object_or_404(Demand, id=demand_id, is_active=True)
    
    if not request.user.is_farmer:
        messages.error(request, _('Only farmers can respond to demands'))
        return redirect('bidding:demand_detail', pk=demand_id)
    
    if request.method == 'POST':
        form = DemandResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.farmer = request.user
            response.demand = demand
            response.save()
            
            # Create notification for the buyer
            Notification.objects.create(
                user=demand.user,
                title=_('New Response Received'),
                message=_('%(farmer)s has responded to your demand for %(crop)s') % {
                    'farmer': request.user.get_full_name(),
                    'crop': demand.title
                },
                notification_type='response'
            )
            
            messages.success(request, _('Your response has been submitted successfully!'))
            return redirect('bidding:demand_detail', pk=demand_id)
    else:
        form = DemandResponseForm()
    
    return render(request, 'bidding/respond_demand.html', {
        'form': form,
        'demand': demand
    })

@login_required
def accept_bid(request, bid_id):
    bid = get_object_or_404(Bid, id=bid_id)
    if request.user != bid.crop.farmer:
        messages.error(request, _("You don't have permission to accept this bid."))
        return redirect('crops:detail', crop_id=bid.crop.id)
    
    # Reject all other bids for this crop
    Bid.objects.filter(crop=bid.crop).exclude(id=bid.id).update(status='rejected')
    
    # Accept the selected bid
    bid.status = 'accepted'
    bid.save()
    
    # Update crop status
    bid.crop.status = 'sold'
    bid.crop.save()
    
    # Create notification for the buyer
    Notification.objects.create(
        user=bid.buyer,
        title=_('Bid Accepted'),
        message=_('Your bid of ₹%(price)s per %(unit)s for %(crop)s has been accepted by %(farmer)s') % {
            'price': bid.price,
            'unit': bid.crop.unit,
            'crop': bid.crop.name,
            'farmer': request.user.get_full_name()
        },
        notification_type='bid_accepted',
        related_url=f'/crops/{bid.crop.id}/'
    )
    
    messages.success(request, _("Bid accepted successfully!"))
    return redirect('crops:detail', crop_id=bid.crop.id)

@login_required
def reject_bid(request, bid_id):
    bid = get_object_or_404(Bid, id=bid_id)
    if request.user != bid.crop.farmer:
        messages.error(request, _("You don't have permission to reject this bid."))
        return redirect('crops:detail', crop_id=bid.crop.id)
    
    bid.status = 'rejected'
    bid.save()
    
    # Create notification for the buyer
    Notification.objects.create(
        user=bid.buyer,
        title=_('Bid Rejected'),
        message=_('Your bid of ₹%(price)s per %(unit)s for %(crop)s has been rejected by %(farmer)s') % {
            'price': bid.price,
            'unit': bid.crop.unit,
            'crop': bid.crop.name,
            'farmer': request.user.get_full_name()
        },
        notification_type='bid_rejected',
        related_url=f'/crops/{bid.crop.id}/'
    )
    
    messages.success(request, _("Bid rejected successfully!"))
    return redirect('crops:detail', crop_id=bid.crop.id)

@login_required
def accept_response(request, response_id):
    response = get_object_or_404(DemandResponse, id=response_id)
    
    if request.user != response.demand.user:
        messages.error(request, _('You are not authorized to accept this response'))
        return redirect('bidding:demand_detail', pk=response.demand.id)
    
    response.status = 'accepted'
    response.save()
    
    # Create notification for the farmer
    Notification.objects.create(
        user=response.farmer,
        title=_('Response Accepted'),
        message=_('Your response to %(demand)s has been accepted by %(buyer)s') % {
            'demand': response.demand.title,
            'buyer': request.user.get_full_name()
        },
        notification_type='response_accepted'
    )
    
    messages.success(request, _('Response accepted successfully!'))
    return redirect('bidding:demand_detail', pk=response.demand.id)

@login_required
def update_demand(request, pk):
    demand = get_object_or_404(Demand, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = DemandForm(request.POST, instance=demand)
        if form.is_valid():
            form.save()
            messages.success(request, _('Demand updated successfully.'))
            return redirect('bidding:demand_detail', pk=demand.id)
    else:
        form = DemandForm(instance=demand)
    
    return render(request, 'bidding/update_demand.html', {
        'form': form,
        'demand': demand
    })

@login_required
def delete_demand(request, pk):
    demand = get_object_or_404(Demand, pk=pk, user=request.user)
    demand.delete()
    messages.success(request, _('Demand deleted successfully.'))
    return redirect('bidding:my_demands')

@login_required
def create_bid(request, pk):
    demand = get_object_or_404(Demand, pk=pk)
    
    if request.method == 'POST':
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        
        bid = Bid.objects.create(
            user=request.user,
            demand=demand,
            price=price,
            quantity=quantity
        )
        
        messages.success(request, _('Bid placed successfully.'))
        return redirect('bidding:demand_detail', pk=demand.id)
    
    return render(request, 'bidding/create_bid.html', {
        'demand': demand
    })
