from flask import Blueprint, jsonify, request
import json
import os
from services.deepseek import generate_speaking_tasks, evaluate_speaking

speaking_bp = Blueprint('speaking', __name__)

@speaking_bp.route('/tasks/<material_id>', methods=['GET'])
def get_speaking_tasks(material_id):
    """基于听力材料生成口语任务"""
    try:
        # 获取材料内容
        with open('data/materials.json', 'r', encoding='utf-8') as f:
            materials = json.load(f)
        
        material = next((m for m in materials if m['id'] == material_id), None)
        if not material:
            return jsonify({"error": "找不到指定材料"}), 404
        
        # 调用DeepSeek API生成口语任务
        speaking_tasks = generate_speaking_tasks(material)
        
        return jsonify(speaking_tasks)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@speaking_bp.route('/evaluate', methods=['POST'])
def evaluate_speaking_submission():
    """评估用户的口语提交"""
    try:
        data = request.json
        audio_data = data.get('audio_data')  # 这里可能是Base64编码的音频数据
        question = data.get('question')
        reference_answer = data.get('reference_answer')
        
        if not audio_data or not question:
            return jsonify({"error": "缺少必要参数"}), 400
        
        # 调用DeepSeek API评估口语
        evaluation = evaluate_speaking(audio_data, question, reference_answer)
        
        return jsonify(evaluation)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@speaking_bp.route('/sample-tasks', methods=['GET'])
def get_sample_speaking_tasks():
    """获取示例口语任务（用于首次使用或无听力材料时）"""
    try:
        # 这里提供一些预定义的基础口语任务
        sample_tasks = [
            {
                "type": "self_introduction",
                "prompt": "请简单介绍一下你自己，包括你的名字、学校、专业和兴趣爱好。",
                "reference": "Hello, my name is [Name]. I am a student at [University] majoring in [Major]. In my free time, I enjoy [Hobbies]."
            },
            {
                "type": "topic_discussion",
                "prompt": "谈谈你认为学习英语的最佳方法是什么？",
                "reference": "I believe the best way to learn English is through consistent practice and immersion. This includes listening to English content, speaking with others, reading books, and writing regularly."
            },
            {
                "type": "picture_description",
                "prompt": "描述一个你最近去过的地方，包括它的特点和你的感受。",
                "reference": "Recently, I visited [Place]. It is characterized by [Features]. During my visit, I felt [Emotions] because [Reasons]."
            }
        ]
        return jsonify(sample_tasks)
    except Exception as e:
        return jsonify({"error": str(e)}), 500 