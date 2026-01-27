# schemas/common.py
from typing import Generic, TypeVar, Optional
from pydantic import BaseModel, Field


T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    """统一 API 响应格式"""
    code: int = Field(0, description="状态码，0表示成功")
    message: str = Field("success", description="响应消息")
    data: Optional[T] = Field(None, description="响应数据")


class PaginationParams(BaseModel):
    """分页参数"""
    page: int = Field(1, ge=1, description="页码")
    page_size: int = Field(20, ge=1, le=100, description="每页数量")


class PaginatedResponse(BaseModel, Generic[T]):
    """分页响应"""
    items: list[T]
    total: int
    page: int
    page_size: int
    total_pages: int
