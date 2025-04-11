from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import CustomUser
from crops.models import Crop

class Bid(models.Model):
    STATUS_CHOICES = (
        ('pending', _('Pending')),
        ('accepted', _('Accepted')),
        ('rejected', _('Rejected')),
    )
    
    buyer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='bids')
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name='bids')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Bid Price'))
    quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Quantity'))
    message = models.TextField(blank=True, verbose_name=_('Message'))
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name=_('Status'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Bid')
        verbose_name_plural = _('Bids')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.buyer.get_full_name()}'s bid for {self.crop.name}"

    @property
    def total_amount(self):
        return self.price * self.quantity

class Demand(models.Model):
    UNIT_CHOICES = (
        ('kg', _('Kilogram')),
        ('quintal', _('Quintal')),
        ('ton', _('Ton')),
        ('bag', _('Bag')),
    )

    buyer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='demands')
    crop_name = models.CharField(max_length=100, verbose_name=_('Crop Name'))
    description = models.TextField(verbose_name=_('Description'))
    quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Quantity'))
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default='kg', verbose_name=_('Unit'))
    max_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Maximum Price'))
    location = models.CharField(max_length=100, verbose_name=_('Location'))
    state = models.CharField(max_length=100, verbose_name=_('State'))
    district = models.CharField(max_length=100, verbose_name=_('District'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Demand')
        verbose_name_plural = _('Demands')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.crop_name} - {self.buyer.get_full_name()}"

class DemandResponse(models.Model):
    demand = models.ForeignKey(Demand, on_delete=models.CASCADE, related_name='responses')
    farmer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='demand_responses')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Price'))
    quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Quantity'))
    message = models.TextField(blank=True, verbose_name=_('Message'))
    is_accepted = models.BooleanField(default=False, verbose_name=_('Is Accepted'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Demand Response')
        verbose_name_plural = _('Demand Responses')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.farmer.get_full_name()}'s response to {self.demand.crop_name}"

    @property
    def total_amount(self):
        return self.price * self.quantity
