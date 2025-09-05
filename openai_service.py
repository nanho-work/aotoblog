import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from search_service import search_and_summarize
from prompts import dev_prompt, info_prompt

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_post(topic: str, style: str = "dev") -> dict:
    summarized_context = search_and_summarize(topic)

    if style == "dev":
        prompt = dev_prompt.get_prompt(topic, summarized_context)
    elif style == "info":
        prompt = info_prompt.get_prompt(topic, summarized_context)
    else:
        raise ValueError(f"Unknown style: {style}")

    model_name = "gpt-4o"

    response = client.chat.completions.create(
        model=model_name,
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

    
def summarize_text(text: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": f"다음 내용을 간결하게 요약해줘:\n\n{text}"}
        ]
    )
    return response.choices[0].message.content.strip()