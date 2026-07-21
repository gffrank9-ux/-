"""
应用配置文件
"""
import os
from pathlib import Path

# 应用基本信息
APP_NAME = "日語N2訓練ソフト"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Japanese N2 Trainer Team"

# 数据目录
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
CACHE_DIR = DATA_DIR / "cache"
BACKUP_DIR = DATA_DIR / "backup"
LOG_DIR = BASE_DIR / "logs"

# 确保目录存在
for directory in [DATA_DIR, CACHE_DIR, BACKUP_DIR, LOG_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# 更新配置
UPDATE_CONFIG = {
    # 远程服务器地址
    "remote_server": os.getenv("N2_UPDATE_SERVER", "https://api.n2trainer.example.com"),
    
    # 自动检查更新（小时）
    "auto_check_interval": 24,
    
    # 自动同步试卷（小时）
    "auto_sync_interval": 24,
    
    # 连接超时（秒）
    "timeout": 30,
    
    # 重试次数
    "max_retries": 3,
}

# 数据库配置
DATABASE_CONFIG = {
    "path": DATA_DIR / "exam_data.db",
    "user_db_path": DATA_DIR / "user_data.db",
}

# UI配置
UI_CONFIG = {
    "window_width": 1200,
    "window_height": 800,
    "theme": "light",
    "font_size": 12,
}

# 日志配置
LOGGING_CONFIG = {
    "level": "INFO",
    "log_file": LOG_DIR / "app.log",
    "max_bytes": 10485760,
    "backup_count": 5,
}

# 学习配置
LEARNING_CONFIG = {
    "daily_target_minutes": 60,
    "review_intervals": [1, 3, 7, 14, 30],
    "pass_score": 60,
}

# 试卷配置
EXAM_CONFIG = {
    "types": {
        "vocabulary": "語彙",
        "grammar": "文法",
        "listening": "聴解",
        "reading": "読解",
        "full_exam": "完全模擬試験"
    },
    "time_limits": {
        "vocabulary": 25,
        "grammar": 25,
        "listening": 30,
        "reading": 45,
        "full_exam": 170,
    },
    "max_scores": {
        "vocabulary": 180,
        "grammar": 180,
        "listening": 120,
        "reading": 160,
        "full_exam": 400,
    },
}

# API端点配置
API_ENDPOINTS = {
    "check_version": "/api/version/{category}",
    "download_data": "/api/download/{category}/{version}",
    "get_exams": "/api/exams",
    "submit_exam": "/api/submit-exam",
}
