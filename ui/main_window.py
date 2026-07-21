"""
主窗口 - 应用程序的主界面
"""
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QStackedWidget, QLabel, QMenuBar, QMenu)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon
import logging

logger = logging.getLogger(__name__)

class MainWindow(QMainWindow):
    """应用程序主窗口"""
    
    def __init__(self, exam_manager):
        """初始化主窗口
        
        Args:
            exam_manager: 试卷数据管理器
        """
        super().__init__()
        self.exam_manager = exam_manager
        self.init_ui()
        
    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle('日語N2訓練ソフト - Japanese N2 Trainer')
        self.setGeometry(100, 100, 1200, 800)
        
        # 创建主容器
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout()
        
        # ===== 左侧菜单栏 =====
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        
        # 应用标题
        title_label = QLabel('日語N2\n訓練ソフト')
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(title_label)
        
        # 分隔线
        separator = QLabel('─' * 20)
        separator.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(separator)
        
        # 菜单按钮
        buttons_info = [
            ('📝 词汇练习\nVocabulary', 0),
            ('📖 语法练习\nGrammar', 1),
            ('👂 听力练习\nListening', 2),
            ('📚 阅读理解\nReading', 3),
            ('📋 模拟考试\nExam', 4),
            ('📊 学习统计\nStatistics', 5),
            ('⬇️ 更新管理\nUpdates', 6),
        ]
        
        for btn_text, page_index in buttons_info:
            btn = QPushButton(btn_text)
            btn.setMinimumHeight(70)
            btn.setFont(QFont('Arial', 10))
            btn.clicked.connect(lambda checked, idx=page_index: self.show_page(idx))
            left_layout.addWidget(btn)
        
        left_layout.addStretch()
        left_panel.setLayout(left_layout)
        left_panel.setMaximumWidth(180)
        left_panel.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;
                border-right: 1px solid #ddd;
            }
            QPushButton {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 10px;
                text-align: center;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e8f4f8;
                border: 1px solid #0080ff;
            }
            QPushButton:pressed {
                background-color: #0080ff;
                color: white;
            }
        """)
        
        # ===== 右侧内容区域 =====
        self.stacked_widget = QStackedWidget()
        
        # 导入各个功能模块（延迟导入避免循环依赖）
        from ui.vocabulary_widget import VocabularyWidget
        from ui.grammar_widget import GrammarWidget
        from ui.listening_widget import ListeningWidget
        from ui.reading_widget import ReadingWidget
        from ui.exam_widget import ExamWidget
        from ui.stats_widget import StatsWidget
        from ui.update_widget import UpdateWidget
        
        self.stacked_widget.addWidget(VocabularyWidget())
        self.stacked_widget.addWidget(GrammarWidget())
        self.stacked_widget.addWidget(ListeningWidget())
        self.stacked_widget.addWidget(ReadingWidget())
        self.stacked_widget.addWidget(ExamWidget(self.exam_manager))
        self.stacked_widget.addWidget(StatsWidget(self.exam_manager))
        self.stacked_widget.addWidget(UpdateWidget())
        
        # 添加到主布局
        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(self.stacked_widget, 4)
        main_widget.setLayout(main_layout)
        
        logger.info("主窗口初始化完成")
    
    def show_page(self, index: int):
        """显示指定页面
        
        Args:
            index: 页面索引
        """
        self.stacked_widget.setCurrentIndex(index)
