import httpx


def send_webhook(webhook_url: str, title: str, content: str):
    """通过飞书自定义机器人 webhook 发送富文本消息。"""
    payload = {
        "msg_type": "post",
        "content": {
            "post": {
                "zh_cn": {
                    "title": title,
                    "content": [
                        [{"tag": "text", "text": content}]
                    ],
                }
            }
        },
    }
    resp = httpx.post(webhook_url, json=payload, timeout=10)
    resp.raise_for_status()

    data = resp.json()
    if data.get("code", 0) != 0:
        raise RuntimeError(f"发送通知失败: {data}")
