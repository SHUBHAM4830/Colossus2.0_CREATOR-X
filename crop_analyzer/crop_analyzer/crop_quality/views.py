from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.storage import FileSystemStorage
from .models import CropImage
from django.core.paginator import Paginator
from django.contrib import messages
from .ml_model import CropAnalyzer

# Initialize the ML model
analyzer = CropAnalyzer()

def analyze_image(image_path):
    try:
        # Use our improved ML model for analysis
        quality, remarks = analyzer.analyze_image(image_path)
        return quality, remarks
    except Exception as e:
        print(f"Error analyzing image: {str(e)}")
        return 'low', 'Error analyzing image. Please try again with a different image.'

def home(request):
    if request.method == 'POST' and request.FILES.get('crop_image'):
        image_file = request.FILES['crop_image']
        fs = FileSystemStorage()
        filename = fs.save(f'crop_images/{image_file.name}', image_file)
        
        # Analyze the image
        quality, remarks = analyze_image(fs.path(filename))
        
        # Save to database
        crop_image = CropImage.objects.create(
            image=filename,
            quality=quality,
            remarks=remarks
        )
        
        return render(request, 'crop_quality/result.html', {
            'crop_image': crop_image
        })
    
    # Get the last 3 analyzed images for the home page
    recent_images = CropImage.objects.order_by('-uploaded_at')[:3]
    return render(request, 'crop_quality/home.html', {'recent_images': recent_images})

def history(request):
    # Get all images ordered by upload date
    images_list = CropImage.objects.order_by('-uploaded_at')
    
    # Add pagination - 6 images per page
    paginator = Paginator(images_list, 6)
    page = request.GET.get('page', 1)
    images = paginator.get_page(page)
    
    # Calculate statistics
    total_analyzed = CropImage.objects.count()
    quality_stats = {
        'high': CropImage.objects.filter(quality='high').count(),
        'intermediate': CropImage.objects.filter(quality='intermediate').count(),
        'low': CropImage.objects.filter(quality='low').count(),
    }
    
    return render(request, 'crop_quality/history.html', {
        'images': images,
        'total_analyzed': total_analyzed,
        'quality_stats': quality_stats,
    })

def delete_analysis(request, pk):
    if request.method == 'POST':
        # Get the image object or return 404 if not found
        image = get_object_or_404(CropImage, pk=pk)
        
        # Delete the image file from storage
        if image.image:
            fs = FileSystemStorage()
            if fs.exists(image.image.path):
                fs.delete(image.image.path)
        
        # Delete the database record
        image.delete()
        
        # Add success message
        messages.success(request, 'Analysis deleted successfully')
        
        # Redirect back to the history page
        return redirect('history')
    
    return redirect('history')
