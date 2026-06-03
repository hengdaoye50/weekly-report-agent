# 周报自动生成智能体

## 项目概述
基于飞书 API + 大模型的周报自动生成工具。从飞书文档/表格收集本周工作内容，通过 AI 整理、分类、润色，自动生成结构化周报并写回飞书。

## 技术栈
- Python 3.12+
- 飞书开放平台 API（文档、表格、消息）
- 大模型 API（待定）
- CLI 交互

## 目录结构
```
├── CLAUDE.md          # 项目规则
├── README.md          # 项目文档
├── requirements.txt   # Python 依赖
├── .env.example       # 环境变量模板
├── .gitignore
├── src/
│   ├── main.py        # 入口
│   ├── config.py      # 配置管理
│   ├── feishu/        # 飞书 API 集成
│   ├── agent/         # 智能体逻辑
│   └── output/        # 输出格式化
├── docs/              # 设计文档
└── tests/             # 测试
```

## 开发规范
- 代码注释用中文
- commit message 用中文，格式：`类型: 描述`（feat/fix/docs/refactor/test）
- 每次改动后验证：`python -m pytest` 或手动测试
- 密钥不进代码、不进 commit
- 大改动先在 Plan Mode 出方案

## 验证命令
```bash
# 运行测试
python -m pytest tests/

# 运行主程序
python -m src.main
```
