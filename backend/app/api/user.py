from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.user import UserCreate, UserResponse, UserUpdate
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