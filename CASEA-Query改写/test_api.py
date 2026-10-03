# -*- coding: utf-8 -*-
# 测试集：10个不同类型的查询，调用本地 Flask API 验证联网搜索识别与改写效果
import json
import urllib.request

API_URL = "http://127.0.0.1:5000/api/rewrite"

# 10个测试用例：覆盖时效、价格、营业、活动、天气、交通、预订、实时状态、无需联网等场景
test_cases = [
    {"name": "时效性-开放状态", "query": "上海迪士尼乐园今天开放吗？现在人多不多？"},
    {"name": "价格信息", "query": "北京环球影城门票现在多少钱？"},
    {"name": "营业信息", "query": "广州长隆欢乐世界万圣节夜场几点开始？"},
    {"name": "活动信息", "query": "上海迪士尼最近有什么新的主题活动？"},
    {"name": "天气信息", "query": "明天去迪士尼会下雨吗？"},
    {"name": "交通信息", "query": "从上海虹桥火车站怎么去迪士尼乐园？"},
    {"name": "预订信息", "query": "国庆假期迪士尼门票需要提前几天预约？"},
    {"name": "实时状态", "query": "现在疯狂动物城园区排队要多久？"},
    {"name": "无需联网-常识", "query": "秦始皇统一六国是哪一年？"},
    {"name": "无需联网-概念", "query": "什么是RAG检索增强生成技术？"},
]


def call_api(query, conversation_history=""):
    """调用本地改写API"""
    payload = json.dumps({"query": query, "conversation_history": conversation_history}).encode("utf-8")
    req = urllib.request.Request(API_URL, data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main():
    results = []
    for i, case in enumerate(test_cases, 1):
        print(f"===== 测试 {i}/10: {case['name']} =====")
        print(f"查询: {case['query']}")
        try:
            r = call_api(case["query"])
            need = r.get("need_web_search", False)
            print(f"需要联网: {'是' if need else '否'}")
            if need:
                print(f"  原因: {r.get('search_reason', '')}")
                print(f"  置信度: {r.get('confidence', '')}")
                print(f"  改写查询: {r.get('rewritten_query', '')}")
                print(f"  关键词: {r.get('search_keywords', [])}")
                strategy = r.get("search_strategy", {})
                print(f"  搜索平台: {strategy.get('search_platforms', [])}")
                print(f"  时间范围: {strategy.get('time_range', '')}")
            else:
                print(f"  原因: {r.get('reason', '')}")
            results.append({"case": case["name"], "query": case["query"], "result": r})
        except Exception as e:
            print(f"  调用失败: {e}")
            results.append({"case": case["name"], "query": case["query"], "error": str(e)})
        print()

    # 保存结果到文件，便于查看
    with open("test_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("结果已保存到 test_results.json")


if __name__ == "__main__":
    main()
