"""
学習統計界面
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QTableWidget,
                             QTableWidgetItem, QProgressBar, QGridLayout)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import logging

logger = logging.getLogger(__name__)

class StatsWidget(QWidget):
    """学習統計模块"""
    
    def __init__(self, exam_manager):
        super().__init__()
        self.exam_manager = exam_manager
        self.init_ui()
        
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout()
        
        # 标题
        title = QLabel('📊 学習統計 (Statistics)')
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # 概括統計
        summary_layout = QGridLayout()
        
        stats_info = [
            ('総学習時間', '45時間'),
            ('完了問題数', '1,250問'),
            ('正解率', '78%'),
            ('現在のレベル', 'N2中級'),
        ]
        
        for i, (label, value) in enumerate(stats_info):
            key_label = QLabel(label + ':')
            key_label.setFont(QFont('Arial', 11, QFont.Bold))
            val_label = QLabel(value)
            val_label.setFont(QFont('Arial', 11))
            summary_layout.addWidget(key_label, i // 2, (i % 2) * 2)
            summary_layout.addWidget(val_label, i // 2, (i % 2) * 2 + 1)
        
        layout.addLayout(summary_layout)
        
        # 最近7日间的学習
        weekly_label = QLabel('最近の7日間の学習:')
        weekly_label.setFont(QFont('Arial', 12, QFont.Bold))
        layout.addWidget(weekly_label)
        
        daily_stats = [
            ('月', '2時間', 40),
            ('火', '1.5時間', 30),
            ('水', '3時間', 60),
            ('木', '2.5時間', 50),
            ('金', '4時間', 80),
            ('土', '3時間', 60),
            ('日', '2時間', 40),
        ]
        
        for day, time, progress in daily_stats:
            day_layout = QGridLayout()
            day_label = QLabel(day)
            day_label.setFont(QFont('Arial', 10, QFont.Bold))
            day_layout.addWidget(day_label, 0, 0)
            
            time_label = QLabel(time)
            day_layout.addWidget(time_label, 0, 1)
            
            progress_bar = QProgressBar()
            progress_bar.setValue(progress)
            day_layout.addWidget(progress_bar, 0, 2)
            
            layout.addLayout(day_layout)
        
        # 成績表
        grade_label = QLabel('溝別成績:')
        grade_label.setFont(QFont('Arial', 12, QFont.Bold))
        layout.addWidget(grade_label)
        
        table = QTableWidget(5, 3)
        table.setHorizontalHeaderLabels(['分類', '完了', '正解率'])
        table.setMaximumHeight(200)
        
        data = [
            ['語彙', '300問', '82%'],
            ['文法', '250問', '75%'],
            ['聴解', '200問', '70%'],
            ['読解', '300問', '80%'],
            ['模拟試験', '4回', '77%']
        ]
        
        for i, row in enumerate(data):
            for j, val in enumerate(row):
                table.setItem(i, j, QTableWidgetItem(val))
        
        layout.addWidget(table)
        layout.addStretch()
        self.setLayout(layout)
