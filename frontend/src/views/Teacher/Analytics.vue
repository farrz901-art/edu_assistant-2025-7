<template>
  <div class="analytics">
    <el-card>
      <h2>学情数据分析</h2>
      <el-input v-model="history" type="textarea" :rows="8" placeholder="粘贴学生练习历史 JSON..." />
      <el-button type="primary" :loading="loading" @click="analyze">AI 分析</el-button>
    </el-card>

    <el-card v-if="result" class="mt">
      <h3>分析结果</h3>
      <p><strong>知识掌握情况：</strong>{{ result.knowledge_mastery_summary }}</p>
      <div v-if="result.teaching_suggestions?.length">
        <p><strong>教学建议：</strong></p>
        <ul>
          <li v-for="(s,i) in result.teaching_suggestions" :key="i">{{ s }}</li>
        </ul>
      </div>
    </el-card>
  </div>
</template>
<script setup>
import { ref } from 'vue'
import { useStore } from 'vuex'
import { ElMessage } from 'element-plus'

const store = useStore()
const history = ref('')
const loading = ref(false)
const result = ref(null)

const analyze = async () => {
  if (!history.value.trim()) {
    ElMessage.warning('请输入历史数据')
    return
  }
  loading.value = true
  try {
    result.value = await store.dispatch('ai/analyzeLearningData', { student_practice_history: history.value })
  } catch (e) { /* 统一错误提示 */ }
  finally { loading.value = false }
}
</script>
<style scoped>
.analytics { max-width:800px; margin:20px auto; }
.mt{margin-top:20px}
</style> 