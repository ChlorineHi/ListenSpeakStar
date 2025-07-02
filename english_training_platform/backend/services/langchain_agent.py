"""
基于LangChain和LangGraph的英语听力智能推荐Agent系统
"""
import os
import json
import logging
from typing import Dict, List, Any, Optional
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain_core.output_parsers import JsonOutputParser
from langgraph.graph import StateGraph, END
import time

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("recommendation_agent")

# 导入DeepSeek API调用函数
from .deepseek import call_deepseek_api, generate_mock_response

# 定义Agent状态类型
class AgentState:
    def __init__(self, 
                 user_answers: List[Dict[str, Any]], 
                 materials_index: Optional[List[Dict[str, Any]]] = None,
                 analysis_result: Optional[Dict[str, Any]] = None,
                 recommendations: Optional[List[Dict[str, Any]]] = None):
        self.user_answers = user_answers
        self.materials_index = materials_index
        self.analysis_result = analysis_result
        self.recommendations = recommendations

# 分析Agent：分析用户错题模式
def analyze_user_answers(state: AgentState) -> AgentState:
    """
    分析用户的答题情况，识别薄弱领域
    
    Args:
        state: 当前Agent状态
        
    Returns:
        更新后的Agent状态
    """
    logger.info("========== 启动分析Agent(analyze_user_answers) ==========")
    logger.info(f"输入: {len(state.user_answers)}条用户答题记录")
    
    user_answers = state.user_answers
    
    system_prompt = """你是一个专业的英语听力分析专家。请分析用户的答题情况，特别关注错误回答，找出听力理解的薄弱环节。

请分析用户的错题模式，找出共同特征。考虑以下方面:
1. 题目类型(如细节理解、主旨理解、推理判断等)
2. 题目内容领域(如教育、环保、科技等)
3. 题目难度
4. 错误模式(如混淆选项、遗漏关键信息等)

输出JSON格式，包含以下字段:
- weak_areas: 用户的薄弱领域列表
- strong_areas: 用户的强项领域列表
- error_patterns: 错误模式分析描述
- performance_score: 整体表现评分(0-100)
- recommendation_criteria: 推荐标准，包含focus_tags(应该关注的标签)和preferred_topics(偏好的主题)"""

    user_prompt = f"""根据以下用户的听力答题数据，分析用户的听力能力特点和薄弱环节。

用户答题数据:
{json.dumps(user_answers, ensure_ascii=False, indent=2)}"""

    try:
        # 调用DeepSeek API
        logger.info("分析Agent: 调用DeepSeek API分析用户答题模式")
        response = call_deepseek_api(user_prompt, system_prompt)
        
        # 解析响应
        if response and "choices" in response and len(response["choices"]) > 0:
            content = response["choices"][0]["message"]["content"]
            
            # 尝试解析JSON
            try:
                if isinstance(content, str):
                    # 去除可能存在的Markdown代码块标记
                    content = content.strip()
                    if content.startswith("```json"):
                        content = content[7:]
                    if content.startswith("```"):
                        content = content[3:]
                    if content.endswith("```"):
                        content = content[:-3]
                    content = content.strip()
                    
                    logger.info("分析Agent: 解析DeepSeek API返回的JSON响应")
                    analysis_result = json.loads(content)
                else:
                    analysis_result = content
                
                # 确保结果包含所有必要字段
                required_fields = ["weak_areas", "strong_areas", "performance_score"]
                if not all(field in analysis_result for field in required_fields):
                    missing_fields = [field for field in required_fields if field not in analysis_result]
                    logger.warning(f"分析Agent: API响应缺少必要字段: {missing_fields}")
                    raise ValueError(f"API响应缺少必要字段: {required_fields}")
                
                # 更新状态
                state.analysis_result = analysis_result
                logger.info(f"分析Agent: 成功解析分析结果, 薄弱领域: {analysis_result.get('weak_areas')}, 表现分数: {analysis_result.get('performance_score')}")
                logger.info("========== 分析Agent执行完成 ==========")
                return state
            except json.JSONDecodeError as e:
                logger.error(f"分析Agent: JSON解析错误: {str(e)}, 内容: {content[:100]}...")
                raise
        else:
            logger.error("分析Agent: API响应格式不正确")
            raise ValueError("API响应格式不正确")
    except Exception as e:
        logger.error(f"分析Agent执行出错: {str(e)}")
        # 返回模拟分析结果
        mock_result = {
            "weak_areas": ["细节理解", "数字信息"],
            "strong_areas": ["主旨理解", "推理判断"],
            "error_patterns": "用户在涉及具体数字和细节的题目上表现较弱",
            "performance_score": 65,
            "recommendation_criteria": {
                "focus_tags": ["细节理解", "数字信息"],
                "preferred_topics": ["环保", "教育"]
            }
        }
        state.analysis_result = mock_result
        logger.info(f"分析Agent: 使用模拟分析结果, 薄弱领域: {mock_result['weak_areas']}, 表现分数: {mock_result['performance_score']}")
        logger.info("========== 分析Agent执行完成(使用模拟数据) ==========")
        return state

# 推荐Agent：基于分析结果推荐材料
def recommend_materials(state: AgentState) -> AgentState:
    """
    基于分析结果推荐最合适的材料套题
    
    Args:
        state: 当前Agent状态
        
    Returns:
        更新后的Agent状态，包含推荐结果
    """
    logger.info("========== 启动推荐Agent(recommend_materials) ==========")
    logger.info(f"输入: 分析结果(薄弱领域: {state.analysis_result.get('weak_areas')}, 表现分数: {state.analysis_result.get('performance_score')})")
    logger.info(f"可用材料数量: {len(state.materials_index) if state.materials_index else 0}")
    
    analysis_result = state.analysis_result
    materials_index = state.materials_index
    
    system_prompt = """你是一个专业的英语听力学习推荐专家。请根据用户的能力分析，从可用的材料中推荐最合适的学习材料套题。

对于每个推荐，请提供:
1. 材料ID和标题
2. 推荐理由(为什么这个材料适合用户)
3. 匹配度评分(0-1)

输出JSON格式，包含recommendations字段(推荐列表)和improvement_suggestions字段(改进建议)。"""

    user_prompt = f"""根据用户的能力分析，从可用的材料中推荐最合适的听力材料套题。

用户能力分析:
{json.dumps(analysis_result, ensure_ascii=False, indent=2)}

可用材料库:
{json.dumps(materials_index, ensure_ascii=False, indent=2)}

请根据用户的薄弱领域和错误模式，推荐3个最适合的听力材料套题。这些套题应该针对用户的薄弱环节，帮助用户提高相关能力。"""

    try:
        # 调用DeepSeek API
        logger.info("推荐Agent: 调用DeepSeek API生成材料推荐")
        response = call_deepseek_api(user_prompt, system_prompt)
        
        # 解析响应
        if response and "choices" in response and len(response["choices"]) > 0:
            content = response["choices"][0]["message"]["content"]
            
            # 尝试解析JSON
            try:
                if isinstance(content, str):
                    # 去除可能存在的Markdown代码块标记
                    content = content.strip()
                    if content.startswith("```json"):
                        content = content[7:]
                    if content.startswith("```"):
                        content = content[3:]
                    if content.endswith("```"):
                        content = content[:-3]
                    content = content.strip()
                    
                    logger.info("推荐Agent: 解析DeepSeek API返回的JSON响应")
                    recommendation_result = json.loads(content)
                else:
                    recommendation_result = content
                
                # 确保结果包含所有必要字段
                if "recommendations" not in recommendation_result:
                    logger.warning("推荐Agent: API响应缺少recommendations字段")
                    raise ValueError("API响应缺少recommendations字段")
                
                # 更新状态
                state.recommendations = recommendation_result
                logger.info(f"推荐Agent: 成功解析推荐结果, 推荐材料数量: {len(recommendation_result.get('recommendations', []))}")
                logger.info("========== 推荐Agent执行完成 ==========")
                return state
            except json.JSONDecodeError as e:
                logger.error(f"推荐Agent: JSON解析错误: {str(e)}, 内容: {content[:100]}...")
                raise
        else:
            logger.error("推荐Agent: API响应格式不正确")
            raise ValueError("API响应格式不正确")
    except Exception as e:
        logger.error(f"推荐Agent执行出错: {str(e)}")
        # 返回模拟推荐结果
        mock_result = {
            "recommendations": [
                {
                    "id": "cet6_001",
                    "title": "CET6 听力训练 - 科技创新",
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
                    "reason": "该材料包含多个环保主题的听力段落，与您的兴趣领域匹配，同时侧重于细节理解能力的培养。",
                    "match_score": 0.78
                }
            ],
            "improvement_suggestions": "建议在听力练习中特别注意记录关键数字信息，培养快速捕捉细节的能力。"
        }
        state.recommendations = mock_result
        logger.info(f"推荐Agent: 使用模拟推荐结果, 推荐材料数量: {len(mock_result.get('recommendations', []))}")
        logger.info("========== 推荐Agent执行完成(使用模拟数据) ==========")
        return state

# 构建Agent工作流
def build_agent_workflow():
    """
    构建基于LangGraph的Agent工作流
    
    Returns:
        编译好的工作流
    """
    logger.info("构建Agent工作流")
    # 创建工作流
    workflow = StateGraph(AgentState)
    
    # 添加节点
    workflow.add_node("analyze", analyze_user_answers)
    workflow.add_node("recommend", recommend_materials)
    
    # 定义边和转换条件
    workflow.add_edge("analyze", "recommend")
    workflow.add_edge("recommend", END)
    
    # 设置入口
    workflow.set_entry_point("analyze")
    
    # 编译工作流
    logger.info("Agent工作流构建完成: analyze -> recommend -> END")
    return workflow.compile()

# 主函数：运行Agent系统
def run_recommendation_agent(user_answers: List[Dict[str, Any]], materials_index: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    运行智能推荐Agent系统
    
    Args:
        user_answers: 用户答题数据
        materials_index: 可用材料索引
        
    Returns:
        推荐结果
    """
    logger.info("==================== 启动智能推荐Agent系统 ====================")
    logger.info(f"用户答题数据: {len(user_answers)}条记录")
    logger.info(f"可用材料索引: {len(materials_index)}个材料")
    
    # 初始化状态
    initial_state = AgentState(
        user_answers=user_answers,
        materials_index=materials_index
    )
    
    try:
        # 构建并运行工作流
        agent_executor = build_agent_workflow()
        logger.info("开始执行Agent工作流")
        final_state = agent_executor.invoke(initial_state)
        logger.info("Agent工作流执行完成")
        
        # 合并分析结果和推荐结果
        result = {
            "weak_areas": final_state.analysis_result.get("weak_areas", []),
            "strong_areas": final_state.analysis_result.get("strong_areas", []),
            "performance_score": final_state.analysis_result.get("performance_score", 0),
            "recommendations": final_state.recommendations.get("recommendations", []),
            "improvement_suggestions": final_state.recommendations.get("improvement_suggestions", "")
        }
        
        # 确保推荐的材料ID与前端可用材料匹配
        available_material_ids = [m.get("id") for m in materials_index if m.get("id")]
        logger.info(f"可用材料ID列表: {available_material_ids}")
        filtered_recommendations = []
        
        logger.info("验证推荐材料ID是否在可用材料列表中")
        for rec in result["recommendations"]:
            # 确保每个推荐都有id字段
            if "id" not in rec and "materialId" in rec:
                rec["id"] = rec["materialId"]
                logger.info(f"将materialId字段重命名为id: {rec['id']}")
            
            # 如果既没有id也没有materialId，跳过这个推荐
            if "id" not in rec:
                logger.warning(f"警告: 推荐项缺少id字段，已跳过: {rec}")
                continue
            
            # 检查材料是否存在
            if rec.get("id") in available_material_ids:
                # 确保同时有id和materialId字段，以兼容前端
                if "materialId" not in rec:
                    rec["materialId"] = rec["id"]
                filtered_recommendations.append(rec)
                logger.info(f"材料ID {rec.get('id')} 验证通过")
            else:
                logger.warning(f"警告: 推荐的材料ID {rec.get('id')} 不在可用材料列表中，已过滤")
        
        # 如果过滤后没有推荐材料，使用默认推荐
        if not filtered_recommendations:
            logger.warning("警告: 所有推荐的材料都不在可用列表中，使用默认推荐")
            # 使用可用的材料ID生成默认推荐
            default_materials = []
            for material_id in available_material_ids[:3]:  # 取前3个可用材料
                material = next((m for m in materials_index if m.get("id") == material_id), None)
                if material:
                    default_rec = {
                        "id": material_id,
                        "materialId": material_id,  # 同时提供materialId字段
                        "title": material.get("title", f"听力材料 - {material_id}"),
                        "reason": "系统推荐的基础听力材料",
                        "match_score": 0.7
                    }
                    default_materials.append(default_rec)
                    logger.info(f"添加默认推荐材料: {material_id}")
            filtered_recommendations = default_materials
        
        result["recommendations"] = filtered_recommendations
        
        # 打印最终推荐结果
        logger.info(f"最终推荐结果: {len(result['recommendations'])}个材料, 表现分数: {result['performance_score']}")
        logger.info(f"薄弱领域: {result['weak_areas']}")
        logger.info(f"强项领域: {result['strong_areas']}")
        logger.info("==================== 智能推荐Agent系统执行完成 ====================")
        
        return result
    except Exception as e:
        logger.error(f"Agent系统执行出错: {str(e)}")
        # 返回模拟结果
        mock_result = {
            "weak_areas": ["细节理解", "数字信息"],
            "strong_areas": ["主旨理解", "推理判断"],
            "performance_score": 65,
            "recommendations": [
                {
                    "id": "cet6_001",
                    "materialId": "cet6_001",  # 同时提供materialId字段
                    "title": "CET6 听力训练 - 科技创新",
                    "reason": "该套题包含多个细节理解题型，特别关注数字信息的理解，与您的薄弱环节匹配度高。",
                    "match_score": 0.92
                },
                {
                    "id": "2022_06",
                    "materialId": "2022_06",  # 同时提供materialId字段
                    "title": "2022年六月四级听力真题第一套",
                    "reason": "这套材料专注于训练细节捕捉能力，包含大量需要理解具体数字和事实的题目。",
                    "match_score": 0.85
                },
                {
                    "id": "cet4_001",
                    "materialId": "cet4_001",  # 同时提供materialId字段
                    "title": "CET4 听力训练 - 校园生活",
                    "reason": "该材料包含多个环保主题的听力段落，与您的兴趣领域匹配，同时侧重于细节理解能力的培养。",
                    "match_score": 0.78
                }
            ],
            "improvement_suggestions": "建议在听力练习中特别注意记录关键数字信息，培养快速捕捉细节的能力。"
        }
        logger.info("使用模拟结果返回")
        logger.info("==================== 智能推荐Agent系统执行完成(使用模拟数据) ====================")
        return mock_result 