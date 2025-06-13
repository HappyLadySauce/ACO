<template>
  <div class="desktop-management">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>桌面管理</span>
          <el-button type="primary" @click="handleAdd">
            <el-icon><Plus /></el-icon>
            新增桌面项目
          </el-button>
        </div>
      </template>

      <!-- 工具栏 -->
      <div class="toolbar">
        <el-row :gutter="20">
          <el-col :span="8">
            <el-card class="tool-card">
              <h3>快捷工具</h3>
              <div class="tool-grid">
                <div class="tool-item" @click="openCalculator">
                  <el-icon><Calculator /></el-icon>
                  <span>计算器</span>
                </div>
                <div class="tool-item" @click="openNotepad">
                  <el-icon><Edit /></el-icon>
                  <span>记事本</span>
                </div>
                <div class="tool-item" @click="openTerminal">
                  <el-icon><Monitor /></el-icon>
                  <span>终端</span>
                </div>
                <div class="tool-item" @click="openFileManager">
                  <el-icon><Folder /></el-icon>
                  <span>文件管理</span>
                </div>
              </div>
            </el-card>
          </el-col>
          
          <el-col :span="8">
            <el-card class="tool-card">
              <h3>系统信息</h3>
              <div class="system-info">
                <div class="info-item">
                  <span class="label">CPU使用率:</span>
                  <el-progress :percentage="systemInfo.cpuUsage" />
                </div>
                <div class="info-item">
                  <span class="label">内存使用率:</span>
                  <el-progress :percentage="systemInfo.memoryUsage" />
                </div>
                <div class="info-item">
                  <span class="label">磁盘使用率:</span>
                  <el-progress :percentage="systemInfo.diskUsage" />
                </div>
              </div>
            </el-card>
          </el-col>
          
          <el-col :span="8">
            <el-card class="tool-card">
              <h3>最近访问</h3>
              <div class="recent-list">
                <div 
                  v-for="item in recentItems" 
                  :key="item.id"
                  class="recent-item"
                  @click="openRecentItem(item)"
                >
                  <el-icon><Document /></el-icon>
                  <span>{{ item.name }}</span>
                  <small>{{ item.time }}</small>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <!-- 桌面项目列表 -->
      <div class="desktop-items">
        <h3>桌面项目管理</h3>
        <el-table :data="desktopItems" v-loading="loading" style="width: 100%">
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="name" label="项目名称" />
          <el-table-column prop="type" label="类型">
            <template #default="scope">
              <el-tag>{{ scope.row.type }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="path" label="路径" show-overflow-tooltip />
          <el-table-column prop="status" label="状态">
            <template #default="scope">
              <el-tag :type="scope.row.status === 'active' ? 'success' : 'info'">
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
      </div>
    </el-card>

    <!-- 桌面项目编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑桌面项目' : '新增桌面项目'"
      width="600px"
    >
      <el-form
        ref="formRef"
        :model="itemForm"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="项目名称" prop="name">
          <el-input v-model="itemForm.name" placeholder="请输入项目名称" />
        </el-form-item>
        <el-form-item label="类型" prop="type">
          <el-select v-model="itemForm.type" placeholder="选择类型">
            <el-option label="应用程序" value="application" />
            <el-option label="文件夹" value="folder" />
            <el-option label="文件" value="file" />
            <el-option label="链接" value="link" />
          </el-select>
        </el-form-item>
        <el-form-item label="路径" prop="path">
          <el-input v-model="itemForm.path" placeholder="请输入文件路径" />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="itemForm.status" placeholder="选择状态">
            <el-option label="激活" value="active" />
            <el-option label="未激活" value="inactive" />
          </el-select>
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input 
            v-model="itemForm.description" 
            type="textarea"
            :rows="3"
            placeholder="请输入描述" 
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
import { 
  Plus, 
  Calculator, 
  Edit, 
  Monitor, 
  Folder, 
  Document 
} from '@element-plus/icons-vue'

interface DesktopItem {
  id: number
  name: string
  type: string
  path: string
  status: string
  description: string
  created_at: string
}

interface RecentItem {
  id: number
  name: string
  time: string
}

interface SystemInfo {
  cpuUsage: number
  memoryUsage: number
  diskUsage: number
}

const loading = ref(false)
const dialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref<FormInstance>()

const itemForm = reactive({
  id: 0,
  name: '',
  type: '',
  path: '',
  status: 'active',
  description: ''
})

const desktopItems = ref<DesktopItem[]>([])
const recentItems = ref<RecentItem[]>([])
const systemInfo = ref<SystemInfo>({
  cpuUsage: 0,
  memoryUsage: 0,
  diskUsage: 0
})

const rules = {
  name: [
    { required: true, message: '请输入项目名称', trigger: 'blur' },
    { min: 2, max: 30, message: '项目名称长度在 2 到 30 个字符', trigger: 'blur' }
  ],
  type: [
    { required: true, message: '请选择类型', trigger: 'change' }
  ],
  path: [
    { required: true, message: '请输入文件路径', trigger: 'blur' }
  ],
  status: [
    { required: true, message: '请选择状态', trigger: 'change' }
  ]
}

const loadDesktopItems = async () => {
  loading.value = true
  try {
    // 模拟数据加载
    desktopItems.value = [
      {
        id: 1,
        name: '系统监控工具',
        type: 'application',
        path: '/usr/bin/monitor',
        status: 'active',
        description: '系统资源监控应用',
        created_at: '2024-01-15 10:30'
      },
      {
        id: 2,
        name: '文档管理器',
        type: 'folder',
        path: '/home/documents',
        status: 'active',
        description: '文档存储目录',
        created_at: '2024-01-14 14:20'
      }
    ]
  } catch (error) {
    ElMessage.error('加载桌面项目失败')
  } finally {
    loading.value = false
  }
}

const loadRecentItems = () => {
  recentItems.value = [
    { id: 1, name: '工作报告.docx', time: '2小时前' },
    { id: 2, name: '系统配置.txt', time: '4小时前' },
    { id: 3, name: '数据分析.xlsx', time: '昨天' }
  ]
}

const loadSystemInfo = () => {
  // 模拟系统信息更新
  systemInfo.value = {
    cpuUsage: Math.floor(Math.random() * 100),
    memoryUsage: Math.floor(Math.random() * 100),
    diskUsage: Math.floor(Math.random() * 100)
  }
}

const openCalculator = () => {
  ElMessage.info('正在打开计算器...')
}

const openNotepad = () => {
  ElMessage.info('正在打开记事本...')
}

const openTerminal = () => {
  ElMessage.info('正在打开终端...')
}

const openFileManager = () => {
  ElMessage.info('正在打开文件管理器...')
}

const openRecentItem = (item: RecentItem) => {
  ElMessage.info(`正在打开: ${item.name}`)
}

const handleAdd = () => {
  isEdit.value = false
  dialogVisible.value = true
  resetForm()
}

const handleEdit = (row: DesktopItem) => {
  isEdit.value = true
  dialogVisible.value = true
  Object.assign(itemForm, row)
}

const handleDelete = async (row: DesktopItem) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除桌面项目 "${row.name}" 吗？`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    
    ElMessage.success('删除成功')
    loadDesktopItems()
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
    loadDesktopItems()
  } catch (error) {
    console.error('表单验证失败:', error)
  }
}

const resetForm = () => {
  itemForm.id = 0
  itemForm.name = ''
  itemForm.type = ''
  itemForm.path = ''
  itemForm.status = 'active'
  itemForm.description = ''
}

onMounted(() => {
  loadDesktopItems()
  loadRecentItems()
  loadSystemInfo()
  
  // 定时更新系统信息
  setInterval(loadSystemInfo, 5000)
})
</script>

<style scoped lang="scss">
.desktop-management {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .toolbar {
    margin-bottom: 30px;
  }

  .tool-card {
    height: 280px;

    h3 {
      margin: 0 0 20px 0;
      color: #333;
      font-size: 16px;
      font-weight: 600;
    }
  }

  .tool-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 15px;

    .tool-item {
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 20px 10px;
      border: 1px solid #e4e7ed;
      border-radius: 8px;
      cursor: pointer;
      transition: all 0.3s;

      &:hover {
        background: #f5f7fa;
        border-color: #1890ff;
        transform: translateY(-2px);
      }

      .el-icon {
        font-size: 28px;
        color: #1890ff;
        margin-bottom: 8px;
      }

      span {
        font-size: 14px;
        color: #333;
      }
    }
  }

  .system-info {
    .info-item {
      margin-bottom: 20px;
      
      .label {
        display: block;
        margin-bottom: 8px;
        font-size: 14px;
        color: #666;
      }
    }
  }

  .recent-list {
    .recent-item {
      display: flex;
      align-items: center;
      padding: 10px 0;
      border-bottom: 1px solid #f0f0f0;
      cursor: pointer;
      transition: background 0.3s;

      &:hover {
        background: #f5f7fa;
      }

      &:last-child {
        border-bottom: none;
      }

      .el-icon {
        margin-right: 10px;
        color: #1890ff;
      }

      span {
        flex: 1;
        font-size: 14px;
        color: #333;
      }

      small {
        color: #999;
        font-size: 12px;
      }
    }
  }

  .desktop-items {
    h3 {
      margin-bottom: 20px;
      color: #333;
      font-size: 18px;
      font-weight: 600;
    }
  }
}
</style> 