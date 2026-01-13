"""
统一的AI模型调用接口
支持多种免费和付费模型，可以轻松切换
"""
from free_models_example import (
    call_deepseek,
    call_huggingface,
    call_gemini,
    call_qwen
)
from tool import get_completion as call_openai


class UnifiedAIClient:
    """统一的AI客户端，支持多种模型"""
    
    def __init__(self, default_provider="deepseek"):
        """
        初始化客户端
        
        参数:
            default_provider: 默认使用的服务提供商
                可选: 'deepseek', 'huggingface', 'gemini', 'qwen', 'openai'
        """
        self.default_provider = default_provider
        self.providers = {
            'deepseek': call_deepseek,
            'huggingface': call_huggingface,
            'gemini': call_gemini,
            'qwen': call_qwen,
            'openai': call_openai
        }
    
    def chat(self, prompt, provider=None, **kwargs):
        """
        统一的聊天接口
        
        参数:
            prompt: 用户输入的提示词
            provider: 服务提供商，如果为None则使用默认提供商
            **kwargs: 其他参数（如temperature, model等）
        
        返回:
            AI模型的回复
        """
        provider = provider or self.default_provider
        
        if provider not in self.providers:
            return f"错误: 不支持的服务提供商 '{provider}'。支持的服务: {list(self.providers.keys())}"
        
        try:
            func = self.providers[provider]
            return func(prompt, **kwargs)
        except Exception as e:
            return f"调用 {provider} 时发生错误: {str(e)}"
    
    def list_providers(self):
        """列出所有可用的服务提供商"""
        return list(self.providers.keys())


# 便捷函数
def quick_chat(prompt, provider="deepseek"):
    """
    快速调用AI模型的便捷函数
    
    参数:
        prompt: 用户输入的提示词
        provider: 服务提供商（默认: deepseek）
    
    返回:
        AI模型的回复
    """
    client = UnifiedAIClient(default_provider=provider)
    return client.chat(prompt)


if __name__ == "__main__":
    # 示例使用
    print("=" * 60)
    print("统一AI客户端测试")
    print("=" * 60)
    
    # 创建客户端
    client = UnifiedAIClient(default_provider="deepseek")
    
    # 测试不同提供商
    test_prompt = "用一句话介绍Python编程语言"
    
    print(f"\n可用提供商: {client.list_providers()}")
    
    print(f"\n[测试] 使用默认提供商 (deepseek):")
    print("-" * 60)
    response = client.chat(test_prompt)
    print(response)
    
    print(f"\n[测试] 切换到Gemini:")
    print("-" * 60)
    response = client.chat(test_prompt, provider="gemini")
    print(response)
    
    print(f"\n[测试] 使用便捷函数:")
    print("-" * 60)
    response = quick_chat(test_prompt, provider="deepseek")
    print(response)
