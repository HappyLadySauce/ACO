from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.schemas.task import (
    TaskCreate, TaskUpdate, TaskResponse, TaskWithAssignments,
    TaskAssignmentCreate, TaskAssignmentUpdate, TaskAssignmentResponse
)
from app.services.task_service import TaskService, TaskAssignmentService
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()

# ======================== 任务管理接口 ========================

@router.get("/tasks", response_model=List[TaskResponse])
async def get_tasks(
    skip: int = Query(0, ge=0, description="跳过的记录数"),
    limit: int = Query(100, ge=1, le=1000, description="限制返回的记录数"),
    status: Optional[str] = Query(None, description="任务状态过滤"),
    task_type: Optional[str] = Query(None, description="任务类型过滤"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取任务列表"""
    tasks = TaskService.get_tasks(
        db=db, 
        skip=skip, 
        limit=limit, 
        status=status, 
        task_type=task_type
    )
    return tasks

@router.get("/tasks/count")
async def get_tasks_count(
    status: Optional[str] = Query(None, description="任务状态过滤"),
    task_type: Optional[str] = Query(None, description="任务类型过滤"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取任务总数"""
    count = TaskService.get_tasks_count(db=db, status=status, task_type=task_type)
    return {"count": count}

@router.get("/tasks/{task_id}", response_model=TaskWithAssignments)
async def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """根据ID获取任务详情（包含分配信息）"""
    task = TaskService.get_task_with_assignments(db=db, task_id=task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="任务不存在"
        )
    return task

@router.post("/tasks", response_model=TaskResponse)
async def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建任务"""
    # 检查权限（只有管理员可以创建任务）
    if current_user.type != "管理员":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有管理员可以创建任务"
        )
    
    db_task = TaskService.create_task(db=db, task=task)
    return db_task

@router.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新任务"""
    # 检查权限（只有管理员可以更新任务）
    if current_user.type != "管理员":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有管理员可以更新任务"
        )
    
    db_task = TaskService.update_task(db=db, task_id=task_id, task=task)
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="任务不存在"
        )
    return db_task

@router.delete("/tasks/{task_id}")
async def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除任务"""
    # 检查权限（只有管理员可以删除任务）
    if current_user.type != "管理员":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有管理员可以删除任务"
        )
    
    success = TaskService.delete_task(db=db, task_id=task_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="任务不存在"
        )
    return {"message": "任务删除成功"}

# ======================== 任务分配接口 ========================

@router.get("/task-assignments", response_model=List[TaskAssignmentResponse])
async def get_task_assignments(
    skip: int = Query(0, ge=0, description="跳过的记录数"),
    limit: int = Query(100, ge=1, le=1000, description="限制返回的记录数"),
    status: Optional[str] = Query(None, description="分配状态过滤"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取任务分配列表"""
    assignments = TaskAssignmentService.get_assignments(
        db=db, 
        skip=skip, 
        limit=limit, 
        status=status
    )
    return assignments

@router.get("/tasks/{task_id}/assignments", response_model=List[TaskAssignmentResponse])
async def get_task_assignments_by_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """根据任务ID获取分配列表"""
    # 检查任务是否存在
    task = TaskService.get_task(db=db, task_id=task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="任务不存在"
        )
    
    assignments = TaskAssignmentService.get_assignments_by_task(db=db, task_id=task_id)
    return assignments

@router.get("/users/{user_id}/task-assignments", response_model=List[TaskAssignmentResponse])
async def get_user_task_assignments(
    user_id: int,
    status: Optional[str] = Query(None, description="分配状态过滤"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """根据用户ID获取任务分配列表"""
    # 检查权限（用户只能查看自己的分配，管理员可以查看所有）
    if current_user.type != "管理员" and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权查看其他用户的任务分配"
        )
    
    assignments = TaskAssignmentService.get_assignments_by_user(
        db=db, 
        user_id=user_id, 
        status=status
    )
    return assignments

@router.get("/users/{user_id}/task-stats")
async def get_user_task_stats(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取用户任务统计"""
    # 检查权限（用户只能查看自己的统计，管理员可以查看所有）
    if current_user.type != "管理员" and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权查看其他用户的任务统计"
        )
    
    stats = TaskAssignmentService.get_user_task_stats(db=db, user_id=user_id)
    return stats

@router.get("/task-assignments/stats")
async def get_task_assignments_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取全部任务分配统计"""
    # 检查权限（只有管理员可以查看全部统计）
    if current_user.type != "管理员":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有管理员可以查看全部任务统计"
        )
    
    stats = TaskAssignmentService.get_all_task_stats(db=db)
    return stats

@router.post("/task-assignments", response_model=TaskAssignmentResponse)
async def create_task_assignment(
    assignment: TaskAssignmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建任务分配"""
    # 检查权限（只有管理员可以分配任务）
    if current_user.type != "管理员":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有管理员可以分配任务"
        )
    
    db_assignment = TaskAssignmentService.create_assignment(db=db, assignment=assignment)
    if not db_assignment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="任务或用户不存在"
        )
    return db_assignment

@router.put("/task-assignments/{assignment_id}", response_model=TaskAssignmentResponse)
async def update_task_assignment(
    assignment_id: int,
    assignment: TaskAssignmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新任务分配"""
    # 获取现有分配
    existing_assignment = TaskAssignmentService.get_assignment(db=db, assignment_id=assignment_id)
    if not existing_assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="任务分配不存在"
        )
    
    # 检查权限（用户只能更新自己的分配，管理员可以更新所有）
    if current_user.type != "管理员" and current_user.id != existing_assignment.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权更新其他用户的任务分配"
        )
    
    db_assignment = TaskAssignmentService.update_assignment(
        db=db, 
        assignment_id=assignment_id, 
        assignment=assignment
    )
    return db_assignment

@router.delete("/task-assignments/{assignment_id}")
async def delete_task_assignment(
    assignment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除任务分配"""
    # 检查权限（只有管理员可以删除任务分配）
    if current_user.type != "管理员":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有管理员可以删除任务分配"
        )
    
    success = TaskAssignmentService.delete_assignment(db=db, assignment_id=assignment_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="任务分配不存在"
        )
    return {"message": "任务分配删除成功"}

# ======================== 我的任务接口 ========================

@router.get("/my-tasks", response_model=List[TaskAssignmentResponse])
async def get_my_tasks(
    status: Optional[str] = Query(None, description="任务状态过滤"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取当前用户的任务分配"""
    assignments = TaskAssignmentService.get_assignments_by_user(
        db=db, 
        user_id=current_user.id, 
        status=status
    )
    return assignments

@router.get("/my-task-stats")
async def get_my_task_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取当前用户的任务统计"""
    stats = TaskAssignmentService.get_user_task_stats(db=db, user_id=current_user.id)
    return stats

@router.put("/my-tasks/{assignment_id}", response_model=TaskAssignmentResponse)
async def update_my_task(
    assignment_id: int,
    assignment: TaskAssignmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新我的任务进度"""
    # 获取现有分配
    existing_assignment = TaskAssignmentService.get_assignment(db=db, assignment_id=assignment_id)
    if not existing_assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="任务分配不存在"
        )
    
    # 检查权限（只能更新自己的任务）
    if current_user.id != existing_assignment.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权更新其他用户的任务"
        )
    
    db_assignment = TaskAssignmentService.update_assignment(
        db=db, 
        assignment_id=assignment_id, 
        assignment=assignment
    )
    return db_assignment 