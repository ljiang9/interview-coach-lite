# interview-coach-lite

模拟面试：题库提问，规则/关键词完整度评分与改进建议，可选 LLM。

## 快速开始
```python
from interview_coach_lite import ask_next, score_answer, suggest
q = ask_next([])
print(suggest(q, score_answer(q, "我的回答")))
```

## 无 API Key
无 OPENAI_API_KEY 时走规则评分。

## 运行测试
```bash
python -m unittest discover -s tests -v
```

## License
MIT © ljiang9
