from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class DeviceBase(BaseModel):
    """设备基础模式"""
    name: str
    type: Optional[str] = None
    status: Optional[str] = 'offline'
    location: Optional[str] = None

class DeviceCreate(DeviceBase):
    """设备创建模式"""
    pass

class DeviceUpdate(BaseModel):
    """设备更新模式"""
    name: Optional[str] = None
    type: Optional[str] = None
    status: Optional[str] = None
    location: Optional[str] = None

class DeviceResponse(DeviceBase):
    """设备响应模式"""
    id: int
    last_active: datetime
    
    model_config = ConfigDict(from_attributes=True) 