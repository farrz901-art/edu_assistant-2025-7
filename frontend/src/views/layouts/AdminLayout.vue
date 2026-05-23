<template>
  <div class="admin-layout">
    <el-breadcrumb separator="/" class="breadcrumb">
      <el-breadcrumb-item :to="{ path: '/admin' }">系统管理</el-breadcrumb-item>
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
        'UserManagement': '用户管理',
        'SystemMonitor': '系统监控'
      }
      return routeMap[route.name] || '仪表盘'
    })

    return { currentRouteName }
  }
}
</script>

<style scoped>
.admin-layout {
  padding: 20px;
}

.breadcrumb {
  margin-bottom: 20px;
}
</style>