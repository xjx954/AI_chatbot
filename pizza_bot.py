# -*- coding: utf-8 -*-
"""
披萨餐厅订餐机器人
使用Panel创建GUI界面，使用DeepSeek API进行对话
"""
import panel as pn
from tool import get_completion_from_messages, moderation_create
import time
import os
from dotenv import load_dotenv, find_dotenv

# 读取环境变量
_ = load_dotenv(find_dotenv())

# 初始化Panel
pn.extension()

# 设置全局样式，实现居中
pn.config.raw_css = ["""
body {
    display: flex;
    justify-content: center;
    align-items: flex-start;
    min-height: 100vh;
    margin: 0;
    padding: 20px;
    background-color: #f5f5f5;
}
.bk-root {
    width: 100%;
    max-width: 800px;
    margin: 0 auto;
}
.bk-panel-models-row {
    justify-content: center !important;
}
.bk-panel-models-column {
    margin: 0 auto !important;
    max-width: 700px;
}
"""]

# 存储对话历史
panels = []  # 收集显示内容

# 系统上下文 - 订餐机器人的角色和菜单信息
context = [{
    'role': 'system',
    'content': """
你是订餐机器人，为披萨餐厅自动收集订单信息。
你要首先问候顾客。然后等待用户回复收集订单信息。收集完信息需确认顾客是否还需要添加其他内容。
最后需要询问是否自取或外送，如果是外送，你要询问地址。
最后告诉顾客订单总金额，并送上祝福。

请确保明确所有选项、附加项和尺寸，以便从菜单中识别出该项唯一的内容。
你的回应应该以简短、非常随意和友好的风格呈现。

菜单包括：

菜品：
意式辣香肠披萨（大、中、小） 12.95、10.00、7.00
芝士披萨（大、中、小） 10.95、9.25、6.50
茄子披萨（大、中、小） 11.95、9.75、6.75
薯条（大、小） 4.50、3.50
希腊沙拉 7.25

配料：
奶酪 2.00
蘑菇 1.50
香肠 3.00
加拿大熏肉 3.50
AI酱 1.50
辣椒 1.00

饮料：
可乐（大、中、小） 3.00、2.00、1.00
雪碧（大、中、小） 3.00、2.00、1.00
瓶装水 5.00
"""
}]

# 存储完整的对话历史
conversation = context.copy()


def check_openai_support():
    """
    检查是否支持OpenAI（是否有OpenAI API Key）
    
    返回:
        bool: 如果支持OpenAI返回True，否则返回False
    """
    openai_api_key = os.getenv('OPENAI_API_KEY')
    return openai_api_key is not None and openai_api_key.strip() != ""


def collect_messages(_):
    """
    收集用户消息并获取AI回复
    
    参数:
        _: Panel按钮点击事件（未使用）
    
    返回:
        Panel对象，显示对话历史
    """
    # 获取用户输入
    user_input = inp.value
    
    if not user_input or user_input.strip() == "":
        return pn.Column(*panels)
    
    # 先检查是否支持OpenAI，如果支持则进行内容审核
    if check_openai_support():
        moderation_result = moderation_create(user_input)
        
        # 检查是否是API错误
        if 'error' in moderation_result and moderation_result.get('api_error', False):
            # API调用失败，显示错误信息但不阻止处理
            error_message = f"⚠️ **审核功能暂时不可用**: {moderation_result['error']}\n\n将跳过审核继续处理。"
            panels.append(
                pn.Row('用户:', pn.pane.Markdown(user_input, width=600))
            )
            panels.append(
                pn.Row('系统:', pn.pane.Markdown(
                    error_message, 
                    width=600, 
                    styles={'background-color': '#FFF4E6', 'color': '#CC6600'}
                ))
            )
            # 继续处理，不阻止
        elif moderation_result.get('flagged', False):
            # 如果内容被标记为不当，拒绝处理
            # 获取问题类别
            categories = moderation_result.get('categories', {})
            flagged_categories = [k for k, v in categories.items() if v]
            
            # 显示警告信息
            warning_message = "⚠️ **警告**: 您的输入包含不当内容，无法处理。"
            if flagged_categories:
                warning_message += f"\n\n问题类别: {', '.join(flagged_categories)}"
            
            panels.append(
                pn.Row('用户:', pn.pane.Markdown(user_input, width=600))
            )
            panels.append(
                pn.Row('系统:', pn.pane.Markdown(
                    warning_message, 
                    width=600, 
                    styles={'background-color': '#FFE6E6', 'color': '#CC0000'}
                ))
            )
            
            # 清空输入框
            inp.value = ''
            return pn.Column(*panels)
    
    # 添加用户消息到对话历史
    conversation.append({'role': 'user', 'content': user_input})
    
    # 获取AI回复
    response = get_completion_from_messages(conversation, temperature=0.7, max_tokens=500)
    
    # 添加AI回复到对话历史
    conversation.append({'role': 'assistant', 'content': response})
    
    # 更新显示面板
    panels.append(
        pn.Row('用户:', pn.pane.Markdown(user_input, width=600))
    )
    panels.append(
        pn.Row('助手:', pn.pane.Markdown(response, width=600, styles={'background-color': '#F6F6F6'}))
    )
    
    # 清空输入框
    inp.value = ''
    
    return pn.Column(*panels)


# 创建输入框
inp = pn.widgets.TextInput(
    value="", 
    placeholder='请输入您的消息...',
    width=600
)

# 创建聊天按钮
button_conversation = pn.widgets.Button(
    name="发送",
    button_type="primary",
    width=100
)

# 绑定按钮点击事件
interactive_conversation = pn.bind(collect_messages, button_conversation)

# 创建主要内容区域
content = pn.Column(
    pn.pane.Markdown(
        "# 🍕 披萨餐厅订餐机器人",
        styles={'font-size': '24px', 'font-weight': 'bold', 'text-align': 'center'}
    ),
    pn.pane.Markdown(
        "欢迎使用订餐机器人！请输入您的订单需求。" + 
        ("\n\n✅ 内容审核功能已启用" if check_openai_support() else "\n\nℹ️ 提示: 设置 OPENAI_API_KEY 可启用内容审核功能"),
        styles={'color': '#666', 'text-align': 'center'}
    ),
    pn.Spacer(height=10),
    inp,
    pn.Row(button_conversation),
    pn.Spacer(height=10),
    pn.panel(interactive_conversation, loading_indicator=True, height=400),
    width=700
)

# 创建仪表板，直接使用content（CSS已处理居中）
dashboard = content

# 显示仪表板
dashboard.servable()

# 如果直接运行此文件，启动服务器
if __name__ == "__main__":
    print("=" * 60)
    print("披萨餐厅订餐机器人")
    print("=" * 60)
    print("\n正在启动服务器...")
    print("请在浏览器中打开显示的地址")
    print("\n提示: 按 Ctrl+C 停止服务器")
    print("=" * 60)
    
    # 启动Panel服务器
    dashboard.show()
