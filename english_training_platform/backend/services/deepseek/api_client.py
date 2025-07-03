import os
import json
import requests
import time
from typing import Dict, List, Any, Optional

# 这里假设DeepSeek API密钥存储在环境变量中
# 在实际部署时应该从环境变量或配置文件中获取
DEEPSEEK_API_KEY = os.environ.get('DEEPSEEK_API_KEY', 'sk-fe2a5d1ec6bc40abaa01867fba5a2c18')
DEEPSEEK_API_ENDPOINT = "https://api.deepseek.com/v1/chat/completions"  # 假设的API端点

def call_deepseek_api(prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
    """
    调用DeepSeek API
    
    Args:
        prompt (str): 向DeepSeek发送的提示词
        system_prompt (str, optional): 系统提示词
        
    Returns:
        dict: DeepSeek API的响应
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
    }
    
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    
    data = {
        "model": "deepseek-chat",  # 使用的模型，根据实际API调整
        "messages": messages,
        "max_tokens": 2000,
        "temperature": 0.7
    }
    
    # 设置最大重试次数和超时时间
    max_retries = 3
    timeout_seconds = 180  # 增加到180秒
    retry_delay = 3  # 每次重试前等待的秒数
    
    for retry in range(max_retries):
        try:
            print(f"发送请求到DeepSeek API: {prompt[:100]}... (尝试 {retry+1}/{max_retries})")
            response = requests.post(DEEPSEEK_API_ENDPOINT, headers=headers, json=data, timeout=timeout_seconds)
            
            # 检查HTTP状态码
            if response.status_code != 200:
                print(f"DeepSeek API返回非200状态码: {response.status_code}, 响应: {response.text[:200]}")
                if retry < max_retries - 1:
                    print(f"等待 {retry_delay} 秒后重试...")
                    time.sleep(retry_delay)
                    continue
                else:
                    print("所有重试均失败，返回模拟响应")
                    return generate_mock_response(prompt)
            
            # 检查响应内容是否为空
            if not response.text.strip():
                print(f"收到空响应 (尝试 {retry+1}/{max_retries})")
                if retry < max_retries - 1:
                    print(f"等待 {retry_delay} 秒后重试...")
                    time.sleep(retry_delay)
                    continue
                else:
                    print("所有重试均失败，返回模拟响应")
                    return generate_mock_response(prompt)
            
            # 尝试解析JSON
            try:
                result = response.json()
                # 验证响应格式是否正确
                if not result or "choices" not in result or not result["choices"]:
                    print(f"响应格式不符合预期 (尝试 {retry+1}/{max_retries})")
                    if retry < max_retries - 1:
                        print(f"等待 {retry_delay} 秒后重试...")
                        time.sleep(retry_delay)
                        continue
                    else:
                        return generate_mock_response(prompt)
                return result
            except json.JSONDecodeError as e:
                print(f"解析JSON失败 (尝试 {retry+1}/{max_retries}): {str(e)}")
                if retry < max_retries - 1:
                    print(f"等待 {retry_delay} 秒后重试...")
                    time.sleep(retry_delay)
                    continue
                else:
                    return generate_mock_response(prompt)
                    
        except requests.exceptions.Timeout as e:
            print(f"请求超时 (尝试 {retry+1}/{max_retries}): {str(e)}")
            if retry < max_retries - 1:
                print(f"等待 {retry_delay} 秒后重试...")
                time.sleep(retry_delay)
                continue
            else:
                print("所有重试均已失败，返回模拟响应")
                return generate_mock_response(prompt)
                
        except requests.RequestException as e:
            print(f"请求异常 (尝试 {retry+1}/{max_retries}): {str(e)}")
            if retry < max_retries - 1:
                print(f"等待 {retry_delay} 秒后重试...")
                time.sleep(retry_delay)
                continue
            else:
                return generate_mock_response(prompt)
                
        except Exception as e:
            print(f"未知错误 (尝试 {retry+1}/{max_retries}): {str(e)}")
            if retry < max_retries - 1:
                print(f"等待 {retry_delay} 秒后重试...")
                time.sleep(retry_delay)
                continue
            else:
                return generate_mock_response(prompt)
    
    # 如果所有重试都失败，返回模拟响应
    return generate_mock_response(prompt)

def generate_mock_response(prompt: str) -> Dict[str, Any]:
    """生成模拟响应（用于开发测试）"""
    # 分析用户答题模式的模拟响应
    if "分析用户的答题情况" in prompt or "analyze user" in prompt:
        return {
            "choices": [{
                "message": {
                    "content": json.dumps({
                        "weak_areas": ["细节理解", "数字信息", "词汇理解"],
                        "strong_areas": ["主旨理解", "推理判断", "语法结构"],
                        "error_patterns": "用户在涉及具体数字和细节的题目上表现较弱，特别是在快速对话和学术讲座中容易错过关键信息。",
                        "performance_score": 75,
                        "recommendation_criteria": {
                            "focus_tags": ["细节理解", "数字信息", "词汇理解"],
                            "preferred_topics": ["教育", "科技", "环保"]
                        }
                    })
                }
            }]
        }
    # 推荐材料的模拟响应
    elif "推荐最合适的听力材料" in prompt or "recommend materials" in prompt:
        return {
            "choices": [{
                "message": {
                    "content": json.dumps({
                        "recommendations": [
                            {
                                "id": "cet6_001",
                                "title": "CET6 听力训练 - 科技发展",
                                "reason": "该套题包含多个细节理解题型，特别关注数字信息的理解，与您的薄弱环节匹配度高。",
                                "match_score": 0.92
                            },
                            {
                                "id": "2022_06",
                                "title": "2022年六月四级听力真题第一套",
                                "reason": "这套材料专注于训练细节捕捉能力，包含大量需要理解具体数字和事实的题目。",
                                "match_score": 0.85
                            },
                            {
                                "id": "cet4_001",
                                "title": "CET4 听力训练 - 校园生活",
                                "reason": "该材料包含多个教育主题的听力段落，与您的兴趣领域匹配，同时侧重于细节理解能力的培养。",
                                "match_score": 0.78
                            }
                        ],
                        "improvement_suggestions": "建议在听力练习中特别注意记录关键数字信息，培养快速捕捉细节的能力。可以尝试使用笔记技巧，如使用符号和缩写记录听到的数字和关键词。同时，建议扩大词汇量，特别是常见听力材料中出现的专业词汇。"
                    })
                }
            }]
        }
    elif "evaluate_listening_level" in prompt:
        return {
            "choices": [{
                "message": {
                    "content": json.dumps({
                        "level": "CET4",
                        "recommended_material": "cet4_003",
                        "analysis": "用户在基础听力理解方面表现良好，但在细节把握和高级词汇理解方面有待提高。建议从CET4难度的材料开始训练。"
                    })
                }
            }]
        }
    elif "learning_feedback" in prompt:
        # 检查是否包含材料信息，以提供更相关的测试数据
        material_info = {}
        try:
            # 提取材料信息以生成更相关的测试数据
            material_start = prompt.find('"title"')
            if material_start > 0:
                material_snippet = prompt[material_start:material_start+200]
                material_title = ""
                if '"title"' in material_snippet:
                    title_start = material_snippet.find('"title"')
                    title_end = material_snippet.find('",', title_start)
                    if title_end > title_start:
                        material_title = material_snippet[title_start+9:title_end].strip()
            
            # 提取主题/话题
            topics = []
            if '"topic"' in prompt or '"topics"' in prompt:
                topic_key = '"topic"' if '"topic"' in prompt else '"topics"'
                topic_start = prompt.find(topic_key)
                if topic_start > 0:
                    topic_end = prompt.find(']', topic_start)
                    if topic_end > topic_start:
                        topics_str = prompt[topic_start:topic_end+1]
                        topics = [t.strip('"[] ') for t in topics_str.split(',') if t.strip('"[] ')]
            
            material_info = {
                "title": material_title,
                "topics": topics
            }
        except:
            pass
            
        # 基于材料信息生成相关反馈
        title = material_info.get("title", "")
        topics = material_info.get("topics", [])
        
        vocabulary = ["significant", "trend", "sustainable", "innovation", "comprehensive"]
        expressions = ["in terms of", "due to", "as a result of"]
        background = "该材料讨论了可再生能源的发展趋势与挑战。"
        structure = "新闻采用了问题-解决方案的结构，先介绍能源危机，再讨论可再生能源的解决方案。"
        
        # 根据主题调整反馈内容
        if "教育" in topics or "校园" in topics or "Education" in topics:
            vocabulary = ["curriculum", "academic", "assessment", "faculty", "enrollment"]
            expressions = ["in accordance with", "with respect to", "take into account"]
            background = "该材料围绕教育体系和校园生活展开，探讨了现代教育理念和学生发展需求。"
            structure = "对话从校园环境描述开始，逐步深入讨论教育改革和学生参与度问题，最后提出改进建议。"
            mistakes_analysis = {
                "2": "在这道题中，你选择了错误选项。听力中明确提到学生需要更多实践机会，但你可能被其他信息干扰。建议在听力时做好关键词笔记，尤其是表达观点和态度的部分。",
                "5": "这道题需要抓住具体数字信息。听力中提到'recreated 500 copies'，但你可能忽略了这个数字细节。建议在听数字信息时特别集中注意力，可以采用快速记数字的方法。"
            }
        elif "科技" in topics or "技术" in topics or "Technology" in topics:
            vocabulary = ["innovation", "algorithm", "interface", "deployment", "optimization"]
            expressions = ["cutting-edge", "state-of-the-art", "breakthrough in"]
            background = "该材料探讨了最新科技发展趋势及其对社会的影响，特别是人工智能和自动化领域的进展。"
            structure = "讲座从技术定义开始，然后介绍历史发展，接着分析当前应用，最后展望未来发展方向。"
            mistakes_analysis = {
                "3": "这道题考查了关于技术发明的细节理解。听力中描述了发明的功能，但你可能对这部分信息理解不充分。建议在听描述性内容时，注意听清楚功能、特点等关键信息。",
                "7": "这道题涉及到专有名词来源，需要对文化背景知识有一定了解。听力明确提到这些名称来源于罗马神话，但你可能错过了这个信息点。建议平时多积累一些背景知识，并在听力中注意这类细节信息。"
            }
        else:
            mistakes_analysis = {
                "8": "这道题考察了对对话中问题的识别。听力中男士问及'arm exercises raise blood pressure?'，女士回答'That they do'，表示确认这个问题。你可能对这种简短的肯定回答方式不够熟悉，建议多注意英语中各种表示肯定的表达方式。",
                "16": "这道题涉及到对数字信息的准确理解。听力中提到'more than 11 million undocumented people'，你需要从选项中找到最接近的数字。建议在听数字信息时，立即记下来，并在答题时仔细对比选项。"
            }
        
        return {
            "choices": [{
                "message": {
                    "content": json.dumps({
                        "vocabulary": vocabulary,
                        "expressions": expressions,
                        "background": background,
                        "structure": structure,
                        "mistakes_analysis": mistakes_analysis
                    })
                }
            }]
        }
    elif "speaking_tasks" in prompt:
        return {
            "choices": [{
                "message": {
                    "content": json.dumps({
                        "questions": [
                            {"type": "retell", "prompt": "请复述听力材料的主要内容。", "reference": "The material discusses the importance of renewable energy..."},
                            {"type": "summary", "prompt": "请总结文章的主要观点。", "reference": "The main points are..."},
                            {"type": "detail", "prompt": "演讲者提到了哪些可再生能源的例子？", "reference": "The speaker mentioned solar, wind, and hydroelectric power..."}
                        ]
                    })
                }
            }]
        }
    elif "evaluate_speaking" in prompt:
        return {
            "choices": [{
                "message": {
                    "content": json.dumps({
                        "pronunciation": "发音清晰，但在重音和语调方面需要改进。",
                        "fluency": "流利度良好，但有些停顿需要注意。",
                        "content": "内容准确，但可以增加更多细节和例子来丰富回答。",
                        "overall_score": 7.5,
                        "improvement_suggestions": [
                            "注意th和r的发音",
                            "练习连读和弱读",
                            "增加回答的具体例子"
                        ]
                    })
                }
            }]
        }
    else:
        return {
            "choices": [{
                "message": {
                    "content": json.dumps({
                        "response": "这是一个模拟响应，实际部署时请配置正确的DeepSeek API。",
                        "timestamp": time.time()
                    })
                }
            }]
        }
