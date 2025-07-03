import json
import time
from typing import Dict, List, Any, Optional
from .api_client import call_deepseek_api

def log_debug(message):
    """记录调试信息"""
    print(f"[DEBUG][{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}")

def evaluate_listening_level(user_answers: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    评估用户的听力水平
    
    Args:
        user_answers: 用户答题数据
        
    Returns:
        dict: 评估结果，包含难度等级和推荐材料
    """
    log_debug(f"开始评估听力水平，答题数据数量: {len(user_answers)}")
    
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
        log_debug(f"听力水平评估完成，结果: {result['level']}")
        return result
    except (KeyError, json.JSONDecodeError) as e:
        log_debug(f"解析DeepSeek响应出错: {str(e)}")
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
    log_debug(f"开始生成学习反馈，材料ID: {material.get('id', '未知')}")
    
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
            log_debug(f"生成学习反馈 (尝试 {attempt+1}/{max_attempts})")
            response = call_deepseek_api(prompt, system_prompt)
            
            if not response or "choices" not in response or not response["choices"]:
                log_debug("DeepSeek API返回的响应为空或格式不正确")
                if attempt < max_attempts - 1:
                    continue
                return generate_mock_feedback(material, user_answers)
            
            content = response["choices"][0]["message"]["content"]
            
            # 确保内容不为空
            if not content or not content.strip():
                log_debug("DeepSeek API返回的内容为空")
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
                    log_debug(f"响应缺少必要字段: {', '.join(missing_fields)}")
                    # 补充缺失的字段
                    mock_data = generate_mock_feedback(material, user_answers)
                    for field in missing_fields:
                        result[field] = mock_data[field]
                    
                # 如果没有错题分析字段但有错题，添加错题分析
                if error_questions and ('mistakes_analysis' not in result or not result['mistakes_analysis']):
                    log_debug("响应缺少错题分析，添加模拟分析")
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
                            except Exception as e:
                                log_debug(f"解析错题分析失败: {str(e)}")
                                processed_analysis[question_id] = analysis
                        else:
                            processed_analysis[question_id] = analysis
                
                result['mistakes_analysis'] = processed_analysis
                return result
            except Exception as e:
                log_debug(f"解析DeepSeek响应出错: {str(e)}")
                return generate_mock_feedback(material, user_answers)
        except Exception as e:
            log_debug(f"生成学习反馈时出错: {str(e)}")
            return generate_mock_feedback(material, user_answers)

def generate_mock_feedback(material: Dict[str, Any], user_answers: List[Dict[str, Any]]) -> Dict[str, Any]:
    """生成模拟的学习反馈（当API调用失败时使用）"""
    log_debug("使用模拟数据生成学习反馈")
    
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
