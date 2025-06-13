<template>
  <div class="layout-container">
    <!-- 头部导航栏 -->
    <header class="layout-header">
      <div class="header-left">
        <h1 class="system-title">多智能体协作运维系统</h1>
      </div>
      <div class="header-right">
        <el-dropdown trigger="click" class="user-dropdown">
          <div class="user-info">
            <el-avatar :size="36" :src="userStore.user?.photo_data || ''" icon="User" />
            <span class="username">{{ userStore.user?.username || 'admin' }}</span>
            <el-icon class="dropdown-icon">
              <ArrowDown />
            </el-icon>
          </div>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item @click="goToProfile">
                <el-icon><User /></el-icon>
                个人资料
              </el-dropdown-item>
              <el-dropdown-item divided @click="handleLogout">
                <el-icon><SwitchButton /></el-icon>
                退出登录
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </header>

    <!-- 侧边栏 -->
    <aside class="layout-sidebar">
      <nav class="sidebar-nav">
        <div class="nav-item" :class="{ active: $route.path === '/dashboard' }" @click="$router.push('/dashboard')">
          <el-icon class="nav-icon"><HomeFilled /></el-icon>
          <span class="nav-text">系统仪表板</span>
        </div>
        
        <div 
          class="nav-item" 
          :class="{ active: $route.path === '/users' }" 
          @click="$router.push('/users')"
          v-if="userStore.isAdmin"
        >
          <el-icon class="nav-icon"><User /></el-icon>
          <span class="nav-text">用户管理</span>
        </div>
        
        <div class="nav-item" :class="{ active: $route.path === '/tasks' }" @click="$router.push('/tasks')">
          <el-icon class="nav-icon"><Tickets /></el-icon>
          <span class="nav-text">任务管理</span>
        </div>
        
        <div class="nav-item" :class="{ active: $route.path === '/devices' }" @click="$router.push('/devices')">
          <el-icon class="nav-icon"><Monitor /></el-icon>
          <span class="nav-text">设备管理</span>
        </div>
        
        <div class="nav-item" :class="{ active: $route.path === '/desktop' }" @click="$router.push('/desktop')">
          <el-icon class="nav-icon"><Monitor /></el-icon>
          <span class="nav-text">桌面管理</span>
        </div>
        
        <div 
          class="nav-item" 
          :class="{ active: $route.path === '/settings' }" 
          @click="$router.push('/settings')"
          v-if="userStore.isAdmin"
        >
          <el-icon class="nav-icon"><Setting /></el-icon>
          <span class="nav-text">系统设置</span>
        </div>
      </nav>
    </aside>

    <!-- 主内容区域 -->
    <main class="layout-main">
      <div class="main-content">
        <router-view />
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { 
  User, 
  SwitchButton, 
  ArrowDown, 
  HomeFilled, 
  Tickets, 
  Monitor, 
  Setting
} from '@element-plus/icons-vue'
import { useAuthStore } from '@/store/modules/auth'

const router = useRouter()
const userStore = useAuthStore()

const goToProfile = () => {
  router.push('/profile')
}

const handleLogout = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要退出登录吗？',
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    
    await userStore.logoutAction()
    ElMessage.success('已成功退出登录')
    router.push('/login')
  } catch (error) {
    // 用户取消了操作
  }
}
</script>

<style scoped lang="scss">
.layout-container {
  display: grid;
  grid-template-areas: 
    "header header"
    "sidebar main";
  grid-template-columns: 280px 1fr;
  grid-template-rows: 64px 1fr;
  height: 100vh;
  width: 100vw;
  background: #f5f7fa;
}

.layout-header {
  grid-area: header;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 32px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  z-index: 1000;
}

.header-left {
  .system-title {
    color: white;
    font-size: 22px;
    font-weight: 700;
    margin: 0;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  }
}

.header-right {
  .user-dropdown {
    .user-info {
      display: flex;
      align-items: center;
      gap: 12px;
      cursor: pointer;
      padding: 8px 16px;
      border-radius: 8px;
      transition: all 0.3s ease;
      background: rgba(255, 255, 255, 0.1);
      
      &:hover {
        background: rgba(255, 255, 255, 0.2);
        transform: translateY(-1px);
      }
    }

    .username {
      font-size: 15px;
      color: white;
      font-weight: 500;
    }

    .dropdown-icon {
      color: white;
      font-size: 14px;
    }
  }
}

.layout-sidebar {
  grid-area: sidebar;
  background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%);
  overflow-y: auto;
  box-shadow: 2px 0 12px rgba(0, 0, 0, 0.1);
}

.sidebar-nav {
  padding: 24px 0;
  
  .nav-item {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 16px 24px;
    margin: 4px 12px;
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    color: #bdc3c7;
    position: relative;
    
    &:hover {
      background: rgba(52, 152, 219, 0.1);
      color: #3498db;
      transform: translateX(4px);
    }
    
    &.active {
      background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
      color: white;
      box-shadow: 0 4px 12px rgba(52, 152, 219, 0.3);
      
      &::before {
        content: '';
        position: absolute;
        left: -12px;
        top: 50%;
        transform: translateY(-50%);
        width: 4px;
        height: 24px;
        background: #3498db;
        border-radius: 2px;
      }
    }
    
    .nav-icon {
      font-size: 20px;
      min-width: 20px;
    }
    
    .nav-text {
      font-size: 15px;
      font-weight: 500;
      white-space: nowrap;
    }
  }
}

.layout-main {
  grid-area: main;
  overflow-y: auto;
  background: #f8fafc;
}

.main-content {
  padding: 32px;
  min-height: 100%;
  max-width: 1600px;
  margin: 0 auto;
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .layout-container {
    grid-template-areas: 
      "header"
      "main";
    grid-template-columns: 1fr;
    grid-template-rows: 64px 1fr;
  }
  
  .layout-sidebar {
    display: none;
  }
}

@media (max-width: 768px) {
  .header-left .system-title {
    font-size: 18px;
  }
  
  .main-content {
    padding: 20px;
  }
}
</style> 