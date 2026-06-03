from src.feishu.client import get_client


def create_document(title: str, folder_token: str = "") -> str:
    """创建一篇新的飞书文档，返回 document_id。"""
    import lark_oapi as lark
    from lark_oapi.api.docx.v1 import CreateDocumentRequest, CreateDocumentRequestBody

    client = get_client()
    body_builder = CreateDocumentRequestBody.builder().title(title)
    if folder_token:
        body_builder.folder_token(folder_token)

    request = CreateDocumentRequest.builder().request_body(body_builder.build()).build()
    response = client.docx.v1.document.create(request)

    if not response.success():
        raise RuntimeError(
            f"创建文档失败: code={response.code}, msg={response.msg}"
        )

    return response.data.document.document_id


def append_text_blocks(document_id: str, parent_block_id: str, paragraphs: list[str]):
    """向文档追加文本段落。

    每个 paragraph 作为一个 paragraph block 追加。
    """
    import json
    import lark_oapi as lark
    from lark_oapi.api.docx.v1 import (
        CreateDocumentBlockChildrenRequest,
        CreateDocumentBlockChildrenRequestBody,
        Block,
        TextElement,
        TextRun,
        BlockType,
    )

    client = get_client()

    children = []
    for text in paragraphs:
        block = Block.builder()
        block.block_type(BlockType.PARAGRAPH)
        block.paragraph(
            {
                "elements": [
                    {
                        "text_run": {
                            "content": text,
                        }
                    }
                ]
            }
        )
        children.append(block.build())

    request = (
        CreateDocumentBlockChildrenRequest.builder()
        .document_id(document_id)
        .block_id(parent_block_id)
        .request_body(
            CreateDocumentBlockChildrenRequestBody.builder()
            .children(children)
            .index(-1)
            .build()
        )
        .build()
    )
    response = client.docx.v1.document_block_children.create(request)

    if not response.success():
        raise RuntimeError(
            f"写入文档失败: code={response.code}, msg={response.msg}"
        )
