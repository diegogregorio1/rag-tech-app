# -*- coding: utf-8 -*-
# Query联网搜索改写 - Web后端服务
# 基于 2-Query联网搜索改写.py 封装为 Flask API
import os
import importlib.util
from flask import Flask, request, jsonify, render_template

# 动态加载 2-Query联网搜索改写.py（文件名含中文和数字开头，不能直接import）
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
module_path = os.path.join(SCRIPT_DIR, "2-Query联网搜索改写.py")
spec = importlib.util.spec_from_file_location("query_web_rewrite", module_path)
query_web_rewrite = importlib.util.module_from_spec(spec)
spec.loader.exec_module(query_web_rewrite)

app = Flask(__name__)
# 初始化改写器（复用模块中的类和API配置）
web_searcher = query_web_rewrite.WebSearchQueryRewriter()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/rewrite", methods=["POST"])
def rewrite():
    data = request.get_json(force=True)
    query = (data.get("query") or "").strip()
    conversation_history = (data.get("conversation_history") or "").strip()

    if not query:
        return jsonify({"error": "查询内容不能为空"}), 400

    try:
        result = web_searcher.auto_web_search_rewrite(query, conversation_history)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
