from PIL import Image
import numpy as np
import os

def create_crop_image(quality, size=(300, 300)):
    # Create base image array
    img_array = np.zeros((size[0], size[1], 3), dtype=np.uint8)
    
    if quality == 'high':
        # Bright green color with some variation for healthy crops
        base_color = [0, 180, 0]
        noise = np.random.normal(0, 15, (size[0], size[1], 3))
    elif quality == 'medium':
        # Yellowish-green for medium quality
        base_color = [180, 180, 0]
        noise = np.random.normal(0, 25, (size[0], size[1], 3))
    else:
        # Brownish color for low quality
        base_color = [139, 69, 19]
        noise = np.random.normal(0, 35, (size[0], size[1], 3))
    
    # Add base color and noise
    for i in range(3):
        img_array[:, :, i] = base_color[i]
    
    # Add noise and clip values
    img_array = np.clip(img_array + noise, 0, 255).astype(np.uint8)
    
    # Create image from array
    img = Image.fromarray(img_array)
    return img

# Create test images directory
os.makedirs('test_images', exist_ok=True)

# Create sample images
qualities = ['high', 'medium', 'low']
for quality in qualities:
    img = create_crop_image(quality)
    img.save(f'test_images/crop_{quality}_quality.jpg')
    print(f"Created {quality} quality test image")
