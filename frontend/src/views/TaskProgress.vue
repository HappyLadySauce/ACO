<template>
  <div class="task-progress">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>{{ authStore.isAdmin ? '全部任务进度' : '我的任务进度' }}</span>
          <div class="header-actions">
            <el-button @click="refreshData">
              <el-icon><Refresh /></el-icon>
              刷新数据
            </el-button>
          </div>
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
          <el-form-item label="时间范围">
            <el-date-picker
              v-model="searchForm.dateRange"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              format="YYYY-MM-DD"
              value-format="YYYY-MM-DD"
            />
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

      <!-- 统计卡片 -->
      <div class="stats-cards">
        <el-row :gutter="20">
          <el-col :span="6">
            <el-card class="stat-card">
              <div class="stat-content">
                <div class="stat-value">{{ stats.total }}</div>
                <div class="stat-label">总任务数</div>
              </div>
              <el-icon class="stat-icon total"><Document /></el-icon>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card class="stat-card">
              <div class="stat-content">
                <div class="stat-value">{{ stats.inProgress }}</div>
                <div class="stat-label">进行中</div>
              </div>
              <el-icon class="stat-icon progress"><Clock /></el-icon>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card class="stat-card">
              <div class="stat-content">
                <div class="stat-value">{{ stats.completed }}</div>
                <div class="stat-label">已完成</div>
              </div>
              <el-icon class="stat-icon completed"><CircleCheck /></el-icon>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card class="stat-card">
              <div class="stat-content">
                <div class="stat-value">{{ stats.avgProgress }}%</div>
                <div class="stat-label">平均进度</div>
              </div>
              <el-icon class="stat-icon avg"><TrendCharts /></el-icon>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <!-- 图表区域 -->
      <div class="charts-section">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-card>
              <template #header>
                <span>任务状态分布</span>
              </template>
              <div ref="statusChartRef" class="chart-container"></div>
            </el-card>
          </el-col>
          <el-col :span="12">
            <el-card>
              <template #header>
                <span>任务进度趋势</span>
              </template>
              <div ref="progressChartRef" class="chart-container"></div>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <!-- 任务进度表格 -->
      <div class="progress-table">
        <el-table :data="progressList" v-loading="loading" style="width: 100%">
          <el-table-column prop="id" label="ID" width="60" />
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
          <el-table-column prop="progress" label="进度" width="150">
            <template #default="scope">
              <el-progress 
                :percentage="scope.row.progress" 
                :status="scope.row.progress === 100 ? 'success' : (scope.row.status === '已暂停' ? 'exception' : '')"
                :stroke-width="8"
              />
            </template>
          </el-table-column>
          <el-table-column prop="performance_score" label="绩效评分" width="120">
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
          <el-table-column prop="last_update" label="最后更新" width="150" />
          <el-table-column prop="comments" label="备注" min-width="120" show-overflow-tooltip />
          <el-table-column label="操作" width="160" fixed="right">
            <template #default="scope">
              <el-button size="small" @click="handleViewDetail(scope.row)">
                详情
              </el-button>
              <el-button 
                size="small" 
                type="primary" 
                @click="handleUpdateProgress(scope.row)"
              >
                更新进度
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
      </div>
    </el-card>

    <!-- 任务详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      title="任务详情"
      width="800px"
    >
      <div v-if="currentTask" class="task-detail">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="任务ID">{{ currentTask.id }}</el-descriptions-item>
          <el-descriptions-item label="任务名称">{{ currentTask.task_name }}</el-descriptions-item>
          <el-descriptions-item label="任务类型">{{ currentTask.task_type }}</el-descriptions-item>
          <el-descriptions-item label="执行人">{{ currentTask.username }}</el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="getStatusType(currentTask.status)">
              {{ currentTask.status }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="进度">
            <el-progress :percentage="currentTask.progress" />
          </el-descriptions-item>
          <el-descriptions-item label="绩效评分">
            <el-rate v-model="currentTask.performance_score" :max="5" disabled show-score />
          </el-descriptions-item>
          <el-descriptions-item label="分配时间">{{ currentTask.assigned_at }}</el-descriptions-item>
          <el-descriptions-item label="最后更新">{{ currentTask.last_update }}</el-descriptions-item>
          <el-descriptions-item label="备注说明" :span="2">
            {{ currentTask.comments || '暂无备注' }}
          </el-descriptions-item>
        </el-descriptions>
      </div>
    </el-dialog>

    <!-- 更新进度对话框 -->
    <el-dialog
      v-model="updateDialogVisible"
      title="更新任务进度"
      width="600px"
    >
      <el-form
        ref="updateFormRef"
        :model="updateForm"
        :rules="updateRules"
        label-width="100px"
      >
        <el-form-item label="任务名称">
          <el-input v-model="updateForm.task_name" disabled />
        </el-form-item>
        <el-form-item label="执行人">
          <el-input v-model="updateForm.username" disabled />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="updateForm.status" placeholder="选择状态">
            <el-option label="进行中" value="进行中" />
            <el-option label="已完成" value="已完成" />
            <el-option label="已暂停" value="已暂停" />
          </el-select>
        </el-form-item>
        <el-form-item label="进度" prop="progress">
          <el-slider 
            v-model="updateForm.progress" 
            :max="100" 
            show-input 
            :format-tooltip="(val) => `${val}%`"
          />
        </el-form-item>
        <el-form-item label="绩效评分" prop="performance_score">
          <el-rate v-model="updateForm.performance_score" :max="5" show-text />
        </el-form-item>
        <el-form-item label="备注说明" prop="comments">
          <el-input 
            v-model="updateForm.comments" 
            type="textarea"
            :rows="4"
            placeholder="请输入更新说明" 
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="updateDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleUpdateSubmit">
            确定更新
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, nextTick } from 'vue'
import { ElMessage, type FormInstance } from 'element-plus'
import { 
  Refresh, 
  Search, 
  Document, 
  Clock, 
  CircleCheck, 
  TrendCharts 
} from '@element-plus/icons-vue'
import * as echarts from 'echarts'
import { getMyTasks, getMyTaskStats, updateMyTask, getTaskAssignments } from '@/api/task'
import { getTaskAssignmentStats } from '@/api/taskAssignment'
import { useAuthStore } from '@/store/modules/auth'

interface TaskProgress {
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

interface Stats {
  total: number
  inProgress: number
  completed: number
  avgProgress: number
}

const authStore = useAuthStore()
const loading = ref(false)
const detailDialogVisible = ref(false)
const updateDialogVisible = ref(false)
const updateFormRef = ref<FormInstance>()
const statusChartRef = ref<HTMLElement>()
const progressChartRef = ref<HTMLElement>()

const searchForm = reactive({
  taskName: '',
  username: '',
  status: '',
  dateRange: [] as string[]
})

const updateForm = reactive({
  id: 0,
  task_name: '',
  username: '',
  status: '',
  progress: 0,
  performance_score: 0,
  comments: ''
})

const pagination = reactive({
  currentPage: 1,
  pageSize: 10,
  total: 0
})

const progressList = ref<TaskProgress[]>([])
const currentTask = ref<TaskProgress | null>(null)
const stats = ref<Stats>({
  total: 0,
  inProgress: 0,
  completed: 0,
  avgProgress: 0
})

const updateRules = {
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

const loadProgressData = async () => {
  loading.value = true
  try {
    let tasksResponse
    
    // 根据用户角色决定调用哪个API
    if (authStore.isAdmin) {
      // 管理员获取所有任务分配
      tasksResponse = await getTaskAssignments({
        status: searchForm.status || undefined,
        skip: (pagination.currentPage - 1) * pagination.pageSize,
        limit: pagination.pageSize
      })
    } else {
      // 普通用户获取个人任务
      tasksResponse = await getMyTasks({
        status: searchForm.status || undefined
      })
    }
    
    // 直接使用后端返回的数据，无需复杂映射
    progressList.value = tasksResponse.data?.map(item => ({
      id: item.id,
      task_id: item.task_id,
      task_name: item.task_name || `任务 ${item.task_id}`,
      task_type: item.task_type || '未知类型',
      username: item.username,
      status: item.status,
      progress: item.progress,
      performance_score: item.performance_score,
      comments: item.comments || '',
      assigned_at: item.assigned_at,
      last_update: item.last_update
    })) || []
    
    // 如果是普通用户，直接使用数据长度作为总数
    // 如果是管理员，需要单独获取总数（这里简化处理）
    pagination.total = progressList.value.length
    
    // 计算统计数据
    calculateStats()
    
    // 获取统计数据
    try {
      if (authStore.isAdmin) {
        // 管理员获取全部任务分配统计
        const statsResponse = await getTaskAssignmentStats()
        if (statsResponse.data) {
          stats.value = {
            total: statsResponse.data.total_assignments,
            inProgress: statsResponse.data.in_progress,
            completed: statsResponse.data.completed,
            avgProgress: Math.round(statsResponse.data.avg_progress || 0)
          }
        }
      } else {
        // 普通用户获取个人任务统计
        const statsResponse = await getMyTaskStats()
        if (statsResponse.data) {
          stats.value = {
            total: statsResponse.data.total_tasks,
            inProgress: statsResponse.data.in_progress_tasks,
            completed: statsResponse.data.completed_tasks,
            avgProgress: Math.round((statsResponse.data.average_score || 0) * 20) // 转换为百分比
          }
        }
      }
    } catch (statsError) {
      console.warn('获取统计数据失败:', statsError)
      // 如果统计API失败，使用计算的统计数据
    }
  } catch (error) {
    ElMessage.error('加载任务进度数据失败')
    console.error('加载任务进度失败:', error)
  } finally {
    loading.value = false
  }
}

const calculateStats = () => {
  const total = progressList.value.length
  const inProgress = progressList.value.filter(item => item.status === '进行中').length
  const completed = progressList.value.filter(item => item.status === '已完成').length
  const avgProgress = total > 0 
    ? Math.round(progressList.value.reduce((sum, item) => sum + item.progress, 0) / total)
    : 0
  
  stats.value = {
    total,
    inProgress,
    completed,
    avgProgress
  }
}

const initCharts = () => {
  nextTick(() => {
    // 状态分布饼图
    if (statusChartRef.value) {
      const statusChart = echarts.init(statusChartRef.value)
      const statusData = [
        { value: stats.value.inProgress, name: '进行中' },
        { value: stats.value.completed, name: '已完成' },
        { value: progressList.value.filter(item => item.status === '已暂停').length, name: '已暂停' }
      ]
      
      statusChart.setOption({
        tooltip: {
          trigger: 'item'
        },
        legend: {
          orient: 'vertical',
          left: 'left'
        },
        series: [
          {
            name: '任务状态',
            type: 'pie',
            radius: '50%',
            data: statusData,
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ]
      })
    }
    
    // 进度趋势图
    if (progressChartRef.value) {
      const progressChart = echarts.init(progressChartRef.value)
      const progressData = progressList.value.map(item => ({
        name: item.task_name,
        value: item.progress
      }))
      
      progressChart.setOption({
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          data: progressData.map(item => item.name),
          axisLabel: {
            rotate: 45,
            interval: 0
          }
        },
        yAxis: {
          type: 'value',
          max: 100,
          axisLabel: {
            formatter: '{value}%'
          }
        },
        series: [
          {
            name: '进度',
            type: 'bar',
            data: progressData.map(item => item.value),
            itemStyle: {
              color: function(params: any) {
                const colorList = ['#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de']
                return colorList[params.dataIndex % colorList.length]
              }
            }
          }
        ]
      })
    }
  })
}

const handleSearch = () => {
  pagination.currentPage = 1
  loadProgressData()
}

const handleReset = () => {
  searchForm.taskName = ''
  searchForm.username = ''
  searchForm.status = ''
  searchForm.dateRange = []
  pagination.currentPage = 1
  loadProgressData()
}

const refreshData = () => {
  loadProgressData()
  ElMessage.success('数据已刷新')
}

const handleViewDetail = (row: TaskProgress) => {
  currentTask.value = row
  detailDialogVisible.value = true
}

const handleUpdateProgress = (row: TaskProgress) => {
  updateDialogVisible.value = true
  Object.assign(updateForm, {
    id: row.id,
    task_name: row.task_name,
    username: row.username,
    status: row.status,
    progress: row.progress,
    performance_score: row.performance_score,
    comments: row.comments
  })
}

const handleUpdateSubmit = async () => {
  if (!updateFormRef.value) return
  
  try {
    await updateFormRef.value.validate()
    
    await updateMyTask(updateForm.id, {
      status: updateForm.status,
      progress: updateForm.progress,
      comments: updateForm.comments
    })
    
    ElMessage.success('进度更新成功')
    updateDialogVisible.value = false
    loadProgressData()
  } catch (error: any) {
    ElMessage.error('更新失败')
    console.error('更新任务进度失败:', error)
  }
}

const handleSizeChange = (val: number) => {
  pagination.pageSize = val
  pagination.currentPage = 1
  loadProgressData()
}

const handleCurrentChange = (val: number) => {
  pagination.currentPage = val
  loadProgressData()
}

onMounted(() => {
  loadProgressData().then(() => {
    initCharts()
  })
})
</script>

<style scoped lang="scss">
.task-progress {
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

  .stats-cards {
    margin-bottom: 20px;

    .stat-card {
      position: relative;
      overflow: hidden;

      .stat-content {
        .stat-value {
          font-size: 32px;
          font-weight: bold;
          color: #333;
          margin-bottom: 8px;
        }

        .stat-label {
          font-size: 14px;
          color: #666;
        }
      }

      .stat-icon {
        position: absolute;
        right: 20px;
        top: 50%;
        transform: translateY(-50%);
        font-size: 48px;
        opacity: 0.3;

        &.total {
          color: #409eff;
        }

        &.progress {
          color: #e6a23c;
        }

        &.completed {
          color: #67c23a;
        }

        &.avg {
          color: #f56c6c;
        }
      }
    }
  }

  .charts-section {
    margin-bottom: 20px;

    .chart-container {
      height: 300px;
    }
  }

  .progress-table {
    .pagination {
      margin-top: 20px;
      text-align: right;
    }
  }

  .task-detail {
    .el-descriptions {
      margin-top: 20px;
    }
  }
}
</style> 