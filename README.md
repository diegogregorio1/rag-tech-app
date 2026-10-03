# RAG技术与应用

RAG（检索增强生成）技术学习与实践案例集，包含 Embedding 模型使用、Query 改写、ChatPDF 问答三个案例，每个案例均可独立运行，部分带 Web 前端页面。

## 目录结构

```
8-RAG技术与应用/
├── CASE-embedding使用/          # Embedding 模型使用示例
│   ├── bge-m3使用.py            # BGE-M3 模型：稠密检索 + 相似度计算
│   ├── gte-qwen2-使用1.py       # GTE-Qwen2：SentenceTransformer 方式调用
│   ├── gte-qwen2-使用2.py       # GTE-Qwen2：Transformers 原生方式调用
│   ├── embedding矩阵乘法详解.html
│   └── requirements.txt
├── CASEA-Query改写/             # Query 改写示例
│   ├── 1-Query改写.py           # 上下文依赖/对比/模糊指代/多意图/反问 五种改写
│   ├── 2-Query联网搜索改写.py   # 联网搜索需求识别 + 查询改写 + 搜索策略生成
│   ├── app.py                   # Flask 后端（端口 5000）
│   ├── templates/index.html     # Web 前端页面
│   ├── test_api.py              # 10 条测试集
│   └── requirements.txt
├── CASE-ChatPDF-Faiss/          # ChatPDF 问答案例
│   ├── chatpdf-faiss.py         # PDF 解析 + FAISS 向量库 + RAG 问答
│   ├── app.py                   # Flask 后端（端口 5001）
│   ├── templates/index.html     # 深色主题聊天式前端
│   ├── vector_db/               # 已构建的 FAISS 向量库
│   └── requirements.txt
└── 1-RAG技术与应用.pdf          # 课程 PDF 资料
```

## 环境要求

- Windows + Python 3.14
- 设置环境变量 `DASHSCOPE_API_KEY`（阿里云百炼 API Key）

安装依赖：

```powershell
pip install -r CASE-ChatPDF-Faiss/requirements.txt
pip install -r CASEA-Query改写/requirements.txt
pip install -r CASE-embedding使用/requirements.txt
```

## 快速开始

### 1. Embedding 模型使用

```powershell
python CASE-embedding使用/bge-m3使用.py
python CASE-embedding使用/gte-qwen2-使用1.py
python CASE-embedding使用/gte-qwen2-使用2.py
```

首次运行会自动从 ModelScope 下载模型到 `CASE-embedding使用/models/` 目录。

### 2. Query 改写（命令行）

```powershell
python CASEA-Query改写/1-Query改写.py
python CASEA-Query改写/2-Query联网搜索改写.py
```

### 3. Query 改写（Web 页面）

```powershell
python CASEA-Query改写/app.py
```

浏览器打开 http://127.0.0.1:5000/ ，输入查询即可查看联网搜索识别与改写结果。

### 4. ChatPDF 问答（Web 页面）

```powershell
python CASE-ChatPDF-Faiss/app.py
```

浏览器打开 http://127.0.0.1:5001/ ，以聊天方式对 PDF 文档提问，回答会标注来源页码。

## 功能特性

- **Embedding 案例**：BGE-M3 / GTE-Qwen2 模型的向量编码与相似度计算
- **Query 改写**：上下文依赖、对比、模糊指代、多意图、反问五种类型改写；自动识别是否需要联网搜索并生成搜索策略
- **ChatPDF**：PDF 文本提取（含页码映射）→ 文本分块 → DashScope Embedding → FAISS 向量检索 → DeepSeek-v3 生成回答

## 注意事项

- 模型默认使用 `qwen-turbo`（部分账号对 `qwen-turbo-latest` 无访问权限）
- FAISS 不支持中文路径，代码中已通过临时目录中转处理
- embedding 模型文件较大（约 5GB），已在 .gitignore 中排除，不会上传到仓库
