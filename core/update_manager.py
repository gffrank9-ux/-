"""
试卷自动更新管理器
"""
import os
import json
import hashlib
import requests
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
import threading
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UpdateManager:
    """管理试卷和学习资料的自动更新"""
    
    # 云端更新服务器地址（可配置）
    REMOTE_SERVER = "https://api.n2trainer.example.com"
    
    # 本地数据目录
    DATA_DIR = Path("data")
    CACHE_DIR = Path("data/cache")
    BACKUP_DIR = Path("data/backup")
    
    # 版本文件
    VERSION_FILE = "versions.json"
    
    def __init__(self):
        """初始化更新管理器"""
        self.ensure_directories()
        self.versions = self.load_versions()
        self.is_checking = False
        
    def ensure_directories(self):
        """确保所有必要的目录存在"""
        for directory in [self.DATA_DIR, self.CACHE_DIR, self.BACKUP_DIR]:
            directory.mkdir(parents=True, exist_ok=True)
    
    def load_versions(self) -> Dict:
        """加载本地版本信息"""
        version_path = self.DATA_DIR / self.VERSION_FILE
        if version_path.exists():
            with open(version_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return self.get_default_versions()
    
    def get_default_versions(self) -> Dict:
        """获取默认版本配置"""
        return {
            "vocabulary": {"version": "1.0.0", "last_update": None, "hash": None},
            "grammar": {"version": "1.0.0", "last_update": None, "hash": None},
            "listening": {"version": "1.0.0", "last_update": None, "hash": None},
            "reading": {"version": "1.0.0", "last_update": None, "hash": None},
            "exam_papers": {"version": "1.0.0", "last_update": None, "hash": None},
        }
    
    def save_versions(self):
        """保存版本信息到本地"""
        version_path = self.DATA_DIR / self.VERSION_FILE
        with open(version_path, 'w', encoding='utf-8') as f:
            json.dump(self.versions, f, indent=2, ensure_ascii=False)
    
    def check_updates(self, categories: Optional[List[str]] = None) -> Dict:
        """检查是否有更新可用
        
        Args:
            categories: 要检查的类别，None表示检查全部
            
        Returns:
            更新信息字典
        """
        if self.is_checking:
            logger.warning("已有更新检查正在进行中")
            return {}
        
        self.is_checking = True
        try:
            if categories is None:
                categories = list(self.versions.keys())
            
            updates_available = {}
            
            for category in categories:
                try:
                    remote_version = self.get_remote_version(category)
                    if remote_version:
                        local_version = self.versions.get(category, {}).get("version", "0.0.0")
                        if self.compare_versions(remote_version, local_version) > 0:
                            updates_available[category] = remote_version
                            logger.info(f"发现 {category} 的新版本: {remote_version}")
                except Exception as e:
                    logger.error(f"检查 {category} 更新时出错: {e}")
            
            return updates_available
        finally:
            self.is_checking = False
    
    def get_remote_version(self, category: str) -> Optional[str]:
        """从远程服务器获取指定类别的版本号
        
        Args:
            category: 数据类别（vocabulary, grammar等）
            
        Returns:
            版本号字符串
        """
        try:
            url = f"{self.REMOTE_SERVER}/api/version/{category}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            return data.get("version")
        except requests.RequestException as e:
            logger.error(f"获取远程版本失败: {e}")
            return None
    
    @staticmethod
    def compare_versions(v1: str, v2: str) -> int:
        """比较两个版本号
        
        Args:
            v1: 版本1
            v2: 版本2
            
        Returns:
            1 if v1 > v2, -1 if v1 < v2, 0 if v1 == v2
        """
        def parse_version(v):
            return tuple(map(int, v.split('.')))
        
        try:
            ver1 = parse_version(v1)
            ver2 = parse_version(v2)
            
            if ver1 > ver2:
                return 1
            elif ver1 < ver2:
                return -1
            else:
                return 0
        except Exception as e:
            logger.error(f"版本比较失败: {e}")
            return 0
    
    def download_update(self, category: str, version: str) -> bool:
        """下载指定类别的更新数据
        
        Args:
            category: 数据类别
            version: 目标版本号
            
        Returns:
            是否成功下载
        """
        try:
            url = f"{self.REMOTE_SERVER}/api/download/{category}/{version}"
            logger.info(f"开始下载 {category} v{version}...")
            
            response = requests.get(url, timeout=30, stream=True)
            response.raise_for_status()
            
            # 保存到临时文件
            temp_file = self.CACHE_DIR / f"{category}_{version}.json.tmp"
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(temp_file, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        progress = (downloaded / total_size * 100) if total_size else 0
                        logger.info(f"下载进度: {progress:.1f}%")
            
            # 验证哈希值
            remote_hash = response.headers.get('X-Content-Hash')
            if remote_hash and not self.verify_hash(temp_file, remote_hash):
                logger.error("文件哈希验证失败，下载的文件可能已损坏")
                temp_file.unlink()
                return False
            
            logger.info(f"成功下载 {category} v{version}")
            return True
            
        except Exception as e:
            logger.error(f"下载更新失败: {e}")
            return False
    
    def verify_hash(self, file_path: Path, expected_hash: str) -> bool:
        """验证文件的哈希值
        
        Args:
            file_path: 文件路径
            expected_hash: 期望的哈希值
            
        Returns:
            是否匹配
        """
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        
        return sha256_hash.hexdigest() == expected_hash
    
    def install_update(self, category: str, version: str) -> bool:
        """安装下载的更新
        
        Args:
            category: 数据类别
            version: 版本号
            
        Returns:
            是否成功安装
        """
        try:
            source_file = self.CACHE_DIR / f"{category}_{version}.json.tmp"
            target_file = self.DATA_DIR / f"{category}.json"
            backup_file = self.BACKUP_DIR / f"{category}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            if not source_file.exists():
                logger.error(f"更新文件不存在: {source_file}")
                return False
            
            # 备份旧文件
            if target_file.exists():
                target_file.rename(backup_file)
                logger.info(f"已备份旧文件: {backup_file}")
            
            # 移动新文件
            source_file.rename(target_file)
            
            # 更新版本信息
            self.versions[category] = {
                "version": version,
                "last_update": datetime.now().isoformat(),
                "hash": self.calculate_hash(target_file)
            }
            self.save_versions()
            
            logger.info(f"成功安装 {category} v{version}")
            return True
            
        except Exception as e:
            logger.error(f"安装更新失败: {e}")
            return False
    
    @staticmethod
    def calculate_hash(file_path: Path) -> str:
        """计算文件的SHA256哈希值"""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    
    def auto_update(self, interval_hours: int = 24):
        """自动更新线程
        
        Args:
            interval_hours: 检查更新的间隔时间（小时）
        """
        def update_loop():
            while True:
                try:
                    logger.info("开始检查更新...")
                    updates = self.check_updates()
                    
                    for category, version in updates.items():
                        if self.download_update(category, version):
                            if self.install_update(category, version):
                                logger.info(f"✓ {category} 已更新到 v{version}")
                            else:
                                logger.error(f"✗ 安装 {category} 更新失败")
                    
                    # 等待指定时间后再次检查
                    import time
                    time.sleep(interval_hours * 3600)
                    
                except Exception as e:
                    logger.error(f"自动更新出错: {e}")
                    import time
                    time.sleep(300)  # 出错后等待5分钟
        
        # 启动后台线程
        update_thread = threading.Thread(target=update_loop, daemon=True)
        update_thread.start()
        logger.info("自动更新线程已启动")
    
    def get_update_status(self) -> Dict:
        """获取当前的更新状态
        
        Returns:
            状态信息字典
        """
        status = {}
        for category, info in self.versions.items():
            status[category] = {
                "version": info.get("version", "unknown"),
                "last_update": info.get("last_update", "never"),
                "checking": self.is_checking
            }
        return status
