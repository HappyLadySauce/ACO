# 多智能体协作运维系统 - 项目部署指南

## 项目概述

基于Vue3 + FastAPI的前后端分离多智能体协作运维系统，提供用户管理、任务分配、设备监控、桌面管理等核心功能。

## 技术栈

### 前端技术栈
- **框架**: Vue3 + TypeScript + Element Plus
- **构建工具**: Vite
- **状态管理**: Pinia
- **路由**: Vue Router 4
- **HTTP客户端**: Axios
- **UI组件**: Element Plus

### 后端技术栈
- **框架**: FastAPI (Python)
- **数据库**: MySQL
- **ORM**: SQLAlchemy
- **认证**: JWT + OAuth2
- **数据验证**: Pydantic

## 项目结构

```
project/
├── frontend/                 # 前端项目
│   ├── src/
│   │   ├── api/             # API接口
│   │   ├── components/       # 组件
│   │   ├── store/           # 状态管理
│   │   ├── types/           # TypeScript类型
│   │   ├── utils/           # 工具函数
│   │   ├── views/           # 页面组件
│   │   └── router/          # 路由配置
│   ├── package.json
│   └── vite.config.ts
├── backend/                  # 后端项目
│   ├── app/
│   │   ├── api/             # API路由
│   │   ├── models/          # 数据模型
│   │   ├── schemas/         # Pydantic模式
│   │   ├── services/        # 业务逻辑
│   │   ├── utils/           # 工具函数
│   │   ├── config.py        # 配置
│   │   ├── database.py      # 数据库连接
│   │   └── main.py          # 应用入口
│   └── requirements.txt
└── 前后端分离重构技术手册.md
```

## 快速开始

### 1. 环境准备

#### 系统要求
- Python 3.8+
- Node.js 16+
- MySQL 8.0+

#### 安装Python依赖
```bash
cd backend
pip install -r requirements.txt
```

#### 安装Node.js依赖
```bash
cd frontend
npm install
```

### 2. 数据库配置

#### 创建数据库
```sql
CREATE DATABASE conlse_test CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

#### 修改数据库连接
编辑 `backend/app/config.py`：
```python
DATABASE_URL = "mysql+pymysql://用户名:密码@localhost:3306/conlse_test"
```

### 3. 启动后端服务

```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

后端服务将在 http://localhost:8000 启动
API文档：http://localhost:8000/docs

### 4. 启动前端服务

```bash
cd frontend
npm run dev
```

前端服务将在 http://localhost:3000 启动

## 系统功能

### 1. 用户管理
- ✅ 用户登录/登出
- ✅ 用户CRUD操作（管理员权限）
- ✅ 角色权限控制
- ✅ 用户状态管理

### 2. 任务管理
- 📋 任务创建和分配
- 📋 任务进度跟踪
- 📋 任务状态管理

### 3. 设备管理
- 🔧 设备状态监控
- 🔧 设备信息管理
- 🔧 设备位置跟踪

### 4. 桌面管理
- 🖥️ 桌面项目管理
- 🖥️ 工具箱配置
- 🖥️ 界面个性化

### 5. 系统设置
- ⚙️ 系统参数配置
- ⚙️ 用户权限设置
- ⚙️ 安全设置

## API 接口

### 认证接口
- `POST /auth/login` - 用户登录
- `POST /auth/logout` - 用户登出
- `GET /auth/me` - 获取当前用户信息
- `POST /auth/refresh` - 刷新令牌

### 用户管理接口
- `GET /api/users` - 获取用户列表
- `POST /api/users` - 创建用户
- `GET /api/users/{user_id}` - 获取用户详情
- `PUT /api/users/{user_id}` - 更新用户
- `DELETE /api/users/{user_id}` - 删除用户

## 数据库表结构

### 1. 用户表 (users)
```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(255),
    type VARCHAR(50),
    status VARCHAR(50) DEFAULT 'inactive',
    photo_data LONGTEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### 2. 任务表 (tasks)
```sql
CREATE TABLE tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(100),
    phase VARCHAR(50),
    description TEXT,
    status VARCHAR(50) DEFAULT '未分配',
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### 3. 设备表 (devices)
```sql
CREATE TABLE devices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(100),
    status VARCHAR(50) DEFAULT 'offline',
    location VARCHAR(255),
    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 开发说明

### 权限控制
- **管理员**: 拥有所有权限
- **操作员**: 拥有用户读取、任务管理、设备管理、桌面管理权限
- **观察员**: 只有读取权限

### 默认账户
- 用户名: `admin`
- 密码: `123456`
- 类型: 管理员

### API认证
系统使用JWT Bearer Token认证，token有效期30分钟。

### 错误处理
- 401: 未授权，需要登录
- 403: 权限不足
- 404: 资源不存在
- 422: 参数验证错误
- 500: 服务器内部错误

## 部署说明

### 生产环境部署

#### 1. 后端部署
```bash
# 使用Gunicorn部署
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

#### 2. 前端部署
```bash
# 构建生产版本
npm run build

# 部署到Nginx
cp -r dist/* /var/www/html/
```

#### 3. Nginx配置
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    # 前端静态文件
    location / {
        root /var/www/html;
        try_files $uri $uri/ /index.html;
    }
    
    # API代理
    location /api/ {
        proxy_pass http://localhost:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /auth/ {
        proxy_pass http://localhost:8000/auth/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 故障排除

### 常见问题

1. **数据库连接失败**
   - 检查MySQL服务是否启动
   - 验证数据库连接字符串是否正确
   - 确认数据库用户权限

2. **前端无法访问后端API**
   - 检查后端服务是否启动在8000端口
   - 验证CORS配置是否正确
   - 检查防火墙设置

3. **登录失败**
   - 确认数据库中有用户数据
   - 检查密码哈希是否正确
   - 验证JWT配置

## 开发团队

如需技术支持，请联系开发团队。

---

📖 **技术手册**: 详见 `前后端分离重构技术手册.md` #   A C O  
 