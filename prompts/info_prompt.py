# prompts/info_prompt.py
def get_prompt(topic, summarized_context):
    return f"""
    주제: {topic}
    참고 요약:
    {summarized_context}

    넌 일상 속 유익한 정보를 대화체로 풀어 쓰는 블로거야.
    출력은 JSON 형식만 사용해.

    {{
    "title": "SEO 친화적이고 독자가 클릭하고 싶게 만드는 제목 (70자 이내)",
    "content": "마크다운 형식으로 3000자 이상 글 작성.\\n
                - 최소 4개 이상의 소제목(H2) 사용\\n
                - 각 소제목마다 구체적 설명, 사례, 비교 포함\\n
                - 본문은 2~4문장 단위 문단으로 나누고 리스트·표 활용 가능\\n
                - 마지막은 간단히 요약 후 질문형으로 마무리\\n
                - SEO 키워드 6~10회 자연스럽게 반복",
    "tags": [
        "주제와 직접 관련된 SEO 키워드 15개"
    ]
    }}
    """