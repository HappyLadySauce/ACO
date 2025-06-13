<template>
  <div class="user-management">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>用户管理</span>
          <el-button type="primary" @click="handleAdd">
            <el-icon><Plus /></el-icon>
            新增用户
          </el-button>
        </div>
      </template>

      <!-- 搜索栏 -->
      <div class="search-bar">
        <el-form :model="searchForm" inline>
          <el-form-item label="用户名">
            <el-input 
              v-model="searchForm.username" 
              placeholder="请输入用户名"
              clearable
            />
          </el-form-item>
          <el-form-item label="角色">
            <el-select v-model="searchForm.role" placeholder="选择角色" clearable>
              <el-option label="网络工程师" value="网络工程师" />
              <el-option label="系统架构师" value="系统架构师" />
              <el-option label="系统规划与管理师" value="系统规划与管理师" />
              <el-option label="系统分析师" value="系统分析师" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">
              <el-icon><Search /></el-icon>
              搜索
            </el-button>
            <el-button @click="handleReset">重置</el-button>
          </el-form-item>
        </el-form>
      </div>

      <!-- 用户表格 -->
      <el-table :data="users" v-loading="loading" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="username" label="用户名" />
        <el-table-column prop="role" label="角色">
          <template #default="scope">
            <el-tag :type="getRoleType(scope.row.role)">
              {{ getRoleText(scope.row.role) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="type" label="类型" />
        <el-table-column prop="status" label="状态">
          <template #default="scope">
            <el-tag :type="scope.row.status === 'active' ? 'success' : 'danger'">
              {{ scope.row.status === 'active' ? '激活' : '未激活' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" />
        <el-table-column label="操作" width="200">
          <template #default="scope">
            <el-button size="small" @click="handleEdit(scope.row)">
              编辑
            </el-button>
            <el-button 
              size="small" 
              type="danger" 
              @click="handleDelete(scope.row)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination">
        <el-pagination
          v-model:current-page="pagination.currentPage"
          v-model:page-size="pagination.pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="pagination.total"
          layout="sizes, prev, pager, next, jumper, total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- 用户编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑用户' : '新增用户'"
      width="600px"
    >
      <el-form
        ref="formRef"
        :model="userForm"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="用户名" prop="username">
          <el-input v-model="userForm.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="密码" prop="password" v-if="!isEdit">
          <el-input 
            v-model="userForm.password" 
            type="password" 
            placeholder="请输入密码" 
          />
        </el-form-item>
        <el-form-item label="角色" prop="role">
          <el-select v-model="userForm.role" placeholder="选择角色">
            <el-option label="网络工程师" value="网络工程师" />
            <el-option label="系统架构师" value="系统架构师" />
            <el-option label="系统规划与管理师" value="系统规划与管理师" />
            <el-option label="系统分析师" value="系统分析师" />
          </el-select>
        </el-form-item>
        <el-form-item label="类型" prop="type">
          <el-select v-model="userForm.type" placeholder="选择用户类型">
            <el-option label="管理员" value="管理员" />
            <el-option label="操作员" value="操作员" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="userForm.status" placeholder="选择状态">
            <el-option label="激活" value="active" />
            <el-option label="未激活" value="inactive" />
          </el-select>
        </el-form-item>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">
            确定
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox, type FormInstance } from 'element-plus'
import { Plus, Search } from '@element-plus/icons-vue'
import { getUserList, createUser, updateUser, deleteUser } from '@/api/user'
import type { UserForm, UserUpdate } from '@/types/user'

interface User {
  id: number
  username: string
  role: string
  type: string
  status: string
  created_at: string
  updated_at: string
}

const loading = ref(false)
const dialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref<FormInstance>()

const searchForm = reactive({
  username: '',
  role: ''
})

const userForm = reactive({
  id: 0,
  username: '',
  password: '',
  role: '',
  type: '',
  status: 'active'
})

const pagination = reactive({
  currentPage: 1,
  pageSize: 10,
  total: 0
})

const users = ref<User[]>([])

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度在 6 到 20 个字符', trigger: 'blur' }
  ],
  role: [
    { required: true, message: '请选择角色', trigger: 'change' }
  ],
  type: [
    { required: true, message: '请输入用户类型', trigger: 'blur' }
  ],
  status: [
    { required: true, message: '请选择状态', trigger: 'change' }
  ]
}

const getRoleType = (role: string) => {
  switch (role) {
    case '网络工程师':
      return 'primary'
    case '系统架构师':
      return 'success'
    case '系统规划与管理师':
      return 'warning'
    case '系统分析师':
      return 'info'
    default:
      return ''
  }
}

const getRoleText = (role: string) => {
  return role
}

const loadUsers = async () => {
  loading.value = true
  try {
    const params = {
      skip: (pagination.currentPage - 1) * pagination.pageSize,
      limit: pagination.pageSize,
      role: searchForm.role || undefined,
      user_type: undefined
    }
    
    const response = await getUserList(params)
    users.value = response.data || []
    // 注意：如果后端没有返回total，这里需要单独获取
    pagination.total = users.value.length
  } catch (error) {
    console.error('加载用户列表失败:', error)
    ElMessage.error('加载用户列表失败')
    // 如果API调用失败，使用模拟数据作为后备
    users.value = [
      {
        id: 1,
        username: 'admin',
        role: '系统架构师',
        type: '管理员',
        status: 'active',
        created_at: '2024-01-15 10:30',
        updated_at: '2024-01-15 10:30'
      },
      {
        id: 2,
        username: 'operator1',
        role: '网络工程师',
        type: '操作员',
        status: 'active',
        created_at: '2024-01-14 14:20',
        updated_at: '2024-01-14 14:20'
      }
    ]
    pagination.total = users.value.length
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  loadUsers()
}

const handleReset = () => {
  searchForm.username = ''
  searchForm.role = ''
  loadUsers()
}

const handleAdd = () => {
  isEdit.value = false
  dialogVisible.value = true
  resetForm()
}

const handleEdit = (row: User) => {
  isEdit.value = true
  dialogVisible.value = true
  Object.assign(userForm, row)
}

const handleDelete = async (row: User) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除用户 "${row.username}" 吗？`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    
    await deleteUser(row.id)
    ElMessage.success('删除成功')
    loadUsers()
  } catch (error: any) {
    if (error === 'cancel') {
      // 用户取消了删除操作
      return
    }
    console.error('删除用户失败:', error)
    const message = error?.response?.data?.detail || '删除失败'
    ElMessage.error(message)
  }
}

const handleSubmit = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    
    if (isEdit.value) {
      // 更新用户
      const updateData: UserUpdate = {
        role: userForm.role,
        type: userForm.type,
        status: userForm.status
      }
      await updateUser(userForm.id, updateData)
      ElMessage.success('更新成功')
    } else {
      // 创建用户
      const createData: UserForm = {
        username: userForm.username,
        password: userForm.password,
        role: userForm.role,
        type: userForm.type,
        status: userForm.status
      }
      await createUser(createData)
      ElMessage.success('创建成功')
    }
    
    dialogVisible.value = false
    loadUsers()
  } catch (error: any) {
    console.error('操作失败:', error)
    const message = error?.response?.data?.detail || (isEdit.value ? '更新失败' : '创建失败')
    ElMessage.error(message)
  }
}

const resetForm = () => {
  userForm.id = 0
  userForm.username = ''
  userForm.password = ''
  userForm.role = ''
  userForm.type = ''
  userForm.status = 'active'
}

const handleSizeChange = (val: number) => {
  pagination.pageSize = val
  loadUsers()
}

const handleCurrentChange = (val: number) => {
  pagination.currentPage = val
  loadUsers()
}

onMounted(() => {
  loadUsers()
})
</script>

<style scoped lang="scss">
.user-management {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .search-bar {
    margin-bottom: 20px;
    padding: 20px;
    background: #f5f5f5;
    border-radius: 4px;
  }

  .pagination {
    margin-top: 20px;
    text-align: right;
  }
}
</style> 