# CLI_Agent

一个简洁高效的命令行AI助手，基于大语言模型构建，支持交互式对话和管道输入处理。

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## ✨ 特性

- 🤖 **智能对话** - 支持与AI助手的自然语言交互
- 🔄 **管道支持** - 可通过管道接收输入，自动处理后退出
- 📤 **简洁输出** - 优化的文本显示格式，无多余换行
- ⚡ **流式响应** - 实时显示AI回复内容
- 🔐 **安全配置** - 基于环境变量的API密钥管理
- 💬 **历史记录** - 自动保存对话历史

## 🚀 快速开始

### 环境要求

- Python 3.10+
- API密钥（支持QNAI接口或其他兼容API）

### 安装配置

1. **克隆项目**
```bash
git clone https://github.com/Bernardyao/CLI_Agent.git
cd CLI_Agent
```

2. **创建虚拟环境（可选但推荐）**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

3. **配置API密钥**
```bash
# 设置环境变量
export QNAI_API_KEY="your_api_key_here"

# 或者在config.py中直接配置（不推荐）
```

4. **安装依赖**
```bash
pip install -r requirements.txt
```

### 使用方法

#### 交互式模式
```bash
python agent.py
```

#### 管道模式（单次分析）
```bash
echo "分析这段代码" | python agent.py
cat file.txt | python agent.py
```

## 📁 项目结构

```
CLI_Agent/
├── agent.py              # 主程序入口
├── config.py             # 配置文件
├── modules/              # 核心模块
│   ├── input_handler.py  # 输入处理
│   ├── llm_client.py     # LLM客户端
│   └── utils.py          # 工具函数
├── .gitignore            # Git忽略规则
└── README.md             # 项目说明
```

## 🛠️ 核心功能

### 1. 智能输入处理
- 自动检测管道输入
- 支持标准输入流
- 历史记录保存

### 2. 流式响应显示
- 实时显示AI回复
- 优化的文本格式
- 无多余换行干扰

### 3. 安全配置管理
- 环境变量优先
- API密钥安全存储
- 配置与代码分离

## ⚙️ 配置说明

在 `config.py` 中配置API信息：

```python
import os

# API配置
API_KEY = os.getenv("QNAI_API_KEY")  # 优先从环境变量读取
BASE_URL = "https://api.qnaigc.com/v1/chat/completions"
MODEL = "deepseek/deepseek-v3.1-terminus"

# 如果环境变量未设置，使用默认值
if not API_KEY:
    API_KEY = "your_default_api_key"
```

## 🔧 开发和调试

### 运行测试
```bash
# 测试基本功能
python -c "from modules.utils import pretty_print; pretty_print('Hello, World!')"

# 测试管道功能
echo "test" | python agent.py
```

### 常见问题

**Q: 提示"401 Unauthorized"错误**
A: 检查API密钥配置，确保环境变量 `QNAI_API_KEY` 已正确设置

**Q: 输出显示空白**
A: 已修复显示问题，使用优化的输出函数

**Q: 管道模式不退出**
A: 管道模式会自动在处理完成后退出

## 📝 更新日志

### v2.0.0 (2025-11-25)
- ✅ 修复了文本显示空白问题
- ✅ 优化了输出格式，移除多余换行
- ✅ 简化了代码结构，提高可维护性
- ✅ 完善了管道输入的自动退出机制
- ✅ 增加了全面的.gitignore文件

### v1.0.0
- 🎉 初始版本发布
- ✅ 基本对话功能
- ✅ 管道输入支持
- ✅ 流式响应显示


## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🙏 致谢

- 感谢DeepSeek提供的优秀AI模型
- Python社区的丰富生态支持
- 所有贡献者的宝贵建议

