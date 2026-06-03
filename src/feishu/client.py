import lark_oapi as lark
from src.config import FEISHU_APP_ID, FEISHU_APP_SECRET

_client: lark.Client | None = None


def get_client() -> lark.Client:
    """获取飞书 SDK 客户端单例。"""
    global _client
    if _client is None:
        _client = (
            lark.Client.builder()
            .app_id(FEISHU_APP_ID)
            .app_secret(FEISHU_APP_SECRET)
            .build()
        )
    return _client
