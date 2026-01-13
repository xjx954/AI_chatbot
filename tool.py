import os
import requests
from dotenv import load_dotenv, find_dotenv

# 读取环境变量
_ = load_dotenv(find_dotenv())

def get_api_config():
    """
    从环境变量获取API配置，支持灵活切换不同的API服务
    
    返回:
        tuple: (api_key, api_url, default_model)
    """
    # 获取API提供商（默认为deepseek）
    provider = os.getenv('API_PROVIDER', 'deepseek').lower()
    
    # 根据提供商返回不同的配置
    configs = {
        'deepseek': {
            'key': 'DEEPSEEK_API_KEY',
            'url': 'https://api.deepseek.com/v1/chat/completions',
            'default_model': 'deepseek-chat'
        },
        'openai': {
            'key': 'OPENAI_API_KEY',
            'url': 'https://api.openai.com/v1/chat/completions',
            'default_model': 'gpt-3.5-turbo'
        }
    }
    
    # 如果提供商不在配置中，使用deepseek作为默认
    if provider not in configs:
        provider = 'deepseek'
    
    config = configs[provider]
    api_key = os.getenv(config['key'])
    
    return api_key, config['url'], config['default_model'], provider

def get_completion(prompt, model=None, temperature=0.7):
    """
    调用AI接口获取回复（可通过环境变量切换API服务）
    
    参数:
        prompt: 用户输入的提示词
        model: 使用的模型，如果为None则使用默认模型
        temperature: 温度参数，控制输出的随机性，范围0-1，默认为0.7
    
    返回:
        AI模型的回复内容
    
    环境变量配置:
        API_PROVIDER: 选择API提供商，可选 'deepseek' 或 'openai'（默认: deepseek）
        DEEPSEEK_API_KEY: DeepSeek API密钥
        OPENAI_API_KEY: OpenAI API密钥
    """
    # 获取API配置
    api_key, api_url, default_model, provider = get_api_config()
    
    if not api_key:
        configs = {
            'deepseek': {'key': 'DEEPSEEK_API_KEY'},
            'openai': {'key': 'OPENAI_API_KEY'}
        }
        key_name = configs.get(provider, configs['deepseek'])['key']
        return f"错误: 请在.env文件中设置 {key_name} 或设置 API_PROVIDER={provider}"
    
    # 如果没有指定模型，使用默认模型
    if model is None:
        model = default_model
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": temperature
    }
    
    try:
        response = requests.post(api_url, json=data, headers=headers)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"调用{provider} API时发生错误: {str(e)}"


def get_completion_from_messages(messages, model=None, temperature=0):
    """
    从消息列表获取AI回复（支持多轮对话，可通过环境变量切换API服务）
    
    参数:
        messages: 消息列表，每个消息是一个字典，包含role和content
                  role可以是: "system", "user", "assistant"
        model: 使用的模型，如果为None则使用默认模型
        temperature: 温度参数，控制模型输出的随机程度，范围0-1，默认为0
    
    返回:
        AI模型的回复内容
    
    环境变量配置:
        API_PROVIDER: 选择API提供商，可选 'deepseek' 或 'openai'（默认: deepseek）
        DEEPSEEK_API_KEY: DeepSeek API密钥
        OPENAI_API_KEY: OpenAI API密钥
    """
    # 获取API配置
    api_key, api_url, default_model, provider = get_api_config()
    
    if not api_key:
        return f"错误: 请在.env文件中设置相应的API密钥，或设置 API_PROVIDER={provider}"
    
    # 如果没有指定模型，使用默认模型
    if model is None:
        model = default_model
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": model,
        "messages": messages,  # 直接使用传入的messages列表
        "temperature": temperature  # 控制模型输出的随机程度
    }
    
    try:
        response = requests.post(api_url, json=data, headers=headers)
        response.raise_for_status()
        # print(str(response.json()['choices'][0]['message']))  # 可选：打印完整响应
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"调用{provider} API时发生错误: {str(e)}"
