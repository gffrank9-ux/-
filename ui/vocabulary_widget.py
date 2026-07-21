"""
词汇练习界面
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QRadioButton, QButtonGroup, QProgressBar, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import logging

logger = logging.getLogger(__name__)

class VocabularyWidget(QWidget):
    """词汇练习模块"""
    
    def __init__(self):
        super().__init__()
        self.current_question = 0
        self.score = 0
        self.init_ui()
        
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout()
        
        # 标题
        title = QLabel('📝 語彙練習 (Vocabulary Practice)')
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # 进度条
        self.progress = QProgressBar()
        self.progress.setValue(25)
        layout.addWidget(self.progress)
        
        # 题目
        self.question_label = QLabel('問題1: 「失礼」という言葉の意味は？')
        question_font = QFont()
        question_font.setPointSize(14)
        self.question_label.setFont(question_font)
        layout.addWidget(self.question_label)
        
        # 选项
        self.button_group = QButtonGroup()
        options = [
            'A) 礼儀に反する態度',
            'B) 丁寧な態度',
            'C) 素直な態度',
            'D) 真摯な態度'
        ]
        
        for i, option in enumerate(options):
            radio = QRadioButton(option)
            self.button_group.addButton(radio, i)
            layout.addWidget(radio)
        
        # 按钮
        btn_layout = QHBoxLayout()
        submit_btn = QPushButton('✓ 答案を提出')
        submit_btn.clicked.connect(self.submit_answer)
        next_btn = QPushButton('→ 次の問題')
        next_btn.clicked.connect(self.next_question)
        
        btn_layout.addWidget(submit_btn)
        btn_layout.addWidget(next_btn)
        layout.addLayout(btn_layout)
        
        layout.addStretch()
        
        # 结果显示
        self.result_label = QLabel('')
        result_font = QFont()
        result_font.setPointSize(12)
        result_font.setBold(True)
        self.result_label.setFont(result_font)
        layout.addWidget(self.result_label)
        
        self.setLayout(layout)
    
    def submit_answer(self):
        """提交答案"""
        checked_id = self.button_group.checkedId()
        if checked_id == -1:
            QMessageBox.warning(self, '警告', '答案を選択してください')
            return
        
        if checked_id == 0:  # 正确答案是A
            self.result_label.setText('✓ 正解です！')
            self.result_label.setStyleSheet("color: green;")
            self.score += 1
        else:
            self.result_label.setText('✗ 不正解です。正解: A) 礼儀に反する態度')
            self.result_label.setStyleSheet("color: red;")
    
    def next_question(self):
        """下一题"""
        self.current_question += 1
        self.result_label.setText('')
        self.button_group.setExclusive(False)
        for button in self.button_group.buttons():
            button.setChecked(False)
        self.button_group.setExclusive(True)
        self.progress.setValue(min(100, (self.current_question + 1) * 25))
