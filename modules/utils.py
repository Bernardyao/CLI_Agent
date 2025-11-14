# modules/utils.py
from rich.console import Console
from rich.markdown import Markdown

console = Console()


def pretty_print(text: str):
    """
    使用 rich.Markdown 渲染输出
    """
    if not isinstance(text, str):
        text = str(text)

    console.print(Markdown(text))
    console.print()

