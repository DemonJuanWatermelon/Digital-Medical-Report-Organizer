"""
Advanced image preprocessing for medical document OCR
"""

import cv2
import numpy as np
from PIL import Image
from typing import Tuple, Optional
import logging

logger = logging.getLogger(__name__)

class MedicalImageProcessor:
    """
    Advanced image preprocessing specifically designed for medical documents
    """
    
    def __init__(self):
        self.kernel_sizes = {
            'small': (3, 3),
            'medium': (5, 5),
            'large': (7, 7)
        }
    
    def preprocess_for_ocr(self, image_path: str) -> np.ndarray:
        """
        Comprehensive preprocessing pipeline for medical document OCR
        
        Args:
            image_path: Path to the input image
            
        Returns:
            Preprocessed image as numpy array
        """
        try:
            # Load image
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"Could not load image from {image_path}")
            
            # Convert to RGB
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Apply preprocessing steps
            processed = self._enhance_contrast(image_rgb)
            processed = self._remove_noise(processed)
            processed = self._deskew_image(processed)
            processed = self._binarize_image(processed)
            processed = self._morphological_operations(processed)
            
            return processed
            
        except Exception as e:
            logger.error(f"Error preprocessing image {image_path}: {str(e)}")
            raise
    
    def _enhance_contrast(self, image: np.ndarray) -> np.ndarray:
        """Enhance contrast using CLAHE (Contrast Limited Adaptive Histogram Equalization)"""
        # Convert to LAB color space
        lab = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)
        l, a, b = cv2.split(lab)
        
        # Apply CLAHE to L channel
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        
        # Merge channels and convert back to RGB
        lab = cv2.merge([l, a, b])
        return cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)
    
    def _remove_noise(self, image: np.ndarray) -> np.ndarray:
        """Remove noise using bilateral filtering"""
        return cv2.bilateralFilter(image, 9, 75, 75)
    
    def _deskew_image(self, image: np.ndarray) -> np.ndarray:
        """Detect and correct skew in the document"""
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        
        # Apply edge detection
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)
        
        # Detect lines using Hough transform
        lines = cv2.HoughLines(edges, 1, np.pi/180, threshold=100)
        
        if lines is not None:
            # Calculate average angle
            angles = []
            for line in lines:
                rho, theta = line[0]
                angle = theta - np.pi/2
                angles.append(angle)
            
            if angles:
                median_angle = np.median(angles)
                # Only correct if angle is significant
                if abs(median_angle) > 0.1:
                    # Rotate image
                    h, w = image.shape[:2]
                    center = (w // 2, h // 2)
                    rotation_matrix = cv2.getRotationMatrix2D(center, median_angle * 180 / np.pi, 1.0)
                    image = cv2.warpAffine(image, rotation_matrix, (w, h), flags=cv2.INTER_CUBIC)
        
        return image
    
    def _binarize_image(self, image: np.ndarray) -> np.ndarray:
        """Convert to binary image using adaptive thresholding"""
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        
        # Use adaptive thresholding for better results with varying lighting
        binary = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
        
        return binary
    
    def _morphological_operations(self, image: np.ndarray) -> np.ndarray:
        """Apply morphological operations to clean up the image"""
        # Define kernel for morphological operations
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        
        # Remove small noise
        cleaned = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
        
        # Fill small holes
        cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_OPEN, kernel)
        
        return cleaned
    
    def detect_text_regions(self, image: np.ndarray) -> list:
        """
        Detect text regions in the image using MSER (Maximally Stable Extremal Regions)
        
        Args:
            image: Preprocessed binary image
            
        Returns:
            List of bounding boxes for text regions
        """
        # Initialize MSER detector
        mser = cv2.MSER_create()
        
        # Detect regions
        regions, _ = mser.detectRegions(image)
        
        # Convert regions to bounding boxes
        text_regions = []
        for region in regions:
            x, y, w, h = cv2.boundingRect(region)
            # Filter out very small regions
            if w > 20 and h > 10:
                text_regions.append((x, y, w, h))
        
        return text_regions
    
    def extract_text_quality_score(self, image: np.ndarray) -> float:
        """
        Calculate a quality score for the preprocessed image
        
        Args:
            image: Preprocessed binary image
            
        Returns:
            Quality score between 0 and 1
        """
        # Calculate various quality metrics
        edges = cv2.Canny(image, 50, 150)
        edge_density = np.sum(edges > 0) / (image.shape[0] * image.shape[1])
        
        # Calculate text line straightness
        lines = cv2.HoughLines(edges, 1, np.pi/180, threshold=50)
        line_straightness = len(lines) / 100 if lines is not None else 0
        
        # Combine metrics
        quality_score = min(1.0, edge_density * 2 + line_straightness * 0.5)
        
        return quality_score
