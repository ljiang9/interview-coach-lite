"""interview_coach_lite: 模拟面试题库 + 规则评分与建议；可选 LLM。"""
from .coach import InterviewQuestion, ask_next, score_answer, suggest

__all__ = ["InterviewQuestion", "ask_next", "score_answer", "suggest"]
__version__ = "0.1.0"
