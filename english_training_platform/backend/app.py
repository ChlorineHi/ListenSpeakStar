from flask import Flask, jsonify
from flask_cors import CORS
import os
import json

# 导入路由模块
from routes.listening import listening_bp
from routes.speaking import speaking_bp
from routes.favorites import favorites_bp
from routes.recommendation import recommendation_bp

# 导入材料管理服务
from services.material_manager import initialize_sample_materials

app = Flask(__name__)
CORS(app)  # 启用跨域资源共享

# 注册蓝图
app.register_blueprint(listening_bp, url_prefix='/api/listening')
app.register_blueprint(speaking_bp, url_prefix='/api/speaking')
app.register_blueprint(favorites_bp, url_prefix='/api/favorites')
app.register_blueprint(recommendation_bp, url_prefix='/api/recommendation')

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({"status": "ok", "message": "服务正常运行"})

if __name__ == '__main__':
    # 确保数据目录存在
    os.makedirs('data', exist_ok=True)
    
    # 初始化材料数据文件（如果不存在）
    if not os.path.exists('data/materials.json'):
        with open('data/materials.json', 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False)
    
    # 初始化收藏数据文件（如果不存在）
    if not os.path.exists('data/favorites.json'):
        with open('data/favorites.json', 'w', encoding='utf-8') as f:
            json.dump({}, f, ensure_ascii=False)
    
    # 初始化示例听力材料
    initialize_sample_materials()
    
    app.run(debug=True, host='0.0.0.0', port=5000) 