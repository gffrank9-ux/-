"""
工具函数
"""
import logging
from pathlib import Path
from config.settings import LOGGING_CONFIG
from logging.handlers import RotatingFileHandler


def setup_logging():
    """
    设置日志系统
    """
    logger = logging.getLogger()
    logger.setLevel(LOGGING_CONFIG["level"])
    
    # 创建日志目录
    log_dir = LOGGING_CONFIG["log_file"].parent
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # 文件处理器
    file_handler = RotatingFileHandler(
        LOGGING_CONFIG["log_file"],
        maxBytes=LOGGING_CONFIG["max_bytes"],
        backupCount=LOGGING_CONFIG["backup_count"]
    )
    file_handler.setLevel(logging.DEBUG)
    
    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # 格式化器
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # 添加处理器
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


def format_time(seconds: int) -> str:
    """
    格式化秒数为分:秒格式
    
    Args:
        seconds: 秒数
        
    Returns:
        格式化后的时间字符串
    """
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes:02d}:{secs:02d}"


def calculate_percentage(current: float, total: float) -> float:
    """
    计算百分比
    
    Args:
        current: 当前值
        total: 总值
        
    Returns:
        百分比
    """
    if total == 0:
        return 0
    return (current / total) * 100


def parse_version(version_str: str) -> tuple:
    """
    解析版本号
    
    Args:
        version_str: 版本号字符串（如 "1.0.0"）
        
    Returns:
        版本号元组
    """
    try:
        return tuple(map(int, version_str.split('.')))
    except (ValueError, AttributeError):
        return (0, 0, 0)


def compare_versions(v1: str, v2: str) -> int:
    """
    比较两个版本号
    
    Args:
        v1: 版本1
        v2: 版本2
        
    Returns:
        1 if v1 > v2, -1 if v1 < v2, 0 if v1 == v2
    """
    ver1 = parse_version(v1)
    ver2 = parse_version(v2)
    
    if ver1 > ver2:
        return 1
    elif ver1 < ver2:
        return -1
    else:
        return 0
