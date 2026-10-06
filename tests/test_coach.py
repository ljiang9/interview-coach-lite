import os, sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from interview_coach_lite.coach import ask_next, score_answer, suggest, llm_feedback, QUESTIONS


class TestInterviewCoach(unittest.TestCase):
    def test_ask_returns_unseen(self):
        self.assertEqual(ask_next([]).id, "q1")
        self.assertEqual(ask_next([{"qid": "q1"}]).id, "q2")
    def test_score_full_hits(self):
        r = score_answer(QUESTIONS[0], "我叫张三，背景是计算机专业，有三年后端经验，优势是工程效率，匹配这个岗位")
        self.assertEqual(r["score"], 100)
    def test_score_partial(self):
        r = score_answer(QUESTIONS[0], "我叫张三，背景是学生")
        self.assertGreater(r["score"], 0); self.assertLess(r["score"], 100)
    def test_suggest_low(self):
        q = QUESTIONS[0]; s = suggest(q, score_answer(q, "你好"))
        self.assertIn("展开", s)
    def test_llm_no_key(self):
        old = os.environ.pop("OPENAI_API_KEY", None)
        try: self.assertIsNone(llm_feedback("q", "a"))
        finally:
            if old: os.environ["OPENAI_API_KEY"] = old


if __name__ == "__main__": unittest.main()
