<template>
  <div class="task-assignment">
    <!-- 主要内容区域 -->
    <div class="assignment-layout">
      <!-- 左侧：任务区域 -->
      <div class="left-panel">
        <!-- 任务下发列表 -->
        <el-card shadow="never" class="task-card">
          <template #header>
            <div class="card-header">
              <span>🔖 任务下发列表</span>
            </div>
          </template>
          
          <div class="task-list">
            <el-table 
              :data="availableTasks" 
              v-loading="loading"
              @current-change="handleTaskSelection"
              highlight-current-row
              height="300"
              style="width: 100%"
            >
              <el-table-column prop="id" label="任务ID" width="80" />
              <el-table-column prop="name" label="任务名称" min-width="200" show-overflow-tooltip />
              <el-table-column prop="type" label="任务类型" width="120" />
              <el-table-column prop="phase" label="阶段任务" width="120" />
            </el-table>
          </div>
        </el-card>

        <!-- 任务详情 -->
        <el-card shadow="never" class="task-detail-card">
          <template #header>
            <div class="card-header">
              <el-icon><Document /></el-icon>
              <span>任务详情</span>
            </div>
          </template>
          
          <div class="task-detail">
            <div v-if="selectedTask" class="detail-content">
              <div class="detail-grid">
                <div class="detail-item">
                  <label class="detail-label">任务名称</label>
                  <div class="detail-value">{{ selectedTask.name }}</div>
                </div>
                <div class="detail-item">
                  <label class="detail-label">任务类型</label>
                  <div class="detail-value">{{ selectedTask.type }}</div>
                </div>
                <div class="detail-item">
                  <label class="detail-label">任务阶段</label>
                  <div class="detail-value">{{ selectedTask.phase }}</div>
                </div>
                <div class="detail-item detail-description">
                  <label class="detail-label">任务描述</label>
                  <div class="detail-value">{{ selectedTask.description || '对生产环境进行全面的安全漏洞扫描，包括操作系统、应用程序和网络设备' }}</div>
                </div>
              </div>
            </div>
            <div v-else class="placeholder">
              <el-icon><InfoFilled /></el-icon>
              <span>选择任务查看详情</span>
            </div>
          </div>
        </el-card>
      </div>

      <!-- 右侧：执行人选择区域 -->
      <div class="right-panel">
        <!-- 选择执行人 -->
        <el-card shadow="never" class="user-selection-card">
          <template #header>
            <div class="card-header">
              <span>👥 选择执行人</span>
            </div>
          </template>

          <div class="user-selection">
            <!-- 可选执行人（左侧） -->
            <div class="available-users-section">
              <div class="section-header">
                <span>选择执行人 ({{ availableUsers.length }}/20 项)</span>
              </div>
              <div class="user-list available" :class="{ loading: userLoading }">
                <div 
                  v-for="user in availableUsers" 
                  :key="user.username"
                  class="user-item"
                  @click="toggleUser(user, 'available')"
                >
                  <el-checkbox :model-value="checkedAvailableUsers.includes(user.username)" />
                  <span>{{ user.username }}</span>
                </div>
                <div v-if="availableUsers.length === 0 && !userLoading" class="empty-state">
                  暂无可选用户
                </div>
              </div>
            </div>

            <!-- 传输按钮 -->
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

            <!-- 已选执行人（右侧） -->
            <div class="selected-users-section">
              <div class="section-header">
                <el-icon><Check /></el-icon>
                <span>已选执行人 ({{ selectedUsers.length }}/20 项)</span>
              </div>
              <div class="user-list selected">
                <div 
                  v-for="user in selectedUsers" 
                  :key="user.username"
                  class="user-item selected"
                  @click="toggleUser(user, 'selected')"
                >
                  <el-checkbox :model-value="checkedSelectedUsers.includes(user.username)" />
                  <span>{{ user.username }}</span>
                </div>
                <div v-if="selectedUsers.length === 0" class="empty-state">
                  已分配执行人 (0 项)
                </div>
              </div>
            </div>
          </div>
        </el-card>

        <!-- 分配任务按钮 -->
        <div class="assignment-controls">
          <el-button 
            type="primary" 
            size="large"
            :disabled="!selectedTask || selectedUsers.length === 0"
            @click="handleAssignTasks"
            style="width: 100%;"
          >
            分配任务
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Check, ArrowRight, ArrowLeft, Document, InfoFilled } from '@element-plus/icons-vue'
import { getTasks, createTaskAssignment } from '@/api/task'
import { getUserList } from '@/api/user'
import type { Task } from '@/types/task'
import type { User } from '@/types/user'

const loading = ref(false)
const userLoading = ref(false)

// 数据
const availableTasks = ref<Task[]>([])
const availableUsers = ref<User[]>([])
const selectedTask = ref<Task | null>(null)
const selectedUsers = ref<User[]>([])
const checkedAvailableUsers = ref<string[]>([])
const checkedSelectedUsers = ref<string[]>([])

// 方法
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
  userLoading.value = true
  try {
    // 使用用户列表API，过滤活跃用户
    const response = await getUserList({ limit: 100 })
    availableUsers.value = response.data?.filter(user => user.status === 'active') || []
  } catch (error) {
    ElMessage.error('加载可用用户失败')
    console.error('加载用户失败:', error)
  } finally {
    userLoading.value = false
  }
}

const handleTaskSelection = (currentRow: Task | null) => {
  selectedTask.value = currentRow
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

const handleAssignTasks = async () => {
  if (!selectedTask.value) {
    ElMessage.warning('请选择要分配的任务')
    return
  }
  
  if (selectedUsers.value.length === 0) {
    ElMessage.warning('请选择执行人')
    return
  }

  try {
    await ElMessageBox.confirm(
      `确定要将任务 "${selectedTask.value.name}" 分配给 ${selectedUsers.value.length} 个执行人吗？`,
      '确认分配',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )

    // 创建任务分配
    for (const user of selectedUsers.value) {
      await createTaskAssignment({
        task_id: selectedTask.value.id,
        username: user.username,
        status: '进行中',
        progress: 0,
        performance_score: 0,
        comments: ''
      })
    }

    ElMessage.success('任务分配成功')
    selectedTask.value = null
    selectedUsers.value = []
    checkedAvailableUsers.value = []
    checkedSelectedUsers.value = []
    loadAvailableTasks()
  } catch (error: any) {
    if (error?.message !== 'cancel') {
      ElMessage.error('任务分配失败')
      console.error('分配任务失败:', error)
    }
  }
}

// 组件挂载时加载数据
onMounted(() => {
  loadAvailableTasks()
  loadAvailableUsers()
})
</script>

<style scoped lang="scss">
.task-assignment {
  padding: 16px;
  background: #f5f5f5;
  min-height: calc(100vh - 60px);

  .assignment-layout {
    display: flex;
    gap: 16px;
    height: calc(100vh - 100px);

    .left-panel {
      width: 60%;
      display: flex;
      flex-direction: column;
      gap: 16px;

      .task-card {
        flex: 1;
        
        .card-header {
          display: flex;
          align-items: center;
          font-weight: 500;
          font-size: 16px;
        }

        .task-list {
          height: 100%;
        }
      }

      .task-detail-card {
        flex: 0 0 200px;

        .card-header {
          display: flex;
          align-items: center;
          gap: 8px;
          font-weight: 500;
          font-size: 16px;
        }

        .task-detail {
          .detail-content {
            .detail-grid {
              display: grid;
              grid-template-columns: 1fr 1fr;
              gap: 16px;

              .detail-item {
                &.detail-description {
                  grid-column: 1 / -1;
                }

                .detail-label {
                  display: block;
                  font-size: 12px;
                  color: #909399;
                  font-weight: 500;
                  margin-bottom: 4px;
                  text-transform: uppercase;
                  letter-spacing: 0.5px;
                }

                .detail-value {
                  font-size: 14px;
                  color: #303133;
                  line-height: 1.4;
                  word-break: break-all;
                  background: #f8f9fa;
                  padding: 8px 12px;
                  border-radius: 4px;
                  border-left: 3px solid #409eff;
                }
              }
            }
          }

          .placeholder {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            color: #909399;
            padding: 40px 0;
            background: #f9f9f9;
            border-radius: 8px;
            font-size: 14px;
            gap: 8px;

            .el-icon {
              font-size: 24px;
              color: #c0c4cc;
            }
          }
        }
      }
    }

    .right-panel {
      width: 40%;
      display: flex;
      flex-direction: column;
      gap: 16px;

      .user-selection-card {
        flex: 1;

        .card-header {
          display: flex;
          align-items: center;
          font-weight: 500;
          font-size: 16px;
        }

        .user-selection {
          display: flex;
          gap: 12px;
          height: 400px;

          .available-users-section,
          .selected-users-section {
            flex: 1;

            .section-header {
              display: flex;
              align-items: center;
              gap: 8px;
              margin-bottom: 12px;
              font-weight: 500;
              color: #333;
              font-size: 14px;
            }

                          .user-list {
                border: 1px solid #dcdfe6;
                border-radius: 4px;
                height: 350px;
                overflow-y: auto;
                background: #fff;
                position: relative;

                &.loading {
                  opacity: 0.6;
                  
                  &::after {
                    content: "加载中...";
                    position: absolute;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    color: #409eff;
                    font-size: 14px;
                  }
                }

              .user-item {
                display: flex;
                align-items: center;
                gap: 8px;
                padding: 8px 12px;
                cursor: pointer;
                border-bottom: 1px solid #f0f0f0;
                font-size: 14px;

                &:hover {
                  background: #f5f7fa;
                }

                &.selected {
                  background: #e6f7ff;
                  border-color: #91d5ff;
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
                font-size: 14px;
              }
            }
          }

          .transfer-buttons {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            gap: 8px;
            width: 40px;
          }
        }
      }

      .assignment-controls {
        flex: 0 0 auto;
      }
    }
  }
}

:deep(.el-card) {
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

:deep(.el-card__header) {
  padding: 16px 20px;
  background: #fafafa;
  border-bottom: 1px solid #ebeef5;
}

:deep(.el-card__body) {
  padding: 16px 20px;
}

:deep(.el-table .el-table__header th) {
  background: #f5f7fa;
  color: #606266;
  font-weight: 500;
}

:deep(.el-table--enable-row-hover .el-table__body tr:hover > td) {
  background-color: #f5f7fa;
}

:deep(.el-table__body tr.current-row > td) {
  background-color: #ecf5ff;
}
</style> 