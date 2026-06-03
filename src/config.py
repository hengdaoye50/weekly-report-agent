import os
from pathlib import Path
from dotenv import load_dotenv

# 加载 .env 文件
_env_path = Path(__file__).parent.parent / ".env"
load_dotenv(_env_path)


# ── 飞书配置 ──
FEISHU_APP_ID = os.getenv("FEISHU_APP_ID", "")
FEISHU_APP_SECRET = os.getenv("FEISHU_APP_SECRET", "")
FEISHU_SOURCE_DOC_ID = os.getenv("FEISHU_SOURCE_DOC_ID", "")
FEISHU_OUTPUT_FOLDER_TOKEN = os.getenv("FEISHU_OUTPUT_FOLDER_TOKEN", "")
FEISHU_WEBHOOK_URL = os.getenv("FEISHU_WEBHOOK_URL", "")


# ── LLM 配置 ──
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://api.deepseek.com/v1")
LLM_MODEL = os.getenv("LLM_MODEL", "deepseek-chat")


def validate():
    """检查必要配置是否已填写，返回缺失项列表。"""
    missing = []
    for name in ("FEISHU_APP_ID", "FEISHU_APP_SECRET", "FEISHU_SOURCE_DOC_ID", "LLM_API_KEY"):
        if not globals()[name]:
            missing.append(name)
    return missing
