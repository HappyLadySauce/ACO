<template>
  <div class="login-container">
    <!-- 背景装饰 -->
    <div class="background-shapes">
      <div class="shape shape-1"></div>
      <div class="shape shape-2"></div>
      <div class="shape shape-3"></div>
    </div>
    
    <!-- 登录卡片 -->
    <div class="login-wrapper">
      <div class="login-card">
        <div class="card-header">
          <div class="logo-section">
            <div class="logo-icon">
              <el-icon size="48"><Monitor /></el-icon>
            </div>
            <h1 class="system-title">多智能体协作运维系统</h1>
            <p class="system-subtitle">Multi-Agent Operations Platform</p>
          </div>
        </div>
        
        <div class="card-body">
          <el-form
            ref="loginFormRef"
            :model="loginForm"
            :rules="loginRules"
            class="login-form"
            @submit.prevent="handleLogin"
          >
            <div class="form-group">
              <label class="form-label">登录类型</label>
              <el-form-item prop="loginType">
                <el-radio-group 
                  v-model="loginForm.loginType" 
                  class="login-type-group"
                  size="large"
                >
                  <el-radio label="管理员" class="login-type-option">
                    <div class="type-content">
                      <el-icon><UserFilled /></el-icon>
                      <span>管理员登录</span>
                    </div>
                  </el-radio>
                  <el-radio label="操作员" class="login-type-option">
                    <div class="type-content">
                      <el-icon><User /></el-icon>
                      <span>操作员登录</span>
                    </div>
                  </el-radio>
                </el-radio-group>
              </el-form-item>
            </div>

            <div class="form-group">
              <label class="form-label">用户名</label>
              <el-form-item prop="username">
                <el-input
                  v-model="loginForm.username"
                  placeholder="请输入用户名"
                  prefix-icon="User"
                  size="large"
                  class="form-input"
                  clearable
                  @keyup.enter="handleLogin"
                />
              </el-form-item>
            </div>
            
            <div class="form-group">
              <label class="form-label">密码</label>
              <el-form-item prop="password">
                <el-input
                  v-model="loginForm.password"
                  type="password"
                  placeholder="请输入密码"
                  prefix-icon="Lock"
                  size="large"
                  class="form-input"
                  show-password
                  clearable
                  @keyup.enter="handleLogin"
                />
              </el-form-item>
            </div>
            
            <el-form-item class="login-button-wrapper">
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
                <span v-else>登录中...</span>
              </el-button>
            </el-form-item>
          </el-form>
        </div>
        
        <div class="card-footer">
          <div class="demo-info">
            <div class="info-item">
              <el-icon><User /></el-icon>
              <span>默认账户：admin</span>
            </div>
            <div class="info-item">
              <el-icon><Lock /></el-icon>
              <span>默认密码：123456</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'
import { Monitor, User, UserFilled, Lock, Right } from '@element-plus/icons-vue'
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
.login-container {
  position: relative;
  width: 100vw;
  height: 100vh;
  display: grid;
  place-items: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  overflow: hidden;
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

.login-wrapper {
  position: relative;
  z-index: 10;
  width: 100%;
  max-width: 480px;
  padding: 20px;
}

.login-card {
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
  padding: 40px 40px 20px;
  text-align: center;
  
  .logo-section {
    .logo-icon {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 80px;
      height: 80px;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      border-radius: 20px;
      color: white;
      margin-bottom: 20px;
      box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);
    }
    
    .system-title {
      font-size: 28px;
      font-weight: 700;
      color: #1a202c;
      margin: 0 0 8px 0;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }
    
    .system-subtitle {
      font-size: 14px;
      color: #718096;
      margin: 0;
      font-weight: 500;
    }
  }
}

.card-body {
  padding: 20px 40px;
}

.login-form {
  .form-group {
    margin-bottom: 24px;
    
    .form-label {
      display: block;
      font-size: 14px;
      font-weight: 600;
      color: #374151;
      margin-bottom: 8px;
    }
    
    .el-form-item {
      margin-bottom: 0;
    }
  }
  
  .form-input {
    :deep(.el-input__wrapper) {
      border-radius: 12px;
      border: 2px solid #e5e7eb;
      box-shadow: none;
      transition: all 0.3s ease;
      
      &:hover {
        border-color: #d1d5db;
      }
      
      &.is-focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
      }
    }
    
    :deep(.el-input__inner) {
      height: 48px;
      font-size: 16px;
      color: #374151;
    }
  }
  
  .login-button-wrapper {
    margin-top: 32px;
    margin-bottom: 0;
  }
  
  .login-type-group {
    width: 100%;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    
    :deep(.el-radio) {
      margin-right: 0;
      width: 100%;
    }
    
    .login-type-option {
      width: 100%;
      
      :deep(.el-radio__input) {
        display: none;
      }
      
      :deep(.el-radio__label) {
        width: 100%;
        padding: 0;
      }
      
      .type-content {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 8px;
        padding: 16px 12px;
        border: 2px solid #e5e7eb;
        border-radius: 12px;
        background: white;
        cursor: pointer;
        transition: all 0.3s ease;
        
        .el-icon {
          font-size: 24px;
          color: #667eea;
        }
        
        span {
          font-size: 14px;
          font-weight: 500;
          color: #374151;
        }
      }
      
      &:hover .type-content {
        border-color: #d1d5db;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
      }
      
      :deep(.el-radio__input.is-checked) + .el-radio__label .type-content {
        border-color: #667eea;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        
        .el-icon {
          color: white;
        }
        
        span {
          color: white;
        }
      }
    }
  }

  .login-button {
    width: 100%;
    height: 52px;
    font-size: 16px;
    font-weight: 600;
    border-radius: 12px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border: none;
    transition: all 0.3s ease;
    
    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);
    }
    
    &:active {
      transform: translateY(0);
    }
    
    .el-icon {
      margin-right: 6px;
    }
  }
}

.card-footer {
  padding: 20px 40px 40px;
  
  .demo-info {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    
    .info-item {
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 12px 16px;
      background: #f8fafc;
      border-radius: 8px;
      font-size: 14px;
      color: #64748b;
      
      .el-icon {
        color: #667eea;
        font-size: 16px;
      }
    }
  }
}

/* 响应式设计 */
@media (max-width: 640px) {
  .login-wrapper {
    padding: 16px;
  }
  
  .login-card {
    border-radius: 16px;
  }
  
  .card-header {
    padding: 32px 24px 16px;
    
    .logo-section {
      .logo-icon {
        width: 64px;
        height: 64px;
      }
      
      .system-title {
        font-size: 24px;
      }
    }
  }
  
  .card-body {
    padding: 16px 24px;
  }
  
  .card-footer {
    padding: 16px 24px 32px;
    
    .demo-info {
      grid-template-columns: 1fr;
      gap: 12px;
    }
  }
  
  .background-shapes .shape {
    &.shape-1 {
      width: 200px;
      height: 200px;
    }
    
    &.shape-2 {
      width: 150px;
      height: 150px;
    }
    
    &.shape-3 {
      width: 100px;
      height: 100px;
    }
  }
}

@media (max-width: 480px) {
  .login-form {
    .form-input {
      :deep(.el-input__inner) {
        font-size: 14px;
      }
    }
    
    .login-button {
      height: 48px;
      font-size: 14px;
    }
  }
}
</style> 