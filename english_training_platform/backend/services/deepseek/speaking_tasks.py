import json
import time
from typing import Dict, List, Any, Optional
from .api_client import call_deepseek_api

def log_debug(message):
    """记录调试信息"""
    print(f"[DEBUG][{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}")

def generate_speaking_tasks(material: Dict[str, Any], user_answers: List[Dict[str, Any]] = None, score: int = None) -> Dict[str, Any]:
    """
    基于听力材料生成口语任务
    
    Args:
        material: 听力材料数据
        user_answers: 用户的答题情况，包含正确和错误的回答
        score: 用户的得分
        
    Returns:
        dict: 口语任务，包含复述、总结和细节问题等
    """
    log_debug(f"开始生成口语任务，材料ID: {material.get('id', '未知')}")
    
    # 如果有用户答题数据，则针对错误点生成更有针对性的口语任务
    if user_answers and isinstance(user_answers, list) and len(user_answers) > 0:
        log_debug(f"基于用户答题情况生成针对性口语任务，得分: {score}")
        
        # 找出用户错误的问题
        errors = [answer for answer in user_answers if answer.get('isCorrect') is False]
        error_topics = [error.get('questionTopic', '') for error in errors if 'questionTopic' in error]
        
        prompt = f"""
        请根据以下听力材料和用户的错误点，生成针对性的口语练习题。
        
        返回格式必须是以下JSON格式，且包含questions字段：
        {{
          "questions": [
            {{
              "type": "retell|summary|opinion",
              "prompt": "口语练习问题...",
              "reference": "参考答案..."
            }},
            // 更多问题...
          ]
        }}

        听力材料：
        {json.dumps(material, ensure_ascii=False)}
        
        用户得分：{score}
        
        用户错误点：
        {json.dumps(errors, ensure_ascii=False)}
        
        错误涉及的主题：{', '.join(error_topics)}
        """
        
        system_prompt = "你是一个专业的英语口语教练，请严格按照JSON格式要求，设计针对用户听力弱点的口语练习题目，帮助用户提高这些方面的能力。"
    else:
        prompt = f"""
        请根据以下听力材料，生成与内容相关的口语试题，包括复述任务、总结任务和细节问题，提供参考答案。
        
        返回格式必须是以下JSON格式，且包含questions字段：
        {{
          "questions": [
            {{
              "type": "retell|summary|opinion",
              "prompt": "口语练习问题...",
              "reference": "参考答案..."
            }},
            // 更多问题...
          ]
        }}

        听力材料：
        {json.dumps(material, ensure_ascii=False)}
        """
        
        system_prompt = "你是一个专业的英语口语教练，请严格按照JSON格式要求，设计与材料内容紧密相关、由浅入深的口语练习题目。"
    
    # 设置最大重试次数
    max_retries = 2
    
    for retry in range(max_retries):
        try:
            log_debug(f"调用DeepSeek API生成口语任务 (尝试 {retry+1}/{max_retries})")
            response = call_deepseek_api(prompt, system_prompt)
            
            if not response or "choices" not in response or not response["choices"]:
                log_debug(f"API响应格式不正确 (尝试 {retry+1}/{max_retries})")
                if retry < max_retries - 1:
                    continue
                else:
                    return generate_default_speaking_tasks(material, user_answers, score)
            
            content = response["choices"][0]["message"]["content"]
            
            # 记录实际返回的内容(前100字符)，用于调试
            log_debug(f"API返回内容预览: {content[:100]}...")
            
            # 验证内容
            if not content or not content.strip():
                log_debug(f"API响应内容为空 (尝试 {retry+1}/{max_retries})")
                if retry < max_retries - 1:
                    continue
                else:
                    return generate_default_speaking_tasks(material, user_answers, score)
            
            # 尝试解析JSON
            try:
                # 清理可能的非JSON前缀和后缀
                content = content.strip()
                
                # 手动构建问题列表的方法
                if "questions" not in content.lower() and "\"prompt\"" in content:
                    log_debug("未找到questions字段但发现prompt字段，尝试手动构建问题列表")
                    
                    # 尝试提取问题
                    questions = []
                    # 寻找包含prompt和reference的部分
                    import re
                    pattern = r'["\'](type|prompt|reference)["\']\s*:\s*["\']([^"\']+)["\']'
                    matches = re.findall(pattern, content)
                    
                    # 重组问题
                    current_q = {}
                    for key, value in matches:
                        current_q[key] = value
                        if len(current_q) == 3:  # 有type, prompt和reference就是一个完整问题
                            questions.append(current_q)
                            current_q = {}
                    
                    if questions:
                        return {"questions": questions}
                
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
                
                # 检查是否包含questions字段，或者尝试适配其他可能的字段名
                if "questions" not in result:
                    # 尝试常见的替代字段名
                    alternative_fields = ["speaking_tasks", "tasks", "oral_practice", "exercises", "items"]
                    for field in alternative_fields:
                        if field in result and isinstance(result[field], list):
                            log_debug(f"找到替代字段: {field}，将其映射到questions")
                            result["questions"] = result[field]
                            break
                
                # 尝试从其他字段构建questions
                if "questions" not in result:
                    # 检查是否直接是一个问题列表
                    if isinstance(result, list) and len(result) > 0:
                        if all(isinstance(item, dict) for item in result):
                            log_debug("API返回直接是问题列表，将其包装到questions字段")
                            return {"questions": result}
                    
                    # 检查是否有题目相关字段但没有按预期格式
                    questions_data = []
                    for key, value in result.items():
                        if isinstance(value, dict) and "prompt" in value:
                            q_type = value.get("type", "retell")
                            questions_data.append({
                                "type": q_type,
                                "prompt": value["prompt"],
                                "reference": value.get("reference", "Reference answer not provided")
                            })
                    
                    if questions_data:
                        log_debug(f"从非标准格式中构建了{len(questions_data)}个问题")
                        return {"questions": questions_data}
                
                # 验证结果包含questions字段
                if "questions" not in result or not result["questions"]:
                    log_debug(f"API响应缺少questions字段 (尝试 {retry+1}/{max_retries})")
                    log_debug(f"API响应内容: {content}")
                    if retry < max_retries - 1:
                        continue
                    else:
                        return generate_default_speaking_tasks(material, user_answers, score)
                
                # 成功解析
                log_debug(f"成功生成口语任务，共{len(result['questions'])}个问题")
                return result
                
            except json.JSONDecodeError as e:
                log_debug(f"解析JSON失败 (尝试 {retry+1}/{max_retries}): {str(e)}")
                log_debug(f"JSON内容: {content}")
                if retry < max_retries - 1:
                    continue
                else:
                    return generate_default_speaking_tasks(material, user_answers, score)
        
        except Exception as e:
            log_debug(f"生成口语任务时出错 (尝试 {retry+1}/{max_retries}): {str(e)}")
            if retry < max_retries - 1:
                continue
            else:
                return generate_default_speaking_tasks(material, user_answers, score)
    
    # 如果所有尝试都失败
    return generate_default_speaking_tasks(material, user_answers, score)

def generate_default_speaking_tasks(material: Dict[str, Any], user_answers: List[Dict[str, Any]] = None, score: int = None) -> Dict[str, Any]:
    """
    生成默认的口语任务，当API调用失败时使用
    
    Args:
        material: 听力材料数据
        user_answers: 用户的答题情况
        score: 用户的得分
        
    Returns:
        dict: 默认口语任务
    """
    log_debug("使用默认任务生成口语题目")
    
    # 获取材料标题和主题
    title = material.get("title", "")
    topics = material.get("topics", material.get("topic", []))
    if not isinstance(topics, list):
        topics = [topics] if topics else []
    
    # 如果有用户答题数据，尝试基于错误点生成更针对性的任务
    if user_answers and isinstance(user_answers, list) and len(user_answers) > 0:
        # 找出用户错误的问题和相关主题
        errors = [answer for answer in user_answers if answer.get('isCorrect') is False]
        error_topics = list(set([error.get('questionTopic', '') for error in errors if 'questionTopic' in error]))
        
        if error_topics:
            log_debug(f"基于用户错误主题生成默认任务: {', '.join(error_topics)}")
            questions = [
                {
                    "type": "retell", 
                    "prompt": f"请复述听力材料中关于{error_topics[0]}的部分。", 
                    "reference": f"The part about {error_topics[0]} in the material discusses..."
                },
                {
                    "type": "summary", 
                    "prompt": f"请总结听力材料中关于{', '.join(error_topics[:2])}的关键信息。", 
                    "reference": f"The key information about {', '.join(error_topics[:2])} includes..."
                },
                {
                    "type": "opinion", 
                    "prompt": f"针对{error_topics[0]}这个话题，请表达你的观点。", 
                    "reference": f"Regarding {error_topics[0]}, I believe that..."
                }
            ]
            return {"questions": questions}
    
    # 根据主题生成不同的默认问题
    if any(t in ['教育', '校园', 'Education'] for t in topics):
        questions = [
            {
                "type": "retell", 
                "prompt": "请复述这段教育相关材料的主要内容。", 
                "reference": "The material discusses educational reforms and campus life..."
            },
            {
                "type": "summary", 
                "prompt": "请总结本段材料中提到的主要教育理念。", 
                "reference": "The main educational concepts mentioned include..."
            },
            {
                "type": "opinion", 
                "prompt": "你认为如何提高学生的学习参与度？", 
                "reference": "To improve student engagement, we could..."
            }
        ]
    elif any(t in ['科技', '技术', 'Technology'] for t in topics):
        questions = [
            {
                "type": "retell", 
                "prompt": "请复述这段关于科技发展的材料内容。", 
                "reference": "The material covers recent technological developments..."
            },
            {
                "type": "summary", 
                "prompt": "请总结材料中提到的技术创新的主要优势。", 
                "reference": "The main advantages of the technological innovations mentioned are..."
            },
            {
                "type": "opinion", 
                "prompt": "你认为这些新技术会如何影响人们的日常生活？", 
                "reference": "These new technologies will affect daily life by..."
            }
        ]
    else:
        # 通用问题
        questions = [
            {
                "type": "retell", 
                "prompt": f"请复述《{title}》的主要内容。", 
                "reference": "The material discusses..."
            },
            {
                "type": "summary", 
                "prompt": "请总结听力材料中的关键观点。", 
                "reference": "The key points made in the material are..."
            },
            {
                "type": "opinion", 
                "prompt": "你对材料中讨论的话题有什么看法？", 
                "reference": "In my opinion, the topic discussed in the material..."
            }
        ]
    
    return {
        "questions": questions
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
    log_debug(f"开始评估口语回答，问题: {question[:30]}...")
    
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
        log_debug("口语评估完成")
        return result
    except (KeyError, json.JSONDecodeError) as e:
        log_debug(f"解析DeepSeek响应出错: {str(e)}")
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
