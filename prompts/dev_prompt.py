# prompts/dev_prompt.py
def get_prompt(topic, summarized_context):
    return f"""
주제: {topic}
참고 요약: {summarized_context}
ㄱ
조건:
- JSON 형식으로만 출력 (불필요한 설명 금지)
- 본문은 반드시 3000자 이상, 마크다운 형식
- 제목은 70자 이내, SEO 친화적이고 클릭을 유도할 것
- 본문은 H1 제목(# )으로 시작, 3~5개 H2 소제목 포함
- 결론은 요약 + 질문형 문장으로 마무리
- 친근한 존댓말, 실용 사례 중심, SEO 키워드 3~5회 자연스럽게 반복

출력 예시:
{{
"title": "제목",
"content": "마크다운 본문 (3000자 이상)",
"tags": ["관련 키워드 10개"]
}}
"""