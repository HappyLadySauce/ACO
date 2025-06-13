from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import Token, UserResponse
from app.services.user_service import UserService
from app.utils.security import create_access_token
from app.config import settings
from app.api.deps import get_current_user

router = APIRouter()

@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    login_type: str = Form(...),
    db: Session = Depends(get_db)
) -> Token:
    """用户登录"""
    user = UserService.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if user.status == 'inactive':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="账户已被禁用",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 验证用户类型是否匹配
    if user.type != login_type:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"您的账户类型是\"{user.type}\"，请选择正确的登录类型",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.model_validate(user)
    )

@router.post("/logout")
async def logout(current_user = Depends(get_current_user)):
    """用户登出"""
    # 在实际应用中，这里可以将token加入黑名单
    return {"message": "登出成功"}

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user = Depends(get_current_user)) -> UserResponse:
    """获取当前用户信息"""
    return UserResponse.model_validate(current_user)

@router.post("/refresh")
async def refresh_token(current_user = Depends(get_current_user)) -> Token:
    """刷新访问令牌"""
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": current_user.username}, expires_delta=access_token_expires
    )
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.model_validate(current_user)
    )