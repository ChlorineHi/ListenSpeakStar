from flask import Blueprint, jsonify, request
import json
import traceback
from services.langchain_agent import run_recommendation_agent
from services.material_manager import get_all_materials

# 创建蓝图
recommendation_bp = Blueprint('recommendation', __name__)

# 添加调试日志函数
def log_debug(message):
    """记录调试信息"""
    print(f"[DEBUG] {message}")

@recommendation_bp.route('/recommend', methods=['POST'])
def recommend_materials():
    """基于用户答题情况，使用Agent系统推荐听力材料"""
    try:
        log_debug("接收到智能推荐请求")
        data = request.json
        
        if not data:
            log_debug("请求数据为空")
            return jsonify({"error": "请求数据为空"}), 400
            
        log_debug(f"接收到的请求数据: {json.dumps(data, ensure_ascii=False)[:200]}...")
        
        # 同时支持user_answers和userAnswers两种参数名
        user_answers = data.get('user_answers') or data.get('userAnswers')
        
        if not user_answers:
            log_debug("缺少user_answers参数")
            return jsonify({"error": "缺少用户答题数据"}), 400
        
        log_debug(f"用户答案数据: {json.dumps(user_answers, ensure_ascii=False)[:200]}...")
        
        # 获取所有可用材料作为索引
        materials_index = get_all_materials()
        log_debug(f"获取到材料索引，共{len(materials_index)}个材料")
        
        # 调用Agent系统进行推荐
        log_debug("调用Agent系统进行智能推荐")
        try:
            recommendation_result = run_recommendation_agent(user_answers, materials_index)
            log_debug("成功生成推荐结果")
        except Exception as e:
            log_debug(f"调用Agent系统失败: {str(e)}")
            return jsonify({"error": f"推荐系统错误: {str(e)}"}), 500
        
        return jsonify(recommendation_result)
    except Exception as e:
        error_trace = traceback.format_exc()
        log_debug(f"智能推荐失败: {str(e)}")
        log_debug(f"错误堆栈: {error_trace}")
        return jsonify({"error": str(e)}), 500 