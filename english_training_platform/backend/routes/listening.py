from flask import Blueprint, jsonify, request
import json
import os
import random
import traceback
from services.deepseek import evaluate_listening_level, generate_learning_feedback
from services.material_manager import get_materials_by_difficulty, get_materials_by_topic

listening_bp = Blueprint('listening', __name__)

# 添加调试日志函数
def log_debug(message):
    """记录调试信息"""
    print(f"[DEBUG] {message}")

@listening_bp.route('/materials', methods=['GET'])
def get_listening_materials():
    """获取所有听力材料"""
    try:
        with open('data/materials.json', 'r', encoding='utf-8') as f:
            materials = json.load(f)
        return jsonify(materials)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@listening_bp.route('/materials/topic/<topic>', methods=['GET'])
def get_materials_by_topic_route(topic):
    """根据话题获取听力材料"""
    try:
        materials = get_materials_by_topic(topic)
        return jsonify(materials)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@listening_bp.route('/materials/difficulty/<difficulty>', methods=['GET'])
def get_materials_by_difficulty_route(difficulty):
    """根据难度获取听力材料"""
    try:
        materials = get_materials_by_difficulty(difficulty)
        return jsonify(materials)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@listening_bp.route('/material/<material_id>', methods=['GET'])
def get_material_by_id(material_id):
    """根据ID获取单个听力材料"""
    try:
        with open('data/materials.json', 'r', encoding='utf-8') as f:
            materials = json.load(f)
        
        material = next((m for m in materials if m['id'] == material_id), None)
        if material:
            return jsonify(material)
        else:
            return jsonify({"error": "找不到指定材料"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@listening_bp.route('/assessment', methods=['GET'])
def get_assessment_questions():
    """获取听力评估试题"""
    try:
        # 从材料库中随机选择不同难度的试题组成评估
        with open('data/materials.json', 'r', encoding='utf-8') as f:
            materials = json.load(f)
        
        # 确保至少有4种难度的材料
        difficulties = ["CET4", "CET6", "IELTS", "TOEFL"]
        assessment_materials = []
        
        for difficulty in difficulties:
            matching_materials = [m for m in materials if m['difficulty'] == difficulty]
            if matching_materials:
                assessment_materials.append(random.choice(matching_materials))
        
        # 如果没有足够的难度材料，则随机补充
        while len(assessment_materials) < 4 and materials:
            random_material = random.choice(materials)
            if random_material not in assessment_materials:
                assessment_materials.append(random_material)
        
        return jsonify(assessment_materials)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@listening_bp.route('/assessment/evaluate', methods=['POST'])
def evaluate_assessment():
    """评估用户的听力水平"""
    try:
        data = request.json
        user_answers = data.get('answers', [])
        
        # 调用DeepSeek API评估听力水平
        evaluation_result = evaluate_listening_level(user_answers)
        
        # 获取推荐的材料
        recommended_level = evaluation_result.get('level', 'CET4')
        recommended_materials = get_materials_by_difficulty(recommended_level)
        
        if recommended_materials:
            evaluation_result['recommended_materials'] = recommended_materials[:5]  # 推荐前5个
        else:
            evaluation_result['recommended_materials'] = []
        
        return jsonify(evaluation_result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@listening_bp.route('/feedback', methods=['POST'])
def get_learning_feedback():
    """根据用户答题情况生成学习反馈"""
    try:
        log_debug("接收到获取学习反馈的请求")
        data = request.json
        
        if not data:
            log_debug("请求数据为空")
            return jsonify({"error": "请求数据为空"}), 400
            
        log_debug(f"接收到的请求数据: {json.dumps(data, ensure_ascii=False)}")
        
        material_id = data.get('material_id')
        user_answers = data.get('answers', [])
        
        if not material_id:
            log_debug("缺少material_id参数")
            return jsonify({"error": "缺少material_id参数"}), 400
            
        if not user_answers:
            log_debug("缺少answers参数")
            return jsonify({"error": "缺少answers参数"}), 400
        
        log_debug(f"处理material_id: {material_id}, 用户答案数量: {len(user_answers)}")
        
        # 定义难度级别映射
        difficulty_map = {
            'CET4': 'CET4',
            'cet4': 'CET4',
            'CET6': 'CET6', 
            'cet6': 'CET6',
            'IELTS': 'IELTS',
            'ielts': 'IELTS', 
            'TOEFL': 'TOEFL',
            'toefl': 'TOEFL'
        }
        
        # 从ID中提取难度级别前缀
        difficulty_prefix = material_id.split('_')[0].lower()
        difficulty = difficulty_map.get(difficulty_prefix, 'CET4')
        log_debug(f"从material_id中提取的难度: {difficulty}")
        
        # 定义基础路径
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        materials_base_path = os.path.join(base_path, 'frontend', 'public', 'materials')
        log_debug(f"材料基础路径: {materials_base_path}")
        
        # 获取材料内容
        material = None
        materials_path = os.path.join(materials_base_path, difficulty, 'materials.json')
        log_debug(f"尝试从以下路径读取材料: {materials_path}")
        
        if os.path.exists(materials_path):
            try:
                with open(materials_path, 'r', encoding='utf-8') as f:
                    materials_data = json.load(f)
                if 'materials' in materials_data:
                    material = next((m for m in materials_data['materials'] if m['id'] == material_id), None)
                    if material:
                        log_debug(f"在材料文件中找到了材料: {material_id}")
                    else:
                        log_debug(f"在材料文件中未找到材料: {material_id}")
            except Exception as e:
                log_debug(f"读取材料文件出错: {str(e)}")
        else:
            log_debug(f"材料文件不存在: {materials_path}")
            
        # 如果在指定难度文件中找不到，尝试从data/materials.json获取
        if not material:
            try:
                materials_json_path = os.path.join(base_path, 'data', 'materials.json')
                log_debug(f"尝试从以下路径读取材料: {materials_json_path}")
                
                if os.path.exists(materials_json_path):
                    with open(materials_json_path, 'r', encoding='utf-8') as f:
                        materials = json.load(f)
                    material = next((m for m in materials if m['id'] == material_id), None)
                    if material:
                        log_debug(f"在data/materials.json中找到了材料: {material_id}")
                else:
                    log_debug(f"文件不存在: {materials_json_path}")
            except Exception as e:
                log_debug(f"从主材料文件读取失败: {str(e)}")
        
        # 如果仍然找不到材料，创建模拟材料
        if not material:
            log_debug(f"找不到指定材料: {material_id}，创建模拟材料")
            material = {
                "id": material_id,
                "title": f"听力材料 ({material_id})",
                "difficulty": difficulty,
                "topic": ["一般话题"],
                "questions": [{"question": q["question"], "answer": q["correct_answer"]} for q in user_answers]
            }
        
        # 获取听力原文数据
        transcript = None
        transcripts_path = os.path.join(materials_base_path, difficulty, 'transcripts.json')
        log_debug(f"尝试从以下路径读取听力原文: {transcripts_path}")
        
        if os.path.exists(transcripts_path):
            try:
                with open(transcripts_path, 'r', encoding='utf-8') as f:
                    transcripts_data = json.load(f)
                
                if 'transcripts' in transcripts_data:
                    transcript = next((t for t in transcripts_data['transcripts'] if t['id'] == material_id), None)
                    if transcript:
                        log_debug(f"找到了听力原文: {material_id}")
                    else:
                        log_debug(f"在transcripts.json中未找到原文: {material_id}")
            except Exception as e:
                log_debug(f"读取听力原文出错: {str(e)}")
        else:
            log_debug(f"听力原文文件不存在: {transcripts_path}")
        
        # 调用DeepSeek API生成学习反馈
        log_debug("调用DeepSeek API生成学习反馈")
        try:
            feedback = generate_learning_feedback(material, user_answers, transcript)
            log_debug("成功生成学习反馈")
        except Exception as e:
            log_debug(f"调用DeepSeek API失败: {str(e)}")
            log_debug("使用备用生成方法")
            # 如果DeepSeek调用失败，使用本地生成的反馈
            from services.deepseek import generate_mock_feedback
            feedback = generate_mock_feedback(material, user_answers)
            log_debug("成功生成备用反馈")
            
        # 添加友好提示
        if 'background' in feedback:
            # 判断是否是备用数据
            if any(keyword in feedback.get('background', '') for keyword in ['相关领域的发展趋势', '请多听此类材料']):
                feedback['is_mock_data'] = True
                feedback['background'] = "【系统提示：由于网络原因，本次反馈由系统自动生成，仅供参考】\n" + feedback['background']
        
        return jsonify(feedback)
    except Exception as e:
        error_trace = traceback.format_exc()
        log_debug(f"获取学习反馈失败: {str(e)}")
        log_debug(f"错误堆栈: {error_trace}")
        return jsonify({"error": str(e)}), 500

@listening_bp.route('/advanced/<current_level>', methods=['GET'])
def get_advanced_materials(current_level):
    """获取进阶难度的听力材料"""
    try:
        # 定义难度级别顺序
        difficulty_levels = ["CET4", "CET6", "IELTS", "TOEFL"]
        
        # 确定当前难度的索引
        current_index = difficulty_levels.index(current_level) if current_level in difficulty_levels else 0
        
        # 获取下一个难度级别(如果当前是最高级别，则维持不变)
        next_level = difficulty_levels[min(current_index + 1, len(difficulty_levels) - 1)]
        
        # 获取进阶难度的材料
        advanced_materials = get_materials_by_difficulty(next_level)
        
        return jsonify({
            "current_level": current_level,
            "advanced_level": next_level,
            "materials": advanced_materials[:3]  # 只返回前3个进阶材料
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500 