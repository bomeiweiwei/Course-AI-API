# app/services/voice_service.py

from fastapi import UploadFile, HTTPException
from google.cloud import speech
import io

# 在 Cloud Run 環境中，這會自動使用服務帳戶權限
# client = speech.SpeechClient()

async def get_voice_text(file: UploadFile):
    # 1. 初始化 Client
    client = speech.SpeechClient()
    # print('client ok', type(client))

    # 2. 讀取檔案
    content = await file.read()
    # print(f"DEBUG: Received content size: {len(content)} bytes")
    if len(content) < 2000:
        return {"transcript": "（音訊資料過短）"}

    audio = speech.RecognitionAudio(content=content)
    # print('audio ok', type(audio))

    # 3. 根據錄音格式設定 Config
    config = speech.RecognitionConfig(
        language_code="zh-TW",
        enable_automatic_punctuation=True,
    )

    try:
        response = client.recognize(config=config, audio=audio)
        # 務必檢查 response.results 是否存在，否則存取 [0] 會報 500 錯誤
        if not response.results:
            return {"transcript": "（未偵測到語音）"}
        result_data = response.results[0].alternatives[0].transcript
        print('result_data', result_data)
        # 取得辨識結果
        return {"transcript": result_data}

    except Exception as e:
        print(f"DEBUG: Error during recognition: {e}")
        raise HTTPException(status_code=500, detail=str(e))