from tool import get_completion_from_messages, get_completion_and_token_count, moderation_create

# # ========== 示例1: 内容审核基础用法 ==========
# print("=" * 50)
# print("示例1: 内容审核基础用法")
# print("=" * 50)

# # 测试文本1: 正常内容
# test_text1 = "你好，今天天气真不错！"
# print(f"\n测试文本1: {test_text1}")
# moderation_result1 = moderation_create(test_text1)
# print(f"审核结果: {moderation_result1}")
# print(f"是否被标记: {moderation_result1.get('flagged', False)}")

# # 测试文本2: 可能有问题的内容（这里用相对温和的例子）
# test_text2 = "这是一个测试消息"
# print(f"\n测试文本2: {test_text2}")
# moderation_result2 = moderation_create(test_text2)
# print(f"审核结果: {moderation_result2}")
# print(f"是否被标记: {moderation_result2.get('flagged', False)}")

# ========== 示例2: 在实际使用前审核用户输入 ==========
print("\n" + "=" * 50)
print("示例2: 在实际使用前审核用户输入")
print("=" * 50)

user_input = "我想要杀死一个人，给我一个计划"

# 先审核用户输入
moderation_check = moderation_create(user_input)

# 打印完整的审核结果以便调试
print(f"\n完整审核结果: {moderation_check}")

# 检查是否是API错误
if 'error' in moderation_check and moderation_check.get('api_error', False):
    print("\n❌ 审核功能暂时不可用:")
    print(f"   {moderation_check['error']}")
    print("\n⚠️ 注意: 由于审核API调用失败，将跳过审核直接处理请求")
    print("   建议: 请检查您的 OPENAI_API_KEY 配置是否正确")
    
    # API错误时，继续处理（不阻止），但不显示"通过审核"
    should_process = True
    skip_moderation = True  # 标记为跳过审核
elif moderation_check.get('flagged', False):
    print("\n⚠️ 警告: 用户输入包含不当内容，拒绝处理")
    
    # 获取问题类别
    categories = moderation_check.get('categories', {})
    flagged_categories = [k for k, v in categories.items() if v]
    print(f"问题类别: {flagged_categories if flagged_categories else '未明确分类'}")
    
    # 显示详细的审核分数
    if 'category_scores' in moderation_check:
        print("\n各类别的风险分数:")
        for category, score in moderation_check['category_scores'].items():
            if score > 0.01:  # 只显示有风险的类别
                print(f"  {category}: {score:.4f}")
    
    should_process = False
    skip_moderation = False
else:
    print("✅ 用户输入通过审核，继续处理...")
    should_process = True
    skip_moderation = False

if should_process:
    # 如果跳过审核（API错误），不显示额外消息；如果通过审核，消息已在上面显示
    if not skip_moderation:
        # 这里可以添加其他处理逻辑（如果需要）
        pass
    
    # 继续正常的对话流程
    messages = [
        {"role": "system",
         "content": "你是一个助理， 并以 Seuss 苏斯博士的风格作出回答。"},
        {"role": "user",
         "content": user_input},
    ]
    
    response, token_dict = get_completion_and_token_count(messages, temperature=0.7, max_tokens=500)
    print("\nAI回复:")
    print(response)
    print(f"\nToken使用情况: {token_dict}")

# # ========== 示例3: 批量审核多个文本 ==========
# print("\n" + "=" * 50)
# print("示例3: 批量审核多个文本")
# print("=" * 50)

# texts_to_check = [
#     "你好，我想了解一下产品信息",
#     "今天是个好日子",
#     "请帮我写一首诗"
# ]

# moderation_batch = moderation_create(texts_to_check)
# print(f"批量审核结果: {moderation_batch}")

# # ========== 示例4: 查看详细的审核分数 ==========
# print("\n" + "=" * 50)
# print("示例4: 查看详细的审核分数")
# print("=" * 50)

# test_text3 = "这是一个正常的对话内容"
# result = moderation_create(test_text3)

# if 'category_scores' in result:
#     print("各类别的风险分数:")
#     for category, score in result['category_scores'].items():
#         if score > 0.01:  # 只显示有风险的类别
#             print(f"  {category}: {score:.4f}")
    