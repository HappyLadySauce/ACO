<template>
  <div class="device-management">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>设备管理</span>
          <el-button type="primary" @click="handleAdd">
            <el-icon><Plus /></el-icon>
            新增设备
          </el-button>
        </div>
      </template>

      <!-- 搜索栏 -->
      <div class="search-bar">
        <el-form :model="searchForm" inline>
          <el-form-item label="设备名称">
            <el-input 
              v-model="searchForm.name" 
              placeholder="请输入设备名称"
              clearable
            />
          </el-form-item>
          <el-form-item label="状态">
            <el-select v-model="searchForm.status" placeholder="选择状态" clearable>
              <el-option label="在线" value="online" />
              <el-option label="离线" value="offline" />
              <el-option label="维护中" value="maintenance" />
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

      <!-- 设备表格 -->
      <el-table :data="devices" v-loading="loading" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="设备名称" />
        <el-table-column prop="type" label="设备类型" />
        <el-table-column prop="status" label="状态">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)">
              <el-icon style="margin-right: 4px;">
                <component :is="getStatusIcon(scope.row.status)" />
              </el-icon>
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="location" label="位置" />
        <el-table-column prop="last_active" label="最后活跃时间" />
        <el-table-column label="操作" width="250">
          <template #default="scope">
            <el-button 
              size="small" 
              :type="scope.row.status === 'online' ? 'warning' : 'success'"
              @click="handleToggleStatus(scope.row)"
            >
              {{ scope.row.status === 'online' ? '停用' : '启用' }}
            </el-button>
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

    <!-- 设备编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑设备' : '新增设备'"
      width="600px"
    >
      <el-form
        ref="formRef"
        :model="deviceForm"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="设备名称" prop="name">
          <el-input v-model="deviceForm.name" placeholder="请输入设备名称" />
        </el-form-item>
        <el-form-item label="设备类型" prop="type">
          <el-select v-model="deviceForm.type" placeholder="选择设备类型">
            <el-option label="服务器" value="server" />
            <el-option label="工作站" value="workstation" />
            <el-option label="路由器" value="router" />
            <el-option label="交换机" value="switch" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="deviceForm.status" placeholder="选择状态">
            <el-option label="在线" value="online" />
            <el-option label="离线" value="offline" />
            <el-option label="维护中" value="maintenance" />
          </el-select>
        </el-form-item>
        <el-form-item label="位置" prop="location">
          <el-input v-model="deviceForm.location" placeholder="请输入设备位置" />
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
import { Plus, Search, Connection, Refresh, Warning } from '@element-plus/icons-vue'

interface Device {
  id: number
  name: string
  type: string
  status: string
  location: string
  last_active: string
}

const loading = ref(false)
const dialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref<FormInstance>()

const searchForm = reactive({
  name: '',
  status: ''
})

const deviceForm = reactive({
  id: 0,
  name: '',
  type: '',
  status: 'offline',
  location: ''
})

const pagination = reactive({
  currentPage: 1,
  pageSize: 10,
  total: 0
})

const devices = ref<Device[]>([])

const rules = {
  name: [
    { required: true, message: '请输入设备名称', trigger: 'blur' },
    { min: 2, max: 30, message: '设备名称长度在 2 到 30 个字符', trigger: 'blur' }
  ],
  type: [
    { required: true, message: '请选择设备类型', trigger: 'change' }
  ],
  status: [
    { required: true, message: '请选择状态', trigger: 'change' }
  ],
  location: [
    { required: true, message: '请输入设备位置', trigger: 'blur' }
  ]
}

const getStatusType = (status: string) => {
  switch (status) {
    case 'online':
      return 'success'
    case 'offline':
      return 'danger'
    case 'maintenance':
      return 'warning'
    default:
      return 'info'
  }
}

const getStatusText = (status: string) => {
  switch (status) {
    case 'online':
      return '在线'
    case 'offline':
      return '离线'
    case 'maintenance':
      return '维护中'
    default:
      return status
  }
}

const getStatusIcon = (status: string) => {
  switch (status) {
    case 'online':
      return Connection
    case 'offline':
      return Refresh
    case 'maintenance':
      return Warning
    default:
      return Connection
  }
}

const loadDevices = async () => {
  loading.value = true
  try {
    // 模拟数据加载
    devices.value = [
      {
        id: 1,
        name: '服务器-01',
        type: 'server',
        status: 'online',
        location: '机房A-01',
        last_active: '2024-01-15 12:30'
      },
      {
        id: 2,
        name: '服务器-02',
        type: 'server',
        status: 'offline',
        location: '机房A-02',
        last_active: '2024-01-14 18:45'
      },
      {
        id: 3,
        name: '工作站-01',
        type: 'workstation',
        status: 'online',
        location: '办公室-203',
        last_active: '2024-01-15 11:20'
      },
      {
        id: 4,
        name: '路由器-01',
        type: 'router',
        status: 'maintenance',
        location: '网络中心',
        last_active: '2024-01-13 09:15'
      }
    ]
    pagination.total = devices.value.length
  } catch (error) {
    ElMessage.error('加载设备列表失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  loadDevices()
}

const handleReset = () => {
  searchForm.name = ''
  searchForm.status = ''
  loadDevices()
}

const handleAdd = () => {
  isEdit.value = false
  dialogVisible.value = true
  resetForm()
}

const handleEdit = (row: Device) => {
  isEdit.value = true
  dialogVisible.value = true
  Object.assign(deviceForm, row)
}

const handleToggleStatus = async (row: Device) => {
  const newStatus = row.status === 'online' ? 'offline' : 'online'
  const action = newStatus === 'online' ? '启用' : '停用'
  
  try {
    await ElMessageBox.confirm(
      `确定要${action}设备 "${row.name}" 吗？`,
      `确认${action}`,
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    
    ElMessage.success(`设备${action}成功`)
    loadDevices()
  } catch (error) {
    // 用户取消了操作
  }
}

const handleDelete = async (row: Device) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除设备 "${row.name}" 吗？`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    
    ElMessage.success('删除成功')
    loadDevices()
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
    loadDevices()
  } catch (error) {
    console.error('表单验证失败:', error)
  }
}

const resetForm = () => {
  deviceForm.id = 0
  deviceForm.name = ''
  deviceForm.type = ''
  deviceForm.status = 'offline'
  deviceForm.location = ''
}

const handleSizeChange = (val: number) => {
  pagination.pageSize = val
  loadDevices()
}

const handleCurrentChange = (val: number) => {
  pagination.currentPage = val
  loadDevices()
}

onMounted(() => {
  loadDevices()
})
</script>

<style scoped lang="scss">
.device-management {
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