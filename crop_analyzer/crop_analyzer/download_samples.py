import urllib.request
import os

# Sample images URLs (these are example URLs, they will be replaced with actual crop images)
sample_images = [
    ('https://upload.wikimedia.org/wikipedia/commons/3/31/Rice_Terrace.jpg', 'high_quality_rice.jpg'),
    ('https://upload.wikimedia.org/wikipedia/commons/d/db/Wheat_field.jpg', 'good_wheat.jpg'),
    ('https://upload.wikimedia.org/wikipedia/commons/8/85/Corn_field.jpg', 'corn_field.jpg'),
]

# Create test_images directory if it doesn't exist
os.makedirs('test_images', exist_ok=True)

# Download images
for url, filename in sample_images:
    try:
        print(f"Downloading {filename}...")
        urllib.request.urlretrieve(url, os.path.join('test_images', filename))
        print(f"Successfully downloaded {filename}")
    except Exception as e:
        print(f"Error downloading {filename}: {str(e)}")
