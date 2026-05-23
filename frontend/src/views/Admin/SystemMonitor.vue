<template>
  <div class="system-monitor">
    <el-card>
      <template #header>
        <div class="card-header">
          <h2>系统监控</h2>
        </div>
      </template>

      <el-row :gutter="20">
        <el-col :span="12">
          <el-card>
            <template #header>
              <div class="card-header">
                <span>数据库状态</span>
              </div>
            </template>
            <div class="monitor-item">
              <el-statistic title="数据库大小" :value="systemInfo.database.size" />
            </div>
            <div class="monitor-item">
              <el-statistic title="当前连接数" :value="systemInfo.database.connections" />
            </div>
          </el-card>
        </el-col>

        <el-col :span="12">
          <el-card>
            <template #header>
              <div class="card-header">
                <span>文件存储</span>
              </div>
            </template>
            <div class="monitor-item">
              <el-statistic title="媒体文件大小" :value="systemInfo.storage.total_size_mb" suffix="MB" />
            </div>
            <div class="monitor-item">
              <el-statistic title="文件数量" :value="systemInfo.storage.file_count" />
            </div>
            <div class="monitor-item">
              <span class="label">存储路径：</span>
              <el-tooltip :content="systemInfo.storage.media_root" placement="top">
                <span class="path">{{ truncatePath(systemInfo.storage.media_root) }}</span>
              </el-tooltip>
            </div>
          </el-card>
        </el-col>
      </el-row>

      <el-row :gutter="20" class="mt-20">
        <el-col :span="24">
          <el-card>
            <template #header>
              <div class="card-header">
                <span>AI服务使用情况</span>
              </div>
            </template>
            <div class="ai-usage">
              <div class="usage-stats">
                <el-statistic title="今日请求" :value="systemInfo.ai_usage.requests_today" />
                <el-statistic title="总请求数" :value="systemInfo.ai_usage.requests_total" />
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>

      <el-row :gutter="20" class="mt-20">
        <el-col :span="24">
          <el-card>
            <template #header>
              <div class="card-header">
                <span>最近活动日志</span>
              </div>
            </template>
            <el-table :data="activityLogs" height="300">
              <el-table-column prop="user.username" label="用户" width="120" />
              <el-table-column prop="action" label="操作" />
              <el-table-column prop="timestamp" label="时间" width="180">
                <template #default="{ row }">
                  {{ formatDateTime(row.timestamp) }}
                </template>
              </el-table-column>
            </el-table>
          </el-card>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useStore } from 'vuex'

export default {
  setup() {
    const store = useStore()
    const systemInfo = ref({
      database: { size: '加载中...', connections: '加载中...' },
      storage: { total_size_mb: 0, file_count: 0, media_root: '' },
      ai_usage: { requests_today: 0, requests_total: 0 }
    })
    const activityLogs = ref([])

    const formatDateTime = (dateString) => {
      return new Date(dateString).toLocaleString()
    }

    const truncatePath = (path) => {
      if (path.length > 50) {
        return '...' + path.slice(-47)
      }
      return path
    }

    onMounted(async () => {
      await store.dispatch('admin/fetchSystemInfo')
      systemInfo.value = store.state.admin.systemInfo

      await store.dispatch('admin/fetchActivityLogs')
      activityLogs.value = store.state.admin.activityLogs.slice(0, 20) // 仅显示最近20条
    })

    return {
      systemInfo,
      activityLogs,
      formatDateTime,
      truncatePath
    }
  }
}
</script>

<style scoped>
.system-monitor {
  padding: 20px;
}

.monitor-item {
  margin-bottom: 15px;
  padding: 10px;
  border-bottom: 1px solid #eee;
}

.monitor-item:last-child {
  border-bottom: none;
}

.label {
  font-weight: bold;
  margin-right: 8px;
}

.path {
  font-family: monospace;
  color: #666;
}

.ai-usage {
  display: flex;
}

.usage-stats {
  display: flex;
  gap: 30px;
}

.mt-20 {
  margin-top: 20px;
}
</style>