import os
import requests
from dotenv import load_dotenv, find_dotenv

# 读取环境变量
_ = load_dotenv(find_dotenv())

def get_completion(prompt, model="deepseek-chat", temperature=0.7):
    """
    调用AI接口获取回复（默认使用DeepSeek）
    
    参数:
        prompt: 用户输入的提示词
        model: 使用的模型，默认为 deepseek-chat
        temperature: 温度参数，控制输出的随机性，范围0-1，默认为0.7
    
    返回:
        AI模型的回复内容
    """
    # 使用DeepSeek API
    api_key = os.getenv('DEEPSEEK_API_KEY')
    if not api_key:
        return "错误: 请在.env文件中设置 DEEPSEEK_API_KEY"
    
    url = "https://api.deepseek.com/v1/chat/completions"
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
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"调用DeepSeek API时发生错误: {str(e)}"


def get_completion_from_messages(messages, model="deepseek-chat", temperature=0):
    """
    从消息列表获取AI回复（支持多轮对话）
    
    参数:
        messages: 消息列表，每个消息是一个字典，包含role和content
                  role可以是: "system", "user", "assistant"
        model: 使用的模型，默认为 deepseek-chat
        temperature: 温度参数，控制模型输出的随机程度，范围0-1，默认为0
    
    返回:
        AI模型的回复内容
    """
    # 使用DeepSeek API
    api_key = os.getenv('DEEPSEEK_API_KEY')
    if not api_key:
        return "错误: 请在.env文件中设置 DEEPSEEK_API_KEY"
    
    url = "https://api.deepseek.com/v1/chat/completions"
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
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        # print(str(response.json()['choices'][0]['message']))  # 可选：打印完整响应
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"调用DeepSeek API时发生错误: {str(e)}"
