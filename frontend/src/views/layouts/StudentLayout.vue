<template>
  <div class="student-layout">
    <el-menu
      :default-active="activeMenu"
      class="el-menu-demo"
      mode="horizontal"
      :router="true"
    >
      <el-menu-item index="/student">我的课程</el-menu-item>
      <!-- 以下菜单项可能需要根据实际课程动态生成，暂时保留静态 -->
      <el-menu-item index="/student/assistant">学习助手</el-menu-item>
      <el-menu-item index="/student/practice">随练与评测</el-menu-item>
    </el-menu>
    <div class="content-area">
        <router-view></router-view>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();

// 根据当前路由路径来决定哪个菜单项是 active 状态
const activeMenu = computed(() => {
  if (route.name === 'StudentAssistant') {
    return '/student/assistant';
  }
  if (route.name === 'StudentPractice') {
    return '/student/practice';
  }
  return '/student'; // 默认是我的课程
});

</script>

<style scoped>
.student-layout {
  width: 100%;
}
.el-menu-demo {
  margin-bottom: 20px;
}
.content-area {
  padding: 0 20px;
}
</style>