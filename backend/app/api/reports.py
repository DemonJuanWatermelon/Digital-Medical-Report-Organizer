from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.report import MedicalReport
from app.models.user import User
from app.services.ocr_service import OCRService
from app.services.ai_service import AIService
from app.schemas.report import ReportCreate, ReportResponse

router = APIRouter()

@router.post("/upload", response_model=ReportResponse)
async def upload_report(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Validate file type
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    # Save file
    file_path = await save_uploaded_file(file)
    
    # Process with OCR
    ocr_service = OCRService()
    ocr_text = await ocr_service.extract_text(file_path)
    
    # Process with AI
    ai_service = AIService()
    extracted_data = await ai_service.extract_medical_data(ocr_text)
    ai_analysis = await ai_service.analyze_report(extracted_data)
    
    # Save to database
    report = MedicalReport(
        user_id=current_user.id,
        title=file.filename,
        file_path=file_path,
        file_type=file.content_type,
        ocr_text=ocr_text,
        extracted_data=extracted_data,
        ai_analysis=ai_analysis
    )
    
    db.add(report)
    db.commit()
    db.refresh(report)
    
    return report

@router.get("/", response_model=list[ReportResponse])
async def get_reports(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    reports = db.query(MedicalReport).filter(
        MedicalReport.user_id == current_user.id
    ).offset(skip).limit(limit).all()
    return reports

@router.get("/{report_id}", response_model=ReportResponse)
async def get_report(
    report_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    report = db.query(MedicalReport).filter(
        MedicalReport.id == report_id,
        MedicalReport.user_id == current_user.id
    ).first()
    
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    
    return report
