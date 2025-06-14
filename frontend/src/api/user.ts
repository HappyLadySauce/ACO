import request from '@/utils/request'
import type { User, UserForm, UserUpdate } from '@/types/user'

// 获取用户列表
export const getUserList = (params?: {
  skip?: number
  limit?: number
  role?: string
  user_type?: string
}) => {
  return request.get<User[]>('/users', { params })
}

// 获取用户列表 (别名)
export const getUsers = (params?: {
  skip?: number
  limit?: number
  role?: string
  user_type?: string
}) => {
  return request.get<User[]>('/users', { params })
}

// 创建用户
export const createUser = (data: UserForm) => {
  return request.post<User>('/users', data)
}

// 更新用户
export const updateUser = (id: number, data: UserUpdate) => {
  return request.put<User>(`/users/${id}`, data)
}

// 删除用户
export const deleteUser = (id: number) => {
  return request.delete(`/users/${id}`)
}

// 获取用户详情
export const getUserDetail = (id: number) => {
  return request.get<User>(`/users/${id}`)
}

// 更新用户状态
export const updateUserStatus = (id: number, status: string) => {
  return request.put<User>(`/users/${id}`, { status })
} 