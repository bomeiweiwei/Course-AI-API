# app/services/voice_service.py

import os
import uuid
import subprocess
from fastapi import UploadFile, HTTPException
from google.cloud import speech

TEMP_DIR = "/tmp/voice"


async def get_voice_text(file: UploadFile):
    os.makedirs(TEMP_DIR, exist_ok=True)

    file_id = str(uuid.uuid4())
    input_path = f"{TEMP_DIR}/{file_id}_input"
    output_path = f"{TEMP_DIR}/{file_id}_output.wav"
    try:

        # 1. 初始化 Client
        client = speech.SpeechClient()
        # print('client ok', type(client))

        # 2. 讀取檔案
        content = await file.read()
        # print(f"DEBUG: Received content size: {len(content)} bytes")
        if len(content) < 2000:
            return {"transcript": "（音訊資料過短）"}
        # 2-1. 先把手機/電腦上傳的原始音檔暫存
        with open(input_path, "wb") as f:
            f.write(content)
        # 2-2. 用 ffmpeg 統一轉成 WAV / LINEAR16 / 16000Hz / mono
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                input_path,
                "-ac",
                "1",
                "-ar",
                "16000",
                "-f",
                "wav",
                output_path,
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        with open(output_path, "rb") as f:
            audio_content = f.read()
        if len(audio_content) < 2000:
            return {"transcript": "（轉檔後音訊資料過短）"}

        audio = speech.RecognitionAudio(content=audio_content)

        # 3. 根據錄音格式設定 Config
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            audio_channel_count=1,
            language_code="zh-TW",
            max_alternatives=1,
            enable_automatic_punctuation=True,
        )

        response = client.recognize(config=config, audio=audio)
        # 務必檢查 response.results 是否存在，否則存取 [0] 會報 500 錯誤
        if not response.results:
            return {"transcript": "（未偵測到語音）"}
        result_data = response.results[0].alternatives[0].transcript
        print("result_data", result_data)
        # 取得辨識結果
        return {"transcript": result_data}

    except subprocess.CalledProcessError:
        raise HTTPException(
            status_code=400, detail="音訊轉檔失敗，請確認上傳的是有效音訊檔"
        )

    except Exception as e:
        print(f"DEBUG: Error during recognition: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        # 辨識完成後刪除暫存檔
        for path in [input_path, output_path]:
            if os.path.exists(path):
                os.remove(path)