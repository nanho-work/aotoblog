import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
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

        self.generate_btn_dev = QPushButton("개발 블로그 글 생성", self)
        self.generate_btn_info = QPushButton("정보 블로그 글 생성", self)
        self.upload_btn = QPushButton("개발새발 업로드", self)
        self.upload_btn2 = QPushButton("FunFactLab 업로드", self)

        self.result_box = QTextEdit(self)
        self.result_box.setPlaceholderText("생성된 글이 여기에 표시됩니다.")

        self.status_label = QLabel("상태: 대기중", self)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.topic_input)
        generate_btn_layout = QHBoxLayout()
        generate_btn_layout.addWidget(self.generate_btn_dev)
        generate_btn_layout.addWidget(self.generate_btn_info)
        layout.addLayout(generate_btn_layout)
        layout.addWidget(self.result_box)
        upload_btn_layout = QHBoxLayout()
        upload_btn_layout.addWidget(self.upload_btn)
        upload_btn_layout.addWidget(self.upload_btn2)
        layout.addLayout(upload_btn_layout)
        layout.addWidget(self.status_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Event connections
        self.generate_btn_dev.clicked.connect(lambda: self.generate_post(style="dev"))
        self.generate_btn_info.clicked.connect(lambda: self.generate_post(style="info"))
        self.upload_btn.clicked.connect(self.upload_post)
        self.upload_btn2.clicked.connect(self.upload_post_funfactlab)

        # Internal state
        self.generated = None

    def generate_post(self, style="dev"):
        topic = self.topic_input.text().strip()
        if not topic:
            self.status_label.setText("상태: 주제를 입력하세요")
            return

        self.status_label.setText("상태: 글 생성중...")
        self.generated = generate_post(topic, style=style)

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
            post_to_tistory(self.generated['title'], self.generated['content'], tags, blog_url="itstory05")
            self.status_label.setText("업로드 완료")
        except Exception as e:
            self.status_label.setText(f"업로드 실패: {str(e)}")

    def upload_post_funfactlab(self):
        if not self.generated:
            self.status_label.setText("상태: 먼저 글을 생성하세요")
            return

        self.status_label.setText("상태: FunFactLab에 업로드중...")
        try:
            tags = ",".join(self.generated.get("tags", []))
            post_to_tistory(self.generated['title'], self.generated['content'], tags, blog_url="funfactlab")
            self.status_label.setText("업로드 완료")
        except Exception as e:
            self.status_label.setText(f"업로드 실패: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BlogAutoWindow()
    window.show()
    sys.exit(app.exec())