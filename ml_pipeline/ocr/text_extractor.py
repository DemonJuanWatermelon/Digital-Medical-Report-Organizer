"""
OCR text extraction using Tesseract with medical document optimizations
"""

import pytesseract
import cv2
import numpy as np
from PIL import Image
from typing import Dict, List, Optional, Tuple
import logging
import re

logger = logging.getLogger(__name__)

class MedicalTextExtractor:
    """
    Specialized OCR text extraction for medical documents
    """
    
    def __init__(self, tesseract_path: Optional[str] = None):
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
        
        # Medical-specific OCR configurations
        self.configs = {
            'default': '--oem 3 --psm 6',
            'single_text_block': '--oem 3 --psm 7',
            'single_word': '--oem 3 --psm 8',
            'single_character': '--oem 3 --psm 10',
            'medical_document': '--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.,:;()[]{}"/-+'
        }
    
    def extract_text(self, image_path: str, config: str = 'medical_document') -> Dict[str, any]:
        """
        Extract text from medical document image
        
        Args:
            image_path: Path to the image file
            config: Tesseract configuration to use
            
        Returns:
            Dictionary containing extracted text and metadata
        """
        try:
            # Load and preprocess image
            image = Image.open(image_path)
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Convert to OpenCV format for preprocessing
            opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            # Extract text with different configurations
            results = {}
            
            # Main text extraction
            main_text = pytesseract.image_to_string(
                opencv_image, 
                config=self.configs[config]
            )
            results['main_text'] = self._clean_text(main_text)
            
            # Extract text with confidence scores
            data = pytesseract.image_to_data(
                opencv_image, 
                config=self.configs[config], 
                output_type=pytesseract.Output.DICT
            )
            
            # Process confidence data
            results['confidence_data'] = self._process_confidence_data(data)
            
            # Extract specific medical information
            results['medical_entities'] = self._extract_medical_entities(results['main_text'])
            
            # Extract structured data
            results['structured_data'] = self._extract_structured_data(results['main_text'])
            
            # Calculate overall confidence
            results['overall_confidence'] = self._calculate_overall_confidence(data)
            
            # Extract text by regions
            results['text_regions'] = self._extract_text_by_regions(opencv_image)
            
            return results
            
        except Exception as e:
            logger.error(f"Error extracting text from {image_path}: {str(e)}")
            return {
                'main_text': '',
                'confidence_data': [],
                'medical_entities': {},
                'structured_data': {},
                'overall_confidence': 0.0,
                'text_regions': [],
                'error': str(e)
            }
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize extracted text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove non-printable characters
        text = ''.join(char for char in text if char.isprintable() or char.isspace())
        
        # Fix common OCR errors
        text = self._fix_common_ocr_errors(text)
        
        return text.strip()
    
    def _fix_common_ocr_errors(self, text: str) -> str:
        """Fix common OCR errors in medical documents"""
        # Common character substitutions
        replacements = {
            '0': 'O',  # Zero to O in some contexts
            '1': 'I',  # One to I in some contexts
            '5': 'S',  # Five to S in some contexts
        }
        
        # Apply replacements carefully
        for old, new in replacements.items():
            # Only replace in specific contexts
            text = re.sub(rf'\b{old}\b', new, text)
        
        return text
    
    def _process_confidence_data(self, data: Dict) -> List[Dict]:
        """Process Tesseract confidence data"""
        processed_data = []
        
        for i in range(len(data['text'])):
            if int(data['conf'][i]) > 0:  # Only include text with confidence > 0
                processed_data.append({
                    'text': data['text'][i],
                    'confidence': int(data['conf'][i]),
                    'bbox': {
                        'x': data['left'][i],
                        'y': data['top'][i],
                        'width': data['width'][i],
                        'height': data['height'][i]
                    }
                })
        
        return processed_data
    
    def _extract_medical_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract medical entities using regex patterns"""
        entities = {
            'dates': [],
            'measurements': [],
            'medications': [],
            'conditions': [],
            'procedures': []
        }
        
        # Date patterns
        date_patterns = [
            r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',
            r'\b\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{2,4}\b',
            r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{2,4}\b'
        ]
        
        for pattern in date_patterns:
            entities['dates'].extend(re.findall(pattern, text, re.IGNORECASE))
        
        # Measurement patterns
        measurement_patterns = [
            r'\b\d+(?:\.\d+)?\s*(?:mg|g|kg|ml|l|cm|mm|in|ft|lb|kg)\b',
            r'\b\d+(?:\.\d+)?\s*(?:mmHg|bpm|%|°F|°C)\b'
        ]
        
        for pattern in measurement_patterns:
            entities['measurements'].extend(re.findall(pattern, text, re.IGNORECASE))
        
        # Medication patterns (simplified)
        medication_patterns = [
            r'\b(?:acetaminophen|ibuprofen|aspirin|metformin|lisinopril|amlodipine)\b',
            r'\b[A-Z][a-z]+(?:mycin|cin|pam|zine|ine|ol|ide)\b'
        ]
        
        for pattern in medication_patterns:
            entities['medications'].extend(re.findall(pattern, text, re.IGNORECASE))
        
        return entities
    
    def _extract_structured_data(self, text: str) -> Dict[str, any]:
        """Extract structured data from medical text"""
        structured = {
            'patient_info': {},
            'vital_signs': {},
            'diagnosis': [],
            'medications': [],
            'procedures': []
        }
        
        # Extract patient information
        patient_patterns = {
            'name': r'Patient:\s*([A-Za-z\s]+)',
            'age': r'Age:\s*(\d+)',
            'dob': r'DOB:\s*([\d/]+)',
            'id': r'ID:\s*([A-Za-z0-9]+)'
        }
        
        for key, pattern in patient_patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                structured['patient_info'][key] = match.group(1).strip()
        
        # Extract vital signs
        vital_patterns = {
            'blood_pressure': r'BP:\s*(\d+/\d+)',
            'heart_rate': r'HR:\s*(\d+)\s*bpm',
            'temperature': r'Temp:\s*(\d+(?:\.\d+)?)\s*°F',
            'weight': r'Weight:\s*(\d+(?:\.\d+)?)\s*lbs?'
        }
        
        for key, pattern in vital_patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                structured['vital_signs'][key] = match.group(1)
        
        return structured
    
    def _calculate_overall_confidence(self, data: Dict) -> float:
        """Calculate overall confidence score"""
        confidences = [int(conf) for conf in data['conf'] if int(conf) > 0]
        if not confidences:
            return 0.0
        
        return sum(confidences) / len(confidences)
    
    def _extract_text_by_regions(self, image: np.ndarray) -> List[Dict]:
        """Extract text from different regions of the image"""
        # This is a simplified version - in practice, you'd use more sophisticated region detection
        height, width = image.shape[:2]
        
        regions = [
            {'name': 'header', 'bbox': (0, 0, width, height // 4)},
            {'name': 'body', 'bbox': (0, height // 4, width, height // 2)},
            {'name': 'footer', 'bbox': (0, 3 * height // 4, width, height)}
        ]
        
        text_regions = []
        for region in regions:
            x, y, w, h = region['bbox']
            roi = image[y:y+h, x:x+w]
            
            text = pytesseract.image_to_string(roi, config=self.configs['medical_document'])
            if text.strip():
                text_regions.append({
                    'name': region['name'],
                    'text': self._clean_text(text),
                    'bbox': region['bbox']
                })
        
        return text_regions
