from app.schemas.recommend import RecommendRequest
from app.services.course_service import filter_courses


def calculate_score(course: dict, request: RecommendRequest) -> float:
    score = 0

    score += course["rating"] * 20
    score += min(course["students"] / 100, 20)

    if request.version_name and course.get("version_name") == request.version_name:
        score += 10

    if request.degree_name and course.get("degree_name") == request.degree_name:
        score += 10

    if request.goal_name and course.get("goal_name") == request.goal_name:
        score += 10

    return round(score, 1)


def build_reason(course: dict, request: RecommendRequest) -> str:
    reasons = []

    reasons.append(f"評價 {course['rating']} 分")
    reasons.append(f"已有 {course['students']:,} 人報名")

    if request.version_name and course.get("version_name") == request.version_name:
        reasons.append(f"符合版本：{request.version_name}")

    if request.degree_name and course.get("degree_name") == request.degree_name:
        reasons.append(f"符合程度：{request.degree_name}")

    if request.goal_name and course.get("goal_name") == request.goal_name:
        reasons.append(f"符合目標：{request.goal_name}")

    return "、".join(reasons)


def recommend_courses(request: RecommendRequest):
    courses = filter_courses(
        school_name=request.school_name,
        grade_name=request.grade_name,
        subject_name=request.subject_name
    )

    results = []

    for course in courses:
        item = course.copy()
        item["score"] = calculate_score(course, request)
        item["reason"] = build_reason(course, request)
        results.append(item)

    return sorted(results, key=lambda x: x["score"], reverse=True)