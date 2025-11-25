# modules/utils.py - 最简化版本（无多余换行）
import sys

def pretty_print(text):
    """最简单的文本输出，不添加多余换行"""
    if text is None:
        return
    
    # 确保输出为字符串
    text = str(text)
    
    # 直接写入，不添加换行
    sys.stdout.write(text)
    sys.stdout.flush()

def safe_pretty_print(text):
    """安全版本：确保文本能显示"""
    if text is None:
        return
    pretty_print(text)

# 兼容性函数别名
direct_pretty_print = pretty_print
enhanced_direct_pretty_print = safe_pretty_print
