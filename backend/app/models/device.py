from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.sql import func
from app.database import Base

class Device(Base):
    """设备模型"""
    __tablename__ = "devices"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, comment="设备名称")
    type = Column(String(100), comment="设备类型")
    status = Column(String(50), default='offline', comment="设备状态")
    location = Column(String(255), comment="设备位置")
    last_active = Column(TIMESTAMP, server_default=func.now(), comment="最后活跃时间")
    
    def __repr__(self):
        return f"<Device(id={self.id}, name='{self.name}', status='{self.status}')>" 