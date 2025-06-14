<template>
  <div class="role-selection-container">
    <!-- 背景装饰 -->
    <div class="background-shapes">
      <div class="shape shape-1"></div>
      <div class="shape shape-2"></div>
      <div class="shape shape-3"></div>
    </div>
    
    <!-- 角色选择卡片 -->
    <div class="selection-wrapper">
      <div class="selection-card">
        <div class="card-header">
          <div class="logo-section">
            <div class="logo-icon">
              <el-icon size="48"><UserFilled /></el-icon>
            </div>
            <h1 class="title">选择您的角色</h1>
            <p class="subtitle">请选择与您职位相符的角色以继续</p>
          </div>
        </div>
        
        <div class="card-body">
          <div class="role-options">
            <div 
              v-for="role in roleOptions" 
              :key="role.value"
              class="role-option"
              :class="{ 
                active: selectedRole === role.value,
                'role-selected': selectedRole === role.value 
              }"
              :data-selected="selectedRole === role.value"
              @click="selectRole(role.value)"
            >
              <div class="role-icon">
                <el-icon size="32">
                  <component :is="role.icon" />
                </el-icon>
              </div>
              <div class="role-info">
                <h3 class="role-name">{{ role.label }}</h3>
                <p class="role-desc">{{ role.description }}</p>
              </div>
              <div class="role-check">
                <el-icon v-if="selectedRole === role.value"><Check /></el-icon>
              </div>
            </div>
          </div>
          
          <div class="action-buttons">
            <el-button
              type="primary"
              size="large"
              :disabled="!selectedRole"
              :loading="loading"
              class="confirm-button"
              @click="confirmSelection"
            >
              <el-icon><Right /></el-icon>
              确认选择
            </el-button>
            
            <el-button
              size="large"
              class="back-button"
              @click="goBack"
            >
              <el-icon><ArrowLeft /></el-icon>
              返回登录
            </el-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { 
  UserFilled, 
  Monitor, 
  Setting, 
  DataAnalysis, 
  Cpu,
  Check,
  Right,
  ArrowLeft 
} from '@element-plus/icons-vue'
import { useAuthStore } from '@/store/modules/auth'
import { USER_ROLE_OPTIONS } from '@/types/user'

const router = useRouter()
const authStore = useAuthStore()

// 选中的角色
const selectedRole = ref<string>('')
const loading = ref(false)

// 角色选项配置
const roleOptions = [
  {
    value: '网络工程师',
    label: '网络工程师',
    description: '负责网络设备配置、监控和故障排除',
    icon: Monitor
  },
  {
    value: '系统架构师',
    label: '系统架构师',
    description: '负责系统架构设计和技术选型决策',
    icon: Cpu
  },
  {
    value: '系统规划与管理师',
    label: '系统规划与管理师',
    description: '负责系统规划、资源管理和运维策略',
    icon: Setting
  },
  {
    value: '系统分析师',
    label: '系统分析师',
    description: '负责需求分析、系统设计和数据分析',
    icon: DataAnalysis
  }
]

// 选择角色
const selectRole = (role: string) => {
  selectedRole.value = role
}



// 确认选择
const confirmSelection = async () => {
  if (!selectedRole.value) {
    ElMessage.warning('请先选择一个角色')
    return
  }
  
  // 检查用户是否有权限使用该角色
  const currentUser = authStore.user
  if (!currentUser) {
    ElMessage.error('用户信息获取失败，请重新登录')
    router.push('/login')
    return
  }
  
  // 检查操作员是否有权限使用选中的角色
  if (currentUser.type === '操作员' && currentUser.role !== selectedRole.value) {
    ElMessage.error(`您无权限使用"${selectedRole.value}"角色，您的角色是"${currentUser.role}"`)
    return
  }
  
  loading.value = true
  try {
    // 模拟角色验证过程
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // 发送当前角色的全部信息到指定地址
    const selectedRoleData = roleOptions.find(role => role.value === selectedRole.value)
    const roleInfoData = {
      user: {
        id: currentUser.id,
        username: currentUser.username,
        role: currentUser.role,
        type: currentUser.type,
        status: currentUser.status,
        photo_data: currentUser.photo_data,
        created_at: currentUser.created_at,
        updated_at: currentUser.updated_at
      },
      selectedRole: {
        value: selectedRoleData?.value || selectedRole.value,
        label: selectedRoleData?.label || selectedRole.value,
        description: selectedRoleData?.description || '',
        icon: selectedRoleData?.icon?.name || ''
      },
      timestamp: new Date().toISOString(),
      action: 'role_selection'
    }
    
    try {
      const response = await fetch('http://127.0.0.1:8800/upload', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(roleInfoData)
      })
      
      if (response.ok) {
        console.log('角色信息已成功上传')
      } else {
        console.warn('角色信息上传失败:', response.status)
      }
    } catch (uploadError) {
      console.error('上传角色信息时发生错误:', uploadError)
      // 不阻断正常流程，只记录错误
    }
    
    ElMessage.success(`已切换到${selectedRole.value}角色`)
    
    // 保存选中的角色到本地存储
    localStorage.setItem('selectedRole', selectedRole.value)
    
    // 跳转到主页面
    router.push('/dashboard')
    
  } catch (error) {
    ElMessage.error('角色切换失败，请重试')
  } finally {
    loading.value = false
  }
}

// 返回登录
const goBack = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要返回登录页面吗？这将退出当前登录状态。',
      '确认返回',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    
    await authStore.logoutAction()
    ElMessage.success('已退出登录')
    router.push('/login')
  } catch (error) {
    // 用户取消了操作
  }
}

// 组件挂载时检查用户类型
onMounted(() => {
  const currentUser = authStore.user
  if (!currentUser) {
    router.push('/login')
    return
  }
  
  // 如果是管理员，直接跳转到主页面
  if (currentUser.type === '管理员') {
    router.push('/dashboard')
    return
  }
  
  // 如果是操作员但没有设置角色，需要选择角色
  if (currentUser.type === '操作员' && !currentUser.role) {
    ElMessage.info('请选择您的角色以继续使用系统')
  }
})
</script>

<style lang="scss">
.role-selection-container {
  position: relative;
  width: 100vw;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  overflow-x: hidden;
  padding: 20px 0;
}

.background-shapes {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
  
  .shape {
    position: absolute;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.1);
    animation: float 6s ease-in-out infinite;
    
    &.shape-1 {
      width: 300px;
      height: 300px;
      top: 10%;
      left: 10%;
      animation-delay: 0s;
    }
    
    &.shape-2 {
      width: 200px;
      height: 200px;
      top: 60%;
      right: 15%;
      animation-delay: 2s;
    }
    
    &.shape-3 {
      width: 150px;
      height: 150px;
      bottom: 20%;
      left: 20%;
      animation-delay: 4s;
    }
  }
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px) rotate(0deg);
  }
  50% {
    transform: translateY(-20px) rotate(180deg);
  }
}

.selection-wrapper {
  position: relative;
  z-index: 10;
  width: 100%;
  max-width: 580px;
  padding: 16px;
}

.selection-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 24px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  animation: slideUp 0.6s ease-out;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.card-header {
  padding: 32px 32px 16px;
  text-align: center;
  
  .logo-section {
    .logo-icon {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 64px;
      height: 64px;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      border-radius: 16px;
      color: white;
      margin-bottom: 16px;
      box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3);
    }
    
    .title {
      font-size: 24px;
      font-weight: 700;
      color: #1a202c;
      margin: 0 0 6px 0;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }
    
    .subtitle {
      font-size: 13px;
      color: #718096;
      margin: 0;
      font-weight: 500;
    }
  }
}

.card-body {
  padding: 16px 32px 32px;
}

.role-options {
  display: grid;
  gap: 12px;
  margin-bottom: 24px;
}

.role-option {
  display: flex;
  align-items: center;
  padding: 16px;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  background: white;
  cursor: pointer;
  transition: all 0.3s ease;
  
  &:hover:not(.active) {
    border-color: #d1d5db;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }
}

// 选中状态样式 - 使用多种选择器确保生效
.role-selection-container .role-option.role-selected,
.role-selection-container .role-option.active,
.role-option.role-selected,
.role-option.active,
.role-option[data-selected="true"] {
  border: 2px solid #667eea !important;
  background: linear-gradient(135deg, #667eea, #764ba2) !important;
  background-color: transparent !important;
  color: white !important;
  box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3) !important;
  transform: translateY(-2px) !important;
}

.role-selection-container .role-option.role-selected .role-icon,
.role-selection-container .role-option.active .role-icon,
.role-option.role-selected .role-icon,
.role-option.active .role-icon {
  background: rgba(255, 255, 255, 0.2) !important;
  color: white !important;
}

.role-selection-container .role-option.role-selected .role-name,
.role-selection-container .role-option.active .role-name,
.role-option.role-selected .role-name,
.role-option.active .role-name {
  color: white !important;
}

.role-selection-container .role-option.role-selected .role-desc,
.role-selection-container .role-option.active .role-desc,
.role-option.role-selected .role-desc,
.role-option.active .role-desc {
  color: rgba(255, 255, 255, 0.9) !important;
}

.role-selection-container .role-option.role-selected .role-check .el-icon,
.role-selection-container .role-option.active .role-check .el-icon,
.role-option.role-selected .role-check .el-icon,
.role-option.active .role-check .el-icon {
  color: white !important;
}

// 确保hover状态不会覆盖选中状态
.role-selection-container .role-option.role-selected:hover,
.role-selection-container .role-option.active:hover,
.role-option.role-selected:hover,
.role-option.active:hover {
  border: 2px solid #667eea !important;
  background: linear-gradient(135deg, #667eea, #764ba2) !important;
  background-color: transparent !important;
  color: white !important;
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
  transform: translateY(-2px) !important;
}

.role-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 56px;
  height: 56px;
  background: #f8fafc;
  border-radius: 10px;
  margin-right: 14px;
  color: #667eea;
  flex-shrink: 0;
}

.role-info {
  flex: 1;
}

.role-name {
  font-size: 16px;
  font-weight: 600;
  color: #1a202c;
  margin: 0 0 6px 0;
}

.role-desc {
  font-size: 13px;
  color: #718096;
  margin: 0;
  line-height: 1.4;
}

.role-check {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 18px;
  
  .el-icon {
    color: white !important;
  }
}

.action-buttons {
  display: grid;
  gap: 12px;
}

.confirm-button {
  width: 100% !important;
  height: 48px !important;
  font-size: 15px !important;
  font-weight: 600 !important;
  border-radius: 12px !important;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
  border: none !important;
  padding: 0 16px !important;
  color: white !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  text-align: center !important;
  
  &:hover:not(:disabled) {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
  }
  
  &:focus:not(:disabled) {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    outline: none !important;
    box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.3) !important;
  }
  
  &:active:not(:disabled) {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    transform: translateY(0) !important;
  }
  
  &:disabled {
    background: #d1d5db !important;
    color: #9ca3af !important;
    transform: none !important;
    box-shadow: none !important;
  }
  
  .el-icon {
    margin-right: 6px !important;
    color: white !important;
    display: inline-flex !important;
    align-items: center !important;
    vertical-align: middle !important;
  }
  
  // 确保按钮内容居中对齐
  span {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    width: 100% !important;
  }
}

.back-button {
  width: 100% !important;
  height: 46px !important;
  font-size: 15px !important;
  font-weight: 600 !important;
  border-radius: 12px !important;
  border: 2px solid #e5e7eb !important;
  background: white !important;
  color: #374151 !important;
  transition: all 0.3s ease !important;
  padding: 0 16px !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  text-align: center !important;
  
  &:hover {
    border-color: #667eea !important;
    background: #f8fafc !important;
    color: #667eea !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2) !important;
  }
  
  &:focus {
    border-color: #667eea !important;
    background: #f8fafc !important;
    color: #667eea !important;
    outline: none !important;
    box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2) !important;
  }
  
  &:active {
    transform: translateY(0) !important;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1) !important;
  }
  
  .el-icon {
    margin-right: 6px !important;
    font-size: 14px !important;
    display: inline-flex !important;
    align-items: center !important;
    vertical-align: middle !important;
  }
  
  // 确保按钮内容居中对齐
  span {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    width: 100% !important;
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .role-selection-container {
    padding: 16px 0;
  }
  
  .selection-wrapper {
    padding: 12px;
    max-width: 100%;
  }
  
  .selection-card {
    border-radius: 16px;
  }
  
  .card-header {
    padding: 24px 20px 12px;
    
    .logo-section {
      .logo-icon {
        width: 56px;
        height: 56px;
        margin-bottom: 12px;
      }
      
      .title {
        font-size: 20px;
        margin-bottom: 4px;
      }
      
      .subtitle {
        font-size: 12px;
      }
    }
  }
  
  .card-body {
    padding: 12px 20px 24px;
  }
  
  .role-options {
    gap: 10px;
    margin-bottom: 20px;
  }
  
  .role-option {
    padding: 14px;
    
    .role-icon {
      width: 48px;
      height: 48px;
      margin-right: 12px;
    }
    
    .role-name {
      font-size: 15px;
      margin-bottom: 4px;
    }
    
    .role-desc {
      font-size: 12px;
    }
  }
  
  .confirm-button {
    height: 46px !important;
    font-size: 14px !important;
    border-radius: 10px !important;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    
    &:hover:not(:disabled) {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    }
    
    &:disabled {
      background: #d1d5db !important;
      color: #9ca3af !important;
    }
    
    .el-icon {
      display: inline-flex !important;
      align-items: center !important;
    }
    
    span {
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      width: 100% !important;
    }
  }
  
  .back-button {
    height: 42px !important;
    font-size: 13px !important;
    border-radius: 10px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    
    .el-icon {
      margin-right: 4px !important;
      font-size: 12px !important;
      display: inline-flex !important;
      align-items: center !important;
    }
    
    span {
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      width: 100% !important;
    }
  }
}

@media (max-width: 480px) {
  .role-selection-container {
    padding: 12px 0;
  }
  
  .selection-wrapper {
    padding: 8px;
  }
  
  .card-header {
    padding: 20px 16px 10px;
  }
  
  .card-body {
    padding: 10px 16px 20px;
  }
  
  .role-option {
    padding: 12px;
    
    .role-icon {
      width: 44px;
      height: 44px;
      margin-right: 10px;
    }
    
    .role-name {
      font-size: 14px;
    }
    
    .role-desc {
      font-size: 11px;
    }
  }
}
</style> 