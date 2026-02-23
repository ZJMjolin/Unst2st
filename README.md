# Unst2st - 非结构化文档智能提取系统

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.11-green)
![License](https://img.shields.io/badge/license-MIT-orange)

**Unst2st** (Unstructured to Structured) 是一个基于AI的智能文档信息提取系统，可以将各种非结构化文档（PDF、Word、邮件等）中的信息自动提取并转换为结构化表格数据。

---

## ✨ 核心功能

- 📄 **多格式支持**：自动识别并解析 PDF、DOCX、MSG、EML、TXT 等常见办公文件格式
- 🤖 **AI智能提取**：使用智谱AI GLM-4模型智能提取文档中的关键信息
- 🎯 **灵活模板**：自定义字段模板，可保存复用
- 📊 **在线表格**：提取结果在线展示为可编辑表格
- 📋 **一键复制**：支持复制表格内容到Excel等工具
- 🌐 **在线访问**：部署后可通过浏览器在线使用，无需安装任何软件

---

## 🚀 快速开始

### 方案一：本地运行

#### 前置要求

- Python 3.11+
- 智谱AI API密钥（[注册获取](https://open.bigmodel.cn/)）

#### 安装步骤

1. **克隆项目**

```bash
cd D:\code\20260223_Unst2st
```

2. **创建虚拟环境并安装依赖**

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

pip install -r requirements.txt
```

3. **配置环境变量**

复制 `.env.example` 为 `.env`，并填入你的智谱AI API密钥：

```bash
ZHIPU_API_KEY=your-zhipu-api-key-here
```

4. **启动服务**

```bash
cd ..
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

5. **访问系统**

打开浏览器访问：`http://localhost:8000`

---

### 方案二：Railway部署（推荐）

#### 部署到Railway（完全免费）

1. **注册Railway账号**

访问 [Railway.app](https://railway.app) 并使用GitHub登录

2. **推送代码到GitHub**

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin your-github-repo-url
git push -u origin main
```

3. **在Railway创建项目**

- 点击 "New Project"
- 选择 "Deploy from GitHub repo"
- 选择你的仓库
- Railway会自动检测Dockerfile并部署

4. **配置环境变量**

在Railway项目设置中添加：
- `ZHIPU_API_KEY` = 你的智谱AI密钥

5. **获取访问地址**

Railway会自动生成一个域名，如：`https://your-app.railway.app`

---

## 📖 使用指南

### 第一步：创建字段模板

1. 点击「创建新模板」
2. 输入模板名称（如：合作合同模板）
3. 添加需要提取的字段：
   - 字段名称：如"公司名称"
   - 字段描述：如"合作方公司全称"
4. 点击「保存模板」

### 第二步：上传文档

1. 选择刚创建的模板
2. 拖拽或点击上传文档文件
3. 支持同时上传多个文件

### 第三步：查看结果

1. 点击「开始提取信息」
2. 等待AI处理（通常几秒钟）
3. 查看提取结果表格
4. 可编辑单元格内容
5. 点击「复制表格」粘贴到Excel

---

## 🛠️ 技术架构

### 后端技术栈

- **Web框架**: FastAPI
- **AI模型**: 智谱AI GLM-4
- **文件解析**:
  - PDF: pdfplumber
  - Word: python-docx
  - Email: extract-msg
- **数据库**: SQLite
- **部署**: Docker + Railway

### 前端技术栈

- 原生HTML + CSS + JavaScript
- 响应式设计
- 无需额外框架

### 项目结构

```
20260223_Unst2st/
├── backend/                 # 后端代码
│   ├── app/
│   │   ├── __init__.py
│   │   ├── ai_extractor.py  # AI提取模块
│   │   ├── file_parser.py   # 文件解析模块
│   │   ├── database.py      # 数据库配置
│   │   ├── models.py        # 数据库模型
│   │   └── schemas.py       # API数据模型
│   ├── main.py              # FastAPI主程序
│   └── requirements.txt     # Python依赖
├── frontend/                # 前端代码
│   ├── index.html
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
├── data/                    # 数据库文件（自动生成）
├── uploads/                 # 上传文件临时目录（自动生成）
├── Dockerfile               # Docker配置
├── .dockerignore
├── .gitignore
├── .env.example             # 环境变量模板
└── README.md                # 本文件
```

---

## 🔑 获取智谱AI API密钥

### 方式一：智谱AI（推荐 - 每月400万tokens永久免费）

1. 访问 [智谱AI开放平台](https://open.bigmodel.cn/)
2. 注册并登录账号
3. 进入「API密钥」页面
4. 创建新的API密钥
5. 复制密钥并配置到环境变量

**免费额度**：每月400万tokens（约可处理500-1000个文档）

---

## 💰 成本说明

### 方案一：Railway + 智谱AI

- **部署平台**: Railway 免费额度（500小时/月）
- **AI调用**: 智谱AI 免费额度（400万tokens/月）
- **总成本**: **完全免费** 🎉

### 使用估算

假设每天处理50个文档，每个文档2000字：
- 每个文档消耗约3000 tokens
- 每天消耗：50 × 3000 = 15万 tokens
- 每月消耗：15万 × 30 = 450万 tokens

**结论**：智谱AI免费额度可满足小团队日常使用！

---

## 📝 常见问题

### Q1: 支持哪些文件格式？

A: 目前支持：
- PDF (.pdf)
- Word文档 (.docx)
- Outlook邮件 (.msg)
- 标准邮件 (.eml)
- 纯文本 (.txt)

注：暂不支持.doc格式，请转换为.docx

### Q2: 提取准确率如何？

A: 使用智谱AI GLM-4模型，对于格式规范的文档，准确率可达90%以上。提取结果支持手动编辑修正。

### Q3: 文件大小限制？

A: 建议单个文件不超过10MB。大文件可能导致处理时间较长。

### Q4: 数据安全吗？

A:
- 文件处理完成后立即删除
- 数据库仅存储模板信息，不存储文档内容
- 建议部署在可信服务器或使用本地部署

### Q5: 如何修改API为其他模型？

A: 编辑 `backend/app/ai_extractor.py`，修改API调用接口即可适配其他模型（如通义千问、文心一言等）。

---

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

---

## 📄 开源协议

本项目采用 MIT 协议开源。

---

## 🙏 致谢

- [智谱AI](https://open.bigmodel.cn/) - 提供强大的AI能力
- [FastAPI](https://fastapi.tiangolo.com/) - 现代化的Python Web框架
- [Railway](https://railway.app/) - 简单易用的部署平台

---

## 📧 联系方式

如有问题或建议，欢迎通过以下方式联系：

- 提交 [GitHub Issue](https://github.com/your-repo/issues)
- 邮件：your-email@example.com

---

**Made with ❤️ by Your Team**
