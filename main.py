"""
应用程序入口
"""
import sys
import logging
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer

from config.settings import APP_NAME, APP_VERSION
from core.utils import setup_logging

# 设置日志
logger = setup_logging()
logger.info("="*50)
logger.info(f"{APP_NAME} v{APP_VERSION} 启动")
logger.info("="*50)

def main():
    """
    主函数
    """
    try:
        # 创建应用
        app = QApplication(sys.argv)
        
        # 延迟导入UI（避免循环导入）
        from ui.main_window import MainWindow
        from core.exam_data_manager import ExamDataManager
        
        # 初始化数据管理器
        exam_manager = ExamDataManager()
        
        # 创建主窗口
        window = MainWindow(exam_manager)
        window.show()
        
        logger.info("应用启动成功")
        
        # 运行应用
        sys.exit(app.exec_())
        
    except Exception as e:
        logger.error(f"应用启动失败: {e}", exc_info=True)
        sys.exit(1)

if __name__ == '__main__':
    main()
