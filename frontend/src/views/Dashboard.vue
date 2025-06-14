<template>
  <div class="dashboard">
    <!-- 统计卡片网格 -->
    <div class="stats-grid">
      <!-- 当前在线设备 -->
      <div class="stat-card stat-card-1">
        <div class="stat-icon">
          <img src="@/assets/icon/组 3589.png" alt="在线设备" />
        </div>
        <div class="stat-info">
          <div class="stat-number">3台</div>
          <div class="stat-label">当前在线设备</div>
        </div>
      </div>

      <!-- 活跃用户数 -->
      <div class="stat-card stat-card-2">
        <div class="stat-icon">
          <img src="@/assets/icon/组 3590.png" alt="活跃用户" />
        </div>
        <div class="stat-info">
          <div class="stat-number">20人</div>
          <div class="stat-label">活跃用户数</div>
        </div>
      </div>

      <!-- 处理任务数 -->
      <div class="stat-card stat-card-3">
        <div class="stat-icon">
          <img src="@/assets/icon/组 3591.png" alt="处理任务" />
        </div>
        <div class="stat-info">
          <div class="stat-number">{{ taskStats.processingTasks }}个</div>
          <div class="stat-label">处理任务数</div>
        </div>
      </div>

      <!-- 系统运行状态 -->
      <div class="stat-card stat-card-4">
        <div class="stat-icon">
          <img src="@/assets/icon/组 3592.png" alt="运行状态" />
        </div>
        <div class="stat-info">
          <div class="stat-number">运行中</div>
          <div class="stat-label">系统运行状态</div>
        </div>
      </div>

      <!-- 备份磁盘占用 -->
      <div class="stat-card stat-card-5">
        <div class="stat-icon">
          <img src="@/assets/icon/组 3593.png" alt="磁盘占用" />
        </div>
        <div class="stat-info">
          <div class="stat-number">694MB</div>
          <div class="stat-label">备份磁盘占用</div>
        </div>
      </div>

      <!-- 告警数量 -->
      <div class="stat-card stat-card-6">
        <div class="stat-icon">
          <img src="@/assets/icon/组 3594.png" alt="告警数量" />
        </div>
        <div class="stat-info">
          <div class="stat-number">5条</div>
          <div class="stat-label">告警数量</div>
        </div>
      </div>
    </div>

    <!-- 图表区域 -->
    <div class="charts-section">
      <!-- 系统综合对比图 -->
      <div class="chart-card system-chart">
        <div class="chart-header">
          <h3 class="chart-title">
            <img src="@/assets/icon/组 3000.png" alt="系统监控" class="chart-icon-img" />
            系统资源实时监控
          </h3>
        </div>
        <div class="chart-content">
          <div class="chart-legend">
            <span class="legend-item">
              <span class="legend-dot cpu"></span>
              CPU 使用率
            </span>
            <span class="legend-item">
              <span class="legend-dot memory"></span>
              内存使用率
            </span>
            <span class="legend-item">
              <span class="legend-dot disk"></span>
              硬盘使用率
            </span>
          </div>
          <div ref="systemChart" class="chart-container"></div>
        </div>
      </div>

      <!-- 告警信息图表 -->
      <div class="charts-row">
        <div class="chart-card alarm-chart">
          <div class="chart-header">
            <div class="header-left">
              <div class="chart-icon-wrapper">
                <img src="@/assets/icon/组 3261.png" alt="告警信息" class="chart-icon-img" />
              </div>
              <h3 class="chart-title">告警信息统计</h3>
            </div>
            <div class="alert-summary">
              <span class="alert-count critical">{{ alarmStats.critical }}</span>
              <span class="alert-count warning">{{ alarmStats.warning }}</span>
              <span class="alert-count info">{{ alarmStats.info }}</span>
            </div>
          </div>
          <div class="chart-content">
            <div class="alarm-overview">
              <div class="alarm-pie-section">
                <div ref="alarmChart" class="pie-chart"></div>
                <div class="chart-center-text">
                  <div class="total-count">{{ alarmStats.total }}</div>
                  <div class="total-label">总告警</div>
                </div>
              </div>
              <div class="alarm-details">
                <div class="alarm-level-item critical">
                  <div class="level-indicator"></div>
                  <div class="level-info">
                    <div class="level-main">
                      <span class="level-name">严重告警</span>
                      <span class="level-count">{{ alarmStats.critical }}条</span>
                    </div>
                    <div class="level-percentage">{{ ((alarmStats.critical / alarmStats.total) * 100).toFixed(1) }}%</div>
                  </div>
                </div>
                <div class="alarm-level-item warning">
                  <div class="level-indicator"></div>
                  <div class="level-info">
                    <div class="level-main">
                      <span class="level-name">警告告警</span>
                      <span class="level-count">{{ alarmStats.warning }}条</span>
                    </div>
                    <div class="level-percentage">{{ ((alarmStats.warning / alarmStats.total) * 100).toFixed(1) }}%</div>
                  </div>
                </div>
                <div class="alarm-level-item info">
                  <div class="level-indicator"></div>
                  <div class="level-info">
                    <div class="level-main">
                      <span class="level-name">提示告警</span>
                      <span class="level-count">{{ alarmStats.info }}条</span>
                    </div>
                    <div class="level-percentage">{{ ((alarmStats.info / alarmStats.total) * 100).toFixed(1) }}%</div>
                  </div>
                </div>
                <div class="alarm-level-item resolved">
                  <div class="level-indicator"></div>
                  <div class="level-info">
                    <div class="level-main">
                      <span class="level-name">已解决</span>
                      <span class="level-count">{{ alarmStats.resolved }}条</span>
                    </div>
                    <div class="level-percentage">{{ ((alarmStats.resolved / alarmStats.total) * 100).toFixed(1) }}%</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="chart-card device-alert-card">
          <div class="chart-header">
            <div class="header-left">
              <div class="chart-icon-wrapper">
                <img src="@/assets/icon/组 3262.png" alt="设备告警" class="chart-icon-img" />
              </div>
              <h3 class="chart-title">实时告警动态</h3>
            </div>
            <div class="refresh-indicator">
              <span class="refresh-dot"></span>
              <span class="refresh-text">实时更新</span>
            </div>
          </div>
          <div class="device-alert-content">
            <div class="alert-list">
              <div 
                class="alert-item" 
                v-for="(alert, index) in realtimeAlerts" 
                :key="index"
                :class="['alert-item', `level-${alert.level}`]"
              >
                <div class="alert-left">
                  <div class="alert-status-dot" :class="`dot-${alert.level}`"></div>
                  <div class="alert-info">
                    <div class="alert-title">{{ alert.title }}</div>
                    <div class="alert-meta">
                      <span class="alert-device">
                        <i class="device-icon">🖥️</i>
                        {{ alert.device }}
                      </span>
                      <span class="alert-category-badge" :class="`category-${alert.category}`">
                        {{ alert.category }}
                      </span>
                    </div>
                    <div class="alert-description">{{ alert.description }}</div>
                  </div>
                </div>
                <div class="alert-right">
                  <div class="alert-time">{{ alert.time }}</div>
                  <div class="alert-actions">
                    <button class="action-btn view-btn" @click="handleViewAlert(alert.id)">
                      <i class="icon">👁️</i>
                    </button>
                    <button class="action-btn handle-btn" @click="handleProcessAlert(alert.id)">
                      <i class="icon">⚡</i>
                    </button>
                  </div>
                </div>
              </div>
            </div>
            <div class="alert-footer">
              <button class="footer-btn view-all" @click="handleViewAllAlerts">
                <i class="btn-icon">📋</i>
                查看全部告警
              </button>
              <button class="footer-btn export-report" @click="handleExportReport">
                <i class="btn-icon">📊</i>
                导出报告
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 设备信息表格 -->
    <div class="device-table-section">
      <div class="table-card">
        <div class="table-header">
          <h3 class="table-title">
            <img src="@/assets/icon/设备.png" alt="任务信息" class="table-icon-img" />
            任务信息
          </h3>
          <div class="table-actions">
            <button class="action-btn create-btn" @click="handleCreateTask">
              <img src="@/assets/icon/添加.png" alt="创建任务" class="btn-icon-img" />
              创建任务
            </button>
            <button class="action-btn download-btn" @click="handleAssignTask">
              <img src="@/assets/icon/任务.png" alt="任务下发" class="btn-icon-img" />
              任务下发
            </button>
            <button class="action-btn progress-btn" @click="handleManageProgress">
              <img src="@/assets/icon/系统参数.png" alt="进度管理" class="btn-icon-img" />
              进度管理
            </button>
            <button class="action-btn import-btn" @click="handleRefreshData">
              <img src="@/assets/icon/upload.png" alt="刷新数据" class="btn-icon-img" />
              刷新数据
            </button>
          </div>
        </div>
        <div class="table-content">
          <div v-if="taskLoading" class="loading-container">
            <div class="loading-text">加载中...</div>
          </div>
          <table v-else class="device-table">
            <thead>
              <tr>
                <th>任务ID</th>
                <th>任务名称</th>
                <th>任务类型</th>
                <th>任务阶段</th>
                <th>任务描述</th>
                <th>执行角色</th>
                <th>状态</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="task in taskList" :key="task.id">
                <td>{{ task.id }}</td>
                <td>{{ task.name }}</td>
                <td>{{ task.type || '-' }}</td>
                <td>{{ task.phase || '-' }}</td>
                <td>{{ task.description || '-' }}</td>
                <td>-</td>
                <td>
                  <span :class="['status-tag', getStatusClass(task.status)]">
                    {{ task.status }}
                  </span>
                </td>
              </tr>
              <tr v-if="taskList.length === 0">
                <td colspan="7" style="text-align: center; color: #999; padding: 40px;">
                  暂无任务数据
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- 任务管理组件 -->
    <TaskManagement ref="taskManagementRef" @refresh="loadTaskData" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import * as echarts from 'echarts'
import { getTasks, getTasksCount, type Task } from '@/api/task'
import { ElMessage } from 'element-plus'
import TaskManagement from '@/components/TaskManagement.vue'

interface DeviceInfo {
  id: number
  type1: string
  type2: string
  phase: string
  description: string
  role: string
  status: string
}

const systemChart = ref<HTMLElement>()
const alarmChart = ref<HTMLElement>()
const deviceChart = ref<HTMLElement>()
const taskManagementRef = ref<InstanceType<typeof TaskManagement>>()

// 实时数据
const realtimeData = ref({
  cpu: [15, 12, 18, 25, 28, 32, 24, 20, 16, 18, 22],
  memory: [32, 28, 25, 15, 35, 42, 38, 25, 22, 18, 25],
  disk: [45, 42, 35, 30, 28, 25, 30, 35, 40, 38, 42]
})

let chartInstance: any = null
let animationTimer: any = null

// 任务列表数据 - 使用后端API
const taskList = ref<Task[]>([])
const taskStats = ref({
  totalTasks: 0,
  processingTasks: 0
})
const taskLoading = ref(false)

// 设备告警数据
const deviceAlertData = ref([
  {
    type1: '蟹农APP AI信息模拟测试',
    type2: '开发测试任务',
    phase: '模拟用户审批请求'
  },
  {
    type1: '全网设备接入INC',
    type2: '运维监管任务',
    phase: '设备管理'
  },
  {
    type1: 'AI运维平台监管',
    type2: '运维监管任务',
    phase: '运维监管'
  }
])

// 告警统计数据
const alarmStats = ref({
  critical: 3,
  warning: 8,
  info: 12,
  resolved: 25,
  total: 48
})

// 实时告警动态数据
const realtimeAlerts = ref([
  {
    id: 1,
    title: 'CPU使用率过高',
    level: 'critical',
    device: '服务器-01',
    category: '系统',
    description: 'CPU使用率达到92%，请及时处理',
    time: '2分钟前'
  },
  {
    id: 2,
    title: '网络连接异常',
    level: 'warning',
    device: '交换机-03',
    category: '网络',
    description: '设备与中心节点连接不稳定',
    time: '5分钟前'
  },
  {
    id: 3,
    title: '存储空间不足',
    level: 'warning',
    device: '存储服务器-02',
    category: '存储',
    description: '磁盘使用率达到85%，建议清理',
    time: '8分钟前'
  },
  {
    id: 4,
    title: '新设备接入',
    level: 'info',
    device: '监控设备-12',
    category: '设备',
    description: '新的监控设备已成功接入系统',
    time: '15分钟前'
  },
  {
    id: 5,
    title: '系统更新完成',
    level: 'info',
    device: 'Web服务器-01',
    category: '系统',
    description: '系统安全更新已完成，运行正常',
    time: '20分钟前'
  }
])

// 加载任务数据
const loadTaskData = async () => {
  if (taskLoading.value) return
  
  taskLoading.value = true
  try {
    // 获取任务列表
    const tasksResponse = await getTasks({ limit: 10 })
    taskList.value = tasksResponse.data
    
    // 获取任务统计
    const totalResponse = await getTasksCount()
    const processingResponse = await getTasksCount({ status: '进行中' })
    
    taskStats.value = {
      totalTasks: totalResponse.data.count,
      processingTasks: processingResponse.data.count
    }
    
  } catch (error) {
    console.error('加载任务数据失败:', error)
    // 如果是网络错误或者无法连接后端，使用默认数据
    if (taskList.value.length === 0) {
      taskList.value = [
        {
          id: 1,
          name: '系统监控任务',
          type: '监控检测',
          phase: '监控阶段',
          description: '对系统进行实时监控和状态检查',
          status: '进行中',
          create_time: new Date().toISOString(),
          update_time: new Date().toISOString()
        },
        {
          id: 2,
          name: '数据备份任务',
          type: '数据管理',
          phase: '备份阶段',
          description: '定期备份重要数据',
          status: '未分配',
          create_time: new Date().toISOString(),
          update_time: new Date().toISOString()
        }
      ]
      taskStats.value = {
        totalTasks: 2,
        processingTasks: 1
      }
      ElMessage.warning('使用演示数据，请确保后端服务正常运行')
    }
  } finally {
    taskLoading.value = false
  }
}

// 任务操作处理函数
const handleCreateTask = () => {
  taskManagementRef.value?.showCreateTask()
}

const handleAssignTask = () => {
  taskManagementRef.value?.showAssignTask()
}

const handleManageProgress = () => {
  taskManagementRef.value?.showProgressManagement()
}

const handleRefreshData = () => {
  loadTaskData()
  ElMessage.success('数据刷新成功')
}

// 告警相关处理函数
const handleViewAllAlerts = () => {
  ElMessage.info('查看全部告警功能开发中')
}

const handleExportReport = () => {
  ElMessage.info('导出报告功能开发中')
}

// 单个告警处理函数
const handleViewAlert = (alertId: number) => {
  ElMessage.info(`查看告警详情: ${alertId}`)
}

const handleProcessAlert = (alertId: number) => {
  ElMessage.info(`处理告警: ${alertId}`)
}

const getStatusClass = (status: string) => {
  const statusMap: { [key: string]: string } = {
    '未分配': 'status-unassigned',
    '已分配': 'status-assigned',
    '进行中': 'status-processing',
    '已完成': 'status-completed'
  }
  return statusMap[status] || 'status-default'
}

const initSystemChart = () => {
  if (!systemChart.value) return
  
  chartInstance = echarts.init(systemChart.value)
  const option = {
    grid: {
      top: 30,
      left: 50,
      right: 30,
      bottom: 30
    },
    xAxis: {
      type: 'category',
      data: ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11'],
      axisLine: {
        lineStyle: { color: '#E5E7EB' }
      },
      axisTick: { show: false },
      axisLabel: {
        color: '#6B7280',
        fontSize: 12
      }
    },
    yAxis: {
      type: 'value',
      max: 50,
      axisLine: { show: false },
      axisTick: { show: false },
      splitLine: {
        lineStyle: { color: '#F3F4F6', type: 'dashed' }
      },
      axisLabel: {
        color: '#6B7280',
        fontSize: 12
      }
    },
    series: [
      {
        name: 'CPU使用率',
        type: 'line',
        smooth: true,
        lineStyle: { color: '#10B981', width: 2 },
        itemStyle: { color: '#10B981' },
        data: realtimeData.value.cpu,
        animationDuration: 1000,
        animationEasing: 'cubicOut'
      },
      {
        name: '内存使用率',
        type: 'line',
        smooth: true,
        lineStyle: { color: '#3B82F6', width: 2 },
        itemStyle: { color: '#3B82F6' },
        data: realtimeData.value.memory,
        animationDuration: 1000,
        animationEasing: 'cubicOut'
      },
      {
        name: '硬盘使用率',
        type: 'line',
        smooth: true,
        lineStyle: { color: '#06B6D4', width: 2 },
        itemStyle: { color: '#06B6D4' },
        data: realtimeData.value.disk,
        animationDuration: 1000,
        animationEasing: 'cubicOut'
      }
    ]
  }
  chartInstance.setOption(option)
  
  // 启动实时更新
  startRealtimeUpdate()
}

// 生成随机数据
const generateRandomData = (baseValue: number, range: number = 10) => {
  return Math.max(0, Math.min(50, baseValue + (Math.random() - 0.5) * range))
}

// 实时更新数据
const updateChartData = () => {
  if (!chartInstance) return
  
  // 移除第一个数据点，添加新的数据点
  realtimeData.value.cpu.shift()
  realtimeData.value.memory.shift()
  realtimeData.value.disk.shift()
  
  // 生成新的随机数据
  const lastCpuValue = realtimeData.value.cpu[realtimeData.value.cpu.length - 1]
  const lastMemoryValue = realtimeData.value.memory[realtimeData.value.memory.length - 1]
  const lastDiskValue = realtimeData.value.disk[realtimeData.value.disk.length - 1]
  
  realtimeData.value.cpu.push(generateRandomData(lastCpuValue, 8))
  realtimeData.value.memory.push(generateRandomData(lastMemoryValue, 8))
  realtimeData.value.disk.push(generateRandomData(lastDiskValue, 6))
  
  // 更新图表
  chartInstance.setOption({
    series: [
      { data: realtimeData.value.cpu },
      { data: realtimeData.value.memory },
      { data: realtimeData.value.disk }
    ]
  })
}

// 启动实时更新
const startRealtimeUpdate = () => {
  animationTimer = setInterval(() => {
    updateChartData()
  }, 2000) // 每2秒更新一次
}

// 停止实时更新
const stopRealtimeUpdate = () => {
  if (animationTimer) {
    clearInterval(animationTimer)
    animationTimer = null
  }
}

const initAlarmChart = () => {
  if (!alarmChart.value) return
  
  const chart = echarts.init(alarmChart.value)
  const option = {
    series: [{
      type: 'pie',
      radius: ['45%', '75%'],
      center: ['50%', '50%'],
      data: [
        { 
          value: alarmStats.value.critical, 
          name: '严重告警', 
          itemStyle: { 
            color: '#EF4444',
            shadowBlur: 10,
            shadowColor: 'rgba(239, 68, 68, 0.5)'
          }
        },
        { 
          value: alarmStats.value.warning, 
          name: '警告告警', 
          itemStyle: { 
            color: '#F59E0B',
            shadowBlur: 10,
            shadowColor: 'rgba(245, 158, 11, 0.5)'
          }
        },
        { 
          value: alarmStats.value.info, 
          name: '提示告警', 
          itemStyle: { 
            color: '#3B82F6',
            shadowBlur: 10,
            shadowColor: 'rgba(59, 130, 246, 0.5)'
          }
        },
        { 
          value: alarmStats.value.resolved, 
          name: '已解决', 
          itemStyle: { 
            color: '#10B981',
            shadowBlur: 10,
            shadowColor: 'rgba(16, 185, 129, 0.5)'
          }
        }
      ],
      label: { 
        show: false 
      },
      labelLine: { 
        show: false 
      },
      emphasis: { 
        scale: true,
        scaleSize: 5,
        itemStyle: {
          shadowBlur: 20,
          shadowOffsetX: 0,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      },
      animationType: 'scale',
      animationEasing: 'elasticOut',
      animationDelay: (idx: number) => Math.random() * 200
    }]
  }
  chart.setOption(option)
}

// 已移除deviceChart初始化，改为表格形式

onMounted(async () => {
  await nextTick()
  initSystemChart()
  initAlarmChart()
  // initDeviceChart() - 已改为表格形式
  loadTaskData()
})

// 组件卸载时清理定时器
onUnmounted(() => {
  stopRealtimeUpdate()
  if (chartInstance) {
    chartInstance.dispose()
    chartInstance = null
  }
})
</script>

<style scoped lang="scss">
.dashboard {
  padding: 24px;
  background: #f8fafc;
  min-height: 100vh;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 16px;
  margin-bottom: 24px;

  .stat-card {
    background: white;
    border-radius: 8px;
    padding: 20px;
    display: flex;
    align-items: center;
    gap: 12px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    position: relative;
    overflow: hidden;

    &::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 4px;
    }

    &.stat-card-1::before {
      background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }

    &.stat-card-2::before {
      background: linear-gradient(90deg, #f093fb 0%, #f5576c 100%);
    }

    &.stat-card-3::before {
      background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
    }

    &.stat-card-4::before {
      background: linear-gradient(90deg, #43e97b 0%, #38f9d7 100%);
    }

    &.stat-card-5::before {
      background: linear-gradient(90deg, #fa709a 0%, #fee140 100%);
    }

    &.stat-card-6::before {
      background: linear-gradient(90deg, #a8edea 0%, #fed6e3 100%);
    }

    .stat-icon {
      width: 40px;
      height: 40px;
      display: flex;
      align-items: center;
      justify-content: center;

      img {
        width: 32px;
        height: 32px;
      }
    }

    .stat-info {
      flex: 1;

      .stat-number {
        font-size: 18px;
        font-weight: 600;
        color: #1f2937;
        margin-bottom: 4px;
      }

      .stat-label {
        font-size: 12px;
        color: #6b7280;
      }
    }
  }
}

.charts-section {
  margin-bottom: 24px;

  .system-chart {
    margin-bottom: 16px;
    position: relative;
    
    &::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 3px;
      background: linear-gradient(90deg, #10B981, #3B82F6, #06B6D4);
      border-radius: 8px 8px 0 0;
      animation: monitoring-pulse 3s ease-in-out infinite;
    }
    
    .chart-title {
      position: relative;
      
      &::after {
        content: '●';
        color: #10B981;
        margin-left: 8px;
        animation: blink 2s ease-in-out infinite;
      }
    }
  }

  .charts-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
  }
}

.chart-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);

  .chart-header {
    padding: 16px 20px;
    border-bottom: 1px solid #e5e7eb;

    .chart-title {
      font-size: 16px;
      font-weight: 600;
      color: #1f2937;
      margin: 0;
      display: flex;
      align-items: center;
      gap: 8px;

      .chart-icon {
        font-size: 14px;
      }
      
      .chart-icon-img {
        width: 16px;
        height: 16px;
        object-fit: contain;
      }
    }
  }

  .chart-content {
    padding: 20px;
  }

  .chart-legend {
    display: flex;
    gap: 24px;
    margin-bottom: 16px;

    .legend-item {
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 12px;
      color: #6b7280;

      .legend-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;

        &.cpu { background: #10B981; }
        &.memory { background: #3B82F6; }
        &.disk { background: #06B6D4; }
      }
    }
  }

  .chart-container {
    height: 200px;
  }

  .pie-chart {
    height: 180px;
    margin-bottom: 16px;
  }

  // 现代化告警信息样式
  .alarm-chart {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    position: relative;
    overflow: hidden;
    
    &::before {
      content: '';
      position: absolute;
      top: -50%;
      right: -50%;
      width: 200%;
      height: 200%;
      background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
      animation: float 6s ease-in-out infinite;
    }
    
    .chart-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      position: relative;
      z-index: 2;
      
      .header-left {
        display: flex;
        align-items: center;
        gap: 12px;
        
        .chart-icon-wrapper {
          width: 40px;
          height: 40px;
          background: rgba(255, 255, 255, 0.2);
          border-radius: 10px;
          display: flex;
          align-items: center;
          justify-content: center;
          backdrop-filter: blur(10px);
          
          .chart-icon-img {
            width: 20px;
            height: 20px;
            filter: brightness(0) invert(1);
          }
        }
        
        .chart-title {
          color: white;
          font-size: 18px;
          font-weight: 600;
          margin: 0;
        }
      }
      
      .alert-summary {
        display: flex;
        gap: 8px;
        
        .alert-count {
          padding: 6px 12px;
          border-radius: 20px;
          font-size: 12px;
          font-weight: 600;
          background: rgba(255, 255, 255, 0.2);
          color: white;
          backdrop-filter: blur(10px);
          border: 1px solid rgba(255, 255, 255, 0.3);
          transition: all 0.3s ease;
          
          &:hover {
            background: rgba(255, 255, 255, 0.3);
            transform: translateY(-2px);
          }
        }
      }
    }
    
    .chart-content {
      position: relative;
      z-index: 2;
    }
    
    .alarm-overview {
      display: grid;
      grid-template-columns: 200px 1fr;
      gap: 30px;
      align-items: center;
      
      .alarm-pie-section {
        position: relative;
        
        .pie-chart {
          position: relative;
          z-index: 2;
        }
        
        .chart-center-text {
          position: absolute;
          top: 50%;
          left: 50%;
          transform: translate(-50%, -50%);
          text-align: center;
          z-index: 3;
          
          .total-count {
            font-size: 28px;
            font-weight: 700;
            color: white;
            line-height: 1;
          }
          
          .total-label {
            font-size: 12px;
            color: rgba(255, 255, 255, 0.8);
            margin-top: 4px;
          }
        }
      }
      
      .alarm-details {
        .alarm-level-item {
          display: flex;
          align-items: center;
          padding: 12px 0;
          transition: all 0.3s ease;
          border-radius: 8px;
          margin-bottom: 8px;
          
          &:hover {
            background: rgba(255, 255, 255, 0.1);
            transform: translateX(4px);
          }
          
          .level-indicator {
            width: 16px;
            height: 16px;
            border-radius: 4px;
            margin-right: 16px;
            position: relative;
            
            &::after {
              content: '';
              position: absolute;
              top: -2px;
              left: -2px;
              right: -2px;
              bottom: -2px;
              border-radius: 6px;
              background: rgba(255, 255, 255, 0.2);
              z-index: -1;
            }
          }
          
          .level-info {
            flex: 1;
            
            .level-main {
              display: flex;
              justify-content: space-between;
              align-items: center;
              margin-bottom: 4px;
              
              .level-name {
                font-size: 14px;
                font-weight: 500;
                color: white;
              }
              
              .level-count {
                font-size: 12px;
                color: rgba(255, 255, 255, 0.8);
              }
            }
            
            .level-percentage {
              font-size: 16px;
              font-weight: 700;
              color: white;
            }
          }
          
          &.critical .level-indicator {
            background: #EF4444;
            box-shadow: 0 0 20px rgba(239, 68, 68, 0.5);
          }
          
          &.warning .level-indicator {
            background: #F59E0B;
            box-shadow: 0 0 20px rgba(245, 158, 11, 0.5);
          }
          
          &.info .level-indicator {
            background: #3B82F6;
            box-shadow: 0 0 20px rgba(59, 130, 246, 0.5);
          }
          
          &.resolved .level-indicator {
            background: #10B981;
            box-shadow: 0 0 20px rgba(16, 185, 129, 0.5);
          }
        }
      }
    }
  }
}

.device-table-section {
  .table-card {
    background: white;
    border-radius: 8px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);

    .table-header {
      padding: 16px 20px;
      border-bottom: 1px solid #e5e7eb;
      display: flex;
      justify-content: space-between;
      align-items: center;

      .table-title {
        font-size: 16px;
        font-weight: 600;
        color: #1f2937;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 8px;

        .table-icon {
          font-size: 14px;
        }
        
        .table-icon-img {
          width: 16px;
          height: 16px;
          object-fit: contain;
        }
      }

      .table-actions {
        display: flex;
        gap: 8px;

        .action-btn {
          display: flex;
          align-items: center;
          gap: 4px;
          padding: 6px 12px;
          border-radius: 4px;
          border: none;
          font-size: 12px;
          cursor: pointer;
          transition: all 0.2s;

          .btn-icon {
            font-size: 12px;
          }
          
          .btn-icon-img {
            width: 12px;
            height: 12px;
            object-fit: contain;
            filter: brightness(0) invert(1);
          }

          &.create-btn {
            background: #10b981;
            color: white;

            &:hover {
              background: #059669;
            }
          }

          &.download-btn {
            background: #3b82f6;
            color: white;

            &:hover {
              background: #2563eb;
            }
          }

          &.progress-btn {
            background: #f59e0b;
            color: white;

            &:hover {
              background: #d97706;
            }
          }

          &.import-btn {
            background: #8b5cf6;
            color: white;

            &:hover {
              background: #7c3aed;
            }
          }
        }
      }
    }

    .table-content {
      overflow-x: auto;

      .loading-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 60px 20px;

        .loading-text {
          color: #6b7280;
          font-size: 14px;
        }
      }

      .device-table {
        width: 100%;
        border-collapse: collapse;

        th {
          background: #f9fafb;
          padding: 12px 16px;
          text-align: left;
          font-size: 12px;
          font-weight: 600;
          color: #374151;
          border-bottom: 1px solid #e5e7eb;
          white-space: nowrap;
        }

        td {
          padding: 12px 16px;
          font-size: 12px;
          color: #6b7280;
          border-bottom: 1px solid #f3f4f6;
          white-space: nowrap;
        }

        .status-tag {
          padding: 2px 8px;
          border-radius: 12px;
          font-size: 11px;
          font-weight: 500;

          &.status-unassigned {
            background: #fef2f2;
            color: #dc2626;
          }

          &.status-assigned {
            background: #eff6ff;
            color: #2563eb;
          }

          &.status-processing {
            background: #fef3c7;
            color: #d97706;
          }

          &.status-completed {
            background: #ecfdf5;
            color: #059669;
          }
        }
      }
    }
  }

  // 现代化实时告警动态样式
  .device-alert-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    position: relative;
    overflow: hidden;
    
    &::before {
      content: '';
      position: absolute;
      top: -50%;
      left: -50%;
      width: 200%;
      height: 200%;
      background: radial-gradient(circle, rgba(255,255,255,0.05) 0%, transparent 70%);
      animation: float 8s ease-in-out infinite reverse;
    }
    
    .chart-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      position: relative;
      z-index: 2;
      
      .header-left {
        display: flex;
        align-items: center;
        gap: 12px;
        
        .chart-icon-wrapper {
          width: 40px;
          height: 40px;
          background: rgba(255, 255, 255, 0.2);
          border-radius: 10px;
          display: flex;
          align-items: center;
          justify-content: center;
          backdrop-filter: blur(10px);
          
          .chart-icon-img {
            width: 20px;
            height: 20px;
            filter: brightness(0) invert(1);
          }
        }
        
        .chart-title {
          color: white;
          font-size: 18px;
          font-weight: 600;
          margin: 0;
        }
      }
      
      .refresh-indicator {
        display: flex;
        align-items: center;
        gap: 8px;
        background: rgba(255, 255, 255, 0.1);
        padding: 8px 12px;
        border-radius: 20px;
        backdrop-filter: blur(10px);
        
        .refresh-dot {
          width: 8px;
          height: 8px;
          border-radius: 50%;
          background: #10B981;
          animation: pulse 2s infinite;
          box-shadow: 0 0 10px rgba(16, 185, 129, 0.5);
        }
        
        .refresh-text {
          font-size: 12px;
          color: rgba(255, 255, 255, 0.9);
          font-weight: 500;
        }
      }
    }
    
    .device-alert-content {
      padding: 20px;
      position: relative;
      z-index: 2;
      
      .alert-list {
        max-height: 320px;
        overflow-y: auto;
        padding-right: 8px;
        
        &::-webkit-scrollbar {
          width: 6px;
        }
        
        &::-webkit-scrollbar-track {
          background: rgba(255, 255, 255, 0.1);
          border-radius: 3px;
        }
        
        &::-webkit-scrollbar-thumb {
          background: rgba(255, 255, 255, 0.3);
          border-radius: 3px;
          
          &:hover {
            background: rgba(255, 255, 255, 0.5);
          }
        }
        
        .alert-item {
          display: flex;
          align-items: flex-start;
          gap: 12px;
          margin-bottom: 16px;
          padding: 16px;
          background: rgba(255, 255, 255, 0.1);
          border-radius: 12px;
          backdrop-filter: blur(10px);
          border: 1px solid rgba(255, 255, 255, 0.2);
          transition: all 0.3s ease;
          
          &:hover {
            background: rgba(255, 255, 255, 0.15);
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
          }
          
          .alert-left {
            flex: 1;
            display: flex;
            align-items: flex-start;
            gap: 12px;
            
            .alert-status-dot {
              width: 12px;
              height: 12px;
              border-radius: 50%;
              margin-top: 6px;
              position: relative;
              flex-shrink: 0;
              
              &::after {
                content: '';
                position: absolute;
                top: -4px;
                left: -4px;
                right: -4px;
                bottom: -4px;
                border-radius: 50%;
                background: rgba(255, 255, 255, 0.2);
                z-index: -1;
              }
            }
            
            .alert-info {
              flex: 1;
              
              .alert-title {
                font-weight: 600;
                font-size: 15px;
                color: white;
                line-height: 1.4;
                margin-bottom: 8px;
              }
              
              .alert-meta {
                display: flex;
                justify-content: flex-start;
                align-items: center;
                gap: 12px;
                margin-bottom: 8px;
                
                .alert-device {
                  display: flex;
                  align-items: center;
                  gap: 6px;
                  font-size: 12px;
                  color: rgba(255, 255, 255, 0.8);
                  background: rgba(255, 255, 255, 0.1);
                  padding: 4px 8px;
                  border-radius: 12px;
                  
                  .device-icon {
                    font-size: 12px;
                  }
                }
                
                .alert-category-badge {
                  padding: 4px 8px;
                  border-radius: 12px;
                  font-size: 10px;
                  font-weight: 600;
                  text-transform: uppercase;
                  letter-spacing: 0.5px;
                  background: rgba(255, 255, 255, 0.2);
                  color: white;
                  
                  &.category-系统 {
                    background: rgba(59, 130, 246, 0.3);
                  }
                  
                  &.category-网络 {
                    background: rgba(245, 158, 11, 0.3);
                  }
                  
                  &.category-存储 {
                    background: rgba(139, 92, 246, 0.3);
                  }
                  
                  &.category-设备 {
                    background: rgba(16, 185, 129, 0.3);
                  }
                }
              }
              
              .alert-description {
                font-size: 13px;
                color: rgba(255, 255, 255, 0.8);
                line-height: 1.5;
              }
            }
          }
          
          .alert-right {
            display: flex;
            flex-direction: column;
            align-items: flex-end;
            gap: 8px;
            
            .alert-time {
              font-size: 11px;
              color: rgba(255, 255, 255, 0.7);
              white-space: nowrap;
              background: rgba(255, 255, 255, 0.1);
              padding: 2px 8px;
              border-radius: 8px;
            }
            
            .alert-actions {
              display: flex;
              gap: 4px;
              
              .action-btn {
                width: 28px;
                height: 28px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 6px;
                border: none;
                background: rgba(255, 255, 255, 0.2);
                color: white;
                cursor: pointer;
                transition: all 0.2s ease;
                
                &:hover {
                  background: rgba(255, 255, 255, 0.3);
                  transform: scale(1.1);
                }
                
                .icon {
                  font-size: 12px;
                }
              }
            }
          }
          
          &.level-critical {
            .alert-left .alert-status-dot {
              background: #EF4444;
              box-shadow: 0 0 15px rgba(239, 68, 68, 0.6);
              animation: criticalPulse 2s infinite;
            }
          }
          
          &.level-warning {
            .alert-left .alert-status-dot {
              background: #F59E0B;
              box-shadow: 0 0 15px rgba(245, 158, 11, 0.6);
            }
          }
          
          &.level-info {
            .alert-left .alert-status-dot {
              background: #3B82F6;
              box-shadow: 0 0 15px rgba(59, 130, 246, 0.6);
            }
          }
        }
      }
      
      .alert-footer {
        display: flex;
        gap: 12px;
        margin-top: 20px;
        padding-top: 20px;
        border-top: 1px solid rgba(255, 255, 255, 0.2);
        
        .footer-btn {
          flex: 1;
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 8px;
          padding: 12px 16px;
          border-radius: 8px;
          border: none;
          font-size: 13px;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.3s ease;
          background: rgba(255, 255, 255, 0.1);
          color: white;
          backdrop-filter: blur(10px);
          
          &:hover {
            background: rgba(255, 255, 255, 0.2);
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
          }
          
          .btn-icon {
            font-size: 14px;
          }
        }
      }
    }
  }
}

// 响应式设计
@media (max-width: 1400px) {
  .stats-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 1024px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .charts-row {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .dashboard {
    padding: 16px;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .table-header {
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
  }
}

// 实时监控动画
@keyframes monitoring-pulse {
  0%, 100% {
    opacity: 0.6;
    transform: scaleX(1);
  }
  50% {
    opacity: 1;
    transform: scaleX(1.02);
  }
}

@keyframes blink {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.3;
  }
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.7;
    transform: scale(1.1);
  }
}

@keyframes criticalPulse {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
    box-shadow: 0 0 0 3px rgba(255, 255, 255, 1), 0 0 0 0 rgba(239, 68, 68, 0.7);
  }
  50% {
    opacity: 0.9;
    transform: scale(1.05);
    box-shadow: 0 0 0 3px rgba(255, 255, 255, 1), 0 0 0 8px rgba(239, 68, 68, 0);
  }
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px) rotate(0deg);
  }
  33% {
    transform: translateY(-10px) rotate(1deg);
  }
  66% {
    transform: translateY(5px) rotate(-1deg);
  }
}
</style> 