<template>
  <div class="role-selection-container">
    <!-- 科技背景 - 使用提供的背景图片 -->
    <div class="tech-background">
      <div class="main-background"></div>
      <div class="overlay-effects">
        <div class="light-beams"></div>
        <div class="particles"></div>
        <div class="grid-overlay"></div>
      </div>
    </div>
    
    <!-- 顶部信息栏 - 炫酷科技样式 -->
    <div class="top-bar">
      <div class="top-bar-background">
        <div class="top-bar-glow"></div>
        <div class="top-bar-lines">
          <div class="line line-left"></div>
          <div class="line line-right"></div>
            </div>
        <div class="top-bar-particles"></div>
          </div>
      
      <div class="top-bar-content">
        <div class="datetime">
          <div class="datetime-glow"></div>
          <span class="datetime-text">{{ currentDateTime }}</span>
        </div>
        
        <div class="system-title">
          <div class="title-glow-bg"></div>
          <span class="title-text">分布式一体化协作平台</span>
          <div class="title-decorations">
            <div class="deco-left"></div>
            <div class="deco-right"></div>
          </div>
        </div>
        
        <div class="admin-info">
          <div class="admin-container">
            <div class="admin-icon-wrapper">
              <div class="icon-glow-ring"></div>
              <el-icon class="admin-icon">👤</el-icon>
            </div>
            <span class="admin-text">{{ authStore.user?.username || 'Admin' }}</span>
            <div class="admin-actions">
              <div class="action-btn">
                <div class="btn-glow"></div>
                <span>🔧</span>
              </div>
              <div class="action-btn">
                <div class="btn-glow"></div>
                <span>⚙️</span>
              </div>
              <div class="action-btn logout-btn" @click="goBack" title="返回登录">
                <div class="btn-glow"></div>
                <span>🚪</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 底部平台 - 使用提供的素材 -->
    <div class="platform-base">
      <div class="platform-surface">
        <img src="/src/assets/image/组 682.png" alt="底部平台" class="platform-background">
      </div>
      <div class="platform-glow"></div>
      <div class="platform-reflections"></div>
    </div>

    <!-- 角色选择区域 - 放在平台上 -->
    <div class="roles-section">
      <!-- 选中指示器 - 动态指向选中角色 -->
      <div class="selection-indicator">
        <div class="selection-dot" :style="getArrowPosition()"></div>
      </div>
      
      <div class="roles-grid">
            <div 
              v-for="role in roleOptions" 
              :key="role.value"
          class="role-card"
              :class="{ 
            'selected': selectedRole === role.value,
            'available': true
              }"
              @click="selectRole(role.value)"
            >
          <div class="card-glow" :class="{ 'active': selectedRole === role.value }"></div>
          <div class="card-inner">
            <div class="role-3d-icon">
              <div class="icon-platform">
                <img :src="role.iconUrl" :alt="role.label" class="tech-icon">
                <div class="icon-glow"></div>
              </div>
              </div>
            <div class="role-name">{{ role.label }}</div>
          </div>
          <div class="card-base"></div>
              </div>
            </div>
          </div>
          
    <!-- 确认按钮 -->
    <div class="action-section" v-if="selectedRole">
            <el-button
              type="primary"
              size="large"
              :loading="loading"
        class="tech-confirm-button"
              @click="confirmSelection"
            >
        <span class="button-text">启动选择</span>
        <div class="button-glow"></div>
        <div class="button-particles"></div>
            </el-button>
    </div>
    
    <!-- 访问权限错误弹窗 -->
    <AccessDeniedDialog 
      :visible="showAccessDenied"
      :message="accessDeniedMessage"
      @close="handleAccessDeniedClose"
      @confirm="handleAccessDeniedConfirm"
    />
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
import AccessDeniedDialog from '@/components/AccessDeniedDialog.vue'

const router = useRouter()
const authStore = useAuthStore()

// 选中的角色
const selectedRole = ref<string>('')
const loading = ref(false)
const currentDateTime = ref<string>('')

// 访问权限弹窗
const showAccessDenied = ref(false)
const accessDeniedMessage = ref('')

// 角色选项配置
const roleOptions = [
  {
    value: '系统分析师',
    label: '系统分析师', 
    description: '负责安全日志审计',
    icon: Monitor,
    iconUrl: '/src/assets/image/系统分析师.png'
  },
  {
    value: '网络工程师',
    label: '网络工程师',
    description: '负责网络设备配置、监控和故障排除',
    icon: Monitor,
    iconUrl: '/src/assets/image/网络工程师.png'
  },
  {
    value: '系统架构工程师',
    label: '系统架构工程师',
    description: '负责系统架构设计和技术选型决策',
    icon: Cpu,
    iconUrl: '/src/assets/image/系统架构工程师.png'
  },
  {
    value: '数据运维工程师',
    label: '数据运维工程师',
    description: '负责数据库和运维系统管理',
    icon: Setting,
    iconUrl: '/src/assets/image/数据运维工程师.png'
  },
  {
    value: '孪生平台',
    label: '孪生平台',
    description: '负责数字孪生平台管理',
    icon: DataAnalysis,
    iconUrl: '/src/assets/image/孪生平台.png'
  }
]

// 更新时间
const updateDateTime = () => {
  const now = new Date()
  const year = now.getFullYear()
  const month = String(now.getMonth() + 1).padStart(2, '0')
  const day = String(now.getDate()).padStart(2, '0')
  const hours = String(now.getHours()).padStart(2, '0')
  const minutes = String(now.getMinutes()).padStart(2, '0')
  currentDateTime.value = `${year}.${month}.${day} ${hours}:${minutes}`
}

// 选择角色
const selectRole = (role: string) => {
  // 检查用户是否有权限使用该角色
  const currentUser = authStore.user
  if (!currentUser) {
    ElMessage.error('用户信息获取失败，请重新登录')
    router.push('/login')
    return
  }
  
  // 检查操作员是否有权限使用选中的角色
  if (currentUser.type === '操作员' && currentUser.role !== role) {
    accessDeniedMessage.value = `您无权限使用"${role}"角色，您的角色是"${currentUser.role}"`
    showAccessDenied.value = true
    return
  }
  
  selectedRole.value = role
}

// 获取指示点位置
const getArrowPosition = () => {
  if (!selectedRole.value) return { display: 'none' }
  
  const selectedIndex = roleOptions.findIndex(role => role.value === selectedRole.value)
  if (selectedIndex === -1) return { display: 'none' }
  
  // 计算指示点位置，基于卡片间距和索引
  const cardWidth = 320
  const cardGap = 40
  const totalCards = roleOptions.length
  const totalWidth = totalCards * cardWidth + (totalCards - 1) * cardGap
  
  // 计算起始位置（第一个卡片的中心位置）
  const containerCenter = 0
  const firstCardCenter = containerCenter - (totalWidth / 2) + (cardWidth / 2)
  
  // 计算选中卡片的中心位置
  const selectedCardCenter = firstCardCenter + selectedIndex * (cardWidth + cardGap)
  
  return {
    left: `calc(50% + ${selectedCardCenter}px)`,
    transform: 'translateX(-50%)',
    transition: 'left 0.5s cubic-bezier(0.23, 1, 0.32, 1)',
    display: 'block'
  }
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
    accessDeniedMessage.value = `您无权限使用"${selectedRole.value}"角色，您的角色是"${currentUser.role}"`
    showAccessDenied.value = true
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

// 处理访问权限错误弹窗关闭
const handleAccessDeniedClose = () => {
  showAccessDenied.value = false
}

// 处理访问权限错误弹窗确认
const handleAccessDeniedConfirm = () => {
  showAccessDenied.value = false
  // 可以在这里添加其他逻辑，比如跳转到帮助页面或联系管理员
  ElMessage.info('如需申请更多权限，请联系系统管理员')
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
  
  // 启动时间更新
  updateDateTime()
  setInterval(updateDateTime, 1000)
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');

.role-selection-container {
  width: 100%;
  height: 100vh;
  position: relative;
  overflow: hidden;
  font-family: 'Orbitron', monospace;
  color: #00ffff;
}

/* 科技背景 */
.tech-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
}
  
.main-background {
    position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url('/src/assets/image/背景.png');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}

.overlay-effects {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.light-beams {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(
    ellipse at center top,
    rgba(0, 255, 255, 0.1),
    rgba(0, 100, 255, 0.05),
    transparent 70%
  );
  animation: breathe 4s ease-in-out infinite;
}

.particles {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.particles::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: 
    radial-gradient(2px 2px at 20px 30px, rgba(0, 255, 255, 0.5), transparent),
    radial-gradient(2px 2px at 40px 70px, rgba(255, 255, 255, 0.3), transparent),
    radial-gradient(1px 1px at 190px 40px, rgba(0, 255, 255, 0.4), transparent),
    radial-gradient(1px 1px at 90px 40px, rgba(255, 255, 255, 0.2), transparent);
  background-repeat: repeat;
  background-size: 250px 250px;
  animation: sparkle 20s linear infinite;
}

.grid-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: 
    linear-gradient(rgba(0, 255, 255, 0.1) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0, 255, 255, 0.1) 1px, transparent 1px);
  background-size: 50px 50px;
  opacity: 0.3;
  animation: gridMove 30s linear infinite;
}

/* 顶部栏 - 炫酷科技样式 */
.top-bar {
  position: relative;
  z-index: 100;
  height: 80px;
  overflow: hidden;
}

.top-bar-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    135deg,
    rgba(0, 30, 60, 0.95) 0%,
    rgba(0, 60, 120, 0.98) 30%,
    rgba(0, 100, 200, 0.95) 50%,
    rgba(0, 60, 120, 0.98) 70%,
    rgba(0, 30, 60, 0.95) 100%
  );
  backdrop-filter: blur(15px);
  border-bottom: 3px solid rgba(0, 255, 255, 0.4);
  box-shadow: 
    0 5px 30px rgba(0, 255, 255, 0.3),
    inset 0 2px 0 rgba(255, 255, 255, 0.1),
    inset 0 -2px 0 rgba(0, 255, 255, 0.2);
}

.top-bar-glow {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    rgba(0, 255, 255, 0.1),
    rgba(0, 255, 255, 0.3),
    rgba(0, 255, 255, 0.1)
  );
  animation: topBarGlow 4s ease-in-out infinite alternate;
}

.top-bar-lines {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.line {
  position: absolute;
  top: 50%;
      width: 200px;
  height: 2px;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(0, 255, 255, 0.8),
    transparent
  );
  animation: linePulse 3s ease-in-out infinite;
}

.line-left {
  left: 50px;
  transform: translateY(-50%) rotate(-15deg);
  animation-delay: 0s;
}

.line-right {
  right: 50px;
  transform: translateY(-50%) rotate(15deg);
  animation-delay: 1.5s;
}

.top-bar-particles {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: 
    radial-gradient(1px 1px at 10% 20%, rgba(0, 255, 255, 0.6), transparent),
    radial-gradient(1px 1px at 90% 80%, rgba(255, 255, 255, 0.4), transparent),
    radial-gradient(1px 1px at 70% 30%, rgba(0, 255, 255, 0.5), transparent);
  background-size: 100px 100px;
  animation: particlesMove 20s linear infinite;
}

.top-bar-content {
  position: relative;
  z-index: 2;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 40px;
  height: 100%;
}

.datetime {
  position: relative;
  display: flex;
  align-items: center;
}

.datetime-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 120px;
  height: 40px;
  background: radial-gradient(
    ellipse,
    rgba(0, 255, 255, 0.3),
    transparent 70%
  );
  filter: blur(8px);
  animation: dateTimeGlow 2s ease-in-out infinite alternate;
}

.datetime-text {
  position: relative;
  z-index: 2;
  font-size: 18px;
  font-weight: 700;
  color: #00ffff;
  text-shadow: 0 0 15px rgba(0, 255, 255, 0.8);
  letter-spacing: 1px;
}

.system-title {
  position: relative;
  text-align: center;
  flex: 1;
  margin: 0 40px;
}

.title-glow-bg {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 600px;
  height: 60px;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(0, 255, 255, 0.2),
    rgba(0, 150, 255, 0.3),
    rgba(0, 255, 255, 0.2),
    transparent
  );
  filter: blur(15px);
  animation: titleBgPulse 3s ease-in-out infinite alternate;
}

.title-text {
  position: relative;
  z-index: 2;
  font-size: 32px;
  font-weight: 900;
  color: #ffffff;
  text-shadow: 
    0 0 25px rgba(0, 255, 255, 1),
    0 0 50px rgba(0, 255, 255, 0.6),
    0 0 75px rgba(0, 255, 255, 0.3);
  letter-spacing: 3px;
  animation: titleTextGlow 4s ease-in-out infinite alternate;
}

.title-decorations {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 100%;
  height: 100%;
}

.deco-left, .deco-right {
  position: absolute;
  top: 50%;
  width: 80px;
  height: 2px;
  background: linear-gradient(
    90deg,
    rgba(0, 255, 255, 0.8),
    transparent
  );
}

.deco-left {
  left: -100px;
  transform: translateY(-50%);
  animation: decoSlideLeft 2s ease-in-out infinite alternate;
}

.deco-right {
  right: -100px;
  transform: translateY(-50%) rotate(180deg);
  animation: decoSlideRight 2s ease-in-out infinite alternate;
}

.admin-info {
  position: relative;
}

.admin-container {
  display: flex;
  align-items: center;
  gap: 15px;
}

.admin-icon-wrapper {
  position: relative;
  width: 45px;
  height: 45px;
  border-radius: 50%;
  background: radial-gradient(
    circle,
    rgba(0, 255, 255, 0.3),
    rgba(0, 100, 200, 0.2),
    transparent
  );
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid rgba(0, 255, 255, 0.4);
  backdrop-filter: blur(5px);
}

.icon-glow-ring {
  position: absolute;
  top: -3px;
  left: -3px;
  right: -3px;
  bottom: -3px;
  border-radius: 50%;
  border: 2px solid rgba(0, 255, 255, 0.6);
  animation: iconRingPulse 2s ease-in-out infinite;
}

.admin-icon {
  font-size: 22px;
  color: #00ffff;
  text-shadow: 0 0 10px rgba(0, 255, 255, 0.8);
}

.admin-text {
  font-size: 16px;
  font-weight: 600;
  color: #ffffff;
  text-shadow: 0 0 10px rgba(0, 255, 255, 0.4);
}

.admin-actions {
  display: flex;
  gap: 10px;
}

.action-btn {
  position: relative;
  width: 36px;
  height: 36px;
  border-radius: 6px;
  background: rgba(0, 255, 255, 0.1);
  border: 1px solid rgba(0, 255, 255, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(5px);
  overflow: hidden;
}

.btn-glow {
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  bottom: -2px;
  background: linear-gradient(
    45deg,
    rgba(0, 255, 255, 0.4),
    rgba(0, 150, 255, 0.6),
    rgba(0, 255, 255, 0.4)
  );
  border-radius: 8px;
    opacity: 0;
  transition: opacity 0.3s ease;
  filter: blur(4px);
}

.action-btn span {
  position: relative;
  z-index: 2;
  font-size: 16px;
}

.action-btn:hover {
  background: rgba(0, 255, 255, 0.2);
  border-color: rgba(0, 255, 255, 0.6);
  box-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
  transform: scale(1.1);
}

.action-btn:hover .btn-glow {
    opacity: 1;
}

/* 退出登录按钮特殊样式 */
.logout-btn {
  background: rgba(255, 100, 100, 0.1) !important;
  border-color: rgba(255, 100, 100, 0.3) !important;
}

.logout-btn .btn-glow {
  background: linear-gradient(
    45deg,
    rgba(255, 100, 100, 0.4),
    rgba(255, 150, 100, 0.6),
    rgba(255, 100, 100, 0.4)
  ) !important;
}

.logout-btn:hover {
  background: rgba(255, 100, 100, 0.2) !important;
  border-color: rgba(255, 100, 100, 0.6) !important;
  box-shadow: 0 0 20px rgba(255, 100, 100, 0.5) !important;
}

/* 底部平台 */
.platform-base {
  position: absolute;
  bottom: 200px;
  left: 50%;
  transform: translateX(-50%);
  width: 1600px;
  height: 200px;
  z-index: 1;
  perspective: 800px;
}

.platform-surface {
  position: relative;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: flex-end;
      justify-content: center;
}

.platform-background {
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 100%;
  height: auto;
  max-height: 100%;
  object-fit: contain;
  filter: drop-shadow(0 0 20px rgba(0, 255, 255, 0.3));
  opacity: 0.8;
  z-index: 1;
}

.platform-glow {
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 80%;
  height: 20px;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(0, 255, 255, 0.3),
    rgba(0, 150, 255, 0.4),
    rgba(0, 255, 255, 0.3),
    transparent
  );
  filter: blur(10px);
  animation: platformGlow 3s ease-in-out infinite alternate;
}

.platform-reflections {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    180deg,
    transparent 70%,
    rgba(0, 255, 255, 0.1) 85%,
    rgba(0, 255, 255, 0.2) 100%
  );
  pointer-events: none;
}

/* 角色选择区域 - 放在平台上 */
.roles-section {
  position: absolute;
  bottom: 320px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 50;
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  max-width: 1600px;
}

.selection-indicator {
  position: absolute;
  top: -30px;
  left: 0;
  width: 100%;
  height: 20px;
  pointer-events: none;
}

.selection-dot {
  position: absolute;
  top: 0;
  width: 10px;
  height: 10px;
  background: #00ffff;
  border-radius: 50%;
  box-shadow: 
    0 0 10px rgba(0, 255, 255, 0.8),
    0 0 20px rgba(0, 255, 255, 0.6),
    0 0 30px rgba(0, 255, 255, 0.4);
  display: none;
}

.roles-grid {
  display: flex;
  /* 📏 修改卡片间距 */
  gap: 40px;      /* 卡片之间的间距 - 调整此值改变卡片间距 */
  justify-content: center;
  align-items: flex-end;
  flex-wrap: nowrap;
  max-width: 1800px;
  perspective: 1200px;
}

/* 角色卡片 */
.role-card {
  position: relative;
  /* 📦 修改卡片大小 - 主要尺寸设置 */
  width: 280px;   /* 卡片宽度 - 调整此值改变卡片宽度 */
  height: 340px;  /* 卡片高度 - 调整此值改变卡片高度 */
  cursor: pointer;
  transform-style: preserve-3d;
  transition: all 0.5s cubic-bezier(0.23, 1, 0.32, 1);
}

.role-card:hover {
  transform: translateY(-15px) scale(1.08);
}

.role-card.selected {
  transform: translateY(-20px) scale(1.1);
}

.card-glow {
  position: absolute;
  top: -5px;
  left: -5px;
  right: -5px;
  bottom: -5px;
  background: linear-gradient(
    45deg,
    rgba(0, 255, 255, 0.2),
    rgba(0, 150, 255, 0.3),
    rgba(0, 255, 255, 0.2)
  );
  border-radius: 12px;
  opacity: 0;
  transition: all 0.5s ease;
  filter: blur(8px);
}

.card-glow.active {
  opacity: 1;
  animation: cardPulse 2s ease-in-out infinite;
}

.card-inner {
  position: relative;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    145deg,
    rgba(15, 30, 60, 0.9),
    rgba(30, 60, 120, 0.8),
    rgba(15, 30, 60, 0.9)
  );
  border-radius: 8px;
  border: 2px solid rgba(0, 255, 255, 0.3);
  backdrop-filter: blur(15px);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 20px;
  box-shadow: 
    0 10px 30px rgba(0, 0, 0, 0.5),
    inset 0 1px 0 rgba(255, 255, 255, 0.1),
    0 0 20px rgba(0, 255, 255, 0.1);
  transition: all 0.5s ease;
}

.role-card:hover .card-inner {
  border-color: rgba(0, 255, 255, 0.6);
  box-shadow: 
    0 20px 40px rgba(0, 0, 0, 0.6),
    inset 0 1px 0 rgba(255, 255, 255, 0.2),
    0 0 30px rgba(0, 255, 255, 0.3);
}

.role-card.selected .card-inner {
  border-color: rgba(0, 255, 255, 0.8);
  background: linear-gradient(
    145deg,
    rgba(20, 40, 80, 0.95),
    rgba(40, 80, 160, 0.9),
    rgba(20, 40, 80, 0.95)
  );
}

.role-3d-icon {
  position: relative;
  /* 🎯 修改图标容器大小 */
  width: 240px;   /* 图标容器宽度 - 调整此值改变图标区域大小 */
  height: 240px;  /* 图标容器高度 - 调整此值改变图标区域大小 */
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon-platform {
  position: relative;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  transform-style: preserve-3d;
}

  .tech-icon {
    /* 🖼️ 修改图标实际大小 */
    width: 240px;   /* 图标实际宽度 - 调整此值改变图标显示大小 */
    height: 240px;  /* 图标实际高度 - 调整此值改变图标显示大小 */
    object-fit: contain;
    filter: drop-shadow(0 0 20px rgba(0, 255, 255, 0.6));
    transition: all 0.5s ease;
    animation: iconFloat 3s ease-in-out infinite;
  }

.role-card:hover .tech-icon {
  filter: drop-shadow(0 0 30px rgba(0, 255, 255, 0.8));
  transform: scale(1.1);
}

.role-card.selected .tech-icon {
  filter: drop-shadow(0 0 40px rgba(0, 255, 255, 1));
  transform: scale(1.15);
}

.icon-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 260px;
  height: 260px;
  transform: translate(-50%, -50%);
  background: radial-gradient(
    circle,
    rgba(0, 255, 255, 0.2),
    rgba(0, 255, 255, 0.1),
    transparent 70%
  );
  border-radius: 50%;
  animation: iconGlow 2s ease-in-out infinite alternate;
}

.role-name {
  font-size: 20px;
  font-weight: 700;
  color: #ffffff;
  text-align: center;
  text-shadow: 0 0 15px rgba(0, 255, 255, 0.6);
  letter-spacing: 1px;
  transition: all 0.3s ease;
}

.role-card:hover .role-name {
  color: #00ffff;
  text-shadow: 0 0 20px rgba(0, 255, 255, 0.8);
}

.role-card.selected .role-name {
  color: #00ffff;
  text-shadow: 0 0 25px rgba(0, 255, 255, 1);
  animation: textGlow 1.5s ease-in-out infinite alternate;
}

.card-base {
  position: absolute;
  bottom: -12px;
  left: 10px;
  right: 10px;
  height: 8px;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(0, 255, 255, 0.4),
    rgba(0, 150, 255, 0.6),
    rgba(0, 255, 255, 0.4),
    transparent
  );
  border-radius: 4px;
  transform: perspective(100px) rotateX(45deg);
  box-shadow: 0 2px 10px rgba(0, 255, 255, 0.3);
  animation: cardBasePulse 3s ease-in-out infinite alternate;
}





/* 确认按钮 */
.action-section {
  position: absolute;
  bottom: 120px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 200;
}

.tech-confirm-button {
  position: relative;
  width: 200px;
  height: 60px;
  background: linear-gradient(
    145deg,
    rgba(0, 100, 200, 0.8),
    rgba(0, 150, 255, 0.9),
    rgba(0, 100, 200, 0.8)
  );
  border: 2px solid rgba(0, 255, 255, 0.6);
  border-radius: 8px;
  color: #ffffff;
  font-family: 'Orbitron', monospace;
  font-size: 16px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
  cursor: pointer;
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.23, 1, 0.32, 1);
  backdrop-filter: blur(10px);
}

.tech-confirm-button:hover {
  transform: translateY(-3px) scale(1.05);
  border-color: rgba(0, 255, 255, 1);
  box-shadow: 
    0 10px 30px rgba(0, 255, 255, 0.4),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

.tech-confirm-button:active {
  transform: translateY(-1px) scale(1.02);
}

.button-text {
  position: relative;
  z-index: 2;
  display: block;
  text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
}

.button-glow {
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  bottom: -2px;
  background: linear-gradient(
    45deg,
    rgba(0, 255, 255, 0.4),
    rgba(0, 150, 255, 0.6),
    rgba(0, 255, 255, 0.4)
  );
  border-radius: 10px;
  opacity: 0;
  transition: opacity 0.3s ease;
  filter: blur(8px);
  z-index: 1;
}

.tech-confirm-button:hover .button-glow {
  opacity: 1;
  animation: rotateGlow 2s linear infinite;
}

.button-particles {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 3;
}

.tech-confirm-button:hover .button-particles::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: 
    radial-gradient(1px 1px at 10% 20%, rgba(255, 255, 255, 0.8), transparent),
    radial-gradient(1px 1px at 80% 80%, rgba(0, 255, 255, 0.6), transparent),
    radial-gradient(1px 1px at 90% 10%, rgba(255, 255, 255, 0.4), transparent);
  background-size: 50px 50px;
  animation: sparkle 1.5s linear infinite;
}

/* 动画效果 */
@keyframes breathe {
  0%, 100% { opacity: 0.6; transform: scale(1); }
  50% { opacity: 1; transform: scale(1.05); }
}

@keyframes sparkle {
  0% { transform: translateY(0) rotate(0deg); }
  100% { transform: translateY(-100px) rotate(360deg); }
}

@keyframes gridMove {
  0% { transform: translate(0, 0); }
  100% { transform: translate(50px, 50px); }
}

/* 顶部栏动画 */
@keyframes topBarGlow {
  0% { opacity: 0.6; }
  100% { opacity: 1; }
}

@keyframes linePulse {
  0%, 100% { opacity: 0.3; transform: scaleX(0.5); }
  50% { opacity: 1; transform: scaleX(1); }
}

@keyframes particlesMove {
  0% { transform: translateX(0); }
  100% { transform: translateX(100px); }
}

@keyframes dateTimeGlow {
  0% { opacity: 0.6; }
  100% { opacity: 1; }
}

@keyframes titleBgPulse {
  0% { opacity: 0.6; transform: translate(-50%, -50%) scaleX(0.8); }
  100% { opacity: 1; transform: translate(-50%, -50%) scaleX(1); }
}

@keyframes titleTextGlow {
  0% { 
    text-shadow: 
      0 0 25px rgba(0, 255, 255, 1),
      0 0 50px rgba(0, 255, 255, 0.6),
      0 0 75px rgba(0, 255, 255, 0.3);
  }
  100% { 
    text-shadow: 
      0 0 35px rgba(0, 255, 255, 1),
      0 0 70px rgba(0, 255, 255, 0.8),
      0 0 100px rgba(0, 255, 255, 0.5);
  }
}

@keyframes decoSlideLeft {
  0% { transform: translateY(-50%) translateX(0); opacity: 0.6; }
  100% { transform: translateY(-50%) translateX(-20px); opacity: 1; }
}

@keyframes decoSlideRight {
  0% { transform: translateY(-50%) rotate(180deg) translateX(0); opacity: 0.6; }
  100% { transform: translateY(-50%) rotate(180deg) translateX(-20px); opacity: 1; }
}

@keyframes iconRingPulse {
  0%, 100% { opacity: 0.6; transform: scale(1); }
  50% { opacity: 1; transform: scale(1.1); }
}



@keyframes cardPulse {
  0%, 100% { opacity: 0.6; }
  50% { opacity: 1; }
}

@keyframes iconFloat {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  33% { transform: translateY(-5px) rotate(1deg); }
  66% { transform: translateY(3px) rotate(-1deg); }
}

@keyframes iconGlow {
  0% { opacity: 0.3; transform: translate(-50%, -50%) scale(1); }
  100% { opacity: 0.6; transform: translate(-50%, -50%) scale(1.1); }
}

@keyframes textGlow {
  0% { text-shadow: 0 0 25px rgba(0, 255, 255, 1); }
  100% { text-shadow: 0 0 35px rgba(0, 255, 255, 1), 0 0 50px rgba(0, 255, 255, 0.8); }
}



@keyframes platformGlow {
  0% { opacity: 0.6; }
  100% { opacity: 1; }
}

@keyframes rotateGlow {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@keyframes cardBasePulse {
  0% { 
    opacity: 0.6; 
    box-shadow: 0 2px 10px rgba(0, 255, 255, 0.3);
  }
  100% { 
    opacity: 1; 
    box-shadow: 0 4px 20px rgba(0, 255, 255, 0.6);
  }
}

/* 响应式设计 - 🔧 修改不同屏幕尺寸下的卡片和图标大小 */
@media (max-width: 1600px) {
  .roles-grid {
    gap: 30px;
    max-width: 1600px;
  }
  
  .role-card {
    /* 📦 1600px以下屏幕的卡片尺寸 */
    width: 260px;   /* 调整卡片宽度 */
    height: 320px;  /* 调整卡片高度 */
  }
  
      .tech-icon {
      /* 🖼️ 1600px以下屏幕的图标尺寸 */
      width: 220px;   /* 调整图标宽度 */
      height: 220px;  /* 调整图标高度 */
    }
  
  .role-3d-icon {
    /* 🎯 1600px以下屏幕的图标容器尺寸 */
    width: 220px;   /* 调整图标容器宽度 */
    height: 220px;  /* 调整图标容器高度 */
  }
  
  .icon-glow {
    width: 260px;
    height: 260px;
  }
  
  .platform-base {
    width: 1600px;
  }
}

@media (max-width: 1400px) {
  .roles-grid {
    gap: 25px;
    max-width: 1200px;
  }
  
  .role-card {
    /* 📦 1400px以下屏幕的卡片尺寸 */
    width: 220px;   /* 调整卡片宽度 */
    height: 280px;  /* 调整卡片高度 */
  }
  
  .tech-icon {
    /* 🖼️ 1400px以下屏幕的图标尺寸 */
    width: 180px;   /* 调整图标宽度 */
    height: 180px;  /* 调整图标高度 */
  }
  
  .role-3d-icon {
    /* 🎯 1400px以下屏幕的图标容器尺寸 */
    width: 180px;   /* 调整图标容器宽度 */
    height: 180px;  /* 调整图标容器高度 */
  }
  
  .platform-base {
    width: 1200px;
  }
}

@media (max-width: 1200px) {
  .roles-grid {
    flex-wrap: wrap;
    gap: 20px;
    max-width: 800px;
  }
  
  .role-card {
    /* 📦 1200px以下屏幕的卡片尺寸 */
    width: 200px;   /* 调整卡片宽度 */
    height: 260px;  /* 调整卡片高度 */
  }
  
  .tech-icon {
    /* 🖼️ 1200px以下屏幕的图标尺寸 */
    width: 140px;   /* 调整图标宽度 */
    height: 140px;  /* 调整图标高度 */
  }
  
  .role-3d-icon {
    /* 🎯 1200px以下屏幕的图标容器尺寸 */
    width: 160px;   /* 调整图标容器宽度 */
    height: 160px;  /* 调整图标容器高度 */
  }
  
  .platform-base {
    width: 1000px;
  }
}

@media (max-width: 768px) {
  .top-bar {
    padding: 15px 20px;
    flex-direction: column;
    gap: 10px;
  }
  
  .system-title {
    font-size: 20px;
  }
  
  .roles-grid {
    gap: 15px;
    max-width: 600px;
  }
  
  .role-card {
    /* 📦 768px以下屏幕(手机)的卡片尺寸 */
    width: 160px;   /* 调整卡片宽度 */
    height: 220px;  /* 调整卡片高度 */
  }
  
  .tech-icon {
    /* 🖼️ 768px以下屏幕(手机)的图标尺寸 */
    width: 120px;   /* 调整图标宽度 */
    height: 120px;  /* 调整图标高度 */
  }
  
  .role-3d-icon {
    /* 🎯 768px以下屏幕(手机)的图标容器尺寸 */
    width: 140px;   /* 调整图标容器宽度 */
    height: 140px;  /* 调整图标容器高度 */
    }
    
    .role-name {
    font-size: 16px;
    }
    
  .platform-base {
    width: 800px;
    }
  
  .tech-confirm-button {
    width: 160px;
    height: 50px;
    font-size: 14px;
  }
}
</style> 