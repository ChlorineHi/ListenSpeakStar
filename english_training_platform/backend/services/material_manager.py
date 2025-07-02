import json
import os
import glob
from typing import Dict, List, Any

def initialize_sample_materials():
    """初始化示例材料数据"""
    # 确保数据目录存在
    os.makedirs('data', exist_ok=True)
    
    # 如果材料数据文件不存在，创建一个空文件
    if not os.path.exists('data/materials.json'):
        with open('data/materials.json', 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False)

def get_all_materials():
    """获取所有可用的听力材料索引，用于推荐系统"""
    materials_index = []
    
    try:
        # 修正前端材料目录路径计算
        # 首先尝试从当前项目根目录获取路径
        frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../frontend/public/materials'))
        if not os.path.exists(frontend_path):
            # 如果路径不存在，尝试从当前工作目录计算
            frontend_path = os.path.abspath('frontend/public/materials')
            
        print(f"使用前端材料目录路径: {frontend_path}")
        index_path = os.path.join(frontend_path, 'index.json')
        
        if os.path.exists(index_path):
            with open(index_path, 'r', encoding='utf-8') as f:
                index_data = json.load(f)
                
            print(f"成功加载材料索引文件: {index_path}")
            
            # 直接使用materials_details数据，这些数据已经包含了完整的材料信息
            if 'materials_details' in index_data and index_data['materials_details']:
                print(f"从materials_details中获取材料，共{len(index_data['materials_details'])}个")
                for material in index_data['materials_details']:
                    # 确保每个材料都有id字段
                    if 'id' not in material:
                        print(f"警告: 材料缺少id字段: {material}")
                        continue
                    materials_index.append(material)
                print(f"成功添加{len(materials_index)}个材料到索引")
            else:
                print("materials_details不存在或为空，尝试从difficulties获取")
                
                # 处理difficulties数据
                for difficulty in index_data.get('difficulties', []):
                    # 修正材料路径计算
                    materials_path = os.path.join(frontend_path, difficulty['materials_path'].lstrip('/').replace('/', os.path.sep))
                    # 如果路径中包含相对路径，需要进行规范化
                    materials_path = os.path.normpath(materials_path)
                    print(f"处理难度级别: {difficulty['id']}, 路径: {materials_path}")
                    
                    if os.path.exists(materials_path):
                        try:
                            with open(materials_path, 'r', encoding='utf-8') as f:
                                materials_data = json.load(f)
                                
                            # 将材料添加到索引中
                            materials_count = 0
                            for material in materials_data.get('materials', []):
                                # 确保每个材料都有id字段
                                if 'id' not in material:
                                    print(f"警告: 材料缺少id字段，添加id: {difficulty['id']}")
                                    material['id'] = difficulty['id']
                                
                                # 添加难度信息
                                material['difficulty_id'] = difficulty['id']
                                material['difficulty_name'] = difficulty['name']
                                materials_index.append(material)
                                materials_count += 1
                            print(f"从{difficulty['id']}添加了{materials_count}个材料")
                        except Exception as e:
                            print(f"读取材料文件失败: {materials_path}, 错误: {str(e)}")
            
            # 如果上面的方法都没有获取到材料，尝试直接从各个材料目录获取
            if not materials_index:
                print("尝试直接从各个材料目录获取")
                # 从available_materials获取材料ID列表
                available_ids = index_data.get('available_materials', [])
                print(f"available_materials包含{len(available_ids)}个材料ID")
                
                # 遍历每个可用的材料ID，尝试从对应目录获取材料
                for material_id in available_ids:
                    material_dir = os.path.join(frontend_path, material_id)
                    material_file = os.path.join(material_dir, 'materials.json')
                    
                    if os.path.exists(material_file):
                        try:
                            with open(material_file, 'r', encoding='utf-8') as f:
                                material_data = json.load(f)
                            
                            if 'materials' in material_data and len(material_data['materials']) > 0:
                                for material in material_data['materials']:
                                    if 'id' not in material:
                                        material['id'] = material_id
                                    materials_index.append(material)
                                print(f"从目录 {material_id} 添加了 {len(material_data['materials'])} 个材料")
                        except Exception as e:
                            print(f"读取材料文件失败: {material_file}, 错误: {str(e)}")
                
                # 如果仍然没有获取到材料，尝试从latest_materials获取
                if not materials_index:
                    print("尝试从latest_materials获取材料")
                    latest_materials = index_data.get('latest_materials', [])
                    print(f"latest_materials包含{len(latest_materials)}个材料")
                    
                    for material in latest_materials:
                        if 'id' in material and material['id'] in available_ids:
                            materials_index.append(material)
                    
                    print(f"从latest_materials添加了{len(materials_index)}个材料")
        else:
            print(f"材料索引文件不存在: {index_path}")
            
        # 如果没有从前端获取到材料，使用后端的材料数据
        if not materials_index:
            print("从后端获取材料数据")
            if os.path.exists('data/materials.json'):
                with open('data/materials.json', 'r', encoding='utf-8') as f:
                    backend_materials = json.load(f)
                    
                # 确保每个材料都有id字段
                for material in backend_materials:
                    if 'id' not in material:
                        print(f"警告: 后端材料缺少id字段: {material}")
                        continue
                    materials_index.append(material)
                print(f"从后端添加了{len(materials_index)}个材料")
        
        # 最终验证所有材料都有id字段
        valid_materials = []
        for material in materials_index:
            if 'id' in material:
                valid_materials.append(material)
            else:
                print(f"警告: 过滤掉没有id字段的材料: {material}")
        
        materials_index = valid_materials
        print(f"最终材料索引包含{len(materials_index)}个有效材料")
        
        # 打印所有材料的ID
        material_ids = [m.get('id') for m in materials_index]
        print(f"材料ID列表: {material_ids}")
    except Exception as e:
        print(f"获取材料索引失败: {str(e)}")
        import traceback
        print(traceback.format_exc())
        
    return materials_index

def get_materials_by_difficulty(difficulty: str) -> List[Dict[str, Any]]:
    """
    根据难度获取听力材料
    
    Args:
        difficulty (str): 难度等级，如CET4, CET6, IELTS, TOEFL
        
    Returns:
        list: 符合难度要求的材料列表
    """
    materials = get_all_materials()
    return [m for m in materials if m.get('difficulty') == difficulty]

def get_materials_by_topic(topic: str) -> List[Dict[str, Any]]:
    """
    根据话题获取听力材料
    
    Args:
        topic (str): 话题标签
        
    Returns:
        list: 符合话题要求的材料列表
    """
    materials = get_all_materials()
    return [m for m in materials if topic.lower() in [t.lower() for t in m.get('topic', [])]]

def get_material_by_id(material_id: str) -> Dict[str, Any]:
    """根据ID获取特定的听力材料"""
    materials = get_all_materials()
    for material in materials:
        if material.get('id') == material_id:
            return material
    return None

def add_material(material: Dict[str, Any]) -> bool:
    """
    添加新的听力材料
    
    Args:
        material (dict): 材料数据
        
    Returns:
        bool: 添加是否成功
    """
    try:
        materials = get_all_materials()
        
        # 检查ID是否已存在
        if any(m.get('id') == material.get('id') for m in materials):
            print(f"材料ID '{material.get('id')}' 已存在")
            return False
        
        # 添加新材料
        materials.append(material)
        
        # 保存到文件
        with open('data/materials.json', 'w', encoding='utf-8') as f:
            json.dump(materials, f, ensure_ascii=False, indent=2)
        
        return True
    except Exception as e:
        print(f"添加材料时出错: {str(e)}")
        return False

def update_material(material_id: str, updated_data: Dict[str, Any]) -> bool:
    """
    更新现有的听力材料
    
    Args:
        material_id (str): 材料ID
        updated_data (dict): 更新的数据
        
    Returns:
        bool: 更新是否成功
    """
    try:
        materials = get_all_materials()
        
        # 查找材料
        for i, material in enumerate(materials):
            if material.get('id') == material_id:
                # 更新数据
                materials[i].update(updated_data)
                
                # 保存到文件
                with open('data/materials.json', 'w', encoding='utf-8') as f:
                    json.dump(materials, f, ensure_ascii=False, indent=2)
                
                return True
        
        print(f"找不到材料ID '{material_id}'")
        return False
    except Exception as e:
        print(f"更新材料时出错: {str(e)}")
        return False

def delete_material(material_id: str) -> bool:
    """
    删除听力材料
    
    Args:
        material_id (str): 材料ID
        
    Returns:
        bool: 删除是否成功
    """
    try:
        materials = get_all_materials()
        
        # 查找并删除材料
        for i, material in enumerate(materials):
            if material.get('id') == material_id:
                del materials[i]
                
                # 保存到文件
                with open('data/materials.json', 'w', encoding='utf-8') as f:
                    json.dump(materials, f, ensure_ascii=False, indent=2)
                
                return True
        
        print(f"找不到材料ID '{material_id}'")
        return False
    except Exception as e:
        print(f"删除材料时出错: {str(e)}")
        return False 