import torch
import torch.nn as nn
import torchvision.transforms as transforms
from torchvision.models import resnet18, ResNet18_Weights
from PIL import Image
import numpy as np
from skimage import feature, color, exposure
import torch.nn.functional as F

class CropQualityModel(nn.Module):
    def __init__(self):
        super(CropQualityModel, self).__init__()
        # Load pre-trained ResNet18
        self.backbone = resnet18(weights=ResNet18_Weights.DEFAULT)
        
        # Remove the last layer
        num_features = self.backbone.fc.in_features
        
        # Add custom layers for crop quality assessment
        self.quality_layers = nn.Sequential(
            nn.Linear(num_features, 512),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, 3)  # 3 classes: high, intermediate, low
        )
        
    def forward(self, x):
        # Extract features using ResNet
        features = self.backbone.conv1(x)
        features = self.backbone.bn1(features)
        features = self.backbone.relu(features)
        features = self.backbone.maxpool(features)
        
        features = self.backbone.layer1(features)
        features = self.backbone.layer2(features)
        features = self.backbone.layer3(features)
        features = self.backbone.layer4(features)
        
        features = self.backbone.avgpool(features)
        features = torch.flatten(features, 1)
        
        # Quality classification
        quality = self.quality_layers(features)
        return quality

class CropAnalyzer:
    def __init__(self):
        self.model = CropQualityModel()
        self.model.eval()
        
        # Image preprocessing
        self.transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
    
    def extract_features(self, image):
        # Convert to LAB color space for better color analysis
        lab_img = color.rgb2lab(np.array(image))
        
        # Calculate color features
        color_std = np.std(lab_img, axis=(0,1))
        color_mean = np.mean(lab_img, axis=(0,1))
        
        # Calculate texture features using Local Binary Patterns
        gray_img = color.rgb2gray(np.array(image))
        lbp = feature.local_binary_pattern(gray_img, P=8, R=1, method='uniform')
        lbp_hist = np.histogram(lbp, bins=10, density=True)[0]
        
        # Calculate contrast using histogram
        contrast = exposure.histogram(gray_img)[0]
        contrast_score = np.std(contrast)
        
        return {
            'color_std': color_std,
            'color_mean': color_mean,
            'texture': lbp_hist,
            'contrast': contrast_score
        }
    
    def analyze_image(self, image_path):
        # Load and preprocess image
        img = Image.open(image_path).convert('RGB')
        img_tensor = self.transform(img)
        img_tensor = img_tensor.unsqueeze(0)
        
        # Extract additional features
        features = self.extract_features(img)
        
        # Get model predictions
        with torch.no_grad():
            outputs = self.model(img_tensor)
            probabilities = F.softmax(outputs, dim=1)
            quality_score = probabilities.max().item()
            predicted_class = torch.argmax(probabilities).item()
        
        # Combine model prediction with feature analysis
        color_score = np.mean(features['color_std'])
        texture_score = np.mean(features['texture'])
        contrast_score = features['contrast']
        
        # Calculate final score combining all factors
        final_score = (quality_score * 0.4 + 
                      color_score * 0.3 + 
                      texture_score * 0.15 + 
                      contrast_score * 0.15)
        
        # Determine quality and generate detailed remarks
        if final_score > 0.7:
            quality = 'high'
            remarks = (f'Excellent crop quality! '
                      f'Good color distribution (score: {color_score:.2f}), '
                      f'uniform texture (score: {texture_score:.2f}), '
                      f'and optimal contrast (score: {contrast_score:.2f})')
        elif final_score > 0.4:
            quality = 'intermediate'
            remarks = (f'Average crop quality. '
                      f'Color variation: {color_score:.2f}, '
                      f'texture uniformity: {texture_score:.2f}, '
                      f'contrast level: {contrast_score:.2f}. '
                      f'Could be improved.')
        else:
            quality = 'low'
            remarks = (f'Below average quality. '
                      f'Issues detected - '
                      f'color score: {color_score:.2f}, '
                      f'texture score: {texture_score:.2f}, '
                      f'contrast: {contrast_score:.2f}. '
                      f'Needs improvement.')
