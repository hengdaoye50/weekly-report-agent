from src.feishu.client import get_client


def read_document(document_id: str) -> str:
    """读取飞书文档的纯文本内容。

    使用 docx v1 的 raw_content 接口，返回文档全部文字。
    """
    import lark_oapi as lark
    from lark_oapi.api.docx.v1 import RawContentDocumentRequest

    client = get_client()
    request = (
        RawContentDocumentRequest.builder()
        .document_id(document_id)
        .build()
    )
    response = client.docx.v1.document.raw_content(request)

    if not response.success():
        raise RuntimeError(
            f"读取文档失败: code={response.code}, msg={response.msg}"
        )

    return response.data.content
