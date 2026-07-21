"""
语法练习界面
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton
from PyQt5.QtGui import QFont
import logging

logger = logging.getLogger(__name__)

class GrammarWidget(QWidget):
    """语法练习模块"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout()
        
        title = QLabel('📖 文法練習 (Grammar Practice)')
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # 语法说明
        grammar_label = QLabel('【～てはいけない】禁止用法')
        grammar_label.setFont(QFont('Arial', 12, QFont.Bold))
        layout.addWidget(grammar_label)
        
        grammar_text = QTextEdit()
        grammar_text.setReadOnly(True)
        grammar_text.setText('''\n意味：〜することは許されない、禁止されている\n\n例文：\n• ここで写真を撮ってはいけません。\n• 授業中に携帯を使ってはいけない。\n• 他人の物を勝手に触ってはいけない。\n\n【～てはいけない】と【～ない方がいい】の違い：\n• てはいけない：絶対的な禁止（ルール・法律）\n• ない方がいい：相対的な忠告（アドバイス）\n        ''')
        layout.addWidget(grammar_text)
        
        # 练习题
        exercise_label = QLabel('練習問題：以下の文を完成させてください')
        layout.addWidget(exercise_label)
        
        exercise = QTextEdit()
        exercise.setPlaceholderText('ここに答えを入力してください...')
        layout.addWidget(exercise)
        
        submit_btn = QPushButton('✓ 確認')
        submit_btn.clicked.connect(lambda: print('提交答案'))
        layout.addWidget(submit_btn)
        
        layout.addStretch()
        self.setLayout(layout)
