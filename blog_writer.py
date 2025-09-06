import os, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
from selenium.webdriver.common.alert import Alert

load_dotenv()

TISTORY_ID = os.getenv("TISTORY_ID")   # 카카오 계정 (이메일 or 전화번호)
TISTORY_PW = os.getenv("TISTORY_PW")   # 카카오 비밀번호

def post_to_tistory(title, content, tags="", blog_url="itstory05"):
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument('user-data-dir="/Users/choenamho/Library/Application Support/Google/Chrome"')
    options.add_argument('profile-directory=Default')  # 평소 쓰는 기본 프로필
    driver = webdriver.Chrome(service=service, options=options)

    # 티스토리 로그인 페이지 접속
    driver.get("https://www.tistory.com/auth/login")
    time.sleep(2)

    # ✅ 카카오 로그인 버튼 클릭
    kakao_btn = driver.find_element(By.CSS_SELECTOR, "a.btn_login.link_kakao_id")  # 노란색 버튼
    kakao_btn.click()

    time.sleep(3)

    # ✅ 카카오 로그인 창에서 ID/PW 입력
    driver.find_element(By.ID, "loginId--1").send_keys(TISTORY_ID)
    driver.find_element(By.ID, "password--2").send_keys(TISTORY_PW)

    # ✅ 로그인 버튼 클릭
    driver.find_element(By.CSS_SELECTOR, "button.btn_g.highlight.submit").click()

    time.sleep(3)

    # ✅ 글쓰기 페이지로 이동
    driver.get(f"https://{blog_url}.tistory.com/manage/newpost")
    time.sleep(3)

    # 에디터 모드 드롭다운 클릭 후 '마크다운' 선택
    driver.find_element(By.ID, "editor-mode-layer-btn-open").click()
    driver.find_element(By.ID, "editor-mode-markdown").click()
    # ✅ confirm 팝업 '확인' 클릭
    alert = Alert(driver)
    alert.accept()
    time.sleep(2)

    # 제목 입력
    driver.find_element(By.ID, "post-title-inp").send_keys(title)

    # 본문 입력 (Markdown mode: CodeMirror)
    
    driver.execute_script("""
        const cm = document.querySelector('.CodeMirror.cm-s-tistory-markdown').CodeMirror;
        cm.refresh();
        cm.focus();
        cm.save();
        // ✅ 강제로 입력 이벤트 발생시켜 저장 반영
        const textarea = document.querySelector('.CodeMirror.cm-s-tistory-markdown textarea');
        textarea.value = arguments[0];
        textarea.dispatchEvent(new Event('input', { bubbles: true }));
        textarea.dispatchEvent(new Event('change', { bubbles: true }));
    """, content)

    # 태그 입력 (사용자 전달)
    if tags:
        driver.find_element(By.ID, "tagText").send_keys(tags)

    # 완료 버튼 클릭 → 발행 설정 레이어 열림
    driver.find_element(By.ID, "publish-layer-btn").click()
    time.sleep(2)

    # 공개 선택
    driver.find_element(By.ID, "open20").click()

    # 발행 버튼 클릭
    driver.find_element(By.ID, "publish-btn").click()

    time.sleep(5)
   # driver.quit()

#if __name__ == "__main__":
#    title = "자동화 테스트 제목"
#    content = "이 글은 OpenAI API를 사용하지 않고, 브라우저 자동화를 테스트하기 위한 더미 본문입니다."
#    tags = "테스트,자동화,브라우저"
#    post_to_tistory(title, content, tags)