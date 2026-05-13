from fastapi import APIRouter, UploadFile, File
from app.services.voice_service import get_voice_text

router = APIRouter()

@router.post("/voice_to_text")
async def voice_to_text(file: UploadFile = File(...)):
    # print(type(file))
    # 務必加上 await
    return await get_voice_text(file)