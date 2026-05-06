from enum import Enum


class PromptType(str, Enum):
    TEST="test"
    COURSE_QUESTION = "course_question"
    RECOMMEND_EXPLANATION = "recommend_explanation"
    GENERAL_ADVISOR = "general_advisor"