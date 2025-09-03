# aotoblog

## 설치 및 실행 방법

### 1. 레포지토리 클론
```bash
git clone https://github.com/사용자명/aotoblog.git
cd aotoblog
```

### 2. 가상환경 생성 및 활성화 (권장)
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. 필수 패키지 설치
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

> `requirements.txt` 파일이 없다면, 주요 패키지는 수동으로 설치해야 합니다:
```bash
pip install openai selenium python-dotenv webdriver-manager
```

### 4. 환경 변수 설정
`.env` 파일을 프로젝트 루트에 생성 후 아래 항목 입력:
```
OPENAI_API_KEY=sk-xxxxxxx
TISTORY_ID=your_tistory_id
TISTORY_PW=your_tistory_password
```

### 5. 실행
```bash
python main.py
```

## 블로그 라이트 설정

`post_to_tistory` 함수에서 블로그 주소(`itstory05.tistory.com`) 부분을 본인 블로그 주소로 수정해야 합니다.  
예를 들어, 아래와 같이 변경합니다:

```python
driver.get("https://본인블로그주소.tistory.com/manage/newpost")
```

---

👉 추가로, 실행 파일(.app) 생성하려면 `pyinstaller`를 설치 후 패키징:
```bash
pip install pyinstaller
pyinstaller --onedir --windowed --name "TistoryAutoBlog" --icon=MyIcon.icns main.py
```
생성된 실행 파일은 `dist/TistoryAutoBlog.app` 에서 확인 가능.