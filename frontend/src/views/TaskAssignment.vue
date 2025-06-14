<template>
  <div class="task-assignment">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>任务下发</span>
          <el-button type="primary" @click="handleAssignTasks" :disabled="selectedTasks.length === 0 || selectedUsers.length === 0">
            <el-icon><Plus /></el-icon>
            分配任务
          </el-button>
        </div>
      </template>

      <div class="assignment-layout">
        <!-- 左侧：任务下发列表 -->
        <div class="left-panel">
          <el-card shadow="never">
            <template #header>
              <span>🔖 任务下发列表</span>
            </template>
            
            <div class="task-list">
              <el-table 
                :data="availableTasks" 
                v-loading="loading"
                @selection-change="handleTaskSelection"
                height="400"
              >
                <el-table-column type="selection" width="55" />
                <el-table-column prop="id" label="任务ID" width="80" />
                <el-table-column prop="name" label="任务名称" min-width="150" show-overflow-tooltip />
                <el-table-column prop="type" label="任务类型" width="120" />
                <el-table-column prop="phase" label="阶段任务" width="100" />
              </el-table>
            </div>
          </el-card>

          <!-- 任务详情 -->
          <el-card shadow="never" style="margin-top: 20px;">
            <template #header>
              <span>📋 任务详情</span>
            </template>
            
            <div class="task-detail">
              <div v-if="selectedTaskDetail" class="detail-content">
                <el-descriptions :column="1" border>
                  <el-descriptions-item label="任务名称">{{ selectedTaskDetail.name }}</el-descriptions-item>
                  <el-descriptions-item label="任务类型">{{ selectedTaskDetail.type }}</el-descriptions-item>
                  <el-descriptions-item label="任务阶段">{{ selectedTaskDetail.phase }}</el-descriptions-item>
                  <el-descriptions-item label="任务描述">{{ selectedTaskDetail.description }}</el-descriptions-item>
                </el-descriptions>
              </div>
              <div v-else class="placeholder">
                请选择任务详情......
              </div>
            </div>
          </el-card>
        </div>

        <!-- 右侧：选择执行人 -->
        <div class="right-panel">
          <el-card shadow="never">
            <template #header>
              <span>👥 选择执行人</span>
            </template>

            <div class="user-selection">
              <div class="selected-users">
                <div class="section-header">
                  <el-icon><Check /></el-icon>
                  <span>已选执行人 ({{ selectedUsers.length }}/20 项)</span>
                </div>
                <div class="user-list selected">
                  <div 
                    v-for="user in selectedUsers" 
                    :key="user.username"
                    class="user-item selected"
                    @click="removeUser(user)"
                  >
                    <el-checkbox :model-value="true" />
                    <span>{{ user.username }}</span>
                  </div>
                  <div v-if="selectedUsers.length === 0" class="empty-state">
                    已分配执行人 (0 项)
                  </div>
                </div>
              </div>

              <div class="transfer-buttons">
                <el-button 
                  type="primary" 
                  circle 
                  size="small"
                  :disabled="checkedAvailableUsers.length === 0"
                  @click="addSelectedUsers"
                >
                  <el-icon><ArrowRight /></el-icon>
                </el-button>
                <el-button 
                  circle 
                  size="small"
                  :disabled="checkedSelectedUsers.length === 0"
                  @click="removeSelectedUsers"
                >
                  <el-icon><ArrowLeft /></el-icon>
                </el-button>
              </div>

              <div class="available-users">
                <div class="section-header">
                  <span>选择执行人 ({{ availableUsers.length }}/20 项)</span>
                </div>
                <div class="user-list available">
                  <div 
                    v-for="user in availableUsers" 
                    :key="user.username"
                    class="user-item"
                    @click="toggleUser(user, 'available')"
                  >
                    <el-checkbox :model-value="checkedAvailableUsers.includes(user.username)" />
                    <span>{{ user.username }}</span>
                  </div>
                  <div 
                    v-for="i in Math.max(0, 10 - availableUsers.length)" 
                    :key="`placeholder-${i}`"
                    class="user-item placeholder"
                  >
                    <span>选择{{ i + availableUsers.length + 1 }}</span>
                  </div>
                </div>
              </div>
            </div>

            <div class="assignment-controls">
              <el-button 
                type="primary" 
                style="width: 100%;"
                :disabled="selectedTasks.length === 0 || selectedUsers.length === 0"
                @click="handleAssignTasks"
              >
                分配任务
              </el-button>
            </div>
          </el-card>
        </div>
      </div>
    </el-card>

    <!-- 已分配任务列表 -->
    <el-card style="margin-top: 20px;">
      <template #header>
        <div class="card-header">
          <span>任务下发</span>
        </div>
      </template>

      <!-- 搜索栏 -->
      <div class="search-bar">
        <el-form :model="searchForm" inline>
          <el-form-item label="任务名称">
            <el-input 
              v-model="searchForm.taskName" 
              placeholder="请输入任务名称"
              clearable
            />
          </el-form-item>
          <el-form-item label="执行人">
            <el-input 
              v-model="searchForm.username" 
              placeholder="请输入执行人"
              clearable
            />
          </el-form-item>
          <el-form-item label="状态">
            <el-select v-model="searchForm.status" placeholder="选择状态" clearable>
              <el-option label="进行中" value="进行中" />
              <el-option label="已完成" value="已完成" />
              <el-option label="已暂停" value="已暂停" />
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

      <!-- 任务分配表格 -->
      <el-table :data="assignments" v-loading="assignmentLoading" style="width: 100%">
        <el-table-column prop="id" label="分配ID" width="80" />
        <el-table-column prop="task_name" label="任务名称" min-width="150" />
        <el-table-column prop="task_type" label="任务类型" width="120" />
        <el-table-column prop="username" label="执行人" width="100" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)">
              {{ scope.row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="progress" label="进度" width="120">
          <template #default="scope">
            <el-progress 
              :percentage="scope.row.progress" 
              :status="scope.row.progress === 100 ? 'success' : ''"
              style="width: 80px;"
            />
          </template>
        </el-table-column>
        <el-table-column prop="performance_score" label="绩效评分" width="100">
          <template #default="scope">
            <el-rate 
              v-model="scope.row.performance_score" 
              :max="5" 
              disabled 
              show-score
              text-color="#ff9900"
            />
          </template>
        </el-table-column>
        <el-table-column prop="assigned_at" label="分配时间" width="150" />
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="scope">
            <el-button size="small" @click="handleEdit(scope.row)">
              编辑
            </el-button>
            <el-button size="small" type="warning" @click="handleReassign(scope.row)">
              重新分配
            </el-button>
            <el-button 
              size="small" 
              type="danger" 
              @click="handleRevoke(scope.row)"
            >
              撤销
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

    <!-- 编辑分配对话框 -->
    <el-dialog
      v-model="editDialogVisible"
      title="编辑任务分配"
      width="600px"
    >
      <el-form
        ref="editFormRef"
        :model="editForm"
        :rules="editRules"
        label-width="100px"
      >
        <el-form-item label="任务名称">
          <el-input v-model="editForm.task_name" disabled />
        </el-form-item>
        <el-form-item label="执行人">
          <el-input v-model="editForm.username" disabled />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="editForm.status" placeholder="选择状态">
            <el-option label="进行中" value="进行中" />
            <el-option label="已完成" value="已完成" />
            <el-option label="已暂停" value="已暂停" />
          </el-select>
        </el-form-item>
        <el-form-item label="进度" prop="progress">
          <el-slider 
            v-model="editForm.progress" 
            :min="0" 
            :max="100" 
            show-input
          />
        </el-form-item>
        <el-form-item label="绩效评分" prop="performance_score">
          <el-rate 
            v-model="editForm.performance_score" 
            :max="5" 
            show-score
            text-color="#ff9900"
          />
        </el-form-item>
        <el-form-item label="备注说明" prop="comments">
          <el-input 
            v-model="editForm.comments" 
            type="textarea"
            :rows="3"
            placeholder="请输入备注说明" 
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="editDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleEditSubmit">
            确定保存
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed, watch } from 'vue'
import { ElMessage, ElMessageBox, type FormInstance } from 'element-plus'
import { Plus, Search, Check, ArrowRight, ArrowLeft } from '@element-plus/icons-vue'
import { getTasks, getTaskAssignments, createTaskAssignment, updateTaskAssignment } from '@/api/task'

interface Task {
  id: number
  name: string
  type: string
  phase: string
  description: string
  status: string
}

interface User {
  id: number
  username: string
  role: string
  type: string
}

interface TaskAssignment {
  id: number
  task_id: number
  task_name: string
  task_type: string
  username: string
  status: string
  progress: number
  performance_score: number
  comments: string
  assigned_at: string
  last_update: string
}

const loading = ref(false)
const assignmentLoading = ref(false)
const editDialogVisible = ref(false)
const editFormRef = ref<FormInstance>()

// 搜索表单
const searchForm = reactive({
  taskName: '',
  username: '',
  status: ''
})

// 编辑表单
const editForm = reactive({
  id: 0,
  task_name: '',
  username: '',
  status: '',
  progress: 0,
  performance_score: 0,
  comments: ''
})

// 分页
const pagination = reactive({
  currentPage: 1,
  pageSize: 10,
  total: 0
})

// 数据
const availableTasks = ref<Task[]>([])
const availableUsers = ref<User[]>([])
const assignments = ref<TaskAssignment[]>([])
const selectedTasks = ref<Task[]>([])
const selectedUsers = ref<User[]>([])
const checkedAvailableUsers = ref<string[]>([])
const checkedSelectedUsers = ref<string[]>([])

// 计算属性
const selectedTaskDetail = computed(() => {
  return selectedTasks.value.length === 1 ? selectedTasks.value[0] : null
})

// 表单验证规则
const editRules = {
  status: [
    { required: true, message: '请选择状态', trigger: 'change' }
  ],
  progress: [
    { required: true, message: '请设置进度', trigger: 'blur' },
    { type: 'number', min: 0, max: 100, message: '进度范围为0-100', trigger: 'blur' }
  ],
  performance_score: [
    { required: true, message: '请设置绩效评分', trigger: 'change' },
    { type: 'number', min: 0, max: 5, message: '绩效评分范围为0-5', trigger: 'change' }
  ]
}

// 方法
const getStatusType = (status: string) => {
  switch (status) {
    case '已完成':
      return 'success'
    case '进行中':
      return 'warning'
    case '已暂停':
      return 'danger'
    default:
      return ''
  }
}

const loadAvailableTasks = async () => {
  loading.value = true
  try {
    const response = await getTasks()
    availableTasks.value = response.data?.filter(task => task.status !== '已完成') || []
  } catch (error) {
    ElMessage.error('加载可用任务失败')
    console.error('加载任务失败:', error)
  } finally {
    loading.value = false
  }
}

const loadAvailableUsers = async () => {
  try {
    // TODO: 调用获取用户列表的API
    // const response = await getUsers()
    // availableUsers.value = response.data || []
    
    // 模拟数据
    availableUsers.value = [
      { id: 1, username: 'user1', role: '网络工程师', type: '操作员' },
      { id: 2, username: 'user2', role: '系统架构师', type: '操作员' },
      { id: 3, username: 'user3', role: '系统规划与管理师', type: '操作员' },
      { id: 4, username: 'user4', role: '运维工程师', type: '操作员' },
      { id: 5, username: 'user5', role: '测试工程师', type: '操作员' },
      { id: 6, username: 'user6', role: '开发工程师', type: '操作员' },
      { id: 7, username: 'user7', role: '产品经理', type: '操作员' },
      { id: 8, username: 'user8', role: '项目经理', type: '操作员' },
    ]
  } catch (error) {
    ElMessage.error('加载可用用户失败')
    console.error('加载用户失败:', error)
  }
}

const loadAssignments = async () => {
  assignmentLoading.value = true
  try {
    const response = await getTaskAssignments({
      skip: (pagination.currentPage - 1) * pagination.pageSize,
      limit: pagination.pageSize,
      status: searchForm.status || undefined
    })
    
    assignments.value = response.data || []
    pagination.total = response.data?.length || 0
  } catch (error) {
    ElMessage.error('加载任务分配列表失败')
    console.error('加载任务分配失败:', error)
  } finally {
    assignmentLoading.value = false
  }
}

const handleTaskSelection = (selection: Task[]) => {
  selectedTasks.value = selection
}

const toggleUser = (user: User, type: 'available' | 'selected') => {
  if (type === 'available') {
    const index = checkedAvailableUsers.value.indexOf(user.username)
    if (index > -1) {
      checkedAvailableUsers.value.splice(index, 1)
    } else {
      checkedAvailableUsers.value.push(user.username)
    }
  } else {
    const index = checkedSelectedUsers.value.indexOf(user.username)
    if (index > -1) {
      checkedSelectedUsers.value.splice(index, 1)
    } else {
      checkedSelectedUsers.value.push(user.username)
    }
  }
}

const addSelectedUsers = () => {
  checkedAvailableUsers.value.forEach(username => {
    const user = availableUsers.value.find(u => u.username === username)
    if (user && !selectedUsers.value.find(u => u.username === username)) {
      selectedUsers.value.push(user)
    }
  })
  checkedAvailableUsers.value = []
}

const removeSelectedUsers = () => {
  checkedSelectedUsers.value.forEach(username => {
    const index = selectedUsers.value.findIndex(u => u.username === username)
    if (index > -1) {
      selectedUsers.value.splice(index, 1)
    }
  })
  checkedSelectedUsers.value = []
}

const removeUser = (user: User) => {
  const index = selectedUsers.value.findIndex(u => u.username === user.username)
  if (index > -1) {
    selectedUsers.value.splice(index, 1)
  }
}

const handleAssignTasks = async () => {
  if (selectedTasks.value.length === 0) {
    ElMessage.warning('请选择要分配的任务')
    return
  }
  
  if (selectedUsers.value.length === 0) {
    ElMessage.warning('请选择执行人')
    return
  }

  try {
    await ElMessageBox.confirm(
      `确定要将 ${selectedTasks.value.length} 个任务分配给 ${selectedUsers.value.length} 个执行人吗？`,
      '确认分配',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )

    // 创建任务分配
    for (const task of selectedTasks.value) {
      for (const user of selectedUsers.value) {
        await createTaskAssignment({
          task_id: task.id,
          username: user.username,
          status: '进行中',
          progress: 0,
          performance_score: 0,
          comments: ''
        })
      }
    }

    ElMessage.success('任务分配成功')
    selectedTasks.value = []
    selectedUsers.value = []
    checkedAvailableUsers.value = []
    checkedSelectedUsers.value = []
    loadAssignments()
    loadAvailableTasks()
  } catch (error: any) {
    if (error?.message !== 'cancel') {
      ElMessage.error('任务分配失败')
      console.error('分配任务失败:', error)
    }
  }
}

const handleEdit = (row: TaskAssignment) => {
  editDialogVisible.value = true
  Object.assign(editForm, row)
}

const handleReassign = async (row: TaskAssignment) => {
  try {
    await ElMessageBox.confirm(
      `确定要重新分配任务 "${row.task_name}" 吗？`,
      '确认重新分配',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    
    // TODO: 实现重新分配逻辑
    ElMessage.success('重新分配成功')
    loadAssignments()
  } catch (error: any) {
    if (error?.message !== 'cancel') {
      ElMessage.error('重新分配失败')
    }
  }
}

const handleRevoke = async (row: TaskAssignment) => {
  try {
    await ElMessageBox.confirm(
      `确定要撤销任务 "${row.task_name}" 的分配吗？`,
      '确认撤销',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    
    // TODO: 调用撤销分配的API
    ElMessage.success('撤销分配成功')
    loadAssignments()
  } catch (error: any) {
    if (error?.message !== 'cancel') {
      ElMessage.error('撤销分配失败')
    }
  }
}

const handleEditSubmit = async () => {
  if (!editFormRef.value) return
  
  try {
    await editFormRef.value.validate()
    
    await updateTaskAssignment(editForm.id, {
      status: editForm.status,
      progress: editForm.progress,
      performance_score: editForm.performance_score,
      comments: editForm.comments
    })
    
    ElMessage.success('更新成功')
    editDialogVisible.value = false
    loadAssignments()
  } catch (error: any) {
    ElMessage.error('更新失败')
    console.error('更新任务分配失败:', error)
  }
}

const handleSearch = () => {
  pagination.currentPage = 1
  loadAssignments()
}

const handleReset = () => {
  searchForm.taskName = ''
  searchForm.username = ''
  searchForm.status = ''
  pagination.currentPage = 1
  loadAssignments()
}

const handleSizeChange = (val: number) => {
  pagination.pageSize = val
  pagination.currentPage = 1
  loadAssignments()
}

const handleCurrentChange = (val: number) => {
  pagination.currentPage = val
  loadAssignments()
}

onMounted(() => {
  loadAvailableTasks()
  loadAvailableUsers()
  loadAssignments()
})
</script>

<style scoped lang="scss">
.task-assignment {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .assignment-layout {
    display: flex;
    gap: 20px;
    margin-top: 20px;

    .left-panel {
      flex: 1;

      .task-list {
        margin-top: 16px;
      }

      .task-detail {
        .detail-content {
          .el-descriptions {
            margin-top: 16px;
          }
        }

        .placeholder {
          text-align: center;
          color: #999;
          padding: 40px 0;
          background: #f9f9f9;
          border-radius: 4px;
        }
      }
    }

    .right-panel {
      width: 400px;

      .user-selection {
        .section-header {
          display: flex;
          align-items: center;
          gap: 8px;
          margin-bottom: 12px;
          font-weight: 500;
          color: #333;
        }

        .user-list {
          border: 1px solid #dcdfe6;
          border-radius: 4px;
          height: 200px;
          overflow-y: auto;
          background: #fff;

          .user-item {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 8px 12px;
            cursor: pointer;
            border-bottom: 1px solid #f0f0f0;

            &:hover {
              background: #f5f7fa;
            }

            &.selected {
              background: #e6f7ff;
              border-color: #91d5ff;
            }

            &.placeholder {
              color: #ccc;
              cursor: default;

              &:hover {
                background: transparent;
              }
            }

            &:last-child {
              border-bottom: none;
            }
          }

          &.selected {
            background: #f0f9ff;
          }

          .empty-state {
            text-align: center;
            color: #999;
            padding: 60px 20px;
          }
        }

        .transfer-buttons {
          display: flex;
          flex-direction: column;
          justify-content: center;
          align-items: center;
          gap: 8px;
          margin: 20px 0;
        }

        .selected-users,
        .available-users {
          margin-bottom: 20px;
        }
      }

      .assignment-controls {
        margin-top: 20px;
      }
    }
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