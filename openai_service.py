import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_post(topic: str) -> dict:
    prompt = f"""
    주제: {topic}

    아래 조건을 반드시 따라 JSON 형식으로만 답변해. 절대 다른 설명이나 불필요한 텍스트는 넣지 마.

    {{
    "title": "SEO 친화적이고 독자가 클릭하고 싶게 만드는 제목 (70자 이내)",
    "content": "본문 (5000~6000자 분량, 반드시 마크다운 형식)\\n\\n"
                "# 도입부\\n"
                "- 독자의 관심을 끌고 주제를 명확히 소개\\n\\n"
                "## 본문\\n"
                "- 3~5개 소제목(H2)을 사용\\n"
                "- 각 소제목 하위에는 구체적인 설명과 예시 포함\\n"
                "- 필요 시 **리스트**나 `코드 블록`을 활용하여 가독성 강화\\n\\n"
                "## 결론\\n"
                "- 핵심 요약 후 질문형으로 마무리하여 독자의 참여(댓글 유도)를 유도\\n\\n"
                "- 문단은 3~5문장 단위로 끊어 가독성 강화",
    "tags": [
        "SEO 키워드 기반 태그 10개 (주제와 직접 관련된 핵심 키워드)"
    ]
    }}
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    content_raw = response.choices[0].message.content.strip()

    # JSON 파싱 안전 처리
    try:
        # 코드블록 제거
        if content_raw.startswith("```"):
            content_raw = content_raw.strip("`").strip()
            if content_raw.startswith("json"):
                content_raw = content_raw[len("json"):].strip()
        content_json = json.loads(content_raw)
    except json.JSONDecodeError:
        # fallback: 그냥 dict로 감싸 반환
        return {
            "title": f"{topic} - 블로그 분석",
            "content": content_raw,
            "tags": []
        }

    return {
        "title": content_json.get("title", f"{topic} - 블로그 분석"),
        "content": content_json.get("content", ""),
        "tags": content_json.get("tags", [])
    }