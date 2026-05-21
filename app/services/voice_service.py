import os
import uuid
from fastapi import UploadFile, HTTPException
from google import genai
from app.core.config import get_settings

TEMP_DIR = "/tmp/voice"


async def get_voice_text(file: UploadFile):
    os.makedirs(TEMP_DIR, exist_ok=True)

    settings = get_settings()

    # 新版 Client
    client = genai.Client(api_key=settings.gemini_api_key)

    file_id = str(uuid.uuid4())

    extension = file.filename.split(".")[-1] if file.filename else "wav"

    input_path = f"{TEMP_DIR}/{file_id}.{extension}"

    try:
        # 1. 讀取音訊 bytes
        content = await file.read()

        if len(content) < 2000:
            return {"transcript": "（音訊資料過短）"}

        # 2. 寫入暫存檔
        with open(input_path, "wb") as f:
            f.write(content)

        # 3. 上傳檔案
        uploaded_file = client.files.upload(
            file=input_path
        )

        prompt = """
請將這段語音檔案精準轉換為逐字稿，
使用繁體中文（台灣），並自動加上標點符號。

如果裡面沒有人說話或無法辨識，
請直接回傳「（未偵測到語音）」，
不要輸出其他解釋。
"""

        # 4. Gemini 語音辨識
        response = client.models.generate_content(
            model=settings.gemini_model_name,
            contents=[
                prompt,
                uploaded_file
            ]
        )

        result_data = (
            response.text.strip()
            if response.text
            else "（未偵測到語音）"
        )

        print("Gemini result_data:", result_data)

        # 5. 刪除 Gemini Files API 暫存檔
        client.files.delete(
            name=uploaded_file.name
        )

        return {
            "transcript": result_data
        }

    except Exception as e:
        print(f"DEBUG: Error during Gemini recognition: {e}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:
        # 刪除本地暫存
        if os.path.exists(input_path):
            os.remove(input_path)