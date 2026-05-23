<template>
  <div class="teacher-layout">
    <el-breadcrumb separator="/" class="breadcrumb">
      <el-breadcrumb-item :to="{ path: '/teacher' }">教师中心</el-breadcrumb-item>
      <el-breadcrumb-item>{{ currentRouteName }}</el-breadcrumb-item>
    </el-breadcrumb>
    <router-view></router-view>
  </div>
</template>

<script>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

export default {
  setup() {
    const route = useRoute()
    const currentRouteName = computed(() => {
      const routeMap = {
        'CourseDesign': '课程设计',
        'ResourceManager': '资源管理',
        'AnalyticsDashboard': '学情分析'
      }
      return routeMap[route.name] || '仪表盘'
    })

    return { currentRouteName }
  }
}
</script>

<style scoped>
.teacher-layout {
  padding: 20px;
}

.breadcrumb {
  margin-bottom: 20px;
}
</style>