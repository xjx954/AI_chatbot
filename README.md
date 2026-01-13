# AI模型调用项目

这是一个使用Python调用各种AI模型的工具包，支持OpenAI、DeepSeek、Hugging Face、Google Gemini等多种API服务。项目包含核心工具模块、统一接口和实际应用示例（披萨订餐机器人）。

## 📋 项目功能

1. **支持多种AI模型API**
   - DeepSeek（推荐，中文支持好，免费额度大）
   - OpenAI（需要付费）
   - Hugging Face（完全免费）
   - Google Gemini（免费额度）
   - 通义千问（新用户免费）

2. **核心功能**
   - 单次对话调用
   - 多轮对话支持
   - 统一接口，轻松切换不同模型
   - 实际应用：披萨餐厅订餐机器人（GUI界面）

## 📁 项目结构

```
A_study/
├── tool.py                      # 核心工具模块（使用DeepSeek API）
│   ├── get_completion()         # 单次对话函数
│   └── get_completion_from_messages()  # 多轮对话函数
│
├── utils.py                     # 工具函数
│   ├── get_openai_key()        # 读取OpenAI API密钥
│   └── get_api_key()           # 通用API密钥读取函数
│
├── unified_ai_client.py        # 统一AI客户端接口
│   ├── UnifiedAIClient         # 统一客户端类
│   └── quick_chat()            # 快速调用函数
│
├── pizza_bot.py                # 披萨餐厅订餐机器人（GUI应用）
│   └── 使用Panel创建Web界面，实现智能订餐对话
│
├── requirements.txt            # Python依赖包
│   ├── openai
│   ├── python-dotenv
│   ├── requests
│   └── panel
│
└── .env                        # 环境变量配置文件（需要自己创建）
    └── 包含各种API密钥配置
```

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置API密钥

创建 `.env` 文件，添加API密钥：

```env
# DeepSeek (推荐)
DEEPSEEK_API_KEY=your_deepseek_api_key_here

# 其他可选API
HF_API_KEY=your_huggingface_token
GEMINI_API_KEY=your_gemini_api_key
DASHSCOPE_API_KEY=your_dashscope_api_key
OPENAI_API_KEY=your_openai_api_key
```

**获取DeepSeek API密钥：**
1. 访问 https://platform.deepseek.com/
2. 注册/登录账号
3. 在控制台创建API密钥
4. 复制密钥到 `.env` 文件

### 3. 运行应用

#### 运行披萨订餐机器人（GUI界面）
```bash
python pizza_bot.py
```
运行后会在浏览器中打开一个Web界面，可以与订餐机器人进行对话。

## 💻 代码使用示例

### 示例1: 单次对话

```python
from tool import get_completion

# 简单调用
response = get_completion("你好，介绍一下Python", temperature=0)
print(response)
```

### 示例2: 多轮对话

```python
from tool import get_completion_from_messages

# 构建消息列表
messages = [
    {"role": "system", "content": "你是一个友好的AI助手"},
    {"role": "user", "content": "什么是Python？"}
]

# 获取回复
response = get_completion_from_messages(messages, temperature=0.7)
print(response)

# 继续对话
messages.append({"role": "assistant", "content": response})
messages.append({"role": "user", "content": "Python有哪些特点？"})
response2 = get_completion_from_messages(messages, temperature=0.7)
print(response2)
```

### 示例3: 使用统一接口切换模型

```python
from unified_ai_client import quick_chat, UnifiedAIClient

# 方式1: 快速调用
response = quick_chat("你好，介绍一下Python", provider="deepseek")
print(response)

# 方式2: 使用统一客户端
client = UnifiedAIClient(default_provider="deepseek")
response = client.chat("你好，介绍一下Python")
print(response)

# 切换到其他模型
response = client.chat("你好，介绍一下Python", provider="gemini")
print(response)
```

## 🔧 核心函数说明

### `tool.py` 中的函数

#### `get_completion(prompt, model="deepseek-chat", temperature=0.7)`
- **功能**: 单次对话调用
- **参数**:
  - `prompt`: 用户输入的提示词（字符串）
  - `model`: 模型名称，默认 "deepseek-chat"
  - `temperature`: 温度参数（0-1），控制输出随机性，默认0.7
- **返回**: AI模型的回复内容（字符串）

#### `get_completion_from_messages(messages, model="deepseek-chat", temperature=0)`
- **功能**: 多轮对话调用
- **参数**:
  - `messages`: 消息列表，每个消息是字典格式 `{"role": "user", "content": "..."}`
  - `model`: 模型名称，默认 "deepseek-chat"
  - `temperature`: 温度参数，默认0
- **返回**: AI模型的回复内容（字符串）
- **消息角色**:
  - `"system"`: 系统消息，设置AI的行为和角色
  - `"user"`: 用户消息
  - `"assistant"`: AI助手的回复

## 🍕 披萨订餐机器人

项目包含一个完整的GUI应用示例：披萨餐厅订餐机器人。

**功能特点：**
- 使用Panel创建Web界面
- 智能对话收集订单信息
- 支持多轮对话，保持上下文
- 友好的用户界面

**运行方式：**
```bash
python pizza_bot.py
```

运行后会在浏览器中打开界面，可以与机器人进行对话订餐。

## 📝 项目特点

1. **统一接口**: 通过 `unified_ai_client.py` 可以轻松切换不同的AI服务
2. **多模型支持**: 支持多种免费和付费的AI模型
3. **对话管理**: 支持单次对话和多轮对话
4. **实际应用**: 包含完整的GUI应用示例
5. **易于使用**: 代码结构清晰，易于理解和扩展

## 🔑 API密钥获取地址

| 服务 | 注册地址 | 免费额度 |
|------|---------|---------|
| DeepSeek | https://platform.deepseek.com/ | 每天200万tokens |
| Hugging Face | https://huggingface.co/ | 完全免费 |
| Google Gemini | https://makersuite.google.com/app/apikey | 每天1500次请求 |
| 通义千问 | https://dashscope.console.aliyun.com/ | 新用户免费额度 |
| OpenAI | https://platform.openai.com/ | 需要付费 |

## ⚠️ 注意事项

1. **API密钥安全**: 
   - 不要将 `.env` 文件提交到Git仓库
   - 确保 `.env` 文件在 `.gitignore` 中

2. **免费额度限制**:
   - 注意各服务的免费额度限制
   - 超出免费额度后需要付费

3. **错误处理**:
   - 代码中已包含基本的错误处理
   - 如果遇到401错误，检查API密钥是否正确配置

## 🐛 常见问题

### Q: 401 Unauthorized 错误
**A**: 检查 `.env` 文件中的API密钥是否正确配置

### Q: 如何切换不同的AI模型？
**A**: 使用 `unified_ai_client.py` 中的 `UnifiedAIClient` 类

### Q: 如何实现多轮对话？
**A**: 使用 `get_completion_from_messages()` 函数，维护一个消息列表，每次对话后添加新的消息

### Q: 披萨机器人界面显示在左上角？
**A**: 已修复，现在界面会自动居中显示

## 📚 相关文档

- DeepSeek API文档: https://platform.deepseek.com/docs
- OpenAI API文档: https://platform.openai.com/docs
- Panel文档: https://panel.holoviz.org/
- Hugging Face文档: https://huggingface.co/docs

## 📄 许可证

本项目仅供学习使用。

---

**最后更新**: 2025年1月
