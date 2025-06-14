"""
任务数据初始化脚本
用于初始化一些测试任务数据
"""

import sys
import os
from pathlib import Path

# 添加backend目录到Python路径
backend_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_dir))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models.task import Task, TaskAssignment
from app.models.user import User
from datetime import datetime

def init_task_data():
    """初始化任务测试数据"""
    db = SessionLocal()
    
    try:
        # 检查是否已有任务数据
        existing_tasks = db.query(Task).count()
        if existing_tasks > 0:
            print(f"数据库中已有 {existing_tasks} 个任务，跳过初始化")
            return
        
        # 创建示例任务
        sample_tasks = [
            {
                "name": "系统漏洞扫描",
                "type": "安全检测",
                "phase": "检测阶段",
                "description": "对生产环境进行全面的安全漏洞扫描，包括操作系统、应用程序和网络设备",
                "status": "未分配"
            },
            {
                "name": "数据库性能优化",
                "type": "性能调优",
                "phase": "优化阶段", 
                "description": "分析数据库查询性能，优化慢查询，调整索引策略",
                "status": "未分配"
            },
            {
                "name": "网络设备健康检查",
                "type": "设备维护",
                "phase": "检查阶段",
                "description": "检查路由器、交换机等网络设备的运行状态和性能指标",
                "status": "未分配"
            },
            {
                "name": "应用服务器监控配置",
                "type": "监控部署",
                "phase": "配置阶段",
                "description": "为应用服务器配置监控系统，设置告警规则和仪表板",
                "status": "未分配"
            },
            {
                "name": "日志系统清理",
                "type": "系统维护",
                "phase": "维护阶段",
                "description": "清理过期日志文件，归档重要日志，释放磁盘空间",
                "status": "未分配"
            },
            {
                "name": "备份系统测试",
                "type": "系统验证",
                "phase": "测试阶段",
                "description": "验证备份系统的可靠性，测试数据恢复流程",
                "status": "未分配"
            }
        ]
        
        # 插入任务数据
        for task_data in sample_tasks:
            task = Task(**task_data)
            db.add(task)
        
        db.commit()
        print(f"成功创建 {len(sample_tasks)} 个示例任务")
        
        # 获取已创建的任务
        tasks = db.query(Task).all()
        print("\n创建的任务列表：")
        for task in tasks:
            print(f"- ID: {task.id}, 名称: {task.name}, 类型: {task.type}, 状态: {task.status}")
            
    except Exception as e:
        print(f"初始化任务数据时发生错误: {e}")
        db.rollback()
    finally:
        db.close()

def init_task_assignments():
    """初始化任务分配数据（需要先有用户数据）"""
    db = SessionLocal()
    
    try:
        # 检查是否有用户数据
        users = db.query(User).all()
        if not users:
            print("没有找到用户数据，请先创建用户")
            return
            
        # 检查是否有任务数据
        tasks = db.query(Task).all()
        if not tasks:
            print("没有找到任务数据，请先创建任务")
            return
            
        # 检查是否已有分配数据
        existing_assignments = db.query(TaskAssignment).count()
        if existing_assignments > 0:
            print(f"数据库中已有 {existing_assignments} 个任务分配，跳过初始化")
            return
        
        # 创建示例任务分配
        assignments_created = 0
        
        # 为前几个任务分配给用户
        for i, task in enumerate(tasks[:3]):  # 只为前3个任务分配
            if i < len(users):
                user = users[i % len(users)]  # 循环分配给用户
                
                assignment = TaskAssignment(
                    task_id=task.id,
                    user_id=user.id,
                    username=user.username,
                    status="进行中",
                    progress=25 + (i * 15),  # 不同的进度
                    performance_score=0,
                    comments=f"任务已开始执行，当前进度: {25 + (i * 15)}%"
                )
                
                db.add(assignment)
                
                # 更新任务状态
                task.status = "进行中"
                assignments_created += 1
        
        db.commit()
        print(f"成功创建 {assignments_created} 个示例任务分配")
        
        # 显示分配结果
        assignments = db.query(TaskAssignment).all()
        print("\n创建的任务分配列表：")
        for assignment in assignments:
            print(f"- 分配ID: {assignment.id}, 任务ID: {assignment.task_id}, "
                  f"用户: {assignment.username}, 状态: {assignment.status}, "
                  f"进度: {assignment.progress}%")
            
    except Exception as e:
        print(f"初始化任务分配数据时发生错误: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("开始初始化任务数据...")
    init_task_data()
    
    print("\n开始初始化任务分配数据...")
    init_task_assignments()
    
    print("\n任务数据初始化完成！") 