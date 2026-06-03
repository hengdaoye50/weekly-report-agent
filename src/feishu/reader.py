from src.feishu.client import get_client


def _resolve_wiki_token(wiki_token: str) -> str:
    """从 wiki 节点 token 获取实际的 document_id。

    飞书知识库文档的 URL 格式为 /wiki/{token}，
    需要先通过 wiki API 查出底层的 obj_token（即 document_id）。
    """
    import httpx
    from src.config import FEISHU_APP_ID, FEISHU_APP_SECRET

    # 先获取 tenant_access_token
    resp = httpx.post(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        json={"app_id": FEISHU_APP_ID, "app_secret": FEISHU_APP_SECRET},
        timeout=10,
    )
    resp.raise_for_status()
    token = resp.json()["tenant_access_token"]

    # 查询 wiki 节点信息
    resp = httpx.get(
        "https://open.feishu.cn/open-apis/wiki/v2/spaces/get_node",
        params={"token": wiki_token},
        headers={"Authorization": f"Bearer {token}"},
        timeout=10,
    )
    resp.raise_for_status()
    data = resp.json()

    if data.get("code", 0) != 0:
        raise RuntimeError(f"查询wiki节点失败: {data}")

    node = data["data"]["node"]
    obj_type = node["obj_type"]
    obj_token = node["obj_token"]

    if obj_type != "docx":
        raise RuntimeError(f"不支持的文档类型: {obj_type}，目前只支持 docx")

    return obj_token


def _extract_token(doc_id_or_url: str) -> str:
    """从 URL 或纯 token 中提取 wiki token。"""
    if "/" in doc_id_or_url:
        # URL 格式: https://xxx.feishu.cn/wiki/Ot5twgRRNieTmFk9LbGcDITSnoc
        parts = doc_id_or_url.rstrip("/").split("/")
        return parts[-1].split("?")[0]
    return doc_id_or_url


def read_document(document_id_or_url: str) -> str:
    """读取飞书文档的纯文本内容。

    支持普通文档ID、wiki文档ID、或完整的飞书URL。
    自动判断是否为 wiki 文档并解析。
    """
    import lark_oapi as lark
    from lark_oapi.api.docx.v1 import RawContentDocumentRequest

    token = _extract_token(document_id_or_url)

    # 尝试当作 wiki token 解析
    try:
        doc_id = _resolve_wiki_token(token)
    except Exception:
        # 解析失败，当作普通文档 ID 直接使用
        doc_id = token

    client = get_client()
    request = (
        RawContentDocumentRequest.builder()
        .document_id(doc_id)
        .build()
    )
    response = client.docx.v1.document.raw_content(request)

    if not response.success():
        raise RuntimeError(
            f"读取文档失败: code={response.code}, msg={response.msg}"
        )

    return response.data.content
