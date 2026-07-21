"""
听力练习界面
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSlider
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import logging

logger = logging.getLogger(__name__)

class ListeningWidget(QWidget):
    """听力练习模块"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout()
        
        title = QLabel('👂 聴解練習 (Listening Practice)')
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # 音频播放器
        audio_label = QLabel('🔊 オーディオ')
        layout.addWidget(audio_label)
        
        play_btn = QPushButton('▶ 再生')
        play_btn.setMaximumWidth(100)
        layout.addWidget(play_btn)
        
        slider = QSlider(Qt.Horizontal)
        slider.setMaximum(100)
        layout.addWidget(slider)
        
        # 问题
        question = QLabel('問題: このオーディオで何について話していますか？')
        layout.addWidget(question)
        
        # 选项
        options = ['A) 天気', 'B) 食べ物', 'C) 仕事', 'D) 旅行']
        for option in options:
            btn = QPushButton(option)
            layout.addWidget(btn)
        
        layout.addStretch()
        self.setLayout(layout)
