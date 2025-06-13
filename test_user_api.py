#!/usr/bin/env python3
"""
用户API测试脚本
"""
import requests
import json

# API基础URL
BASE_URL = "http://localhost:8000"

def test_user_api():
    """测试用户API功能"""
    
    # 1. 先登录获取token
    print("1. 测试登录...")
    login_data = {
        "username": "admin",
        "password": "123456"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        if response.status_code == 200:
            token_data = response.json()
            token = token_data["access_token"]
            print(f"✅ 登录成功，获取token: {token[:20]}...")
            
            headers = {"Authorization": f"Bearer {token}"}
            
            # 2. 测试获取用户列表
            print("\n2. 测试获取用户列表...")
            users_response = requests.get(f"{BASE_URL}/users", headers=headers)
            
            if users_response.status_code == 200:
                users = users_response.json()
                print(f"✅ 获取用户列表成功，共{len(users)}个用户")
                for user in users:
                    print(f"   - {user['username']} ({user['role']}, {user['type']})")
            else:
                print(f"❌ 获取用户列表失败: {users_response.status_code}")
                print(f"   响应: {users_response.text}")
            
            # 3. 测试创建用户
            print("\n3. 测试创建用户...")
            new_user_data = {
                "username": "test_user",
                "password": "test123",
                "role": "网络工程师",
                "type": "操作员",
                "status": "active"
            }
            
            create_response = requests.post(
                f"{BASE_URL}/users",
                json=new_user_data,
                headers=headers
            )
            
            if create_response.status_code == 200:
                created_user = create_response.json()
                print(f"✅ 创建用户成功: {created_user['username']}")
                user_id = created_user['id']
                
                # 4. 测试删除用户
                print("\n4. 测试删除用户...")
                delete_response = requests.delete(
                    f"{BASE_URL}/users/{user_id}",
                    headers=headers
                )
                
                if delete_response.status_code == 200:
                    print("✅ 删除用户成功")
                else:
                    print(f"❌ 删除用户失败: {delete_response.status_code}")
                    print(f"   响应: {delete_response.text}")
                    
            else:
                print(f"❌ 创建用户失败: {create_response.status_code}")
                print(f"   响应: {create_response.text}")
                
        else:
            print(f"❌ 登录失败: {response.status_code}")
            print(f"   响应: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到后端服务器，请确保后端正在运行在 http://localhost:8000")
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {e}")

if __name__ == "__main__":
    print("开始测试用户API功能...")
    test_user_api() 