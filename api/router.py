from fastapi import APIRouter, UploadFile, File
from .service import GS1Service

router = APIRouter()
gs1_service = GS1Service()

@router.post("/GS1-128/")
async def validate_codes(file: UploadFile = File(...)):
    contents = await file.read()
    text = contents.decode("utf-8")
    
    # Primero extraemos y validamos los códigos
    results = gs1_service.extract_and_validate_codes(text)
    
    # Formateamos la respuesta
    formatted_results = {
        "total_codes": len(results),
        "results": results
    }
    
    return formatted_results
