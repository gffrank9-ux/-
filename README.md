# 日語N2訓練ソフト (Japanese N2 Trainer)

一个功能完整的日语N2级别考试训练桌面应用，帮助学习者高效备考。

## 🎯 功能特性

- 📝 **词汇练习** — N2级词汇选择题、填空、发音
- 📖 **语法练习** — 系统的语法讲解与练习题
- 👂 **听力练习** — 带音频的听力理解题
- 📚 **阅读理解** — 短文阅读与问题匹配
- 📊 **模拟考试** — 完整的N2模拟考试
- 📈 **学习统计** — 进度追踪与成绩分析
- 💾 **本地数据库** — SQLite本地存储，离线使用
- 🔄 **自动更新系统** — 自动检查并下载最新试卷

## 📂 项目结构

```
Japanese-N2-Trainer/
├── main.py                    # 应用程序入口
├── requirements.txt           # 依赖包列表
├── config/
│   └── settings.py           # 配置文件
├── data/
│   ├── exam_papers_sample.json
│   ├── exam_data.db          # SQLite数据库
│   ├── cache/                # 缓存目录
│   └── backup/               # 备份目录
├── ui/
│   ├── main_window.py        # 主窗口
│   ├── vocabulary_widget.py  # 词汇练习界面
│   ├── grammar_widget.py     # 语法练习界面
│   ├── listening_widget.py   # 听力练习界面
│   ├── reading_widget.py     # 阅读理解界面
│   ├── exam_widget.py        # 模拟考试界面
│   ├── stats_widget.py       # 统计分析界面
│   └── update_widget.py      # 更新管理界面
├── core/
│   ├── update_manager.py     # 更新管理器
│   ├── exam_data_manager.py  # 试卷数据管理
│   └── utils.py              # 工具函数
└── resources/
    ├── styles.qss            # 样式文件
    └── audio/                # 音频文件存储
```

## 🚀 快速开始

### 系统要求
- Python 3.8+
- PyQt5
- SQLite3
- requests

### 安装步骤

```bash
# 克隆项目
git clone https://github.com/gffrank9-ux/Japanese-N2-Trainer.git
cd Japanese-N2-Trainer

# 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 运行应用
python main.py
```

## 📖 使用指南

### 1. 启动应用
```bash
python main.py
```

### 2. 主菜单导航
- **词汇练习** - 练习N2级别词汇
- **语法练习** - 学习和练习语法知识
- **听力练习** - 通过音频进行听力训练
- **阅读理解** - 进行阅读理解练习
- **模拟考试** - 进行完整的N2模拟考试
- **学习统计** - 查看学习进度和成绩分析
- **更新管理** - 检查和安装最新试卷

### 3. 自动更新
应用会自动检查最新的试卷和学习资料，你也可以在"更新管理"页面手动检查更新。

## 🔄 自动更新系统

### 系统架构
- **UpdateManager** - 通用更新管理器
- **ExamDataManager** - 试卷数据管理
- **后台线程** - 自动检查更新和试卷同步

### 功能特性
✓ 自动检测更新（每24小时）
✓ 断点续传支持
✓ SHA256文件完整性验证
✓ 自动备份旧版本
✓ 更新失败自动回滚
✓ 完整的更新日志
✓ 版本管理

## 📊 数据库结构

### exam_papers 表
- exam_id - 试卷ID
- title - 试卷标题
- type - 试卷类型（full_exam, vocabulary等）
- version - 版本号
- release_date - 发布日期
- total_questions - 题目总数
- duration_minutes - 考试时间

### questions 表
- exam_id - 关联的试卷ID
- question_number - 题号
- question_text - 题目文本
- options - 选项（JSON格式）
- correct_answer - 正确答案
- explanation - 解释说明

### user_exam_records 表
- exam_id - 试卷ID
- user_id - 用户ID
- score - 用户得分
- answers - 用户答案（JSON格式）
- created_at - 考试时间

## 🔧 配置

编辑 `config/settings.py` 配置以下内容：

```python
# 更新服务器地址
UPDATE_CONFIG = {
    "remote_server": "https://api.n2trainer.example.com",
    "auto_check_interval": 24,  # 24小时检查一次
    "timeout": 30,
}

# 学习目标
LEARNING_CONFIG = {
    "daily_target_minutes": 60,
    "review_intervals": [1, 3, 7, 14, 30],
    "pass_score": 60,
}
```

## 🌐 API 集成

### 远程服务器要求

你的更新服务器需要实现以下端点：

```
GET /api/version/{category}
  返回: {"version": "1.0.1"}

GET /api/download/{category}/{version}
  返回: 二进制文件 + X-Content-Hash 头

GET /api/exams
  返回: {"exams": [...]}
```

## 📝 示例数据

查看 `data/exam_papers_sample.json` 了解数据格式。

## 🛠️ 开发指南

### 添加新的练习模块

1. 在 `ui/` 中创建新的Widget文件
2. 继承 `QWidget`
3. 在 `main_window.py` 中注册新模块

### 扩展数据库

编辑 `core/exam_data_manager.py` 中的 `init_database()` 方法。

## 📚 学习资源

- [PyQt5 官方文档](https://www.riverbankcomputing.com/software/pyqt/)
- [SQLite3 教程](https://docs.python.org/3/library/sqlite3.html)
- [日语N2考试信息](https://www.jlpt.jp/)

## 🐛 问题报告

如果遇到问题，请：
1. 检查日志文件（`logs/app.log`）
2. 提交 Issue 并附上错误信息
3. 包含你的系统信息和Python版本

## 📄 许可证

MIT License - 详见 LICENSE 文件

## 🤝 贡献

欢迎提交 Pull Request 或 Issue！

## 📞 联系方式

- GitHub Issues: [项目问题](https://github.com/gffrank9-ux/-/issues)

---

**最后更新**: 2024年7月21日
**当前版本**: 1.0.0
