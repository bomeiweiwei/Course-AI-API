from app.prompts.prompt_type import PromptType
from app.services.textbook_service import get_textbook_knowledge


def build_prompt(
    data: dict
) -> tuple[str, str]:
        form = data["filters"]
        course = data["course"]

        textbook_knowledge = get_textbook_knowledge(
            course["subject_name"],
            course["version_name"]
        )
        
        system_prompt = "你是專業但不誇張的教育課程推薦顧問。"
        user_prompt = f'''
你是一位線上課程推薦顧問，使用對家長友善、清楚、可信任的語氣。

請根據以下資料，產生一段推薦原因。
限制：
1. 使用繁體中文
2. 60字以內
3. 不要條列
4. 不要誇大
5. 重點放在「為什麼適合這位學生」

家長篩選條件：
- 預算：{form["budget"]} 元
- 學制 ：{form["school_name"]}
- 年級 ：{form["grade_name"]}
- 科目 ：{form["subject_name"]}
- 版本 ：{form.get("version_name", "無")}
- 程度 ：{form.get("degree_name", "無")}
- 目標 ：{form.get("goal_name", "無")}

課程資料：
- 課程名稱：{course["course_name"]}
- 學制：{course["school_name"]}
- 年級：{course["grade_name"]}
- 科目：{course["subject_name"]}
- 版本：{course["version_name"]}
- 程度：{course["degree_name"]}
- 目標：{course["goal_name"]}
- 價格：{course["price"]} 元
- 評價：{course["rating"]}
- 報名人數：{course["students"]}

教材補充資訊：
{textbook_knowledge}

請直接輸出推薦原因，不要加標題。
'''
        return system_prompt, user_prompt