from app.knowledge.textbook_knowledge import TEXTBOOK_KNOWLEDGE


def get_textbook_knowledge(
    subject_name: str,
    version_name: str
) -> str:

    return TEXTBOOK_KNOWLEDGE.get(
        (subject_name, version_name),
        "目前無教材補充資訊。"
    )