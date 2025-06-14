<template>
  <div class="login-container">
    <!-- 动态背景 -->
    <div class="background-overlay">
      <!-- 渐变网格 -->
      <div class="gradient-grid"></div>
      
      <!-- 浮动粒子 -->
      <div class="particles">
        <div class="particle" v-for="i in 15" :key="i" :style="getParticleStyle(i)"></div>
      </div>
      
      <!-- 光效 -->
      <div class="light-effects">
        <div class="light light-1"></div>
        <div class="light light-2"></div>
        <div class="light light-3"></div>
      </div>
    </div>
    
    <!-- 主要内容区域 -->
    <div class="main-content">
      <!-- 左侧欢迎区域 -->
      <div class="welcome-section">
        <div class="welcome-content">
          <div class="brand-section">
            <div class="brand-icon">
              <el-icon size="60"><Monitor /></el-icon>
            </div>
            <h1 class="brand-title">多智能体协作运维系统</h1>
            <p class="brand-subtitle">Multi-Agent Operations Platform</p>
          </div>
          
          <div class="features-grid">
            <div class="feature-item" v-for="(feature, index) in features" :key="index">
              <el-icon :size="24">
                <component :is="feature.icon" />
              </el-icon>
              <span>{{ feature.text }}</span>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 右侧登录区域 -->
      <div class="login-section">
        <div class="login-card">
          <!-- 卡片头部 -->
          <div class="card-header">
            <h2 class="login-title">欢迎回来</h2>
            <p class="login-subtitle">请选择您的身份并登录系统</p>
          </div>
          
          <!-- 登录表单 -->
          <div class="card-body">
            <el-form
              ref="loginFormRef"
              :model="loginForm"
              :rules="loginRules"
              class="login-form"
              @submit.prevent="handleLogin"
            >
              <!-- 登录类型选择 -->
              <div class="form-section">
                <h3 class="section-title">选择您的身份</h3>
                <el-form-item prop="loginType">
                  <div class="role-selector-wrapper">
                    <!-- 背景滑块 -->
                    <div class="selector-background">
                      <div 
                        class="active-indicator"
                        :class="{ 'move-right': loginForm.loginType === '操作员' }"
                      ></div>
                    </div>
                    
                    <!-- 角色选项 -->
                    <div class="role-tabs">
                      <div 
                        v-for="(role, index) in roles" 
                        :key="role.value"
                        class="role-tab"
                        :class="{ 
                          active: loginForm.loginType === role.value,
                          'tab-left': index === 0,
                          'tab-right': index === 1
                        }"
                        @click="selectRole(role.value)"
                      >
                        <div class="tab-content">
                          <div class="tab-icon">
                            <div class="icon-wrapper">
                              <el-icon :size="24">
                                <component :is="role.icon" />
                              </el-icon>
                            </div>
                            <div class="icon-glow"></div>
                          </div>
                          <div class="tab-text">
                            <h4>{{ role.title }}</h4>
                            <p>{{ role.subtitle }}</p>
                          </div>
                        </div>
                      </div>
                    </div>
                    
                    <!-- 角色详情卡片 -->
                    <div class="role-details">
                      <transition name="role-fade" mode="out-in">
                        <div 
                          :key="loginForm.loginType"
                          class="role-detail-card"
                        >
                          <div class="detail-header">
                            <div class="detail-icon">
                              <el-icon :size="20">
                                <component :is="currentRole.icon" />
                              </el-icon>
                            </div>
                            <h5>{{ currentRole.title }}</h5>
                          </div>
                          <p class="detail-description">{{ currentRole.description }}</p>
                          <div class="permissions-list">
                            <div 
                              v-for="permission in currentRole.permissions" 
                              :key="permission"
                              class="permission-item"
                            >
                              <el-icon size="14"><Check /></el-icon>
                              <span>{{ permission }}</span>
                            </div>
                          </div>
                        </div>
                      </transition>
                    </div>
                  </div>
                </el-form-item>
              </div>

              <!-- 用户名输入 -->
              <div class="form-section">
                <h3 class="section-title">账户信息</h3>
                <el-form-item prop="username">
                  <div class="input-wrapper">
                    <el-input
                      v-model="loginForm.username"
                      placeholder="请输入您的用户名"
                      size="large"
                      class="custom-input"
                      clearable
                      @keyup.enter="handleLogin"
                    >
                      <template #prefix>
                        <el-icon class="input-icon"><User /></el-icon>
                      </template>
                    </el-input>
                  </div>
                </el-form-item>
                
                <!-- 密码输入 -->
                <el-form-item prop="password">
                  <div class="input-wrapper">
                    <el-input
                      v-model="loginForm.password"
                      type="password"
                      placeholder="请输入您的密码"
                      size="large"
                      class="custom-input"
                      show-password
                      clearable
                      @keyup.enter="handleLogin"
                    >
                      <template #prefix>
                        <el-icon class="input-icon"><Lock /></el-icon>
                      </template>
                    </el-input>
                  </div>
                </el-form-item>
              </div>
              
              <!-- 登录按钮 -->
              <el-form-item class="login-button-section">
                <el-button
                  type="primary"
                  size="large"
                  :loading="loading"
                  class="login-button"
                  @click="handleLogin"
                >
                  <span v-if="!loading">
                    <el-icon><Right /></el-icon>
                    登录系统
                  </span>
                  <span v-else>
                    <el-icon class="is-loading"><Loading /></el-icon>
                    登录中...
                  </span>
                </el-button>
              </el-form-item>
            </el-form>
          </div>
          
          <!-- 演示信息 -->
          <div class="card-footer">
            <div class="demo-banner">
              <el-icon><InfoFilled /></el-icon>
              <div class="demo-text">
                <h4>演示账户</h4>
                <div class="demo-accounts">
                  <span class="account-tag">admin / 123456</span>
                  <span class="account-tag">operator / 123456</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'
import { 
  Monitor, User, UserFilled, Lock, Right, Check, InfoFilled, Loading,
  Setting, DataAnalysis, Connection 
} from '@element-plus/icons-vue'
import { useAuthStore } from '@/store/modules/auth'
import type { LoginForm } from '@/types/user'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

// 表单引用
const loginFormRef = ref<FormInstance>()

// 登录表单数据
const loginForm = reactive<LoginForm>({
  username: '',
  password: '',
  loginType: '管理员'
})

// 角色选项
const roles = [
  {
    value: '管理员',
    title: '系统管理员',
    subtitle: '全权管理',
    description: '拥有系统全部权限，可以管理用户、配置系统设置',
    icon: UserFilled,
    permissions: ['用户管理', '系统设置', '设备管理', '任务调度']
  },
  {
    value: '操作员',
    title: '系统操作员',
    subtitle: '日常运维',
    description: '负责日常运维操作，执行监控和维护任务',
    icon: User,
    permissions: ['设备监控', '任务执行', '数据查看', '报告生成']
  }
]

// 功能特性
const features = [
  { icon: DataAnalysis, text: '智能数据分析' },
  { icon: Lock, text: '安全权限管理' },
  { icon: Connection, text: '多设备协同' },
  { icon: Setting, text: '灵活配置管理' }
]

// 表单验证规则
const loginRules: FormRules = {
  loginType: [
    { required: true, message: '请选择登录类型', trigger: 'change' }
  ],
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 2, max: 50, message: '用户名长度应在2-50个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 50, message: '密码长度应在6-50个字符', trigger: 'blur' }
  ]
}

// 加载状态
const loading = ref(false)

// 粒子样式
const getParticleStyle = (index: number) => {
  const size = Math.random() * 6 + 2
  const left = Math.random() * 100
  const animationDelay = Math.random() * 20
  const animationDuration = Math.random() * 10 + 15
  
  return {
    width: `${size}px`,
    height: `${size}px`,
    left: `${left}%`,
    animationDelay: `${animationDelay}s`,
    animationDuration: `${animationDuration}s`
  }
}

// 选择角色
const selectRole = (roleValue: string) => {
  loginForm.loginType = roleValue
}

// 当前选中的角色
const currentRole = computed(() => {
  return roles.find(role => role.value === loginForm.loginType) || roles[0]
})

// 处理登录
const handleLogin = async () => {
  if (!loginFormRef.value) return
  
  try {
    await loginFormRef.value.validate()
    loading.value = true
    
    const loginResponse = await authStore.loginAction(loginForm)
    const user = loginResponse.user
    
    // 验证用户类型是否匹配
    if (user.type !== loginForm.loginType) {
      ElMessage.error(`您的账户类型是"${user.type}"，请选择正确的登录类型`)
      return
    }
    
    ElMessage.success('登录成功！')
    
    // 根据用户类型进行不同的跳转
    if (user.type === '管理员') {
      // 管理员直接进入主页面
      const redirect = route.query.redirect as string
      router.push(redirect || '/dashboard')
    } else if (user.type === '操作员') {
      // 操作员进入角色选择界面
      router.push('/role-selection')
    }
    
  } catch (error: any) {
    console.error('登录失败:', error)
    ElMessage.error(error.response?.data?.detail || '登录失败，请检查用户名和密码')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped lang="scss">
// 全局容器
.login-container {
  position: relative;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

// 背景层
.background-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, 
    #667eea 0%, 
    #764ba2 25%, 
    #f093fb 50%, 
    #f5576c 75%, 
    #4facfe 100%);
  background-size: 400% 400%;
  animation: gradientShift 15s ease infinite;
}

@keyframes gradientShift {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

// 渐变网格
.gradient-grid {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: 
    linear-gradient(rgba(255,255,255,0.1) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.1) 1px, transparent 1px);
  background-size: 50px 50px;
  animation: gridMove 20s linear infinite;
}

@keyframes gridMove {
  0% { transform: translate(0, 0); }
  100% { transform: translate(50px, 50px); }
}

// 浮动粒子
.particles {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  
  .particle {
    position: absolute;
    background: rgba(255, 255, 255, 0.6);
    border-radius: 50%;
    animation: particleFloat linear infinite;
  }
}

@keyframes particleFloat {
  0% {
    transform: translateY(100vh) rotate(0deg);
    opacity: 0;
  }
  10% {
    opacity: 1;
  }
  90% {
    opacity: 1;
  }
  100% {
    transform: translateY(-100px) rotate(360deg);
    opacity: 0;
  }
}

// 光效
.light-effects {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  
  .light {
    position: absolute;
    border-radius: 50%;
    filter: blur(40px);
    animation: lightPulse 4s ease-in-out infinite alternate;
    
    &.light-1 {
      width: 300px;
      height: 300px;
      background: rgba(102, 126, 234, 0.3);
      top: 20%;
      left: 10%;
      animation-delay: 0s;
    }
    
    &.light-2 {
      width: 400px;
      height: 400px;
      background: rgba(245, 87, 108, 0.2);
      top: 50%;
      right: 15%;
      animation-delay: 1.5s;
    }
    
    &.light-3 {
      width: 250px;
      height: 250px;
      background: rgba(79, 172, 254, 0.25);
      bottom: 20%;
      left: 20%;
      animation-delay: 3s;
    }
  }
}

@keyframes lightPulse {
  0% { transform: scale(1) rotate(0deg); opacity: 0.3; }
  100% { transform: scale(1.2) rotate(180deg); opacity: 0.6; }
}

// 主要内容区域
.main-content {
  position: relative;
  z-index: 10;
  display: grid;
  grid-template-columns: 1fr 480px;
  width: 100%;
  height: 100vh;
}

// 左侧欢迎区域
.welcome-section {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 60px;
  
  .welcome-content {
    max-width: 500px;
    color: white;
    text-align: center;
    
    .brand-section {
      margin-bottom: 60px;
      
      .brand-icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 100px;
        height: 100px;
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 24px;
        margin-bottom: 32px;
        animation: iconFloat 3s ease-in-out infinite;
      }
      
      .brand-title {
        font-size: 40px;
        font-weight: 800;
        margin: 0 0 16px 0;
        background: linear-gradient(135deg, #ffffff 0%, rgba(255,255,255,0.8) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 4px 8px rgba(0,0,0,0.1);
      }
      
      .brand-subtitle {
        font-size: 18px;
        color: rgba(255, 255, 255, 0.8);
        margin: 0;
        font-weight: 400;
        letter-spacing: 1px;
      }
    }
    
    .features-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 24px;
      
      .feature-item {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 20px;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 16px;
        transition: all 0.3s ease;
        
        &:hover {
          transform: translateY(-4px);
          background: rgba(255, 255, 255, 0.15);
          box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        }
        
        .el-icon {
          color: rgba(255, 255, 255, 0.9);
        }
        
        span {
          font-size: 14px;
          font-weight: 500;
          color: rgba(255, 255, 255, 0.9);
        }
      }
    }
  }
}

@keyframes iconFloat {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-10px); }
}

// 右侧登录区域
.login-section {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  border-left: 1px solid rgba(255, 255, 255, 0.1);
}

.login-card {
  width: 100%;
  max-width: 400px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(40px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 24px;
  box-shadow: 
    0 32px 64px rgba(0, 0, 0, 0.1),
    0 0 0 1px rgba(255, 255, 255, 0.05);
  overflow: hidden;
  animation: cardSlideIn 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

@keyframes cardSlideIn {
  0% {
    opacity: 0;
    transform: translateX(40px) scale(0.95);
  }
  100% {
    opacity: 1;
    transform: translateX(0) scale(1);
  }
}

.card-header {
  padding: 40px 32px 32px;
  text-align: center;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  
  .login-title {
    font-size: 28px;
    font-weight: 700;
    color: #1a202c;
    margin: 0 0 8px 0;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }
  
  .login-subtitle {
    font-size: 15px;
    color: #64748b;
    margin: 0;
    font-weight: 400;
  }
}

.card-body {
  padding: 32px;
}

// 表单样式
.login-form {
  .form-section {
    margin-bottom: 32px;
    
    .section-title {
      font-size: 16px;
      font-weight: 600;
      color: #374151;
      margin: 0 0 20px 0;
      display: flex;
      align-items: center;
      gap: 8px;
      
      &::before {
        content: '';
        width: 4px;
        height: 16px;
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 2px;
      }
    }
  }
  
  // 角色选择器
  .role-selector-wrapper {
    position: relative;
    
    // 背景滑块
    .selector-background {
      position: relative;
      height: 60px;
      background: rgba(248, 250, 252, 0.8);
      border-radius: 16px;
      border: 2px solid #e5e7eb;
      margin-bottom: 20px;
      overflow: hidden;
      
      .active-indicator {
        position: absolute;
        top: 4px;
        left: 4px;
        width: calc(50% - 4px);
        height: calc(100% - 8px);
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 
          0 4px 12px rgba(102, 126, 234, 0.3),
          0 2px 4px rgba(102, 126, 234, 0.2);
        
        &::before {
          content: '';
          position: absolute;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          background: linear-gradient(135deg, rgba(255,255,255,0.2) 0%, transparent 100%);
          border-radius: 12px;
        }
        
        &.move-right {
          transform: translateX(100%);
        }
      }
    }
    
    // 角色标签页
    .role-tabs {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 60px;
      display: flex;
      z-index: 2;
      
      .role-tab {
        flex: 1;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.3s ease;
        
        &.active {
          .tab-content {
            .tab-icon {
              .icon-wrapper {
                color: white;
                transform: scale(1.1);
              }
              
              .icon-glow {
                opacity: 1;
                animation: iconPulse 2s ease-in-out infinite;
              }
            }
            
            .tab-text {
              h4 {
                color: white;
                font-weight: 700;
              }
              
              p {
                color: rgba(255, 255, 255, 0.9);
              }
            }
          }
        }
        
        .tab-content {
          display: flex;
          align-items: center;
          gap: 10px;
          padding: 8px 12px;
          
          .tab-icon {
            position: relative;
            
            .icon-wrapper {
              display: flex;
              align-items: center;
              justify-content: center;
              color: #667eea;
              transition: all 0.3s ease;
            }
            
            .icon-glow {
              position: absolute;
              top: 50%;
              left: 50%;
              width: 40px;
              height: 40px;
              background: radial-gradient(circle, rgba(255,255,255,0.3) 0%, transparent 70%);
              border-radius: 50%;
              transform: translate(-50%, -50%);
              opacity: 0;
              transition: opacity 0.3s ease;
            }
          }
          
          .tab-text {
            h4 {
              font-size: 14px;
              font-weight: 600;
              color: #6b7280;
              margin: 0;
              transition: all 0.3s ease;
            }
            
            p {
              font-size: 12px;
              color: #9ca3af;
              margin: 0;
              transition: all 0.3s ease;
            }
          }
        }
      }
    }
    
    // 角色详情卡片
    .role-details {
      margin-top: 20px;
      
      .role-detail-card {
        padding: 24px;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.02), rgba(118, 75, 162, 0.02));
        border: 1px solid rgba(102, 126, 234, 0.1);
        border-radius: 16px;
        position: relative;
        overflow: hidden;
        
        &::before {
          content: '';
          position: absolute;
          top: 0;
          left: 0;
          width: 100%;
          height: 2px;
          background: linear-gradient(90deg, #667eea, #764ba2);
        }
        
        .detail-header {
          display: flex;
          align-items: center;
          gap: 12px;
          margin-bottom: 16px;
          
          .detail-icon {
            width: 36px;
            height: 36px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, #667eea, #764ba2);
            border-radius: 10px;
            color: white;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
          }
          
          h5 {
            font-size: 16px;
            font-weight: 600;
            color: #374151;
            margin: 0;
          }
        }
        
        .detail-description {
          font-size: 14px;
          color: #6b7280;
          line-height: 1.5;
          margin: 0 0 20px 0;
        }
        
        .permissions-list {
          display: grid;
          grid-template-columns: repeat(2, 1fr);
          gap: 12px;
          
          .permission-item {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 8px 12px;
            background: rgba(16, 185, 129, 0.05);
            border: 1px solid rgba(16, 185, 129, 0.1);
            border-radius: 8px;
            font-size: 13px;
            color: #374151;
            transition: all 0.3s ease;
            
            &:hover {
              background: rgba(16, 185, 129, 0.1);
              transform: translateY(-1px);
            }
            
            .el-icon {
              color: #10b981;
            }
          }
        }
      }
    }
  }
  
  @keyframes iconPulse {
    0%, 100% { 
      opacity: 0.6; 
      transform: translate(-50%, -50%) scale(1);
    }
    50% { 
      opacity: 1; 
      transform: translate(-50%, -50%) scale(1.2);
    }
  }
  
  // 角色切换动画
  .role-fade-enter-active,
  .role-fade-leave-active {
    transition: all 0.3s ease;
  }
  
  .role-fade-enter-from {
    opacity: 0;
    transform: translateY(10px);
  }
  
  .role-fade-leave-to {
    opacity: 0;
    transform: translateY(-10px);
  }
  
  // 输入框样式
  .input-wrapper {
    position: relative;
    
    .custom-input {
      :deep(.el-input__wrapper) {
        border-radius: 14px;
        border: 2px solid #e5e7eb;
        box-shadow: none;
        background: rgba(248, 250, 252, 0.8);
        backdrop-filter: blur(10px);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        padding: 4px 16px;
        
        &:hover {
          border-color: #c7d2fe;
          background: rgba(248, 250, 252, 0.95);
        }
        
        &.is-focus {
          border-color: #667eea;
          background: white;
          box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
          transform: translateY(-2px);
        }
      }
      
      :deep(.el-input__inner) {
        height: 50px;
        font-size: 15px;
        color: #374151;
        font-weight: 500;
        
        &::placeholder {
          color: #9ca3af;
        }
      }
      
      .input-icon {
        color: #667eea;
        font-size: 18px;
      }
    }
  }
  
  // 登录按钮
  .login-button-section {
    margin-top: 40px;
    margin-bottom: 0;
  }
  
  .login-button {
    width: 100%;
    height: 56px;
    font-size: 16px;
    font-weight: 600;
    border-radius: 14px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border: none;
    box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
    
    &::before {
      content: '';
      position: absolute;
      top: 0;
      left: -100%;
      width: 100%;
      height: 100%;
      background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
      transition: left 0.5s ease;
    }
    
    &:hover {
      transform: translateY(-3px);
      box-shadow: 0 8px 32px rgba(102, 126, 234, 0.4);
      
      &::before {
        left: 100%;
      }
    }
    
    &:active {
      transform: translateY(-1px);
    }
    
    .el-icon {
      margin-right: 8px;
      
      &.is-loading {
        animation: spin 1s linear infinite;
      }
    }
  }
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

// 卡片底部
.card-footer {
  padding: 24px 32px 32px;
  border-top: 1px solid rgba(0, 0, 0, 0.05);
  
  .demo-banner {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 20px;
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.05), rgba(147, 51, 234, 0.05));
    border: 1px solid rgba(59, 130, 246, 0.1);
    border-radius: 12px;
    
    .el-icon {
      color: #3b82f6;
      font-size: 20px;
      margin-top: 2px;
    }
    
    .demo-text {
      flex: 1;
      
      h4 {
        font-size: 14px;
        font-weight: 600;
        color: #374151;
        margin: 0 0 8px 0;
      }
      
      .demo-accounts {
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
        
        .account-tag {
          display: inline-block;
          padding: 4px 8px;
          background: rgba(59, 130, 246, 0.1);
          color: #3b82f6;
          font-size: 12px;
          font-weight: 500;
          border-radius: 6px;
          font-family: 'Monaco', 'Menlo', monospace;
        }
      }
    }
  }
}

// 响应式设计
@media (max-width: 1200px) {
  .main-content {
    grid-template-columns: 1fr 420px;
  }
  
  .welcome-section {
    padding: 40px;
    
    .welcome-content .brand-section .brand-title {
      font-size: 36px;
    }
  }
}

@media (max-width: 768px) {
  .main-content {
    grid-template-columns: 1fr;
  }
  
  .welcome-section {
    display: none;
  }
  
  .login-section {
    padding: 20px;
    background: none;
    border-left: none;
  }
  
  .login-card {
    border-radius: 20px;
  }
  
  .card-header, .card-body, .card-footer {
    padding-left: 24px;
    padding-right: 24px;
  }
  
  .role-selector .role-option {
    padding: 16px;
    
    .role-icon {
      width: 48px;
      height: 48px;
    }
  }
}

@media (max-width: 480px) {
  .login-section {
    padding: 16px;
  }
  
  .card-header {
    padding: 32px 20px 24px;
    
    .login-title {
      font-size: 24px;
    }
  }
  
  .card-body {
    padding: 24px 20px;
  }
  
  .card-footer {
    padding: 20px 20px 24px;
  }
  
  .demo-banner {
    flex-direction: column;
    text-align: center;
    
    .demo-accounts {
      justify-content: center;
    }
  }
}
</style> 