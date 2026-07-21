"""
模拟考试界面
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QProgressBar, QMessageBox, QComboBox)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer, Qt
import logging

logger = logging.getLogger(__name__)

class ExamWidget(QWidget):
    """模拟考试模块"""
    
    def __init__(self, exam_manager):
        super().__init__()
        self.exam_manager = exam_manager
        self.time_remaining = 0
        self.is_exam_running = False
        self.init_ui()
        
    def init_ui(self):
        """��始化UI"""
        layout = QVBoxLayout()
        
        # 标题
        title = QLabel('📋 完全模拟試験 (Full Exam)')
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # 试卷选择
        exam_layout = QHBoxLayout()
        exam_layout.addWidget(QLabel('試卷選択:'))
        
        self.exam_combo = QComboBox()
        self.exam_combo.addItem('最新のN2模拟試験')
        self.exam_combo.addItem('2024年7月 N2')
        self.exam_combo.addItem('2024年12月 N2')
        exam_layout.addWidget(self.exam_combo)
        layout.addLayout(exam_layout)
        
        # 考试信息
        info_label = QLabel('''
試験時間: 170分
総問題数: 170問
満点: 400点
程度: N2
        ''')
        layout.addWidget(info_label)
        
        # 试验说明
        notice_label = QLabel('注意事項:')
        notice_label.setFont(QFont('Arial', 11, QFont.Bold))
        layout.addWidget(notice_label)
        
        notice_text = QLabel('''
• 「開始」をクリックすると試験が始まり、時間が計時されます
• 一度始まったら、戻ることを推奨しません
• 時間内に��了して下さい
        ''')
        layout.addWidget(notice_text)
        
        # 试验状态
        status_layout = QHBoxLayout()
        status_layout.addWidget(QLabel('状態:'))
        self.status_label = QLabel('未開始')
        self.status_label.setFont(QFont('Arial', 12, QFont.Bold))
        status_layout.addWidget(self.status_label)
        status_layout.addStretch()
        layout.addLayout(status_layout)
        
        # 时间表示
        timer_layout = QHBoxLayout()
        timer_layout.addWidget(QLabel('残り時間:'))
        self.timer_label = QLabel('00:00')
        self.timer_label.setFont(QFont('Arial', 24, QFont.Bold))
        self.timer_label.setStyleSheet('color: green;')
        timer_layout.addWidget(self.timer_label)
        timer_layout.addStretch()
        layout.addLayout(timer_layout)
        
        # 进度条
        self.progress = QProgressBar()
        self.progress.setMaximum(170)
        layout.addWidget(self.progress)
        
        # 按钮
        btn_layout = QHBoxLayout()
        
        self.start_btn = QPushButton('🚀 開始')
        self.start_btn.clicked.connect(self.start_exam)
        btn_layout.addWidget(self.start_btn)
        
        self.pause_btn = QPushButton('⏸ 一時停止')
        self.pause_btn.clicked.connect(self.pause_exam)
        self.pause_btn.setEnabled(False)
        btn_layout.addWidget(self.pause_btn)
        
        self.submit_btn = QPushButton('✓ 提出')
        self.submit_btn.clicked.connect(self.submit_exam)
        self.submit_btn.setEnabled(False)
        btn_layout.addWidget(self.submit_btn)
        
        layout.addLayout(btn_layout)
        layout.addStretch()
        
        # 试验纲要
        self.result_label = QLabel('')
        result_font = QFont()
        result_font.setPointSize(12)
        self.result_label.setFont(result_font)
        layout.addWidget(self.result_label)
        
        # 试验用计时器
        self.exam_timer = QTimer()
        self.exam_timer.timeout.connect(self.update_timer)
        
        self.setLayout(layout)
    
    def start_exam(self):
        """開始試験"""
        self.time_remaining = 170 * 60  # 170分
        self.is_exam_running = True
        self.start_btn.setEnabled(False)
        self.pause_btn.setEnabled(True)
        self.submit_btn.setEnabled(True)
        self.status_label.setText('作成中...')
        self.status_label.setStyleSheet('color: blue;')
        self.exam_timer.start(1000)  # 毎秒更新一回
    
    def pause_exam(self):
        """一時停止"""
        if self.is_exam_running:
            self.exam_timer.stop()
            self.is_exam_running = False
            self.pause_btn.setText('▶ 続行')
            self.status_label.setText('一時停止中...')
            self.status_label.setStyleSheet('color: orange;')
        else:
            self.exam_timer.start()
            self.is_exam_running = True
            self.pause_btn.setText('⏸ 一時停止')
            self.status_label.setText('作成中...')
            self.status_label.setStyleSheet('color: blue;')
    
    def update_timer(self):
        """更新試験計時者"""
        self.time_remaining -= 1
        minutes = self.time_remaining // 60
        seconds = self.time_remaining % 60
        self.timer_label.setText(f'{minutes:02d}:{seconds:02d}')
        
        # 時間提醒（最後10分��"""
        if self.time_remaining == 600:
            QMessageBox.warning(self, '警告', '残り時間10分です！')
            self.timer_label.setStyleSheet('color: red;')
        
        # 時間到時
        if self.time_remaining <= 0:
            self.exam_timer.stop()
            self.submit_exam()
    
    def submit_exam(self):
        """提出試験"""
        if self.is_exam_running:
            self.exam_timer.stop()
        
        score = 320  # 例梗得点
        total = 400
        percentage = (score / total) * 100
        
        self.result_label.setText(f'''
試験完了！
程度: {percentage:.1f}%
睡点: {score} / {total}
接筆値: {percentage >= 60 and '合格' or '不合格'}
        ''')
        self.result_label.setStyleSheet(
            'color: green; font-weight: bold;' if percentage >= 60 else 'color: red; font-weight: bold;'
        )
        
        self.is_exam_running = False
        self.start_btn.setEnabled(True)
        self.pause_btn.setEnabled(False)
        self.submit_btn.setEnabled(False)
        self.status_label.setText('完了')
        self.status_label.setStyleSheet('color: green;')
