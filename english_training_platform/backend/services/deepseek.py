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
            response.raise_for_status()
            
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

def evaluate_listening_level(user_answers: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    评估用户的听力水平
    
    Args:
        user_answers: 用户答题数据
        
    Returns:
        dict: 评估结果，包含难度等级和推荐材料
    """
    prompt = f"""
    根据以下用户的听力答题数据，评估其英语听力水平，并推荐适合的难度等级（CET4、CET6、IELTS、TOEFL）。
    输出JSON格式，包含难度等级、推荐材料ID和分析。
    
    用户答题数据：
    {json.dumps(user_answers, ensure_ascii=False)}
    """
    
    system_prompt = "你是一个专业的英语听力水平评估助手，请根据用户的答题情况给出客观评价和合适的难度推荐。"
    
    response = call_deepseek_api(prompt, system_prompt)
    
    try:
        content = response["choices"][0]["message"]["content"]
        # 尝试解析JSON
        if isinstance(content, str):
            result = json.loads(content)
        else:
            result = content
        return result
    except (KeyError, json.JSONDecodeError) as e:
        print(f"解析DeepSeek响应出错: {str(e)}")
        # 返回默认结果
        return {
            "level": "CET4",
            "recommended_material": "cet4_001",
            "analysis": "无法获取完整分析，建议从基础难度开始训练。"
        }

def generate_learning_feedback(material: Dict[str, Any], user_answers: List[Dict[str, Any]], transcript: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    生成学习反馈
    
    Args:
        material: 听力材料数据
        user_answers: 用户答题数据
        transcript: 听力原文数据（可选）
        
    Returns:
        dict: 学习反馈，包含重要单词、表达、背景知识、听力结构分析和针对错题的详细解释
    """
    # 准备提示词
    prompt_parts = [
        "作为英语听力学习助手，请根据以下信息为用户生成详细的学习反馈。",
        "用户已完成听力理解练习，现在需要针对性的反馈来提高听力能力。",
        "请认真分析用户的答题情况，特别关注错误回答，找出听力理解的薄弱环节。",
        "",
        "请以JSON格式输出，包含以下字段：",
        "- vocabulary: 材料中的重要词汇列表（5-10个单词）",
        "- expressions: 重要表达或短语列表（3-5个）",
        "- background: 材料相关背景知识（100-200字）",
        "- structure: 听力结构分析（80-150字）",
        "- mistakes_analysis: 针对用户答错题目的详细分析和建议"
    ]
    
    # 添加错题分析的特定指导
    error_questions = [a for a in user_answers if not a.get('is_correct', True)]
    if error_questions:
        prompt_parts.append(f"\n用户有{len(error_questions)}道题回答错误，请针对每道错题提供具体分析。")
        prompt_parts.append("对于每道错题，请提供以下分析（直接用自然语言描述，不要使用JSON格式）：")
        prompt_parts.append("1. 用户选错的原因（可能的理解障碍）")
        prompt_parts.append("2. 听力中包含的关键信息")
        prompt_parts.append("3. 具体的改进建议和听力技巧")
        prompt_parts.append("\n请确保分析语言通顺自然，像专业教师的点评一样，而不是机器生成的格式化文本。")
    else:
        prompt_parts.append("\n用户全部回答正确，请提供整体的听力技巧和进阶建议。")
    
    # 添加听力原文信息（如果有）
    if transcript:
        prompt_parts.append("\n听力原文：")
        if isinstance(transcript, dict):
            if 'sections' in transcript:
                # 提取听力原文的结构化内容
                sections_text = []
                for section in transcript.get('sections', []):
                    section_text = f"## {section.get('description', '部分')}\n\n"
                    for passage in section.get('passages', []):
                        section_text += f"### 段落 {passage.get('passage_id', '')}\n{passage.get('content', '')}\n\n"
                    sections_text.append(section_text)
                prompt_parts.append("\n".join(sections_text))
            else:
                # 如果没有结构化内容，直接使用transcript
                prompt_parts.append(json.dumps(transcript, ensure_ascii=False))
        else:
            prompt_parts.append(str(transcript))
    
    # 添加材料和用户答题情况
    prompt_parts.extend([
        "\n听力材料：",
        json.dumps(material, ensure_ascii=False),
        "\n用户答题情况：",
        json.dumps(user_answers, ensure_ascii=False)
    ])
    
    # 构建最终提示词
    prompt = "\n".join(prompt_parts)
    
    # 设置系统提示词
    system_prompt = """你是一个专业的英语听力教师，擅长分析听力理解问题并提供针对性的学习反馈。
请根据用户的学习材料、听力原文和答题情况，提供有价值的学习反馈，特别是针对用户答错的题目提供详细的解释和学习建议。
你的反馈应该既有针对性又有教育意义，帮助用户理解他们的错误并改进听力技能。

请确保输出为有效的JSON格式，但mistakes_analysis字段中的内容应该是自然流畅的教师点评，而不是结构化数据。
为每个错题提供详细分析时，请使用自然语言描述问题所在、关键信息和改进建议，语气亲切专业。

示例格式：
{
  "vocabulary": ["单词1", "单词2", ...],
  "expressions": ["表达1", "表达2", ...],
  "background": "背景知识...",
  "structure": "结构分析...",
  "mistakes_analysis": {
    "1": "这道题你选错了，主要是因为... 听力原文中其实提到... 建议你下次...",
    "5": "这道题的关键在于... 听力中明确说到... 提高这方面能力可以..."
  }
}"""
    
    max_attempts = 2
    for attempt in range(max_attempts):
        try:
            print(f"生成学习反馈 (尝试 {attempt+1}/{max_attempts})")
            response = call_deepseek_api(prompt, system_prompt)
            
            if not response or "choices" not in response or not response["choices"]:
                print("DeepSeek API返回的响应为空或格式不正确")
                if attempt < max_attempts - 1:
                    continue
                return generate_mock_feedback(material, user_answers)
            
            content = response["choices"][0]["message"]["content"]
            
            # 确保内容不为空
            if not content or not content.strip():
                print("DeepSeek API返回的内容为空")
                if attempt < max_attempts - 1:
                    continue
                return generate_mock_feedback(material, user_answers)
            
            # 尝试解析JSON
            try:
                # 清理可能的非JSON前缀和后缀
                content = content.strip()
                # 查找第一个 { 和最后一个 }
                start_idx = content.find('{')
                end_idx = content.rfind('}') + 1
                
                if start_idx >= 0 and end_idx > start_idx:
                    # 提取JSON部分
                    json_content = content[start_idx:end_idx]
                    result = json.loads(json_content)
                else:
                    # 如果找不到JSON标记，尝试直接解析
                    result = json.loads(content)
                
                # 确保结果包含所有需要的字段
                required_fields = ['vocabulary', 'expressions', 'background', 'structure']
                missing_fields = [field for field in required_fields if field not in result or not result[field]]
                
                if missing_fields:
                    print(f"响应缺少必要字段: {', '.join(missing_fields)}")
                    # 补充缺失的字段
                    mock_data = generate_mock_feedback(material, user_answers)
                    for field in missing_fields:
                        result[field] = mock_data[field]
                    
                # 如果没有错题分析字段但有错题，添加错题分析
                if error_questions and ('mistakes_analysis' not in result or not result['mistakes_analysis']):
                    print("响应缺少错题分析，添加模拟分析")
                    mock_data = generate_mock_feedback(material, user_answers)
                    result['mistakes_analysis'] = mock_data['mistakes_analysis']
                
                # 处理错题分析格式，使其更加人性化
                if 'mistakes_analysis' in result and isinstance(result['mistakes_analysis'], dict):
                    processed_analysis = {}
                    for question_id, analysis in result['mistakes_analysis'].items():
                        # 检查是否是JSON格式的字符串
                        if isinstance(analysis, str) and (analysis.startswith('{') or '"key_information"' in analysis or '"why_wrong"' in analysis or '"suggestion"' in analysis):
                            try:
                                # 尝试解析JSON
                                analysis_data = json.loads(analysis) if analysis.startswith('{') else {"content": analysis}
                                
                                # 构建人性化的错题分析文本
                                formatted_text = ""
                                
                                # 添加错误原因
                                if "why_wrong" in analysis_data:
                                    formatted_text += f"{analysis_data['why_wrong']}\n\n"
                                
                                # 添加关键信息
                                if "key_information" in analysis_data:
                                    formatted_text += f"听力中的关键信息：{analysis_data['key_information']}\n\n"
                                
                                # 添加建议
                                if "suggestion" in analysis_data:
                                    formatted_text += f"提升建议：{analysis_data['suggestion']}"
                                
                                # 如果没有成功提取结构化内容，则使用原始文本
                                if not formatted_text and "content" in analysis_data:
                                    formatted_text = analysis_data["content"]
                                elif not formatted_text:
                                    formatted_text = analysis
                                
                                processed_analysis[question_id] = formatted_text
                            except:
                                # 如果解析失败，保留原始文本
                                processed_analysis[question_id] = analysis
                        else:
                            processed_analysis[question_id] = analysis
                    
                    # 更新错题分析
                    result['mistakes_analysis'] = processed_analysis
                
                return result
                
            except json.JSONDecodeError as e:
                print(f"解析DeepSeek响应内容为JSON失败 (尝试 {attempt+1}/{max_attempts}): {str(e)}")
                print(f"原始内容: {content[:200]}...")
                
                if attempt < max_attempts - 1:
                    # 修改系统提示，更强调JSON格式
                    system_prompt = "你是专业的英语学习助手。请严格以JSON格式输出分析结果，不要包含任何额外文本。确保输出可以被json.loads()直接解析。格式示例：{\"vocabulary\": [\"word1\"], \"expressions\": [\"expr1\"], \"background\": \"text\", \"structure\": \"text\", \"mistakes_analysis\": {\"1\": \"analysis\"}}"
                    continue
                
                # 所有尝试都失败，使用模拟数据
                return generate_mock_feedback(material, user_answers)
        
        except Exception as e:
            print(f"生成学习反馈过程中出错 (尝试 {attempt+1}/{max_attempts}): {str(e)}")
            if attempt < max_attempts - 1:
                continue
            return generate_mock_feedback(material, user_answers)
    
    # 如果所有尝试都失败，返回模拟数据
    return generate_mock_feedback(material, user_answers)

def generate_mock_feedback(material: Dict[str, Any], user_answers: List[Dict[str, Any]]) -> Dict[str, Any]:
    """生成模拟的学习反馈（当API调用失败时使用）"""
    # 提取材料信息
    title = material.get('title', '')
    topics = material.get('topic', material.get('topics', []))
    
    # 默认反馈内容
    vocabulary = ["significant", "trend", "sustainable", "innovation", "comprehensive"]
    expressions = ["in terms of", "due to", "as a result of"]
    background = "该材料讨论了相关领域的发展趋势与挑战。请多听此类材料以提高理解能力。"
    structure = "材料采用了总-分-总的结构，先引入主题，然后展开讨论，最后总结观点。"
    
    # 找出用户答错的题目
    mistakes = {}
    for answer in user_answers:
        if not answer.get('is_correct', True):
            question_id = answer.get('question_id', '')
            if question_id:
                mistakes[str(question_id)] = f"您在第{question_id}题的回答有误。请注意听力中的关键词和细节信息，特别是事实类信息和数字部分。建议多听几遍，集中注意力。"
    
    # 如果没有错题，提供一般性建议
    if not mistakes:
        mistakes = "您的答题表现很好！继续保持，可以尝试更高难度的听力材料。"
    
    # 根据主题调整反馈内容
    if any(t in ['教育', '校园', 'Education'] for t in topics):
        vocabulary = ["curriculum", "academic", "assessment", "faculty", "enrollment"]
        expressions = ["in accordance with", "with respect to", "take into account"]
        background = "该材料围绕教育体系和校园生活展开，探讨了现代教育理念和学生发展需求。"
        structure = "对话从校园环境描述开始，逐步深入讨论教育改革和学生参与度问题，最后提出改进建议。"
    elif any(t in ['科技', '技术', 'Technology'] for t in topics):
        vocabulary = ["innovation", "algorithm", "interface", "deployment", "optimization"]
        expressions = ["cutting-edge", "state-of-the-art", "breakthrough in"]
        background = "该材料探讨了最新科技发展趋势及其对社会的影响，特别是人工智能和自动化领域的进展。"
        structure = "讲座从技术定义开始，然后介绍历史发展，接着分析当前应用，最后展望未来发展方向。"
    
    return {
        "vocabulary": vocabulary,
        "expressions": expressions,
        "background": background,
        "structure": structure,
        "mistakes_analysis": mistakes
    }

def generate_speaking_tasks(material: Dict[str, Any]) -> Dict[str, Any]:
    """
    基于听力材料生成口语任务
    
    Args:
        material: 听力材料数据
        
    Returns:
        dict: 口语任务，包含复述、总结和细节问题等
    """
    prompt = f"""
    根据以下听力材料，生成与内容相关的口语试题，包括复述任务、总结任务和细节问题，提供参考答案。输出JSON格式。
    
    听力材料：
    {json.dumps(material, ensure_ascii=False)}
    """
    
    system_prompt = "你是一个专业的英语口语教练，请设计与材料内容紧密相关、由浅入深的口语练习题目。"
    
    response = call_deepseek_api(prompt, system_prompt)
    
    try:
        content = response["choices"][0]["message"]["content"]
        # 尝试解析JSON
        if isinstance(content, str):
            result = json.loads(content)
        else:
            result = content
        return result
    except (KeyError, json.JSONDecodeError) as e:
        print(f"解析DeepSeek响应出错: {str(e)}")
        # 返回默认结果
        return {
            "questions": [
                {"type": "retell", "prompt": "请复述听力材料的主要内容。", "reference": "参考答案..."},
                {"type": "summary", "prompt": "请总结文章的主要观点。", "reference": "参考答案..."},
                {"type": "detail", "prompt": "详细问题示例", "reference": "参考答案..."}
            ]
        }

def evaluate_speaking(audio_data: str, question: str, reference_answer: Optional[str] = None) -> Dict[str, Any]:
    """
    评估用户的口语
    
    Args:
        audio_data: 音频数据（Base64编码）
        question: 口语问题
        reference_answer: 参考答案（可选）
        
    Returns:
        dict: 评估结果，包含发音、流利度和内容准确性评价
    """
    # 在实际项目中，需要处理音频数据，可能需要转录为文本
    # 这里假设已经有了转录文本，简化处理
    # 在实际项目中可以考虑使用DeepSeek的语音识别API或其他服务
    
    # 简化模拟：假设音频数据的前100字符是转录文本
    transcription = audio_data[:100] if len(audio_data) > 100 else audio_data
    
    prompt = f"""
    评估以下口语录音的发音、流利度和内容准确性，提供改进建议。输出JSON格式。
    
    问题：{question}
    
    用户回答（转录）：{transcription}
    """
    
    if reference_answer:
        prompt += f"\n参考答案：{reference_answer}"
    
    system_prompt = "你是一个专业的英语口语评估师，请对用户的口语表现给出客观、全面的评价，并提供有针对性的改进建议。"
    
    response = call_deepseek_api(prompt, system_prompt)
    
    try:
        content = response["choices"][0]["message"]["content"]
        # 尝试解析JSON
        if isinstance(content, str):
            result = json.loads(content)
        else:
            result = content
        return result
    except (KeyError, json.JSONDecodeError) as e:
        print(f"解析DeepSeek响应出错: {str(e)}")
        # 返回默认结果
        return {
            "pronunciation": "发音评价",
            "fluency": "流利度评价",
            "content": "内容准确性评价",
            "overall_score": 7.0,
            "improvement_suggestions": [
                "改进建议1",
                "改进建议2",
                "改进建议3"
            ]
        } 