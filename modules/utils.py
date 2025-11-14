# modules/utils.py
from rich.console import Console
from rich.markdown import Markdown

console = Console()


def pretty_print(text: str):
    """
    智能输出渲染 - 修复版
    """
    if not isinstance(text, str):
        text = str(text)
    
    # ✅ 修复:判断是否为Markdown格式
    # 如果文本包含Markdown标记,使用Markdown渲染
    # 否则直接打印
    markdown_indicators = ['**', '#', '`', '[', '](', '- ', '* ', '> ']
    is_markdown = any(indicator in text for indicator in markdown_indicators)
    
    if is_markdown:
        try:
            console.print(Markdown(text))
        except:
            # 如果Markdown渲染失败,降级为普通打印
            console.print(text)
    else:
        # 普通文本直接打印
        console.print(text)

