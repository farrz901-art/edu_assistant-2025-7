<template>
  <div class="page-container">
    <div class="header">
      <el-page-header @back="$router.push('/teacher')">
        <template #content>
          <span class="text-large font-600 mr-3"> 考核内容生成 </span>
        </template>
      </el-page-header>
    </div>

    <div class="content-wrapper">
      <!-- Input Section -->
      <div class="input-section">
        <el-card shadow="never" class="input-card">
          <template #header>
            <div class="card-header">
              <span>教学内容 (必填)</span>
            </div>
          </template>
          <el-input
            v-model="teachingContent"
            type="textarea"
            :rows="10"
            placeholder="请粘贴需要生成考核题目的教学内容，AI将根据内容自动识别学科并生成相应题型..."
            show-word-limit
            maxlength="5000"
          />
        </el-card>

        <el-button
          type="primary"
          size="large"
          :loading="loading"
          @click="handleGenerate"
          class="generate-btn"
        >
          {{ loading ? '正在生成...' : 'AI 生成考核题目' }}
        </el-button>
      </div>

      <!-- Result Section -->
      <div v-if="questions.length" class="result-section">
        <el-divider><h3>共生成 {{ questions.length }} 道题目</h3></el-divider>
        <div class="actions">
          <el-button @click="copyAllQuestions">复制全部</el-button>
        </div>
        <div class="questions-list">
          <el-card v-for="(q, i) in questions" :key="q.id || i" class="question-card">
            <template #header>
              <div class="question-header">
                <span>第 {{ i + 1 }} 题 ({{ q.type }})</span>
                <el-button type="text" @click="copyQuestion(q, i + 1)">复制</el-button>
              </div>
            </template>
            <p><strong>题目：</strong>{{ q.text }}</p>
            <p v-if="q.options"><strong>选项：</strong>{{ q.options.join(', ') }}</p>
            <p><strong>答案：</strong>{{ q.answer }}</p>
            <p v-if="q.explanation"><strong>解析：</strong>{{ q.explanation }}</p>
            <pre v-if="q.test_cases" class="test-cases"><strong>测试用例：</strong>\n{{ q.test_cases }}</pre>
          </el-card>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useStore } from 'vuex'
import { ElMessage } from 'element-plus'

const store = useStore()
const teachingContent = ref('')
const loading = ref(false)
const questions = ref([])

const handleGenerate = async () => {
  if (!teachingContent.value.trim()) {
    ElMessage.warning('教学内容不能为空')
    return
  }
  loading.value = true
  questions.value = []
  try {
    const response = await store.dispatch('ai/generateAssessment', {
      teaching_content: teachingContent.value
    })
    questions.value = response.questions || []
    ElMessage.success(`成功生成 ${questions.value.length} 道题目`)
  } catch (error) {
    ElMessage.error('生成失败，请稍后再试')
    console.error('Generate assessment failed:', error)
  } finally {
    loading.value = false
  }
}

const formatQuestionForCopy = (q, index) => {
  let content = `第 ${index} 题 (${q.type})\n\n`
  content += `题目：\n${q.text}\n\n`
  if (q.options) {
    content += `选项：\n${q.options.map((opt, i) => `${String.fromCharCode(65 + i)}. ${opt}`).join('\n')}\n\n`
  }
  content += `答案：\n${q.answer}\n\n`
  if (q.explanation) {
    content += `解析：\n${q.explanation}\n\n`
  }
  if (q.test_cases) {
    content += `测试用例：\n${JSON.stringify(q.test_cases, null, 2)}\n\n`
  }
  return content
}

const copyQuestion = async (q, index) => {
  const content = formatQuestionForCopy(q, index)
  await navigator.clipboard.writeText(content)
  ElMessage.success('题目已复制到剪贴板')
}

const copyAllQuestions = async () => {
  const allContent = questions.value.map((q, i) => formatQuestionForCopy(q, i + 1)).join('\n' + '-'.repeat(20) + '\n\n')
  await navigator.clipboard.writeText(allContent)
  ElMessage.success('全部题目已复制到剪贴板')
}
</script>

<style scoped>
.page-container {
  padding: 20px;
  background-color: #f0f2f5;
  min-height: 100vh;
}
.header {
  background-color: #fff;
  padding: 10px 20px;
  border-radius: 8px;
  margin-bottom: 20px;
}
.content-wrapper {
  background-color: #fff;
  padding: 24px;
  border-radius: 8px;
}
.input-section {
  max-width: 800px;
  margin: 0 auto 30px auto;
}
.input-card {
  margin-bottom: 20px;
}
.card-header {
  font-weight: bold;
}
.generate-btn {
  width: 100%;
}
.actions {
  text-align: right;
  margin-bottom: 10px;
}
.questions-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}
.question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.question-card p {
  margin: 10px 0;
}
.test-cases {
  background-color: #eee;
  padding: 10px;
  border-radius: 4px;
  white-space: pre-wrap;
}
</style> 