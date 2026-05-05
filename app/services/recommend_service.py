from app.schemas.recommend import RecommendRequest
from app.services.course_service import filter_courses, get_all_courses


def calculate_score(course: dict, request: RecommendRequest) -> float:
    score = 0

    # 基礎品質分數
    score += course["rating"] * 20

    # 報名人數加分，上限 20
    score += min(course["students"] / 100, 20)

    # 版本符合
    if request.version_id is not None and course["version_id"] == request.version_id:
        score += 10

    # 程度符合
    if request.degree_id is not None and course["degree_id"] == request.degree_id:
        score += 15

    # 目標符合
    if request.goal_id is not None and course["goal_id"] == request.goal_id:
        score += 15

    # 偏好符合，多個偏好可累加
    if request.preference_ids:
        matched_preferences = set(request.preference_ids) & set(course["preferences"])
        score += len(matched_preferences) * 8

    # 價格加分：價格越低加一點分
    if course["price"] <= 1500:
        score += 8
    elif course["price"] <= 2500:
        score += 4

    return round(score, 1)

def build_reason(course: dict, request: RecommendRequest) -> str:
    reasons = []

    reasons.append(f"評價 {course['rating']} 分")
    reasons.append(f"已有 {course['students']:,} 人報名")

    if request.version_id is not None and course["version_id"] == request.version_id:
        reasons.append(f"符合版本：{course['version_name']}")

    if request.degree_id is not None and course["degree_id"] == request.degree_id:
        reasons.append(f"符合程度：{course['degree_name']}")

    if request.goal_id is not None and course["goal_id"] == request.goal_id:
        reasons.append(f"符合目標：{course['goal_name']}")

    if request.preference_ids:
        matched_preferences = set(request.preference_ids) & set(course["preferences"])
        if matched_preferences:
            reasons.append(f"符合 {len(matched_preferences)} 個學習偏好")

    if course["price"] <= 1500:
        reasons.append("價格相對低")
    elif course["price"] <= 2500:
        reasons.append("價格中等")

    return "、".join(reasons)

def recommend_courses(request: RecommendRequest) -> list[dict]:
    courses = get_all_courses()

    # 只用基本條件做第一層過濾
    filtered_courses = filter_courses(
        courses=courses,
        school_id=request.school_id,
        grade_id=request.grade_id,
        subject_id=request.subject_id,
    )

    results = []

    for course in filtered_courses:
        item = course.copy()
        item["score"] = calculate_score(course, request)
        item["reason"] = build_reason(course, request)
        results.append(item)

    sorted_results = sorted(
        results,
        key=lambda x: x["score"],
        reverse=True
    )

    return sorted_results[:request.limit]