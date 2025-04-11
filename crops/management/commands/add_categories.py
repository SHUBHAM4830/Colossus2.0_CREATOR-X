from django.core.management.base import BaseCommand
from crops.models import CropCategory
from django.utils.translation import gettext_lazy as _

class Command(BaseCommand):
    help = 'Adds default crop categories'

    def handle(self, *args, **options):
        categories = [
            {
                'name': _('Fruits'),
                'description': _('Fresh and seasonal fruits')
            },
            {
                'name': _('Vegetables'),
                'description': _('Fresh and seasonal vegetables')
            },
            {
                'name': _('Grains'),
                'description': _('Cereals and staple grains')
            },
            {
                'name': _('Pulses'),
                'description': _('Legumes and pulses')
            },
            {
                'name': _('Spices'),
                'description': _('Aromatic spices and herbs')
            },
            {
                'name': _('Oilseeds'),
                'description': _('Oil-bearing crops')
            },
            {
                'name': _('Tubers'),
                'description': _('Root vegetables and tubers')
            },
            {
                'name': _('Medicinal Plants'),
                'description': _('Medicinal and aromatic plants')
            },
            {
                'name': _('Flowers'),
                'description': _('Ornamental and cut flowers')
            },
            {
                'name': _('Other'),
                'description': _('Other agricultural products')
            }
        ]

        for category_data in categories:
            category, created = CropCategory.objects.get_or_create(
                name=category_data['name'],
                defaults={'description': category_data['description']}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {category.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Category already exists: {category.name}')) 