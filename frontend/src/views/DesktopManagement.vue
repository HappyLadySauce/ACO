<template>
  <div class="desktop-management">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1 class="page-title">模板｜任务下发列表</h1>
    </div>

    <!-- 筛选条件栏 -->
    <div class="filter-bar">
      <div class="filter-group">
        <!-- 话题分组 -->
        <div class="filter-item">
          <span class="filter-label">话题分组：</span>
          <el-select v-model="selectedTopic" placeholder="全部分组" class="filter-select">
            <el-option label="全部分组" value="all"></el-option>
            <el-option label="办公应用" value="office"></el-option>
            <el-option label="开发工具" value="dev"></el-option>
          </el-select>
        </div>

        <!-- 最高管理 -->
        <div class="filter-item">
          <span class="filter-label">最高管理</span>
          <el-select v-model="selectedManagement" placeholder="选择管理" class="filter-select">
            <el-option label="管理员" value="admin"></el-option>
            <el-option label="普通用户" value="user"></el-option>
          </el-select>
        </div>

        <!-- 模板统计 -->
        <div class="filter-item">
          <span class="filter-label">11个模板：</span>
          <div class="image-stats">
            <span class="stat-item stat-blue">🔵 0个</span>
            <span class="stat-item stat-black">⚫ 11个</span>
            <span class="stat-item stat-red">🔴 0个</span>
          </div>
        </div>

        <!-- 模板分组 -->
        <div class="filter-item">
          <span class="filter-label">模板分组</span>
          <el-select v-model="selectedImageGroup" placeholder="选择分组" class="filter-select">
            <el-option label="Windows系统" value="windows"></el-option>
            <el-option label="Linux系统" value="linux"></el-option>
          </el-select>
        </div>

        <!-- 内置充值使模块 -->
        <div class="filter-item">
          <el-radio-group v-model="chargeModule" class="charge-module">
            <el-radio :label="true" size="small">内置充值使模块</el-radio>
          </el-radio-group>
        </div>

        <!-- 模板从属管理 -->
        <div class="filter-item">
          <span class="filter-label">模板从属管理</span>
          <el-select v-model="selectedSubordinate" placeholder="选择管理" class="filter-select">
            <el-option label="主管理" value="main"></el-option>
            <el-option label="从管理" value="sub"></el-option>
          </el-select>
        </div>
      </div>
    </div>

    <!-- 操作栏 -->
    <div class="operation-bar">
      <div class="left-operations">
        <!-- 时间筛选 -->
        <div class="time-filter">
          <span class="filter-label">按创建时间排序</span>
          <el-select v-model="timeSort" placeholder="全部" class="time-select">
            <el-option label="全部" value="all"></el-option>
            <el-option label="最新" value="newest"></el-option>
            <el-option label="最旧" value="oldest"></el-option>
          </el-select>
        </div>

        <!-- 搜索框 -->
        <div class="search-box">
          <el-input
            v-model="searchKeyword"
            placeholder="搜索"
            class="search-input"
            :prefix-icon="Search"
          />
        </div>
      </div>

      <div class="right-operations">
        <!-- 操作按钮 -->
        <el-button type="primary" :icon="Plus" class="action-btn">新增</el-button>
        <el-button type="primary" :icon="Edit" class="action-btn">编辑</el-button>
        <el-button type="danger" :icon="Delete" class="action-btn">关机</el-button>
        <el-button type="success" class="action-btn register-btn">📋 注册模板</el-button>
        <el-button type="danger" class="action-btn delete-btn">🗑️ 删除模板</el-button>
      </div>
    </div>

    <!-- 模板卡片网格 -->
    <div class="image-grid">
      <div v-for="(image, index) in imageList" :key="index" class="image-card">
        <!-- 卡片头部 -->
        <div class="card-header">
          <div class="card-title">
            <span class="title-icon">📱</span>
            <span class="title-text">{{ image.name }}</span>
            <span class="system-badge">{{ image.system }}</span>
          </div>
          <div class="card-actions">
            <el-button type="primary" size="small" :icon="Edit">编辑</el-button>
            <el-button type="info" size="small" :icon="DocumentCopy">复制</el-button>
            <el-button type="success" size="small" :icon="Download">下载</el-button>
            <el-button type="info" size="small" :icon="MoreFilled">更多</el-button>
          </div>
        </div>

        <!-- 卡片内容 -->
        <div class="card-content">
          <div class="content-row">
            <div class="content-left">
              <div class="info-item">
                <span class="info-label">系统盘：</span>
                <span class="info-value status-connected">{{ image.systemDisk }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">数据盘：</span>
                <span class="info-value">{{ image.dataDisk }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">关联桌面数：</span>
                <span class="info-value">{{ image.associatedDesktops }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">属主：</span>
                <span class="info-value">{{ image.owner }}</span>
              </div>
            </div>
            <div class="content-right">
              <div class="info-item">
                <span class="info-label">VOL上层...：</span>
                <span class="info-value">{{ image.volLayer }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">异构驱动信息：</span>
                <span class="info-value">{{ image.driverInfo }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">创建时间：</span>
                <span class="info-value">{{ image.createTime }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">更新时间：</span>
                <span class="info-value">{{ image.updateTime }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { Search, Plus, Edit, Delete, DocumentCopy, Download, MoreFilled } from '@element-plus/icons-vue'

// 筛选条件
const selectedTopic = ref('all')
const selectedManagement = ref('')
const selectedImageGroup = ref('')
const chargeModule = ref(true)
const selectedSubordinate = ref('')
const timeSort = ref('all')
const searchKeyword = ref('')

// 模板数据
const imageList = reactive([
  {
    name: '1506考试系统',
    system: 'windows10 64bit',
    systemDisk: '已连接',
    dataDisk: '192.168.255.255',
    associatedDesktops: '255.255.255.0',
    owner: '-- --',
    volLayer: '-- --',
    driverInfo: '-- --',
    createTime: '-- --',
    updateTime: '-- --'
  },
  {
    name: '1506考试系统',
    system: 'windows10 64bit',
    systemDisk: '已连接',
    dataDisk: '192.168.255.255',
    associatedDesktops: '255.255.255.0',
    owner: '-- --',
    volLayer: '-- --',
    driverInfo: '-- --',
    createTime: '-- --',
    updateTime: '-- --'
  },
  {
    name: '1506考试系统',
    system: 'windows10 64bit',
    systemDisk: '已连接',
    dataDisk: '192.168.255.255',
    associatedDesktops: '255.255.255.0',
    owner: '-- --',
    volLayer: '-- --',
    driverInfo: '-- --',
    createTime: '-- --',
    updateTime: '-- --'
  },
  {
    name: '1506考试系统',
    system: 'windows10 64bit',
    systemDisk: '已连接',
    dataDisk: '192.168.255.255',
    associatedDesktops: '255.255.255.0',
    owner: '-- --',
    volLayer: '-- --',
    driverInfo: '-- --',
    createTime: '-- --',
    updateTime: '-- --'
  }
])
</script>

<style scoped>
.desktop-management {
  padding: 20px;
  background: #f5f7fa;
  min-height: 100vh;
}

/* 页面标题 */
.page-header {
  margin-bottom: 20px;
}

.page-title {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin: 0;
}

/* 筛选条件栏 */
.filter-bar {
  background: white;
  padding: 16px 20px;
  border-radius: 8px;
  margin-bottom: 16px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.filter-group {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 24px;
}

.filter-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.filter-label {
  font-size: 14px;
  color: #666;
  white-space: nowrap;
}

.filter-select {
  width: 140px;
}

.image-stats {
  display: flex;
  gap: 12px;
}

.stat-item {
  font-size: 14px;
  padding: 2px 8px;
  border-radius: 4px;
}

.stat-blue {
  color: #1890ff;
}

.stat-black {
  color: #333;
}

.stat-red {
  color: #ff4d4f;
}

.charge-module {
  margin: 0;
}

/* 操作栏 */
.operation-bar {
  background: white;
  padding: 16px 20px;
  border-radius: 8px;
  margin-bottom: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.left-operations {
  display: flex;
  align-items: center;
  gap: 20px;
}

.time-filter {
  display: flex;
  align-items: center;
  gap: 8px;
}

.time-select {
  width: 100px;
}

.search-input {
  width: 300px;
}

.right-operations {
  display: flex;
  gap: 12px;
}

.action-btn {
  height: 36px;
}

.register-btn {
  background: #52c41a;
  border-color: #52c41a;
}

.delete-btn {
  background: #ff4d4f;
  border-color: #ff4d4f;
}

/* 模板卡片网格 */
.image-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.image-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: transform 0.2s, box-shadow 0.2s;
}

.image-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

/* 卡片头部 */
.card-header {
  padding: 16px 20px 12px;
  border-bottom: 1px solid #f0f0f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-title {
  display: flex;
  align-items: center;
  gap: 8px;
}

.title-icon {
  font-size: 18px;
}

.title-text {
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.system-badge {
  background: #1890ff;
  color: white;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
}

.card-actions {
  display: flex;
  gap: 8px;
}

.card-actions .el-button {
  height: 28px;
  padding: 4px 12px;
  font-size: 12px;
}

/* 卡片内容 */
.card-content {
  padding: 16px 20px 20px;
}

.content-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.content-left,
.content-right {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.info-label {
  font-size: 14px;
  color: #666;
  white-space: nowrap;
  min-width: 80px;
}

.info-value {
  font-size: 14px;
  color: #333;
  flex: 1;
}

.status-connected {
  color: #52c41a;
  font-weight: 500;
}

/* 响应式设计 */
@media (max-width: 1400px) {
  .image-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .filter-group {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .operation-bar {
    flex-direction: column;
    gap: 16px;
    align-items: stretch;
  }
  
  .left-operations,
  .right-operations {
    justify-content: center;
  }
  
  .content-row {
    grid-template-columns: 1fr;
  }
}
</style>
