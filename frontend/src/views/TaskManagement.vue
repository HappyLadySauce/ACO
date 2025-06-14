<template>
  <div class="task-management">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>任务管理</span>
          <el-button type="primary" @click="handleAdd">
            <el-icon><Plus /></el-icon>
            新增任务
          </el-button>
        </div>
      </template>

      <!-- 搜索栏 -->
      <div class="search-bar">
        <el-form :model="searchForm" inline>
          <el-form-item label="任务名称">
            <el-input 
              v-model="searchForm.name" 
              placeholder="请输入任务名称"
              clearable
            />
          </el-form-item>
          <el-form-item label="任务类型">
            <el-select v-model="searchForm.type" placeholder="选择任务类型" clearable>
              <el-option label="运维监控任务" value="运维监控任务" />
              <el-option label="运维管理任务" value="运维管理任务" />
              <el-option label="开发测试任务" value="开发测试任务" />
            </el-select>
          </el-form-item>
          <el-form-item label="阶段">
            <el-select v-model="searchForm.phase" placeholder="选择任务阶段" clearable>
              <el-option label="计划阶段" value="计划阶段" />
              <el-option label="执行阶段" value="执行阶段" />
              <el-option label="验收阶段" value="验收阶段" />
              <el-option label="完成阶段" value="完成阶段" />
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

      <!-- 任务表格 -->
      <el-table :data="tasks" v-loading="loading" style="width: 100%">
        <el-table-column prop="id" label="任务ID" width="80" />
        <el-table-column prop="name" label="任务名称" min-width="120" />
        <el-table-column prop="type" label="任务类型" width="120" />
        <el-table-column prop="phase" label="阶段" width="100" />
        <el-table-column prop="description" label="任务描述" show-overflow-tooltip min-width="150" />
        <el-table-column label="执行人" width="120">
          <template #default="scope">
            <span v-if="scope.row.assignments && scope.row.assignments.length > 0">
              {{ scope.row.assignments.map((a: any) => a.username).join(', ') }}
            </span>
            <el-tag v-else type="info" size="small">未分配</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="create_time" label="创建时间" width="150" />
        <el-table-column prop="update_time" label="更新时间" width="150" />
        <el-table-column label="操作" width="160" fixed="right">
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

    <!-- 任务编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑任务' : '新增任务'"
      width="700px"
    >
      <el-form
        ref="formRef"
        :model="taskForm"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="任务名称" prop="name">
          <el-input v-model="taskForm.name" placeholder="请输入任务名称" />
        </el-form-item>
        <el-form-item label="任务类型" prop="type">
          <el-select v-model="taskForm.type" placeholder="选择任务类型">
            <el-option label="运维监控任务" value="运维监控任务" />
            <el-option label="运维管理任务" value="运维管理任务" />
            <el-option label="开发测试任务" value="开发测试任务" />
          </el-select>
        </el-form-item>
        <el-form-item label="阶段" prop="phase">
          <el-select v-model="taskForm.phase" placeholder="选择任务阶段">
            <el-option label="计划阶段" value="计划阶段" />
            <el-option label="执行阶段" value="执行阶段" />
            <el-option label="验收阶段" value="验收阶段" />
            <el-option label="完成阶段" value="完成阶段" />
          </el-select>
        </el-form-item>
        <el-form-item label="任务描述" prop="description">
          <el-input 
            v-model="taskForm.description" 
            type="textarea"
            :rows="4"
            placeholder="请输入任务描述" 
          />
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
import { getTasks, getTasksCount, createTask, updateTask, deleteTask, getTask } from '@/api/task'

interface Task {
  id: number
  name: string
  type: string
  phase: string
  description: string
  create_time: string
  update_time: string
  assignments?: any[]
}

const loading = ref(false)
const dialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref<FormInstance>()

const searchForm = reactive({
  name: '',
  type: '',
  phase: ''
})

const taskForm = reactive({
  id: 0,
  name: '',
  type: '',
  phase: '',
  description: ''
})

const pagination = reactive({
  currentPage: 1,
  pageSize: 10,
  total: 0
})

const tasks = ref<Task[]>([])

const rules = {
  name: [
    { required: true, message: '请输入任务名称', trigger: 'blur' },
    { min: 2, max: 50, message: '任务名称长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  type: [
    { required: true, message: '请选择任务类型', trigger: 'change' }
  ],
  phase: [
    { required: true, message: '请选择任务阶段', trigger: 'change' }
  ],
  description: [
    { required: true, message: '请输入任务描述', trigger: 'blur' },
    { min: 5, max: 500, message: '任务描述长度在 5 到 500 个字符', trigger: 'blur' }
  ]
}

const loadTasks = async () => {
  loading.value = true
  try {
    const response = await getTasks({
      skip: (pagination.currentPage - 1) * pagination.pageSize,
      limit: pagination.pageSize,
      task_type: searchForm.type || undefined
    })
    
    // 为每个任务获取分配信息
    const tasksWithAssignments = await Promise.all(
      (response.data || []).map(async (task) => {
        try {
          const taskDetail = await getTask(task.id)
          return {
            ...task,
            assignments: taskDetail.data?.assignments || []
          }
        } catch (error) {
          console.warn(`获取任务 ${task.id} 分配信息失败:`, error)
          return {
            ...task,
            assignments: []
          }
        }
      })
    )
    
    tasks.value = tasksWithAssignments
    
    // 获取总数
    const countResponse = await getTasksCount({
      task_type: searchForm.type || undefined
    })
    pagination.total = countResponse.data?.count || 0
  } catch (error) {
    ElMessage.error('加载任务列表失败')
    console.error('加载任务失败:', error)
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  pagination.currentPage = 1
  loadTasks()
}

const handleReset = () => {
  searchForm.name = ''
  searchForm.type = ''
  searchForm.phase = ''
  pagination.currentPage = 1
  loadTasks()
}

const handleAdd = () => {
  isEdit.value = false
  dialogVisible.value = true
  resetForm()
}

const handleEdit = (row: Task) => {
  isEdit.value = true
  dialogVisible.value = true
  Object.assign(taskForm, row)
}

const handleDelete = async (row: Task) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除任务 "${row.name}" 吗？`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    
    await deleteTask(row.id)
    ElMessage.success('删除成功')
    loadTasks()
  } catch (error: any) {
    if (error?.message !== 'cancel') {
      ElMessage.error('删除失败')
      console.error('删除任务失败:', error)
    }
  }
}

const handleSubmit = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    
    if (isEdit.value) {
      await updateTask(taskForm.id, {
        name: taskForm.name,
        type: taskForm.type,
        phase: taskForm.phase,
        description: taskForm.description
      })
    } else {
      await createTask({
        name: taskForm.name,
        type: taskForm.type,
        phase: taskForm.phase,
        description: taskForm.description,
        status: '未分配'
      })
    }
    
    ElMessage.success(isEdit.value ? '更新成功' : '创建成功')
    dialogVisible.value = false
    loadTasks()
  } catch (error: any) {
    ElMessage.error(isEdit.value ? '更新失败' : '创建失败')
    console.error('保存任务失败:', error)
  }
}

const resetForm = () => {
  taskForm.id = 0
  taskForm.name = ''
  taskForm.type = ''
  taskForm.phase = ''
  taskForm.description = ''
}

const handleSizeChange = (val: number) => {
  pagination.pageSize = val
  pagination.currentPage = 1
  loadTasks()
}

const handleCurrentChange = (val: number) => {
  pagination.currentPage = val
  loadTasks()
}

onMounted(() => {
  loadTasks()
})
</script>

<style scoped lang="scss">
.task-management {
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