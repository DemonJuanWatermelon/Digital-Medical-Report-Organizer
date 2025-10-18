"""
Medical Named Entity Recognition using Emergent Medical models
"""

import torch
from transformers import pipeline, AutoTokenizer, AutoModelForTokenClassification
from typing import Dict, List, Any, Optional
import logging
import re

logger = logging.getLogger(__name__)

class MedicalNER:
    """
    Medical Named Entity Recognition using pre-trained models
    """
    
    def __init__(self, model_name: str = "emergentmedical/emergent-medical-ner"):
        self.model_name = model_name
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        try:
            # Initialize the NER pipeline
            self.ner_pipeline = pipeline(
                "ner",
                model=model_name,
                aggregation_strategy="simple",
                device=0 if self.device == "cuda" else -1
            )
            
            # Load tokenizer and model for custom processing
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForTokenClassification.from_pretrained(model_name)
            self.model.to(self.device)
            
            logger.info(f"Medical NER model loaded successfully on {self.device}")
            
        except Exception as e:
            logger.error(f"Error loading Medical NER model: {str(e)}")
            self.ner_pipeline = None
            self.tokenizer = None
            self.model = None
    
    def extract_entities(self, text: str) -> Dict[str, List[Dict[str, Any]]]:
        """
        Extract medical entities from text
        
        Args:
            text: Input text to process
            
        Returns:
            Dictionary containing categorized entities
        """
        if not self.ner_pipeline:
            return self._fallback_entity_extraction(text)
        
        try:
            # Extract entities using the pipeline
            entities = self.ner_pipeline(text)
            
            # Categorize entities
            categorized = self._categorize_entities(entities)
            
            # Post-process entities
            categorized = self._post_process_entities(categorized, text)
            
            return categorized
            
        except Exception as e:
            logger.error(f"Error in entity extraction: {str(e)}")
            return self._fallback_entity_extraction(text)
    
    def _categorize_entities(self, entities: List[Dict]) -> Dict[str, List[Dict[str, Any]]]:
        """Categorize entities by medical type"""
        categories = {
            'medications': [],
            'conditions': [],
            'procedures': [],
            'anatomy': [],
            'symptoms': [],
            'vital_signs': [],
            'measurements': [],
            'dates': [],
            'other': []
        }
        
        for entity in entities:
            entity_type = entity.get('entity_group', '').lower()
            entity_text = entity.get('word', '')
            confidence = entity.get('score', 0.0)
            
            # Map entity types to categories
            if entity_type in ['drug', 'medication', 'medicine']:
                categories['medications'].append({
                    'text': entity_text,
                    'confidence': confidence,
                    'start': entity.get('start', 0),
                    'end': entity.get('end', 0)
                })
            elif entity_type in ['condition', 'disease', 'disorder', 'syndrome']:
                categories['conditions'].append({
                    'text': entity_text,
                    'confidence': confidence,
                    'start': entity.get('start', 0),
                    'end': entity.get('end', 0)
                })
            elif entity_type in ['procedure', 'treatment', 'therapy', 'surgery']:
                categories['procedures'].append({
                    'text': entity_text,
                    'confidence': confidence,
                    'start': entity.get('start', 0),
                    'end': entity.get('end', 0)
                })
            elif entity_type in ['anatomy', 'body_part', 'organ']:
                categories['anatomy'].append({
                    'text': entity_text,
                    'confidence': confidence,
                    'start': entity.get('start', 0),
                    'end': entity.get('end', 0)
                })
            elif entity_type in ['symptom', 'sign']:
                categories['symptoms'].append({
                    'text': entity_text,
                    'confidence': confidence,
                    'start': entity.get('start', 0),
                    'end': entity.get('end', 0)
                })
            elif entity_type in ['vital_sign', 'measurement']:
                categories['vital_signs'].append({
                    'text': entity_text,
                    'confidence': confidence,
                    'start': entity.get('start', 0),
                    'end': entity.get('end', 0)
                })
            elif entity_type in ['date', 'time']:
                categories['dates'].append({
                    'text': entity_text,
                    'confidence': confidence,
                    'start': entity.get('start', 0),
                    'end': entity.get('end', 0)
                })
            else:
                categories['other'].append({
                    'text': entity_text,
                    'confidence': confidence,
                    'start': entity.get('start', 0),
                    'end': entity.get('end', 0)
                })
        
        return categories
    
    def _post_process_entities(self, entities: Dict[str, List[Dict]], text: str) -> Dict[str, List[Dict]]:
        """Post-process entities for better accuracy"""
        processed = {}
        
        for category, entity_list in entities.items():
            processed[category] = []
            
            for entity in entity_list:
                # Clean entity text
                cleaned_text = self._clean_entity_text(entity['text'])
                
                if cleaned_text and len(cleaned_text) > 1:
                    entity['text'] = cleaned_text
                    entity['normalized'] = self._normalize_entity(entity['text'], category)
                    processed[category].append(entity)
        
        return processed
    
    def _clean_entity_text(self, text: str) -> str:
        """Clean entity text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove non-alphanumeric characters at the beginning/end
        text = text.strip('.,;:()[]{}"\'')
        
        # Remove very short entities (likely noise)
        if len(text) < 2:
            return ""
        
        return text.strip()
    
    def _normalize_entity(self, text: str, category: str) -> str:
        """Normalize entity text for consistency"""
        # Convert to lowercase for normalization
        normalized = text.lower()
        
        # Apply category-specific normalization
        if category == 'medications':
            # Remove common medication suffixes
            normalized = re.sub(r'\b(tablet|capsule|mg|ml|g)\b', '', normalized)
        elif category == 'conditions':
            # Standardize condition names
            normalized = re.sub(r'\b(syndrome|disorder|disease)\b', '', normalized)
        
        return normalized.strip()
    
    def _fallback_entity_extraction(self, text: str) -> Dict[str, List[Dict[str, Any]]]:
        """Fallback entity extraction using regex patterns"""
        logger.warning("Using fallback entity extraction")
        
        entities = {
            'medications': [],
            'conditions': [],
            'procedures': [],
            'anatomy': [],
            'symptoms': [],
            'vital_signs': [],
            'measurements': [],
            'dates': [],
            'other': []
        }
        
        # Medication patterns
        med_patterns = [
            r'\b(?:acetaminophen|ibuprofen|aspirin|metformin|lisinopril|amlodipine|atorvastatin|metoprolol|omeprazole|simvastatin)\b',
            r'\b[A-Z][a-z]+(?:mycin|cin|pam|zine|ine|ol|ide|pril|sartan|statin)\b'
        ]
        
        for pattern in med_patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                entities['medications'].append({
                    'text': match.group(),
                    'confidence': 0.7,
                    'start': match.start(),
                    'end': match.end(),
                    'normalized': match.group().lower()
                })
        
        # Condition patterns
        condition_patterns = [
            r'\b(?:diabetes|hypertension|asthma|arthritis|depression|anxiety|migraine|pneumonia|bronchitis)\b',
            r'\b(?:cancer|carcinoma|tumor|neoplasm|malignancy)\b'
        ]
        
        for pattern in condition_patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                entities['conditions'].append({
                    'text': match.group(),
                    'confidence': 0.7,
                    'start': match.start(),
                    'end': match.end(),
                    'normalized': match.group().lower()
                })
        
        # Measurement patterns
        measurement_patterns = [
            r'\b\d+(?:\.\d+)?\s*(?:mg|g|kg|ml|l|cm|mm|in|ft|lb|kg|mmHg|bpm|%|°F|°C)\b'
        ]
        
        for pattern in measurement_patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                entities['measurements'].append({
                    'text': match.group(),
                    'confidence': 0.8,
                    'start': match.start(),
                    'end': match.end(),
                    'normalized': match.group().lower()
                })
        
        return entities
    
    def get_entity_statistics(self, entities: Dict[str, List[Dict]]) -> Dict[str, Any]:
        """Get statistics about extracted entities"""
        stats = {
            'total_entities': sum(len(entity_list) for entity_list in entities.values()),
            'categories': {},
            'high_confidence_entities': 0,
            'average_confidence': 0.0
        }
        
        total_confidence = 0
        total_count = 0
        
        for category, entity_list in entities.items():
            stats['categories'][category] = len(entity_list)
            
            for entity in entity_list:
                confidence = entity.get('confidence', 0.0)
                total_confidence += confidence
                total_count += 1
                
                if confidence > 0.8:
                    stats['high_confidence_entities'] += 1
        
        if total_count > 0:
            stats['average_confidence'] = total_confidence / total_count
        
        return stats
