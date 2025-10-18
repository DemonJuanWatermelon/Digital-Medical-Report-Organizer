"""
Medical document classification using AI models
"""

import torch
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from typing import Dict, List, Any, Optional
import logging
import re

logger = logging.getLogger(__name__)

class MedicalDocumentClassifier:
    """
    Classify medical documents by type and content
    """
    
    def __init__(self, model_name: str = "emergentmedical/emergent-medical-classification"):
        self.model_name = model_name
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        try:
            # Initialize the classification pipeline
            self.classifier = pipeline(
                "text-classification",
                model=model_name,
                device=0 if self.device == "cuda" else -1
            )
            
            # Load tokenizer and model for custom processing
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
            self.model.to(self.device)
            
            logger.info(f"Medical document classifier loaded successfully on {self.device}")
            
        except Exception as e:
            logger.error(f"Error loading document classifier: {str(e)}")
            self.classifier = None
            self.tokenizer = None
            self.model = None
    
    def classify_document(self, text: str) -> Dict[str, Any]:
        """
        Classify a medical document
        
        Args:
            text: Document text to classify
            
        Returns:
            Classification results with confidence scores
        """
        if not self.classifier:
            return self._fallback_classification(text)
        
        try:
            # Get classification results
            results = self.classifier(text)
            
            # Process results
            classification = self._process_classification_results(results)
            
            # Add additional analysis
            classification['additional_analysis'] = self._analyze_document_content(text)
            
            return classification
            
        except Exception as e:
            logger.error(f"Error in document classification: {str(e)}")
            return self._fallback_classification(text)
    
    def _process_classification_results(self, results: List[Dict]) -> Dict[str, Any]:
        """Process raw classification results"""
        if not results:
            return {
                'primary_class': 'unknown',
                'confidence': 0.0,
                'all_classes': []
            }
        
        # Sort by confidence score
        sorted_results = sorted(results, key=lambda x: x['score'], reverse=True)
        
        return {
            'primary_class': sorted_results[0]['label'],
            'confidence': sorted_results[0]['score'],
            'all_classes': sorted_results
        }
    
    def _analyze_document_content(self, text: str) -> Dict[str, Any]:
        """Analyze document content for additional insights"""
        analysis = {
            'document_length': len(text),
            'word_count': len(text.split()),
            'has_patient_info': self._detect_patient_info(text),
            'has_vital_signs': self._detect_vital_signs(text),
            'has_medications': self._detect_medications(text),
            'has_diagnosis': self._detect_diagnosis(text),
            'has_procedures': self._detect_procedures(text),
            'document_sections': self._identify_sections(text),
            'urgency_level': self._assess_urgency(text)
        }
        
        return analysis
    
    def _detect_patient_info(self, text: str) -> bool:
        """Detect if document contains patient information"""
        patient_patterns = [
            r'patient\s*name',
            r'patient\s*id',
            r'date\s*of\s*birth',
            r'dob\s*:',
            r'age\s*:',
            r'mrn\s*:',
            r'medical\s*record\s*number'
        ]
        
        for pattern in patient_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        
        return False
    
    def _detect_vital_signs(self, text: str) -> bool:
        """Detect if document contains vital signs"""
        vital_patterns = [
            r'blood\s*pressure',
            r'heart\s*rate',
            r'temperature',
            r'respiratory\s*rate',
            r'oxygen\s*saturation',
            r'bp\s*:',
            r'hr\s*:',
            r'temp\s*:',
            r'rr\s*:',
            r'spo2\s*:'
        ]
        
        for pattern in vital_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        
        return False
    
    def _detect_medications(self, text: str) -> bool:
        """Detect if document contains medication information"""
        med_patterns = [
            r'medications?',
            r'prescriptions?',
            r'drugs?',
            r'pharmacy',
            r'dosage',
            r'mg\s*',
            r'ml\s*',
            r'tablet',
            r'capsule'
        ]
        
        for pattern in med_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        
        return False
    
    def _detect_diagnosis(self, text: str) -> bool:
        """Detect if document contains diagnosis information"""
        diagnosis_patterns = [
            r'diagnosis',
            r'diagnosed',
            r'condition',
            r'disease',
            r'disorder',
            r'syndrome',
            r'icd\s*code',
            r'diagnostic'
        ]
        
        for pattern in diagnosis_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        
        return False
    
    def _detect_procedures(self, text: str) -> bool:
        """Detect if document contains procedure information"""
        procedure_patterns = [
            r'procedure',
            r'surgery',
            r'operation',
            r'treatment',
            r'therapy',
            r'intervention',
            r'cpt\s*code'
        ]
        
        for pattern in procedure_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        
        return False
    
    def _identify_sections(self, text: str) -> List[str]:
        """Identify document sections"""
        sections = []
        
        section_patterns = {
            'chief_complaint': r'chief\s*complaint',
            'history': r'history\s*of\s*present\s*illness',
            'physical_exam': r'physical\s*examination',
            'assessment': r'assessment\s*and\s*plan',
            'plan': r'plan',
            'medications': r'medications?',
            'allergies': r'allergies?',
            'vital_signs': r'vital\s*signs?',
            'lab_results': r'lab\s*results?',
            'imaging': r'imaging|radiology'
        }
        
        for section_name, pattern in section_patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                sections.append(section_name)
        
        return sections
    
    def _assess_urgency(self, text: str) -> str:
        """Assess document urgency level"""
        urgent_keywords = [
            'emergency', 'urgent', 'critical', 'acute', 'severe',
            'immediate', 'stat', 'asap', 'life-threatening'
        ]
        
        moderate_keywords = [
            'moderate', 'mild', 'stable', 'routine', 'follow-up'
        ]
        
        urgent_count = sum(1 for keyword in urgent_keywords if keyword in text.lower())
        moderate_count = sum(1 for keyword in moderate_keywords if keyword in text.lower())
        
        if urgent_count > 0:
            return 'high'
        elif moderate_count > 0:
            return 'moderate'
        else:
            return 'low'
    
    def _fallback_classification(self, text: str) -> Dict[str, Any]:
        """Fallback classification using rule-based approach"""
        logger.warning("Using fallback document classification")
        
        # Simple rule-based classification
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['prescription', 'medication', 'drug', 'pharmacy']):
            doc_type = 'prescription'
            confidence = 0.7
        elif any(word in text_lower for word in ['lab', 'laboratory', 'test', 'result']):
            doc_type = 'lab_result'
            confidence = 0.7
        elif any(word in text_lower for word in ['x-ray', 'ct', 'mri', 'ultrasound', 'imaging']):
            doc_type = 'imaging_report'
            confidence = 0.7
        elif any(word in text_lower for word in ['discharge', 'summary', 'hospital']):
            doc_type = 'discharge_summary'
            confidence = 0.7
        elif any(word in text_lower for word in ['visit', 'appointment', 'consultation']):
            doc_type = 'visit_note'
            confidence = 0.6
        else:
            doc_type = 'general_medical'
            confidence = 0.5
        
        return {
            'primary_class': doc_type,
            'confidence': confidence,
            'all_classes': [{'label': doc_type, 'score': confidence}],
            'additional_analysis': self._analyze_document_content(text)
        }
    
    def get_classification_confidence(self, classification: Dict[str, Any]) -> float:
        """Get overall confidence in classification"""
        return classification.get('confidence', 0.0)
    
    def is_high_confidence(self, classification: Dict[str, Any], threshold: float = 0.8) -> bool:
        """Check if classification is high confidence"""
        return self.get_classification_confidence(classification) >= threshold
