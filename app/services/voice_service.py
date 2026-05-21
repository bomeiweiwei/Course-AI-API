# app/services/voice_service.py

import os
import uuid
import subprocess
from fastapi import UploadFile, HTTPException
from app.core.config import get_settings
import google.generativeai as genai

TEMP_DIR = "/tmp/voice"


async def get_voice_text(file: UploadFile):
    os.makedirs(TEMP_DIR, exist_ok=True)

    settings = get_settings()
    genai.configure(api_key=settings.gemini_api_key)

    file_id = str(uuid.uuid4())
    # 這裡保留原檔名後綴，讓 Gemini 更好辨識檔案類型（前端傳入 "audio.wav"）
    extension = file.filename.split(".")[-1] if file.filename else "wav"
    input_path = f"{TEMP_DIR}/{file_id}.{extension}"

    try:
        # 1. 讀取前端傳入的 bytes
        content = await file.read()
        
        if len(content) < 2000:
            return {"transcript": "（音訊資料過短）"}

        # 2. 暫存檔案（Gemini API 上傳本地檔案時需要實體路徑或透過 Files API）
        with open(input_path, "wb") as f:
            f.write(content)

        # 3. 使用 Gemini Files API 上傳音訊檔案
        # 註：Gemini 1.5 支援直接傳入音訊檔案進行多模態推理
        audio_file = genai.upload_file(path=input_path)

        # 4. 初始化 Gemini 模型並進行語音辨識
        # 轉錄語音使用速度快且便宜的 gemini-1.5-flash 效果就非常卓越
        model = genai.GenerativeModel(settings.gemini_model_name)
        
        prompt = "請將這段語音檔案精準轉換為逐字稿，使用繁體中文（台灣），並自動加上標點符號。如果裡面沒有人說話或無法辨識，請直接回傳「（未偵測到語音）」，不要輸出其他多餘的解釋。"
        
        response = model.generate_content([prompt, audio_file])
        
        result_data = response.text.strip() if response.text else "（未偵測到語音）"
        print("Gemini result_data:", result_data)

        # 5. 清理 Gemini 雲端的暫存檔案（良好的檔案管理習慣）
        audio_file.delete()

        # 取得辨識結果，維持與原本相同的回傳格式
        return {"transcript": result_data}

    except Exception as e:
        print(f"DEBUG: Error during Gemini recognition: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        # 辨識完成後刪除本地暫存檔
        if os.path.exists(input_path):
            os.remove(input_path)