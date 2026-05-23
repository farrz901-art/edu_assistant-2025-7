<template>
  <div class="student-home">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>我的课程</span>
        </div>
      </template>
      <div v-if="loading" class="loading-text">正在加载课程...</div>
      <div v-else-if="error" class="error-text">{{ error }}</div>
      <div v-else-if="courses.length > 0">
        <el-row :gutter="20">
          <el-col v-for="course in courses" :key="course.id" :span="24" style="margin-bottom: 20px;">
            <el-card shadow="hover">
              <h4>{{ course.name }}</h4>
              <p>{{ course.description }}</p>
              <el-button type="primary" @click="goToAssistant(course.id)">在线学习助手</el-button>
              <el-button type="success" @click="goToPractice(course.id)">随练与评测</el-button>
            </el-card>
          </el-col>
        </el-row>
      </div>
      <div v-else class="empty-text">
        暂无课程。请联系管理员或教师为您分配课程。
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';

const store = useStore();
const router = useRouter();

const loading = ref(true);
const error = ref(null);

// 从 Vuex store 获取课程数据
const courses = computed(() => store.state.courses.courses);

onMounted(async () => {
  // Only fetch courses if the list is empty in the store
  if (store.state.courses.courses.length === 0) {
    loading.value = true;
    try {
      // Dispatch action to fetch courses from the backend
      await store.dispatch('courses/fetchCourses');
    } catch (err) {
      error.value = '无法连接到服务器，请检查网络或联系管理员。';
      console.error('获取课程失败:', err);
    } finally {
      loading.value = false;
    }
  } else {
    // If courses are already in store, no need to load
    loading.value = false;
  }
});

const goToAssistant = (courseId) => {
  if (courseId) {
    router.push({ name: 'StudentAssistant', params: { courseId } });
  } else {
    error.value = "课程ID无效，无法进入学习助手。";
  }
};

const goToPractice = (courseId) => {
  if (courseId) {
    router.push({ name: 'StudentPractice', params: { courseId } });
  } else {
    error.value = "课程ID无效，无法进入随练与评测。";
  }
};
</script>

<style scoped>
.student-home {
  max-width: 800px;
  margin: 40px auto;
}
.card-header {
  font-size: 20px;
  font-weight: bold;
}
.loading-text, .error-text, .empty-text {
  text-align: center;
  color: #909399;
  padding: 20px;
}
</style> 