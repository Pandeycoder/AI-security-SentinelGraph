from fastapi import APIRouter, Depends
from api.requests.scan_request import WebsiteScanRequest
from api.dependencies.use_cases import get_scan_website_uc
from application.use_cases.scan_website import ScanWebsiteUseCase

router = APIRouter()

@router.post("/website")
async def scan_website(
    request: WebsiteScanRequest,
    use_case: ScanWebsiteUseCase = Depends(get_scan_website_uc),
):
    return await use_case.execute(request.url)
