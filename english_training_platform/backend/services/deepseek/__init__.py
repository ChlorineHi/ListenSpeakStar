"""
将DeepSeek API客户端和各功能模块导出，使其可以从主模块导入。
"""

from .api_client import call_deepseek_api, generate_mock_response
from .listening_assessment import evaluate_listening_level, generate_learning_feedback, generate_mock_feedback
from .speaking_tasks import generate_speaking_tasks, evaluate_speaking, generate_default_speaking_tasks 