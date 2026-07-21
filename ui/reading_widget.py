"""
阅读理解界面
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton
from PyQt5.QtGui import QFont
import logging

logger = logging.getLogger(__name__)

class ReadingWidget(QWidget):
    """阅读理解模块"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout()
        
        title = QLabel('📚 読解練習 (Reading Practice)')
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # 文章内容
        article_label = QLabel('記事 (Article)')
        layout.addWidget(article_label)
        
        article = QTextEdit()
        article.setReadOnly(True)
        article.setText('''\nある企業の人事部長は、新入社員の教育プログラムについて話していた。\n「今年度のプログラムは、従来の方法とは異なり、より実践的な内容を重視しています。\n学生たちが実際の仕事の場面で必要とされるスキルを身につけることが目的です。」\n\nこのプログラムの目的は何ですか？\n        ''')
        layout.addWidget(article)
        
        # 问题选项
        question = QLabel('問題: このプログラムの目的は何ですか？')
        layout.addWidget(question)
        
        options = [
            'A) 新入社員の数を増やすこと',
            'B) 実際の仕事に必要なスキルを教えること',
            'C) 従来の教育方法を続けること',
            'D) 学生の興味を調べること'
        ]
        
        for option in options:
            btn = QPushButton(option)
            layout.addWidget(btn)
        
        layout.addStretch()
        self.setLayout(layout)
