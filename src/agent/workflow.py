import json
from datetime import datetime, timedelta

from src.feishu.reader import read_document
from src.feishu.writer import create_document, append_text_blocks
from src.feishu.notifier import send_webhook
from src.agent.llm import chat
from src.agent.prompts import (
    CLASSIFY_SYSTEM, CLASSIFY_USER,
    POLISH_SYSTEM, POLISH_USER,
    ASSEMBLE_SYSTEM, ASSEMBLE_USER,
)
from src.output.formatter import format_report


def _current_week_range() -> str:
    """返回本周日期范围字符串，如 '2026-06-02 ~ 2026-06-06'。"""
    today = datetime.now()
    monday = today - timedelta(days=today.weekday())
    friday = monday + timedelta(days=4)
    return f"{monday.strftime('%Y-%m-%d')} ~ {friday.strftime('%Y-%m-%d')}"


def run(
    source_doc_id: str = "",
    output_folder_token: str = "",
    webhook_url: str = "",
    dry_run: bool = False,
    input_file: str | None = None,
) -> str:
    """执行周报生成工作流。

    Args:
        source_doc_id: 源工作记录文档ID
        output_folder_token: 周报输出文件夹token（空则输出到根目录）
        webhook_url: 飞书webhook地址（空则不发通知）
        dry_run: 为True时只返回结果，不写飞书
        input_file: 本地文件路径（优先于飞书文档读取）

    Returns:
        生成的周报Markdown文本
    """
    # Step 1: 收集
    print("[1/5] 正在读取工作记录...")
    if input_file:
        with open(input_file, encoding="utf-8") as f:
            raw_content = f.read()
    else:
        raw_content = read_document(source_doc_id)

    if not raw_content.strip():
        raise ValueError("源文档内容为空")

    # Step 2: 分类
    print("[2/5] 正在分类工作内容...")
    classified_json = chat(CLASSIFY_SYSTEM, CLASSIFY_USER.format(raw_content=raw_content))

    # Step 3: 润色
    print("[3/5] 正在润色周报条目...")
    polished_json = chat(POLISH_SYSTEM, POLISH_USER.format(classified_json=classified_json))

    # Step 4: 组装
    print("[4/5] 正在组装周报...")
    date_range = _current_week_range()
    report = chat(ASSEMBLE_SYSTEM, ASSEMBLE_USER.format(
        date_range=date_range,
        polished_json=polished_json,
    ))

    # 本地文件模式或 dry-run 模式：只输出到终端
    if dry_run or input_file:
        print("[5/5] 输出到终端")
        format_report(report)
        return report

    # Step 5: 输出到飞书
    print("[5/5] 正在输出...")

    # 5a: 写飞书文档
    title = f"周报 {date_range}"
    doc_id = create_document(title, output_folder_token)
    paragraphs = [line for line in report.split("\n") if line.strip()]
    append_text_blocks(doc_id, doc_id, paragraphs)
    print(f"  -> 飞书文档已创建: {doc_id}")

    # 5b: 发通知
    if webhook_url:
        summary = report[:200] + "..." if len(report) > 200 else report
        send_webhook(webhook_url, title, summary)
        print("  -> 飞书通知已发送")

    # 5c: CLI输出
    format_report(report)

    return report
