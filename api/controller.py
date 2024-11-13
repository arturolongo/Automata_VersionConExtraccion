from .service import GS1Service

gs1_service = GS1Service()

def validate_gs1_code(code: str):
    result = gs1_service.validate_gs1_code(code) 
    return result

async def validate_and_generate_report(codes: list) -> str:
    file_path = 'report.csv' 
    gs1_service.generate_csv_report(codes, file_path)  
    return file_path  
