import requests
import json
import sys

def test_feedback_api():
    """测试获取学习反馈的API"""
    url = "http://localhost:5000/api/listening/feedback"
    
    # 测试数据
    data = {
        "material_id": "cet4_model_test1",
        "answers": [
            {
                "question_id": 1,
                "question": "What kind of beds will be provided for the athletes of the Tokyo Olympics?",
                "user_answer": "A",
                "correct_answer": "A",
                "is_correct": True
            },
            {
                "question_id": 2,
                "question": "What would the bed parts be turned into after the games?",
                "user_answer": "B",
                "correct_answer": "C",
                "is_correct": False
            }
        ]
    }
    
    print("发送请求到:", url)
    print("请求数据:", json.dumps(data, indent=2, ensure_ascii=False))
    
    try:
        response = requests.post(url, json=data, timeout=30)
        response.raise_for_status()
        
        print("\n请求成功!")
        print("状态码:", response.status_code)
        print("响应头:", response.headers)
        print("响应内容:", json.dumps(response.json(), indent=2, ensure_ascii=False))
        return True
    except requests.exceptions.RequestException as e:
        print("\n请求失败!")
        print("错误信息:", str(e))
        return False

if __name__ == "__main__":
    print("开始测试API...")
    success = test_feedback_api()
    if success:
        print("\n测试成功完成!")
        sys.exit(0)
    else:
        print("\n测试失败!")
        sys.exit(1) 