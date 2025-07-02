from flask import Blueprint, jsonify, request
import json
import os

favorites_bp = Blueprint('favorites', __name__)

@favorites_bp.route('/list/<user_id>', methods=['GET'])
def get_favorites(user_id):
    """获取用户的收藏列表"""
    try:
        with open('data/favorites.json', 'r', encoding='utf-8') as f:
            favorites_data = json.load(f)
        
        # 如果用户ID不存在，则返回空列表
        user_favorites = favorites_data.get(user_id, [])
        
        # 如果只是ID列表，则获取完整的材料信息
        if user_favorites and isinstance(user_favorites[0], str):
            with open('data/materials.json', 'r', encoding='utf-8') as f:
                materials = json.load(f)
            
            # 获取收藏的完整材料信息
            favorite_materials = [m for m in materials if m['id'] in user_favorites]
            return jsonify(favorite_materials)
        else:
            return jsonify(user_favorites)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@favorites_bp.route('/add', methods=['POST'])
def add_favorite():
    """添加收藏"""
    try:
        data = request.json
        user_id = data.get('user_id')
        material_id = data.get('material_id')
        
        if not user_id or not material_id:
            return jsonify({"error": "缺少必要参数"}), 400
        
        # 读取收藏数据
        try:
            with open('data/favorites.json', 'r', encoding='utf-8') as f:
                favorites_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            favorites_data = {}
        
        # 添加到收藏
        if user_id not in favorites_data:
            favorites_data[user_id] = []
        
        if material_id not in favorites_data[user_id]:
            favorites_data[user_id].append(material_id)
        
        # 保存收藏数据
        with open('data/favorites.json', 'w', encoding='utf-8') as f:
            json.dump(favorites_data, f, ensure_ascii=False)
        
        return jsonify({"success": True, "message": "添加收藏成功"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@favorites_bp.route('/remove', methods=['POST'])
def remove_favorite():
    """移除收藏"""
    try:
        data = request.json
        user_id = data.get('user_id')
        material_id = data.get('material_id')
        
        if not user_id or not material_id:
            return jsonify({"error": "缺少必要参数"}), 400
        
        # 读取收藏数据
        with open('data/favorites.json', 'r', encoding='utf-8') as f:
            favorites_data = json.load(f)
        
        # 从收藏中移除
        if user_id in favorites_data and material_id in favorites_data[user_id]:
            favorites_data[user_id].remove(material_id)
        
        # 保存收藏数据
        with open('data/favorites.json', 'w', encoding='utf-8') as f:
            json.dump(favorites_data, f, ensure_ascii=False)
        
        return jsonify({"success": True, "message": "移除收藏成功"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@favorites_bp.route('/check', methods=['POST'])
def check_favorite():
    """检查材料是否已收藏"""
    try:
        data = request.json
        user_id = data.get('user_id')
        material_id = data.get('material_id')
        
        if not user_id or not material_id:
            return jsonify({"error": "缺少必要参数"}), 400
        
        # 读取收藏数据
        with open('data/favorites.json', 'r', encoding='utf-8') as f:
            favorites_data = json.load(f)
        
        # 检查是否已收藏
        is_favorited = user_id in favorites_data and material_id in favorites_data[user_id]
        
        return jsonify({"is_favorited": is_favorited})
    except Exception as e:
        return jsonify({"error": str(e)}), 500 