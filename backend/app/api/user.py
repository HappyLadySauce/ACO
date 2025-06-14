from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List
import io
import json
from openpyxl import Workbook, load_workbook
from app.database import get_db
from app.schemas.user import UserCreate, UserResponse, UserUpdate, BulkImportResult
from app.services.user_service import UserService
from app.api.deps import get_current_user, get_admin_user

router = APIRouter()

@router.get("/users", response_model=List[UserResponse])
async def get_users(
    skip: int = Query(0, ge=0, description="跳过的记录数"),
    limit: int = Query(100, ge=1, le=1000, description="返回的记录数"),
    role: str = Query(None, description="筛选角色"),
    user_type: str = Query(None, description="筛选用户类型"),
    db: Session = Depends(get_db),
    current_user = Depends(get_admin_user)
) -> List[UserResponse]:
    """获取用户列表（管理员权限）"""
    if role:
        users = UserService.get_users_by_role(db, role)
    elif user_type:
        users = UserService.get_users_by_type(db, user_type)
    else:
        users = UserService.get_users(db, skip=skip, limit=limit)
    
    return [UserResponse.model_validate(user) for user in users]

@router.post("/users", response_model=UserResponse)
async def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_admin_user)
) -> UserResponse:
    """创建用户（管理员权限）"""
    db_user = UserService.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已存在"
        )
    
    new_user = UserService.create_user(db=db, user=user)
    return UserResponse.model_validate(new_user)

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_admin_user)
) -> UserResponse:
    """获取指定用户信息（管理员权限）"""
    db_user = UserService.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    return UserResponse.model_validate(db_user)

@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_admin_user)
) -> UserResponse:
    """更新用户信息（管理员权限）"""
    db_user = UserService.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    updated_user = UserService.update_user(db=db, user_id=user_id, user=user)
    return UserResponse.model_validate(updated_user)

@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_admin_user)
):
    """删除用户（管理员权限）"""
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不能删除自己的账户"
        )
    
    success = UserService.delete_user(db=db, user_id=user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    return {"message": "用户删除成功"}

@router.patch("/users/{user_id}/status")
async def update_user_status(
    user_id: int,
    status: str = Query(..., description="用户状态"),
    db: Session = Depends(get_db),
    current_user = Depends(get_admin_user)
) -> UserResponse:
    """更新用户状态（管理员权限）"""
    if user_id == current_user.id and status == 'inactive':
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不能禁用自己的账户"
        )
    
    updated_user = UserService.update_user_status(db=db, user_id=user_id, status=status)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    return UserResponse.model_validate(updated_user)

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user = Depends(get_current_user)) -> UserResponse:
    """获取当前用户信息"""
    return UserResponse.model_validate(current_user)

@router.put("/profile", response_model=UserResponse)
async def update_profile(
    user: UserUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
) -> UserResponse:
    """更新个人资料"""
    # 普通用户只能更新自己的头像等基本信息
    profile_data = UserUpdate(photo_data=user.photo_data)
    updated_user = UserService.update_user(db=db, user_id=current_user.id, user=profile_data)
    return UserResponse.model_validate(updated_user)

@router.post("/users/bulk-import", response_model=BulkImportResult)
async def bulk_import_users(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_admin_user)
) -> BulkImportResult:
    """批量导入用户（管理员权限）"""
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="只支持Excel文件格式（.xlsx, .xls）"
        )
    
    try:
        # 读取Excel文件
        contents = await file.read()
        workbook = load_workbook(io.BytesIO(contents))
        worksheet = workbook.active
        
        # 获取表头
        headers = [cell.value for cell in worksheet[1]]
        
        # 验证必要的列
        required_columns = ['用户名', '密码', '角色', '用户类型', '状态']
        missing_columns = [col for col in required_columns if col not in headers]
        if missing_columns:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Excel文件缺少必要列：{', '.join(missing_columns)}"
            )
        
        # 获取列索引
        column_indexes = {col: headers.index(col) for col in required_columns}
        
        # 转换为UserCreate对象列表
        users_to_create = []
        for row in worksheet.iter_rows(min_row=2, values_only=True):
            if not row or not any(row):  # 跳过空行
                continue
                
            try:
                user_create = UserCreate(
                    username=str(row[column_indexes['用户名']]).strip(),
                    password=str(row[column_indexes['密码']]).strip(),
                    role=str(row[column_indexes['角色']]).strip(),
                    type=str(row[column_indexes['用户类型']]).strip(),
                    status=str(row[column_indexes['状态']]).strip()
                )
                users_to_create.append(user_create)
            except (IndexError, ValueError, TypeError) as e:
                continue  # 跳过无效行
        
        if not users_to_create:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="文件中没有有效的用户数据"
            )
        
        # 批量创建用户
        result = UserService.bulk_create_users(db, users_to_create)
        return result
        
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"文件处理失败：{str(e)}"
        )

@router.get("/users/template/download")
async def download_user_template():
    """下载用户导入模板"""
    # 创建工作簿
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "用户导入模板"
    
    # 设置表头
    headers = ['用户名', '密码', '角色', '用户类型', '状态']
    for col, header in enumerate(headers, 1):
        worksheet.cell(row=1, column=col, value=header)
    
    # 添加示例数据
    sample_data = [
        ['user1', '123456', '网络工程师', '操作员', 'active'],
        ['user2', '123456', '系统架构师', '操作员', 'active'],
        ['user3', '123456', '系统规划与管理师', '管理员', 'active']
    ]
    
    for row_idx, row_data in enumerate(sample_data, 2):
        for col_idx, value in enumerate(row_data, 1):
            worksheet.cell(row=row_idx, column=col_idx, value=value)
    
    # 保存到内存
    output = io.BytesIO()
    workbook.save(output)
    output.seek(0)
    
    return StreamingResponse(
        io.BytesIO(output.read()),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={"Content-Disposition": "attachment; filename=user_import_template.xlsx"}
    ) 