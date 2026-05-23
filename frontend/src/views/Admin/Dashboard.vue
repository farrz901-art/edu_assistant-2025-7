<template>
  <!-- 顶部统计卡片布局优化 -->
  <el-row :gutter="20" class="stats-row">
    <el-col :xs="24" :sm="12" :md="6" v-for="stat in statsItems" :key="stat.title">
      <stat-card v-bind="stat" />
    </el-col>
  </el-row>

  <!-- 系统资源展示优化 -->
  <el-row :gutter="20" class="mt-20">
    <el-col :span="24">
      <el-card>
        <template #header>
          <div class="card-header">
            <span>系统资源使用情况</span>
          </div>
        </template>

        <el-row :gutter="20">
          <el-col :span="8">
            <div class="resource-item">
              <h4>内存使用</h4>
              <el-progress
                :percentage="system.memory.percent"
                :color="getProgressColor(system.memory.percent)"
                :text-inside="true"
                :stroke-width="20"
              />
              <div class="resource-meta">
                <span>{{ system.memory.used }} / {{ system.memory.total }} GB</span>
                <span>{{ system.memory.percent }}%</span>
              </div>
            </div>
          </el-col>

          <el-col :span="8">
            <div class="resource-item">
              <h4>磁盘使用</h4>
              <el-progress
                :percentage="system.disk.percent"
                :color="getProgressColor(system.disk.percent)"
                :text-inside="true"
                :stroke-width="20"
              />
              <div class="resource-meta">
                <span>{{ system.disk.used }} / {{ system.disk.total }} GB</span>
                <span>{{ system.disk.percent }}%</span>
              </div>
            </div>
          </el-col>

          <el-col :span="8">
            <div class="resource-item">
              <h4>数据库连接</h4>
              <el-statistic
                :value="system.database.connections"
                title="当前连接数"
                class="connection-stat"
              />
            </div>
          </el-col>
        </el-row>
      </el-card>
    </el-col>
  </el-row>

  <!-- AI使用情况图表实现 -->
  <el-row :gutter="20" class="mt-20">
    <el-col :span="24">
      <el-card>
        <template #header>
          <div class="card-header">
            <span>AI服务使用情况</span>
          </div>
        </template>
        <div class="ai-usage-chart">
          <div class="chart-container">
            <h3>最近7天使用趋势</h3>
            <div class="chart-placeholder">
              <!-- 实际项目中这里应集成图表库 -->
              <el-image :src="chartPlaceholder" fit="contain" />
              <p class="tip">图表展示区域 - 实际项目中将显示AI使用趋势图</p>
            </div>
          </div>
          <div class="usage-stats">
            <el-statistic title="今日请求" :value="system.ai_usage.requests_today" />
            <el-statistic title="总请求数" :value="system.ai_usage.requests_total" />
          </div>
        </div>
      </el-card>
    </el-col>
  </el-row>
</template>

<script>
// {{ edit_1 }}
import { computed, ref } from 'vue'; // 导入 ref
import StatCard from "@/components/admin/StatCard.vue";

export default {
  components: { StatCard },
  setup() {
    // 提供静态的统计数据
    const stats = ref({
      total: 1500, // 示例数据
      teachers: 150,
      students: 1300,
      active: 1000,
      inactive: 500,
      active_recent: 300,
    });

    // 提供静态的系统资源使用情况数据
    const system = ref({
      memory: {
        percent: 65,
        used: 12.5,
        total: 16,
      },
      disk: {
        percent: 45,
        used: 225,
        total: 500,
      },
      database: {
        connections: 25,
      },
      ai_usage: {
        requests_today: 120,
        requests_total: 5800,
      },
    });

    // 添加统计卡片数据
    const statsItems = computed(() => [
      { title: '总用户', value: stats.value.total, icon: 'User', color: '#409EFF' },
      { title: '教师', value: stats.value.teachers, icon: 'User', color: '#67C23A' },
      { title: '学生', value: stats.value.students, icon: 'User', color: '#E6A23C' },
      { title: '活跃用户', value: stats.value.active_recent, icon: 'User', color: '#F56C6C' }
    ]);

    // 添加图表占位图
    const chartPlaceholder = require('@/assets/chart-placeholder.png');

    // 进度条颜色逻辑
    const getProgressColor = (percentage) => {
      if (percentage < 60) return '#67C23A'; // Green
      if (percentage < 80) return '#E6A23C'; // Orange
      return '#F56C6C'; // Red
    };

    return {
      statsItems,
      chartPlaceholder,
      system, // 导出 system 数据
      getProgressColor // 导出方法
    };
  }
};
</script>

<style scoped>
/* 添加新样式 */
.stats-row {
  margin-bottom: 20px;
}

.mt-20 {
  margin-top: 20px;
}

.resource-item {
  padding: 15px;
}

.resource-meta {
  display: flex;
  justify-content: space-between;
  margin-top: 8px;
  color: #909399;
  font-size: 14px;
}

.connection-stat {
  text-align: center;
  padding-top: 10px;
}

.ai-usage-chart {
  display: flex;
}

.chart-container {
  flex: 3;
  padding: 15px;
}

.usage-stats {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 30px;
  border-left: 1px solid #ebeef5;
}

.chart-placeholder {
  height: 250px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: #f9f9f9;
  border-radius: 4px;
  margin-top: 15px;
}

.tip {
  margin-top: 15px;
  color: #909399;
  font-size: 14px;
}
</style>