# -*- coding: utf-8 -*-
# ChatPDF-Faiss Web 后端服务
# 加载已保存的向量数据库，提供问答 API
import os
import pickle
import shutil
import tempfile
from flask import Flask, request, jsonify, render_template
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import Tongyi

DASHSCOPE_API_KEY = os.getenv('DASHSCOPE_API_KEY')
if not DASHSCOPE_API_KEY:
    raise ValueError("请设置环境变量 DASHSCOPE_API_KEY")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
VECTOR_DB_DIR = os.path.join(SCRIPT_DIR, "vector_db")
PDF_NAME = "浦发上海浦东发展银行西安分行个金客户经理考核办法.pdf"


def load_knowledge_base(load_path: str) -> FAISS:
    """从磁盘加载向量数据库和页码信息（FAISS 不支持中文路径，需临时目录中转）"""
    embeddings = DashScopeEmbeddings(
        model="text-embedding-v1",
        dashscope_api_key=DASHSCOPE_API_KEY,
    )
    tmp_dir = tempfile.mkdtemp()
    try:
        for fname in os.listdir(load_path):
            shutil.copy2(os.path.join(load_path, fname), os.path.join(tmp_dir, fname))
        knowledgeBase = FAISS.load_local(tmp_dir, embeddings, allow_dangerous_deserialization=True)
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)
    print(f"向量数据库已从 {load_path} 加载。")

    page_info_path = os.path.join(load_path, "page_info.pkl")
    if os.path.exists(page_info_path):
        with open(page_info_path, "rb") as f:
            knowledgeBase.page_info = pickle.load(f)
        print("页码信息已加载。")
    else:
        knowledgeBase.page_info = {}
        print("警告: 未找到页码信息文件。")
    return knowledgeBase


print("正在加载知识库...")
knowledgeBase = load_knowledge_base(VECTOR_DB_DIR)
llm = Tongyi(model_name="deepseek-v3", dashscope_api_key=DASHSCOPE_API_KEY)
print("知识库加载完成，服务就绪。")

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", pdf_name=PDF_NAME)


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    query = (data.get("query") or "").strip()
    if not query:
        return jsonify({"error": "问题不能为空"}), 400

    try:
        # 相似度搜索
        docs = knowledgeBase.similarity_search(query, k=10)

        # 构建上下文并调用大模型
        context = "\n\n".join([doc.page_content for doc in docs])
        prompt = f"""根据以下上下文回答问题:

{context}

问题: {query}"""
        answer = llm.invoke(prompt)

        # 收集来源页码（去重并排序）
        unique_pages = []
        seen = set()
        for doc in docs:
            text_content = getattr(doc, "page_content", "")
            source_page = knowledgeBase.page_info.get(text_content.strip(), "未知")
            if source_page not in seen:
                seen.add(source_page)
                unique_pages.append(source_page)
        try:
            unique_pages.sort(key=lambda x: (isinstance(x, str), x))
        except Exception:
            pass

        return jsonify({
            "answer": answer,
            "source_pages": unique_pages,
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=False)
