import os
from dotenv import load_dotenv, find_dotenv

def get_openai_key():
    """
    读取本地/项目的环境变量。
    find_dotenv()寻找并定位.env文件的路径
    load_dotenv()读取该.env文件,并将其中的环境变量加载到当前的运行环境中
    如果你设置的是全局的环境变量,这行代码则没有任何作用。
    """
    _ = load_dotenv(find_dotenv())
    return os.environ.get('OPENAI_API_KEY', '')

def get_api_key(key_name):
    """
    通用函数：获取任意API密钥
    
    参数:
        key_name: 环境变量名称，如 'DEEPSEEK_API_KEY', 'HF_API_KEY' 等
    
    返回:
        API密钥字符串，如果不存在则返回空字符串
    """
    _ = load_dotenv(find_dotenv())
    return os.environ.get(key_name, '')
