"""
FastAPI主程序 - Unst2st后端服务
"""
import os
import json
import shutil
from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
from dotenv import load_dotenv

from app.database import init_db, get_db
from app.models import Template
from app.schemas import (
    TemplateCreate,
    TemplateUpdate,
    TemplateResponse,
    ExtractionResponse
)
from app.file_parser import FileParser
from app.ai_extractor import AIExtractor

# 加载环境变量
load_dotenv()

# 创建FastAPI应用
app = FastAPI(
    title="Unst2st - 非结构化文档智能提取系统",
    description="将非结构化文档转换为结构化数据",
    version="1.0.0"
)

# 配置CORS（允许前端跨域访问）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 创建必要的目录
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 初始化数据库
init_db()

# 初始化文件解析器
file_parser = FileParser()

# 获取智谱AI API密钥
ZHIPU_API_KEY = os.getenv("ZHIPU_API_KEY", "")
if not ZHIPU_API_KEY:
    print("警告: 未设置ZHIPU_API_KEY环境变量，AI提取功能将不可用")


# ==================== 模板管理API ====================

@app.post("/api/templates", response_model=TemplateResponse)
async def create_template(template: TemplateCreate, db: Session = Depends(get_db)):
    """创建新模板"""
    try:
        # 将字段列表转换为JSON字符串
        fields_json = json.dumps([field.dict() for field in template.fields], ensure_ascii=False)

        # 创建模板
        db_template = Template(
            name=template.name,
            fields=fields_json
        )
        db.add(db_template)
        db.commit()
        db.refresh(db_template)

        return db_template.to_dict()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"创建模板失败: {str(e)}")


@app.get("/api/templates", response_model=List[TemplateResponse])
async def get_templates(db: Session = Depends(get_db)):
    """获取所有模板"""
    templates = db.query(Template).all()
    return [t.to_dict() for t in templates]


@app.get("/api/templates/{template_id}", response_model=TemplateResponse)
async def get_template(template_id: int, db: Session = Depends(get_db)):
    """获取指定模板"""
    template = db.query(Template).filter(Template.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="模板不存在")
    return template.to_dict()


@app.put("/api/templates/{template_id}", response_model=TemplateResponse)
async def update_template(
    template_id: int,
    template: TemplateUpdate,
    db: Session = Depends(get_db)
):
    """更新模板"""
    db_template = db.query(Template).filter(Template.id == template_id).first()
    if not db_template:
        raise HTTPException(status_code=404, detail="模板不存在")

    try:
        if template.name is not None:
            db_template.name = template.name
        if template.fields is not None:
            fields_json = json.dumps([field.dict() for field in template.fields], ensure_ascii=False)
            db_template.fields = fields_json

        db.commit()
        db.refresh(db_template)
        return db_template.to_dict()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"更新模板失败: {str(e)}")


@app.delete("/api/templates/{template_id}")
async def delete_template(template_id: int, db: Session = Depends(get_db)):
    """删除模板"""
    db_template = db.query(Template).filter(Template.id == template_id).first()
    if not db_template:
        raise HTTPException(status_code=404, detail="模板不存在")

    try:
        db.delete(db_template)
        db.commit()
        return {"success": True, "message": "模板已删除"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"删除模板失败: {str(e)}")


# ==================== 文件上传和信息提取API ====================

@app.post("/api/extract", response_model=ExtractionResponse)
async def extract_information(
    template_id: int = Form(...),
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    """上传文件并提取信息"""

    # 检查API密钥
    if not ZHIPU_API_KEY:
        raise HTTPException(status_code=500, detail="未配置智谱AI API密钥")

    # 获取模板
    template = db.query(Template).filter(Template.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="模板不存在")

    template_data = template.to_dict()
    fields = template_data["fields"]

    # 初始化AI提取器
    ai_extractor = AIExtractor(ZHIPU_API_KEY)

    results = []

    try:
        for uploaded_file in files:
            # 保存上传的文件
            file_path = os.path.join(UPLOAD_DIR, uploaded_file.filename)
            with open(file_path, "wb") as f:
                shutil.copyfileobj(uploaded_file.file, f)

            try:
                # 解析文件
                document_text = file_parser.parse_file(file_path)

                # AI提取信息
                extracted_data = ai_extractor.extract_information(document_text, fields)

                # 添加文件名到结果
                extracted_data["文件名"] = uploaded_file.filename

                results.append(extracted_data)

            except Exception as e:
                # 单个文件处理失败，记录错误但继续处理其他文件
                results.append({
                    "文件名": uploaded_file.filename,
                    "错误": str(e)
                })

            finally:
                # 清理临时文件
                if os.path.exists(file_path):
                    os.remove(file_path)

        return ExtractionResponse(
            success=True,
            data=results,
            message=f"成功处理 {len(results)} 个文件"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"提取失败: {str(e)}")


# ==================== 健康检查 ====================

@app.get("/health")
async def health_check_endpoint():
    """健康检查端点"""
    return {
        "status": "healthy",
        "api_key_configured": bool(ZHIPU_API_KEY)
    }


# ==================== 静态文件服务 ====================

# 挂载静态文件目录（前端） - 必须放在最后，否则会覆盖API路由
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(FRONTEND_DIR):
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
