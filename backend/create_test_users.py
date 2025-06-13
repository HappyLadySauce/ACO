#!/usr/bin/env python3
"""
创建测试用户脚本
用于初始化系统的管理员和操作员用户
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models.user import User
from app.utils.security import get_password_hash

def create_test_users():
    """创建测试用户"""
    db: Session = SessionLocal()
    
    try:
        # 创建管理员用户
        admin_users = [
            {
                'username': 'admin',
                'password': '123456',
                'type': '管理员',
                'role': '系统管理员',
                'status': 'active'
            },
            {
                'username': 'admin2',
                'password': '123456',
                'type': '管理员',
                'role': '系统管理员',
                'status': 'active'
            }
        ]
        
        # 创建操作员用户
        operator_users = [
            {
                'username': 'network_engineer',
                'password': '123456',
                'type': '操作员',
                'role': '网络工程师',
                'status': 'active'
            },
            {
                'username': 'sys_architect',
                'password': '123456',
                'type': '操作员',
                'role': '系统架构师',
                'status': 'active'
            },
            {
                'username': 'sys_planner',
                'password': '123456',
                'type': '操作员',
                'role': '系统规划与管理师',
                'status': 'active'
            },
            {
                'username': 'sys_analyst',
                'password': '123456',
                'type': '操作员',
                'role': '系统分析师',
                'status': 'active'
            }
        ]
        
        all_users = admin_users + operator_users
        
        for user_data in all_users:
            # 检查用户是否已存在
            existing_user = db.query(User).filter(User.username == user_data['username']).first()
            if existing_user:
                print(f"用户 {user_data['username']} 已存在，跳过创建")
                continue
            
            # 创建新用户
            hashed_password = get_password_hash(user_data['password'])
            new_user = User(
                username=user_data['username'],
                hashed_password=hashed_password,
                type=user_data['type'],
                role=user_data['role'],
                status=user_data['status']
            )
            
            db.add(new_user)
            print(f"创建用户: {user_data['username']} ({user_data['type']} - {user_data['role']})")
        
        db.commit()
        print("\n用户创建完成！")
        
        # 显示创建的用户信息
        print("\n=== 管理员账户 ===")
        print("用户名: admin, 密码: 123456 (管理员)")
        print("用户名: admin2, 密码: 123456 (管理员)")
        
        print("\n=== 操作员账户 ===")
        print("用户名: network_engineer, 密码: 123456 (操作员 - 网络工程师)")
        print("用户名: sys_architect, 密码: 123456 (操作员 - 系统架构师)")
        print("用户名: sys_planner, 密码: 123456 (操作员 - 系统规划与管理师)")
        print("用户名: sys_analyst, 密码: 123456 (操作员 - 系统分析师)")
        
        print("\n=== 登录说明 ===")
        print("1. 管理员可以选择\"管理员登录\"直接进入系统管理后台")
        print("2. 操作员需要选择\"操作员登录\"，然后选择对应的角色")
        print("3. 操作员只能选择与自己权限匹配的角色")
        
    except Exception as e:
        print(f"创建用户失败: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("开始创建测试用户...")
    create_test_users() 