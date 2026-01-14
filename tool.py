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


def get_completion_from_messages(messages, model=None, temperature=0, max_tokens = 500):
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
        "temperature": temperature,  # 控制模型输出的随机程度
        "max_tokens": max_tokens,
    }
    
    try:
        response = requests.post(api_url, json=data, headers=headers)
        response.raise_for_status()
        # print(str(response.json()['choices'][0]['message']))  # 可选：打印完整响应
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"调用{provider} API时发生错误: {str(e)}"

def get_completion_and_token_count(messages, 
                                   model=None, 
                                   temperature=0, 
                                   max_tokens=500):
    """
    使用 OpenAI 的 GPT-3 模型生成聊天回复，并返回生成的回复内容以及使用的 token 数量。

    参数:
    messages: 聊天消息列表。
    model: 使用的模型名称。默认为"gpt-3.5-turbo"。
    temperature: 控制生成回复的随机性。值越大，生成的回复越随机。默认为 0。
    max_tokens: 生成回复的最大 token 数量。默认为 500。

    返回:
    content: 生成的回复内容。
    token_dict: 包含'prompt_tokens'、'completion_tokens'和'total_tokens'的字典，分别表示提示的 token 数量、生成的回复的 token 数量和总的 token 数量。
    """
    api_key, api_url, default_model, provider = get_api_config()
    
    if not api_key:
        return f"错误: 请在.env文件中设置相应的API密钥，或设置 API_PROVIDER={provider}"
    
    if model is None:
        model = default_model
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    
    try:
        response = requests.post(api_url, json=data, headers=headers)
        response.raise_for_status()
        # return response.json()['choices'][0]['message']['content']
    except Exception as e:
        print(f"调用{provider} API时发生错误: {str(e)}")

    content = response.json()['choices'][0]['message']['content']
    
    token_dict = {
        'prompt_tokens':response.json()['usage']['prompt_tokens'],
        'completion_tokens':response.json()['usage']['completion_tokens'],
        'total_tokens':response.json()['usage']['total_tokens'],
    }

    return content, token_dict

def moderation_create(input_text, model="omni-moderation-latest"):
    """
    内容审核函数，类似于OpenAI的Moderation.create()
    用于检测文本中是否包含有害内容
    
    参数:
        input_text: 需要审核的文本内容（字符串或字符串列表）
        model: 审核模型，默认为"omni-moderation-latest"（OpenAI最新模型）
               可选值: "omni-moderation-latest", "text-moderation-latest", "text-moderation-stable"
    
    返回:
        字典，包含审核结果：
        {
            'id': 审核ID,
            'model': 使用的模型,
            'results': [
                {
                    'flagged': bool,  # 是否被标记为有害内容
                    'categories': {   # 各类别的布尔值
                        'hate': bool,
                        'hate/threatening': bool,
                        'harassment': bool,
                        'harassment/threatening': bool,
                        'self-harm': bool,
                        'self-harm/intent': bool,
                        'self-harm/instructions': bool,
                        'sexual': bool,
                        'sexual/minors': bool,
                        'violence': bool,
                        'violence/graphic': bool
                    },
                    'category_scores': {  # 各类别的概率分数（0-1）
                        'hate': float,
                        'hate/threatening': float,
                        ...
                    },
                    'flagged': bool
                }
            ]
        }
    
    注意:
        - 目前仅支持OpenAI的Moderation API
        - DeepSeek API目前没有官方的moderation端点
        - 如果DeepSeek将来提供类似功能，可以在此函数中扩展支持
    
    环境变量配置:
        OPENAI_API_KEY: OpenAI API密钥（用于审核功能）
    """
    # 获取OpenAI API密钥
    openai_api_key = os.getenv('OPENAI_API_KEY')
    
    if not openai_api_key:
        return {
            'error': '错误: 请在.env文件中设置 OPENAI_API_KEY 以使用审核功能',
            'flagged': True  # 如果无法审核，默认标记为需要审核
        }
    
    # OpenAI Moderation API端点
    moderation_url = 'https://api.openai.com/v1/moderations'
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}"
    }
    
    # 确保input是列表格式
    if isinstance(input_text, str):
        input_list = [input_text]
    else:
        input_list = input_text
    
    data = {
        "input": input_list,
        "model": model
    }
    
    try:
        response = requests.post(moderation_url, json=data, headers=headers)
        response.raise_for_status()
        result = response.json()
        
        # 如果输入是单个字符串，返回单个结果；如果是列表，返回所有结果
        if isinstance(input_text, str) and len(result.get('results', [])) > 0:
            # 返回格式化的单个结果
            single_result = result['results'][0]
            return {
                'id': result.get('id'),
                'model': result.get('model'),
                'flagged': single_result.get('flagged', False),
                'categories': single_result.get('categories', {}),
                'category_scores': single_result.get('category_scores', {}),
                'results': result.get('results', [])
            }
        else:
            # 返回完整结果
            return result
            
    except requests.exceptions.HTTPError as e:
        # HTTP错误（如401未授权、403禁止等）
        error_msg = str(e)
        if e.response.status_code == 401:
            error_msg = "OpenAI API密钥无效或未授权。请检查您的 OPENAI_API_KEY 是否正确。"
        elif e.response.status_code == 403:
            error_msg = "OpenAI API访问被禁止。请检查您的API密钥权限。"
        elif e.response.status_code == 429:
            error_msg = "OpenAI API请求频率过高，请稍后再试。"
        
        return {
            'error': f'调用OpenAI Moderation API时发生错误: {error_msg}',
            'flagged': False,  # API调用失败时，不标记为不当内容，避免误判
            'api_error': True  # 标记这是API错误，不是内容问题
        }
    except Exception as e:
        return {
            'error': f'调用OpenAI Moderation API时发生错误: {str(e)}',
            'flagged': False,  # API调用失败时，不标记为不当内容，避免误判
            'api_error': True  # 标记这是API错误，不是内容问题
        }
