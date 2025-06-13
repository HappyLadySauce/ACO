<template>
  <div class="dashboard">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1 class="page-title">系统仪表板</h1>
      <p class="page-subtitle">实时监控系统运行状态</p>
    </div>

    <!-- 统计卡片网格 -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon user-icon">
          <el-icon><User /></el-icon>
        </div>
        <div class="stat-info">
          <div class="stat-number">{{ stats.totalUsers }}</div>
          <div class="stat-label">总用户数</div>
        </div>
        <div class="stat-trend">
          <span class="trend-up">+12%</span>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon task-icon">
          <el-icon><Tickets /></el-icon>
        </div>
        <div class="stat-info">
          <div class="stat-number">{{ stats.totalTasks }}</div>
          <div class="stat-label">总任务数</div>
        </div>
        <div class="stat-trend">
          <span class="trend-up">+8%</span>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon device-icon">
          <el-icon><Monitor /></el-icon>
        </div>
        <div class="stat-info">
          <div class="stat-number">{{ stats.totalDevices }}</div>
          <div class="stat-label">总设备数</div>
        </div>
        <div class="stat-trend">
          <span class="trend-down">-2%</span>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon online-icon">
          <el-icon><Connection /></el-icon>
        </div>
        <div class="stat-info">
          <div class="stat-number">{{ stats.onlineDevices }}</div>
          <div class="stat-label">在线设备</div>
        </div>
        <div class="stat-trend">
          <span class="trend-up">+5%</span>
        </div>
      </div>
    </div>

    <!-- 主要内容网格 -->
    <div class="content-grid">
      <!-- 最近任务 -->
      <div class="content-card tasks-card">
        <div class="card-header">
          <h3 class="card-title">最近任务</h3>
          <el-button type="primary" size="small" @click="$router.push('/tasks')">
            查看全部
          </el-button>
        </div>
        <div class="card-content">
          <div class="task-list">
            <div v-for="task in recentTasks" :key="task.id" class="task-item">
              <div class="task-info">
                <div class="task-name">{{ task.name }}</div>
                <div class="task-time">{{ task.create_time }}</div>
              </div>
              <el-tag :type="getTaskStatusType(task.status)" size="small">
                {{ task.status }}
              </el-tag>
            </div>
          </div>
        </div>
      </div>

      <!-- 设备状态 -->
      <div class="content-card devices-card">
        <div class="card-header">
          <h3 class="card-title">设备状态</h3>
          <el-button type="primary" size="small" @click="$router.push('/devices')">
            查看全部
          </el-button>
        </div>
        <div class="card-content">
          <div class="device-list">
            <div v-for="device in deviceStatus" :key="device.id" class="device-item">
              <div class="device-info">
                <div class="device-name">{{ device.name }}</div>
                <div class="device-time">{{ device.last_active }}</div>
              </div>
              <div class="device-status">
                <div class="status-dot" :class="device.status"></div>
                <span class="status-text">{{ device.status === 'online' ? '在线' : '离线' }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 系统性能图表 -->
      <div class="content-card performance-card">
        <div class="card-header">
          <h3 class="card-title">系统性能</h3>
        </div>
        <div class="card-content">
          <div class="performance-metrics">
            <div class="metric">
              <div class="metric-label">CPU使用率</div>
              <div class="metric-value">68%</div>
              <div class="metric-bar">
                <div class="metric-progress" style="width: 68%"></div>
              </div>
            </div>
            <div class="metric">
              <div class="metric-label">内存使用率</div>
              <div class="metric-value">45%</div>
              <div class="metric-bar">
                <div class="metric-progress" style="width: 45%"></div>
              </div>
            </div>
            <div class="metric">
              <div class="metric-label">磁盘使用率</div>
              <div class="metric-value">72%</div>
              <div class="metric-bar">
                <div class="metric-progress" style="width: 72%"></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 活动日志 -->
      <div class="content-card activity-card">
        <div class="card-header">
          <h3 class="card-title">活动日志</h3>
        </div>
        <div class="card-content">
          <div class="activity-list">
            <div class="activity-item">
              <div class="activity-time">10:30</div>
              <div class="activity-content">用户admin登录系统</div>
            </div>
            <div class="activity-item">
              <div class="activity-time">09:45</div>
              <div class="activity-content">系统维护任务已完成</div>
            </div>
            <div class="activity-item">
              <div class="activity-time">09:20</div>
              <div class="activity-content">新设备已添加到系统</div>
            </div>
            <div class="activity-item">
              <div class="activity-time">08:55</div>
              <div class="activity-content">数据备份任务开始执行</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { User, Tickets, Monitor, Connection } from '@element-plus/icons-vue'

interface Stats {
  totalUsers: number
  totalTasks: number
  totalDevices: number
  onlineDevices: number
}

interface Task {
  id: number
  name: string
  status: string
  create_time: string
}

interface Device {
  id: number
  name: string
  status: string
  last_active: string
}

const stats = ref<Stats>({
  totalUsers: 156,
  totalTasks: 28,
  totalDevices: 42,
  onlineDevices: 38
})

const recentTasks = ref<Task[]>([
  { id: 1, name: '系统维护任务', status: '进行中', create_time: '2024-01-15 10:30' },
  { id: 2, name: '数据备份任务', status: '已完成', create_time: '2024-01-14 14:20' },
  { id: 3, name: '安全检查任务', status: '未开始', create_time: '2024-01-13 09:15' },
  { id: 4, name: '性能优化任务', status: '进行中', create_time: '2024-01-12 16:45' }
])

const deviceStatus = ref<Device[]>([
  { id: 1, name: '服务器-01', status: 'online', last_active: '2024-01-15 12:30' },
  { id: 2, name: '服务器-02', status: 'offline', last_active: '2024-01-14 18:45' },
  { id: 3, name: '工作站-01', status: 'online', last_active: '2024-01-15 11:20' },
  { id: 4, name: '工作站-02', status: 'online', last_active: '2024-01-15 10:15' }
])

const getTaskStatusType = (status: string) => {
  switch (status) {
    case '已完成':
      return 'success'
    case '进行中':
      return 'warning'
    case '未开始':
      return 'info'
    default:
      return 'danger'
  }
}

onMounted(() => {
  console.log('Dashboard 组件已挂载')
})
</script>

<style scoped lang="scss">
.dashboard {
  min-height: 100%;
  display: grid;
  grid-gap: 24px;
  grid-template-rows: auto auto 1fr;
}

.page-header {
  .page-title {
    font-size: 32px;
    font-weight: 700;
    color: #1a202c;
    margin: 0 0 8px 0;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  .page-subtitle {
    font-size: 16px;
    color: #718096;
    margin: 0;
  }
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
}

.stat-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  display: grid;
  grid-template-columns: auto 1fr auto;
  gap: 16px;
  align-items: center;
  border: 1px solid #e2e8f0;
  transition: all 0.3s ease;

  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
  }

  .stat-icon {
    width: 48px;
    height: 48px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    color: white;

    &.user-icon {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }

    &.task-icon {
      background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }

    &.device-icon {
      background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }

    &.online-icon {
      background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
    }
  }

  .stat-info {
    .stat-number {
      font-size: 32px;
      font-weight: 700;
      color: #1a202c;
      line-height: 1;
    }

    .stat-label {
      font-size: 14px;
      color: #718096;
      margin-top: 4px;
    }
  }

  .stat-trend {
    .trend-up {
      color: #10b981;
      font-weight: 600;
    }

    .trend-down {
      color: #ef4444;
      font-weight: 600;
    }
  }
}

.content-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 24px;
}

.content-card {
  background: white;
  border-radius: 16px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  transition: all 0.3s ease;

  &:hover {
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
  }

  .card-header {
    padding: 24px 24px 16px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #f1f5f9;

    .card-title {
      font-size: 18px;
      font-weight: 600;
      color: #1a202c;
      margin: 0;
    }
  }

  .card-content {
    padding: 16px 24px 24px;
  }
}

.task-list {
  .task-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 0;
    border-bottom: 1px solid #f1f5f9;

    &:last-child {
      border-bottom: none;
    }

    .task-info {
      .task-name {
        font-weight: 500;
        color: #1a202c;
        margin-bottom: 4px;
      }

      .task-time {
        font-size: 12px;
        color: #718096;
      }
    }
  }
}

.device-list {
  .device-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 0;
    border-bottom: 1px solid #f1f5f9;

    &:last-child {
      border-bottom: none;
    }

    .device-info {
      .device-name {
        font-weight: 500;
        color: #1a202c;
        margin-bottom: 4px;
      }

      .device-time {
        font-size: 12px;
        color: #718096;
      }
    }

    .device-status {
      display: flex;
      align-items: center;
      gap: 8px;

      .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;

        &.online {
          background: #10b981;
        }

        &.offline {
          background: #ef4444;
        }
      }

      .status-text {
        font-size: 14px;
        font-weight: 500;
      }
    }
  }
}

.performance-metrics {
  .metric {
    margin-bottom: 24px;

    &:last-child {
      margin-bottom: 0;
    }

    .metric-label {
      font-size: 14px;
      color: #718096;
      margin-bottom: 8px;
    }

    .metric-value {
      font-size: 24px;
      font-weight: 700;
      color: #1a202c;
      margin-bottom: 8px;
    }

    .metric-bar {
      height: 8px;
      background: #f1f5f9;
      border-radius: 4px;
      overflow: hidden;

      .metric-progress {
        height: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        transition: width 0.3s ease;
      }
    }
  }
}

.activity-list {
  .activity-item {
    display: flex;
    gap: 16px;
    padding: 12px 0;
    border-bottom: 1px solid #f1f5f9;

    &:last-child {
      border-bottom: none;
    }

    .activity-time {
      font-size: 12px;
      color: #718096;
      font-weight: 500;
      min-width: 40px;
    }

    .activity-content {
      font-size: 14px;
      color: #1a202c;
    }
  }
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .stats-grid {
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  }

  .content-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .dashboard {
    grid-gap: 16px;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .stat-card {
    padding: 20px;
  }

  .page-header .page-title {
    font-size: 24px;
  }
}
</style> 