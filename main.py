import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QLineEdit, QPushButton,
    QTextEdit, QLabel
)
from openai_service import generate_post
from blog_writer import post_to_tistory


class BlogAutoWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("티스토리 자동 블로그 툴 (PyQt + Selenium)")
        self.setGeometry(200, 200, 600, 400)

        # Widgets
        self.topic_input = QLineEdit(self)
        self.topic_input.setPlaceholderText("주제를 입력하세요")

        self.generate_btn = QPushButton("글 생성", self)
        self.upload_btn = QPushButton("티스토리에 업로드", self)

        self.result_box = QTextEdit(self)
        self.result_box.setPlaceholderText("생성된 글이 여기에 표시됩니다.")

        self.status_label = QLabel("상태: 대기중", self)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.topic_input)
        layout.addWidget(self.generate_btn)
        layout.addWidget(self.result_box)
        layout.addWidget(self.upload_btn)
        layout.addWidget(self.status_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Event connections
        self.generate_btn.clicked.connect(self.generate_post)
        self.upload_btn.clicked.connect(self.upload_post)

        # Internal state
        self.generated = None

    def generate_post(self):
        topic = self.topic_input.text().strip()
        if not topic:
            self.status_label.setText("상태: 주제를 입력하세요")
            return

        self.status_label.setText("상태: 글 생성중...")
        self.generated = generate_post(topic)

        if self.generated:
            self.result_box.setText(f"# {self.generated['title']}\n\n{self.generated['content']}")
            self.status_label.setText("상태: 글 생성 완료")

    def upload_post(self):
        if not self.generated:
            self.status_label.setText("상태: 먼저 글을 생성하세요")
            return

        self.status_label.setText("상태: 티스토리에 업로드중...")
        try:
            # tags 배열을 문자열로 변환해서 전달
            tags = ",".join(self.generated.get("tags", []))
            post_to_tistory(self.generated['title'], self.generated['content'], tags)
            self.status_label.setText("업로드 완료")
        except Exception as e:
            self.status_label.setText(f"업로드 실패: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BlogAutoWindow()
    window.show()
    sys.exit(app.exec())