"""模拟面试：内置题库，关键词完整度评分；可选 LLM。无 key 走规则。"""
from __future__ import annotations
import os, json, urllib.request
from dataclasses import dataclass

@dataclass
class InterviewQuestion:
    id: str
    question: str
    keywords: list
    points: list


QUESTIONS = [
    InterviewQuestion(id="q1", question="自我介绍一下你自己。", keywords=["背景", "经验", "优势", "岗位"], points=["说清背景", "讲相关经验", "点出优势"]),
    InterviewQuestion(id="q2", question="说一个你遇到过的最大挑战及你怎么解决的。", keywords=["背景", "行动", "结果", "复盘"], points=["讲清情境", "你的动作", "量化结果"]),
    InterviewQuestion(id="q3", question="你为什么想加入我们公司？", keywords=["业务", "岗位", "文化", "发展"], points=["研究过业务", "匹配岗位", "有长期理由"]),
]


def ask_next(history):
    used = {h["qid"] for h in history}
    for q in QUESTIONS:
        if q.id not in used: return q
    return QUESTIONS[0]


def score_answer(q, answer):
    hits = [k for k in q.keywords if k in answer]
    return {"score": round(100*len(hits)/max(1,len(q.keywords))), "hits": hits, "missing": [k for k in q.keywords if k not in answer]}


def suggest(q, result):
    if result["score"] >= 80: return "回答很完整，保持即可。"
    if result["score"] >= 50: return f"基本合格；建议补充：{', '.join(result['missing'])}。"
    return f"回答偏单薄；请围绕这些点展开：{', '.join(q.points)}。"


def llm_feedback(question, answer):
    key = os.environ.get("OPENAI_API_KEY")
    if not key: return None
    base = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
    payload = {"model": os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
               "messages": [{"role": "system", "content": "你是面试官，给一段中文面试回答打分并给改进建议，简洁。"},
                            {"role": "user", "content": f"问题：{question}\n回答：{answer}"}], "temperature": 0.3}
    req = urllib.request.Request(f"{base}/chat/completions", data=json.dumps(payload).encode("utf-8"),
                                 headers={"Content-Type": "application/json", "Authorization": f"Bearer {key}"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            d = json.loads(r.read().decode("utf-8"))
        return d["choices"][0]["message"]["content"].strip()
    except Exception:
        return None
