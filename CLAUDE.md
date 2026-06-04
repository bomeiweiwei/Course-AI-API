# CLAUDE.md

此檔案提供 Claude Code (claude.ai/code) 在此專案中的操作指引。

## 指令

**安裝相依套件：**
```bash
pip install -r requirements.txt
```

**啟動開發伺服器：**
```bash
uvicorn app.main:app --reload
```
API 位址：http://127.0.0.1:8000，Swagger UI：http://127.0.0.1:8000/docs

**Docker 建置與執行：**
```bash
docker build -t course-api:latest .

# 使用 Gemini：
docker run --rm -p 8000:8080 -e PORT=8080 -e AI_PROVIDER=gemini -e GEMINI_API_KEY=YOUR-KEY course-api

# 使用 LM Studio：
docker run --rm -p 8000:8080 -e PORT=8080 -e AI_PROVIDER=lmstudio -e LMSTUDIO_BASE_URL=http://host.docker.internal:1234/v1 course-api
```

目前尚未設定測試或程式碼檢查工具。

## 架構

本專案為線上課程智能推薦顧問的 FastAPI 後端，資料以 JSON 檔案提供（無資料庫）。

### 請求流程

```
Router → Service → (AI Layer | Data Layer)
```

- **路由層** (`app/routers/`)：輕薄的 HTTP 處理器，委派邏輯至 Service
- **服務層** (`app/services/`)：核心業務邏輯——篩選、評分、AI 協調
- **AI 層** (`app/ai/`)：基於 LangChain 的抽象層，支援 Gemini 與 LM Studio
- **資料層** (`app/data/`)：`courses.json`（課程目錄）與 `options.json`（下拉選單的階層式後設資料）

### 推薦流程

1. 從 `courses.json` 依 `school_id`、`grade_id`、`subject_id`（必填）及可選的 `version_id`、`degree_id`、`goal_id` 篩選課程
2. 對每門課程評分：評分×10 + 報名人數加分（0–20）+ 預算匹配（0–20）+ 偏好吻合（每項 0–5）
3. 回傳前 N 筆結果（預設 3 筆，最多 10 筆），附帶 `reason` 說明字串
4. 可選擇呼叫 `POST /api/ai/course/recommendation` 透過 AI 產生自然語言推薦說明

### AI 供應商抽象層

`app/ai/factory.py` 依 `AI_PROVIDER` 環境變數建立 AI 客戶端：
- `gemini` → `GeminiClient`（透過 LangChain 封裝 `ChatGoogleGenerativeAI`）
- `lmstudio` → `LmStudioClient`（透過 LangChain 封裝 `ChatOpenAI`，指向本機 LM Studio 端點）

兩者皆實作 `BaseAILangchain` 介面，提供 `invoke()` 與 `chat()` 方法。

語音轉文字（`app/services/voice_service.py`）直接使用 `google-genai` SDK（非 LangChain），將音訊上傳至 Gemini Files API 並轉錄為繁體中文。

### 提示詞

`app/prompts/recommend_prompt_builder.py` 為 AI 推薦說明建構結構化提示詞。`app/knowledge/textbook_knowledge.py` 提供精選的教科書描述，透過 `app/services/textbook_service.py` 注入至提示詞中。

## 環境變數

將 `.env.example` 複製為 `.env`。主要變數如下：

| 變數 | 預設值 | 說明 |
|---|---|---|
| `AI_PROVIDER` | `lmstudio` | `gemini` 或 `lmstudio` |
| `GEMINI_API_KEY` | — | 使用 Gemini 時必填 |
| `GEMINI_MODEL_NAME` | `gemini-1.5-flash` | Gemini 模型 ID |
| `LMSTUDIO_BASE_URL` | `http://localhost:1234/v1` | LM Studio OpenAI 相容端點 |
| `LMSTUDIO_MODEL_NAME` | `local-model` | LM Studio 中顯示的模型名稱 |

設定透過 `app/core/config.py` 中的 Pydantic Settings 載入，並使用 LRU 快取（`get_settings()`）。

## 部署

目標部署平台為 GCP Cloud Run。`PORT` 環境變數控制 uvicorn 埠號（Docker 中預設為 8080）。`feature/cloud` 分支包含進行中的雲端基礎設施工作；`develop` 為主要整合分支。
