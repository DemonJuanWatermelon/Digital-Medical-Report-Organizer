from transformers import pipeline
import json
from typing import Dict, Any, Optional

class AIService:
    def __init__(self):
        # Initialize medical NER pipeline
        self.ner_pipeline = pipeline(
            "ner",
            model="emergentmedical/emergent-medical-ner",
            aggregation_strategy="simple"
        )
        
        # Initialize text classification for medical reports
        self.classifier = pipeline(
            "text-classification",
            model="emergentmedical/emergent-medical-classification"
        )
    
    async def extract_medical_data(self, ocr_text: str) -> Dict[str, Any]:
        """
        Extract structured medical data from OCR text using AI
        """
        try:
            # Extract named entities
            entities = self.ner_pipeline(ocr_text)
            
            # Classify the document type
            classification = self.classifier(ocr_text)
            
            # Structure the extracted data
            structured_data = {
                "document_type": classification[0]["label"] if classification else "unknown",
                "confidence": classification[0]["score"] if classification else 0.0,
                "entities": {
                    "medications": [],
                    "conditions": [],
                    "procedures": [],
                    "dates": [],
                    "measurements": [],
                    "other": []
                },
                "raw_entities": entities
            }
            
            # Categorize entities
            for entity in entities:
                entity_type = entity["entity_group"].lower()
                if entity_type in ["drug", "medication"]:
                    structured_data["entities"]["medications"].append({
                        "text": entity["word"],
                        "confidence": entity["score"]
                    })
                elif entity_type in ["condition", "disease", "symptom"]:
                    structured_data["entities"]["conditions"].append({
                        "text": entity["word"],
                        "confidence": entity["score"]
                    })
                elif entity_type in ["procedure", "treatment"]:
                    structured_data["entities"]["procedures"].append({
                        "text": entity["word"],
                        "confidence": entity["score"]
                    })
                elif entity_type in ["date", "time"]:
                    structured_data["entities"]["dates"].append({
                        "text": entity["word"],
                        "confidence": entity["score"]
                    })
                elif entity_type in ["measurement", "value"]:
                    structured_data["entities"]["measurements"].append({
                        "text": entity["word"],
                        "confidence": entity["score"]
                    })
                else:
                    structured_data["entities"]["other"].append({
                        "text": entity["word"],
                        "confidence": entity["score"]
                    })
            
            return structured_data
            
        except Exception as e:
            print(f"AI Processing Error: {str(e)}")
            return {
                "document_type": "unknown",
                "confidence": 0.0,
                "entities": {
                    "medications": [],
                    "conditions": [],
                    "procedures": [],
                    "dates": [],
                    "measurements": [],
                    "other": []
                },
                "raw_entities": [],
                "error": str(e)
            }
    
    async def analyze_report(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform additional AI analysis on extracted medical data
        """
        try:
            analysis = {
                "summary": "",
                "key_findings": [],
                "recommendations": [],
                "risk_level": "low",
                "follow_up_required": False
            }
            
            # Analyze conditions
            conditions = extracted_data.get("entities", {}).get("conditions", [])
            if conditions:
                analysis["key_findings"].extend([
                    f"Identified condition: {cond['text']}" 
                    for cond in conditions if cond['confidence'] > 0.7
                ])
            
            # Analyze medications
            medications = extracted_data.get("entities", {}).get("medications", [])
            if medications:
                analysis["key_findings"].extend([
                    f"Prescribed medication: {med['text']}" 
                    for med in medications if med['confidence'] > 0.7
                ])
            
            # Generate summary
            if analysis["key_findings"]:
                analysis["summary"] = f"Report contains {len(analysis['key_findings'])} key findings including conditions and medications."
            else:
                analysis["summary"] = "No significant medical findings detected in the report."
            
            # Determine risk level based on conditions
            high_risk_conditions = ["cancer", "diabetes", "heart", "stroke", "emergency"]
            for condition in conditions:
                if any(risk_word in condition["text"].lower() for risk_word in high_risk_conditions):
                    analysis["risk_level"] = "high"
                    analysis["follow_up_required"] = True
                    break
            
            return analysis
            
        except Exception as e:
            print(f"AI Analysis Error: {str(e)}")
            return {
                "summary": "Analysis failed due to processing error",
                "key_findings": [],
                "recommendations": [],
                "risk_level": "unknown",
                "follow_up_required": False,
                "error": str(e)
            }
