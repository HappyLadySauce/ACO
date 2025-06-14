# 多智能体协作运维系统 - 后端

## 环境要求

- Python 3.11+
- MySQL 5.7+
- Redis (可选)

## 快速开始

### 1. 创建虚拟环境并安装依赖

```bash
# 创建虚拟环境
python.exe -m venv .venv

# 激活虚拟环境 (Windows)
.\.venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置数据库

确保 MySQL 服务正在运行，并且数据库 `conlse_sql` 已创建。

### 3. 启动服务

```bash
# 方式1: 使用 uvicorn 命令
python.exe -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 方式2: 使用启动脚本 (Windows)
start.bat
```

### 4. 访问API文档

服务启动后，访问以下地址查看API文档：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 项目结构

```
backend/
├── app/
│   ├── api/          # API路由
│   ├── models/       # 数据模型
│   ├── schemas/      # Pydantic模式
│   ├── services/     # 业务逻辑
│   ├── utils/        # 工具函数
│   ├── config.py     # 配置文件
│   ├── database.py   # 数据库连接
│   └── main.py       # 应用入口
├── requirements.txt  # 依赖列表
└── start.bat        # 启动脚本
```

## 依赖问题解决

如果遇到依赖安装问题，特别是 `pydantic-core` 编译错误，请按以下步骤操作：

1. 确保使用最新版本的 pip：
   ```bash
   python.exe -m pip install --upgrade pip
   ```

2. 安装基础构建工具：
   ```bash
   pip install wheel setuptools
   ```

3. 分步安装依赖：
   ```bash
   # 先安装核心依赖
   pip install fastapi uvicorn[standard] sqlalchemy pymysql python-multipart python-dotenv redis alembic
   
   # 再安装其他依赖
   pip install pydantic-settings python-jose[cryptography] passlib[bcrypt] celery mysql-connector-python
   ```

## 配置说明

主要配置项在 `app/config.py` 中：

- `DATABASE_URL`: 数据库连接字符串
- `SECRET_KEY`: JWT密钥
- `BACKEND_CORS_ORIGINS`: 允许的跨域源
- `DEBUG`: 调试模式

## API接口

### 认证相关
- `POST /api/auth/login` - 用户登录
- `POST /api/auth/register` - 用户注册

### 用户管理
- `GET /api/users/me` - 获取当前用户信息
- `PUT /api/users/me` - 更新用户信息

更多接口详情请查看 API 文档。 