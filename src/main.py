import click
from src import config
from src.agent.workflow import run


@click.command()
@click.option("--dry-run", is_flag=True, help="只输出到终端，不写飞书")
@click.option("--doc-id", default=None, help="覆盖默认的源文档ID")
def main(dry_run: bool, doc_id: str | None):
    """周报自动生成智能体 —— 从飞书文档读取工作记录，AI生成周报。"""
    missing = config.validate()
    if missing:
        click.echo(f"缺少必要配置: {', '.join(missing)}")
        click.echo("请在 .env 文件中填写对应项（参考 .env.example）")
        raise SystemExit(1)

    source_doc = doc_id or config.FEISHU_SOURCE_DOC_ID

    try:
        report = run(
            source_doc_id=source_doc,
            output_folder_token=config.FEISHU_OUTPUT_FOLDER_TOKEN,
            webhook_url=config.FEISHU_WEBHOOK_URL,
            dry_run=dry_run,
        )
        if dry_run:
            click.echo("\n[dry-run] 周报已生成，未写入飞书。")
    except Exception as e:
        click.echo(f"错误: {e}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
