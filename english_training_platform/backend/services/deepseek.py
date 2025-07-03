"""
DeepSeek API集成模块
提供与DeepSeek大模型API的交互功能，支持听力评估、学习反馈和口语练习等功能。
"""

# 导入子模块中的所有函数
from .deepseek.api_client import call_deepseek_api, generate_mock_response
from .deepseek.listening_assessment import (
    evaluate_listening_level,
    generate_learning_feedback,
    generate_mock_feedback,
    log_debug
)
from .deepseek.speaking_tasks import (
    generate_speaking_tasks,
    evaluate_speaking,
    generate_default_speaking_tasks
)

# 提供向后兼容性，这样其他模块导入时不需要修改
__all__ = [
    'call_deepseek_api',
    'generate_mock_response',
    'evaluate_listening_level',
    'generate_learning_feedback',
    'generate_mock_feedback',
    'generate_speaking_tasks',
    'evaluate_speaking',
    'generate_default_speaking_tasks',
    'log_debug'
] 