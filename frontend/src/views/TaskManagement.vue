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
          <el-form-item label="状态">
            <el-select v-model="searchForm.status" placeholder="选择状态" clearable>
              <el-option label="未开始" value="未分配" />
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

      <!-- 任务表格 -->
      <el-table :data="tasks" v-loading="loading" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="任务名称" />
        <el-table-column prop="type" label="任务类型" />
        <el-table-column prop="phase" label="阶段" />
        <el-table-column prop="status" label="状态">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)">
              {{ scope.row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="description" label="描述" show-overflow-tooltip />
        <el-table-column prop="create_time" label="创建时间" />
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
          <el-input v-model="taskForm.type" placeholder="请输入任务类型" />
        </el-form-item>
        <el-form-item label="阶段" prop="phase">
          <el-input v-model="taskForm.phase" placeholder="请输入任务阶段" />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="taskForm.status" placeholder="选择状态">
            <el-option label="未分配" value="未分配" />
            <el-option label="进行中" value="进行中" />
            <el-option label="已完成" value="已完成" />
            <el-option label="已暂停" value="已暂停" />
          </el-select>
        </el-form-item>
        <el-form-item label="描述" prop="description">
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

interface Task {
  id: number
  name: string
  type: string
  phase: string
  description: string
  status: string
  create_time: string
  update_time: string
}

const loading = ref(false)
const dialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref<FormInstance>()

const searchForm = reactive({
  name: '',
  status: ''
})

const taskForm = reactive({
  id: 0,
  name: '',
  type: '',
  phase: '',
  description: '',
  status: '未分配'
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
    { required: true, message: '请输入任务类型', trigger: 'blur' }
  ],
  phase: [
    { required: true, message: '请输入任务阶段', trigger: 'blur' }
  ],
  status: [
    { required: true, message: '请选择状态', trigger: 'change' }
  ]
}

const getStatusType = (status: string) => {
  switch (status) {
    case '已完成':
      return 'success'
    case '进行中':
      return 'warning'
    case '未分配':
      return 'info'
    case '已暂停':
      return 'danger'
    default:
      return ''
  }
}

const loadTasks = async () => {
  loading.value = true
  try {
    // 模拟数据加载
    tasks.value = [
      {
        id: 1,
        name: '系统维护任务',
        type: '维护',
        phase: '执行阶段',
        description: '对系统进行定期维护和检查',
        status: '进行中',
        create_time: '2024-01-15 10:30',
        update_time: '2024-01-15 10:30'
      },
      {
        id: 2,
        name: '数据备份任务',
        type: '备份',
        phase: '准备阶段',
        description: '进行重要数据的备份操作',
        status: '已完成',
        create_time: '2024-01-14 14:20',
        update_time: '2024-01-14 16:30'
      },
      {
        id: 3,
        name: '安全检查任务',
        type: '安全',
        phase: '计划阶段',
        description: '系统安全漏洞检查和修复',
        status: '未分配',
        create_time: '2024-01-13 09:15',
        update_time: '2024-01-13 09:15'
      }
    ]
    pagination.total = tasks.value.length
  } catch (error) {
    ElMessage.error('加载任务列表失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  loadTasks()
}

const handleReset = () => {
  searchForm.name = ''
  searchForm.status = ''
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
    
    ElMessage.success('删除成功')
    loadTasks()
  } catch (error) {
    // 用户取消了删除操作
  }
}

const handleSubmit = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    ElMessage.success(isEdit.value ? '更新成功' : '创建成功')
    dialogVisible.value = false
    loadTasks()
  } catch (error) {
    console.error('表单验证失败:', error)
  }
}

const resetForm = () => {
  taskForm.id = 0
  taskForm.name = ''
  taskForm.type = ''
  taskForm.phase = ''
  taskForm.description = ''
  taskForm.status = '未分配'
}

const handleSizeChange = (val: number) => {
  pagination.pageSize = val
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