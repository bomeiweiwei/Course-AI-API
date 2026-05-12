from app.schemas.recommend import RecommendRequest
from app.services.course_service import filter_courses, get_all_courses
from app.enums.sys_preference import SysPreference
from fastapi.responses import StreamingResponse
import csv
import io

def calculate_score(course: dict, request: RecommendRequest) -> float:
    score = 0

    rating = course.get("rating", 0)
    students = course.get("students", 0)
    price = course.get("price", 0)

    budget = request.budget
    preferences = request.preference_ids

    # 基礎分：評價，最核心權重
    # 4.8 星 → +48 分
    # 4.2 星 → +42 分
    score += float(rating) * 10

    # 報名人數分，很多人買有一定品質
    if students >= 1000:
        score += 20
    elif students >= 500:
        score += 15
    elif students >= 100:
        score += 10

    # 預算分，價格符合度
    if budget and price <= budget:
        score += 20
    elif budget and price <= budget * 1.2:
        score += 10

    # 偏好加權
    if SysPreference.VIDEO_SHORT.code in preferences:
        if SysPreference.VIDEO_SHORT.code in course.get("preferences", []):
            score += 5

    if SysPreference.QUESTION_MORE.code in preferences:
        if SysPreference.QUESTION_MORE.code in course.get("preferences", []):
            score += 5

    if SysPreference.TEACHER_GOOD.code in preferences:
        if SysPreference.TEACHER_GOOD.code in course.get("preferences", []):
            score += 5

    return round(score, 1)

def build_reason(course: dict, request: RecommendRequest) -> str:
    reasons = []

    rating = course.get("rating", 0)
    students = course.get("students", 0)
    price = course.get("price", 0)
    budget = request.budget

    if rating >= 4.5:
        reasons.append("評價表現良好")

    if students >= 1000:
        reasons.append("報名人數多，課程受歡迎")
    elif students >= 500:
        reasons.append("已有一定報名人數")

    if budget and price <= budget:
        reasons.append("價格符合預算")
    elif budget and price <= budget * 1.2:
        reasons.append("價格略高於預算，但仍可考慮")

    if not reasons:
        reasons.append("符合目前基本篩選條件")

    return "、".join(reasons)

def recommend_courses(request: RecommendRequest) -> list[dict]:
    courses = get_all_courses()

    # 只用基本條件做第一層過濾
    filtered_courses = filter_courses(
        courses=courses,
        school_id=request.school_id,
        grade_id=request.grade_id,
        subject_id=request.subject_id,
        version_id=request.version_id,
        degree_id=request.degree_id,
        goal_id=request.goal_id,
        # preference_ids=request.preference_ids
    )

    results = []

    for course in filtered_courses:
        item = course.copy()
        item["recommend_score"] = calculate_score(course, request)
        item["recommend_reasons"] = build_reason(course, request)
        results.append(item)

    sorted_results = sorted(
        results,
        key=lambda x: x["recommend_score"],
        reverse=True
    )

    return sorted_results[:request.limit]

def export_recommend_csv(courses):
    output = io.StringIO()

    # utf-8-sig：讓 Excel 開啟中文不亂碼
    output.write("\ufeff")

    writer = csv.writer(output)

    writer.writerow([
        "排名",
        "課程名稱",
        
        "目標",
        "價格",
        "評價",
        "報名人數",
        "推薦分數"
    ])

    for index, course in enumerate(courses, start=1):
        writer.writerow([
            index,
            course.get("course_name", ""),
            
            course.get("goal_name", ""),
            course.get("price", ""),
            course.get("rating", ""),
            course.get("students", ""),
            course.get("recommend_score", "")
        ])

    output.seek(0)

    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=recommend_courses.csv"
        }
    )