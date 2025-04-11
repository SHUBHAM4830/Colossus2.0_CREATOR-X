from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import CustomUser

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('bid', _('Bid')),
        ('bid_accepted', _('Bid Accepted')),
        ('bid_rejected', _('Bid Rejected')),
        ('demand', _('Demand')),
        ('response', _('Demand Response')),
        ('system', _('System')),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200, verbose_name=_('Title'))
    message = models.TextField(verbose_name=_('Message'))
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='system', verbose_name=_('Type'))
    related_url = models.CharField(max_length=200, blank=True, null=True, verbose_name=_('Related URL'))
    is_read = models.BooleanField(default=False, verbose_name=_('Is Read'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.user.get_full_name()}"

    def mark_as_read(self):
        self.is_read = True
        self.save()
