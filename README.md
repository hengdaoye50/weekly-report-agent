# 周报自动生成智能体

AI 智能体设计开发及应用大作业。基于飞书 API + 大模型，自动从飞书文档/表格收集工作内容，生成结构化周报。

## 功能

- 从飞书文档/表格读取本周工作记录
- AI 自动分类、整理、润色
- 生成结构化周报（按项目/类别分组）
- 写回飞书文档或发送飞书消息通知

## 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 填入飞书和大模型的凭证

# 运行
python -m src.main
```

## 项目结构

```
├── src/
│   ├── main.py        # 入口
│   ├── config.py      # 配置管理
│   ├── feishu/        # 飞书 API 集成
│   ├── agent/         # 智能体逻辑（工作流、提示词）
│   └── output/        # 输出格式化
├── docs/              # 设计文档
└── tests/             # 测试
```
