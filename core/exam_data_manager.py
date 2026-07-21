"""
试卷数据管理器 - 专门处理考试试卷的下载和管理
"""
import json
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional
import logging

from core.update_manager import UpdateManager

logger = logging.getLogger(__name__)

class ExamDataManager:
    """管理N2考试试卷数据"""
    
    # 数据库路径
    DB_PATH = Path("data/exam_data.db")
    
    # 试卷类型
    EXAM_TYPES = {
        "vocabulary": "語彙",
        "grammar": "文法",
        "listening": "聴解",
        "reading": "読解",
        "full_exam": "完全模擬試験"
    }
    
    def __init__(self):
        """初始化试卷数据管理器"""
        self.update_manager = UpdateManager()
        self.db_path = self.DB_PATH
        self.init_database()
    
    def init_database(self):
        """初始化数据库"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # 创建试卷表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS exam_papers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    exam_id TEXT UNIQUE NOT NULL,
                    title TEXT NOT NULL,
                    type TEXT NOT NULL,
                    version TEXT NOT NULL,
                    release_date TEXT,
                    difficulty TEXT,
                    total_questions INTEGER,
                    duration_minutes INTEGER,
                    description TEXT,
                    file_path TEXT,
                    downloaded_at TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # 创建问题表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS questions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    exam_id TEXT NOT NULL,
                    question_number INTEGER NOT NULL,
                    question_text TEXT NOT NULL,
                    question_type TEXT,
                    options TEXT,
                    correct_answer TEXT,
                    explanation TEXT,
                    audio_url TEXT,
                    image_url TEXT,
                    FOREIGN KEY (exam_id) REFERENCES exam_papers(exam_id)
                )
            ''')
            
            # 创建用户试卷记录表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_exam_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    exam_id TEXT NOT NULL,
                    user_id TEXT,
                    start_time TIMESTAMP,
                    end_time TIMESTAMP,
                    score REAL,
                    total_score REAL,
                    answers TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (exam_id) REFERENCES exam_papers(exam_id)
                )
            ''')
            
            # 创建索引
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_exam_type ON exam_papers(type)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_exam_id ON questions(exam_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_exam ON user_exam_records(user_id, exam_id)')
            
            conn.commit()
            logger.info("数据库初始化完成")
    
    def get_available_exams(self, exam_type: Optional[str] = None, limit: int = 20) -> List[Dict]:
        """获取可用的试卷列表
        
        Args:
            exam_type: 试卷类型筛选
            limit: 返回的数量限制
            
        Returns:
            试卷列表
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            if exam_type:
                cursor.execute('''
                    SELECT * FROM exam_papers 
                    WHERE type = ? 
                    ORDER BY release_date DESC 
                    LIMIT ?
                ''', (exam_type, limit))
            else:
                cursor.execute('''
                    SELECT * FROM exam_papers 
                    ORDER BY release_date DESC 
                    LIMIT ?
                ''', (limit,))
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def get_exam_detail(self, exam_id: str) -> Optional[Dict]:
        """获取试卷详情
        
        Args:
            exam_id: 试卷ID
            
        Returns:
            试卷详情
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM exam_papers WHERE exam_id = ?', (exam_id,))
            exam = cursor.fetchone()
            
            if not exam:
                return None
            
            # 获取问题列表
            cursor.execute('''
                SELECT * FROM questions 
                WHERE exam_id = ? 
                ORDER BY question_number
            ''', (exam_id,))
            questions = cursor.fetchall()
            
            result = dict(exam)
            result['questions'] = [dict(q) for q in questions]
            
            return result
    
    def import_exam_data(self, exam_id: str, exam_data: Dict) -> bool:
        """导入试卷数据
        
        Args:
            exam_id: 试卷ID
            exam_data: 试卷数据字典
            
        Returns:
            是否成功导入
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # 插入或更新试卷信息
                cursor.execute('''
                    INSERT OR REPLACE INTO exam_papers
                    (exam_id, title, type, version, release_date, difficulty, 
                     total_questions, duration_minutes, description, downloaded_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    exam_id,
                    exam_data.get('title', ''),
                    exam_data.get('type', ''),
                    exam_data.get('version', ''),
                    exam_data.get('release_date', ''),
                    exam_data.get('difficulty', ''),
                    exam_data.get('total_questions', 0),
                    exam_data.get('duration_minutes', 0),
                    exam_data.get('description', ''),
                    datetime.now().isoformat()
                ))
                
                # 删除旧的问题数据
                cursor.execute('DELETE FROM questions WHERE exam_id = ?', (exam_id,))
                
                # 插入新的问题数据
                for idx, question in enumerate(exam_data.get('questions', []), 1):
                    cursor.execute('''
                        INSERT INTO questions
                        (exam_id, question_number, question_text, question_type,
                         options, correct_answer, explanation, audio_url, image_url)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        exam_id,
                        idx,
                        question.get('text', ''),
                        question.get('type', ''),
                        json.dumps(question.get('options', [])),
                        question.get('correct_answer', ''),
                        question.get('explanation', ''),
                        question.get('audio_url', ''),
                        question.get('image_url', '')
                    ))
                
                conn.commit()
                logger.info(f"成功导入试卷数据: {exam_id}")
                return True
                
        except Exception as e:
            logger.error(f"导入试卷数据失败: {e}")
            return False
    
    def save_user_exam_record(self, exam_id: str, user_id: str, 
                              answers: Dict, score: float, total_score: float) -> bool:
        """保存用户的考试记录
        
        Args:
            exam_id: 试卷ID
            user_id: 用户ID
            answers: 用户答案字典
            score: 用户得分
            total_score: 满分
            
        Returns:
            是否成功保存
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO user_exam_records
                    (exam_id, user_id, start_time, end_time, score, total_score, answers)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    exam_id,
                    user_id,
                    datetime.now().isoformat(),
                    datetime.now().isoformat(),
                    score,
                    total_score,
                    json.dumps(answers)
                ))
                conn.commit()
                logger.info(f"已保存用户考试记录: {exam_id}")
                return True
        except Exception as e:
            logger.error(f"保存考试记录失败: {e}")
            return False
    
    def get_user_exam_history(self, user_id: str, limit: int = 20) -> List[Dict]:
        """获取用户的考试历史
        
        Args:
            user_id: 用户ID
            limit: 返回数量
            
        Returns:
            考试历史列表
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT r.*, p.title, p.type 
                FROM user_exam_records r
                JOIN exam_papers p ON r.exam_id = p.exam_id
                WHERE r.user_id = ?
                ORDER BY r.created_at DESC
                LIMIT ?
            ''', (user_id, limit))
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def get_statistics(self, user_id: str) -> Dict:
        """获取用户的统计数据
        
        Args:
            user_id: 用户ID
            
        Returns:
            统计数据字典
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # 总考试次数
            cursor.execute('SELECT COUNT(*) as count FROM user_exam_records WHERE user_id = ?', (user_id,))
            total_exams = cursor.fetchone()[0]
            
            # 平均得分
            cursor.execute('''
                SELECT AVG(score/total_score*100) as avg_score 
                FROM user_exam_records 
                WHERE user_id = ?
            ''', (user_id,))
            avg_score = cursor.fetchone()[0] or 0
            
            # 最高得分
            cursor.execute('''
                SELECT MAX(score/total_score*100) as max_score 
                FROM user_exam_records 
                WHERE user_id = ?
            ''', (user_id,))
            max_score = cursor.fetchone()[0] or 0
            
            # 按类型统计
            cursor.execute('''
                SELECT p.type, AVG(r.score/r.total_score*100) as avg_score, COUNT(*) as count
                FROM user_exam_records r
                JOIN exam_papers p ON r.exam_id = p.exam_id
                WHERE r.user_id = ?
                GROUP BY p.type
            ''', (user_id,))
            
            by_type = {}
            for row in cursor.fetchall():
                by_type[row[0]] = {"avg_score": row[1], "count": row[2]}
            
            return {
                "total_exams": total_exams,
                "average_score": round(avg_score, 2),
                "max_score": round(max_score, 2),
                "by_type": by_type
            }
    
    def auto_sync_exams(self, interval_hours: int = 24):
        """自动同步最新试卷
        
        Args:
            interval_hours: 同步间隔（��时）
        """
        def sync_loop():
            while True:
                try:
                    logger.info("开始同步最新试卷...")
                    
                    # 检查并下载最新试卷
                    updates = self.update_manager.check_updates(["exam_papers"])
                    
                    if "exam_papers" in updates:
                        version = updates["exam_papers"]
                        if self.update_manager.download_update("exam_papers", version):
                            if self.update_manager.install_update("exam_papers", version):
                                # 加载新试卷数据
                                self.load_exam_data_from_file()
                                logger.info(f"✓ 试卷已更新到 v{version}")
                    
                    import time
                    time.sleep(interval_hours * 3600)
                    
                except Exception as e:
                    logger.error(f"同步试卷出错: {e}")
                    import time
                    time.sleep(300)
        
        import threading
        sync_thread = threading.Thread(target=sync_loop, daemon=True)
        sync_thread.start()
        logger.info("试卷自动同步线程已启动")
    
    def load_exam_data_from_file(self, file_path: str = "data/exam_papers.json"):
        """从JSON文件加载试卷数据
        
        Args:
            file_path: JSON文件路径
        """
        try:
            if not Path(file_path).exists():
                logger.warning(f"试卷数据文件不存在: {file_path}")
                return
            
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for exam in data.get('exams', []):
                self.import_exam_data(exam['exam_id'], exam)
            
            logger.info(f"成功从文件加载试卷数据: {file_path}")
            
        except Exception as e:
            logger.error(f"加载试卷数据失败: {e}")
