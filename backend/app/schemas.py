"""
Pydantic模型（用于API请求和响应验证）
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class FieldSchema(BaseModel):
    """字段定义"""
    name: str = Field(..., description="字段名称")
    description: str = Field("", description="字段描述")


class TemplateCreate(BaseModel):
    """创建模板请求"""
    name: str = Field(..., description="模板名称")
    fields: List[FieldSchema] = Field(..., description="字段列表")


class TemplateUpdate(BaseModel):
    """更新模板请求"""
    name: Optional[str] = Field(None, description="模板名称")
    fields: Optional[List[FieldSchema]] = Field(None, description="字段列表")


class TemplateResponse(BaseModel):
    """模板响应"""
    id: int
    name: str
    fields: List[Dict[str, str]]
    created_at: Optional[str]
    updated_at: Optional[str]

    class Config:
        from_attributes = True


class ExtractionRequest(BaseModel):
    """信息提取请求"""
    template_id: int = Field(..., description="使用的模板ID")


class ExtractionResponse(BaseModel):
    """信息提取响应"""
    success: bool
    data: List[Dict[str, Any]]
    message: Optional[str] = None
