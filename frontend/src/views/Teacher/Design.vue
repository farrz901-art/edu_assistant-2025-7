<template>
  <div class="page-container">
    <div class="header">
      <el-page-header @back="$router.push('/teacher')">
        <template #content>
          <span class="text-large font-600 mr-3"> 备课与设计 </span>
        </template>
      </el-page-header>
    </div>

    <div class="content-wrapper">
      <!-- Input Section -->
      <div class="input-section">
        <el-card shadow="never" class="input-card">
          <template #header>
            <div class="card-header">
              <span>课程大纲 (必填)</span>
            </div>
          </template>
          <el-input
            v-model="syllabus"
            type="textarea"
            :rows="8"
            placeholder="请输入课程的教学目标、主要内容、重点难点等信息..."
            show-word-limit
            maxlength="2000"
          />
        </el-card>

        <el-card shadow="never" class="input-card">
          <template #header>
            <div class="card-header">
              <span>知识库文档 (可选)</span>
            </div>
          </template>
          <el-input
            v-model="knowledgeBase"
            type="textarea"
            :rows="6"
            placeholder="可在此输入相关的教材、参考资料或笔记，帮助AI生成更贴合需求的内容。"
            show-word-limit
            maxlength="5000"
          />
        </el-card>

        <el-button
          type="primary"
          size="large"
          :loading="loading"
          @click="handleDesign"
          class="generate-btn"
        >
          {{ loading ? '正在生成...' : 'AI 生成教学内容' }}
        </el-button>
      </div>

      <!-- Result Section -->
      <div v-if="result" class="result-section">
        <el-divider><h3>生成结果</h3></el-divider>
        <el-row :gutter="20">
          <el-col :span="8">
            <el-card class="result-card">
              <template #header>知识讲解</template>
              <MarkdownView :content="result.knowledge_explanation || '无内容'" />
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card class="result-card">
              <template #header>实训练习与指导</template>
              <MarkdownView :content="result.practical_exercises || '无内容'" />
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card class="result-card">
              <template #header>时间分布建议</template>
              <MarkdownView :content="result.time_distribution || '无内容'" />
            </el-card>
          </el-col>
        </el-row>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useStore } from 'vuex'
import { ElMessage } from 'element-plus'
import MarkdownView from '@/components/common/MarkdownView.vue'

const store = useStore()
const syllabus = ref('')
const knowledgeBase = ref('')
const loading = ref(false)
const result = ref(null)

const handleDesign = async () => {
  if (!syllabus.value.trim()) {
    ElMessage.warning('课程大纲不能为空')
    return
  }
  loading.value = true
  result.value = null
  try {
    const response = await store.dispatch('ai/designCourse', {
      syllabus: syllabus.value,
      knowledge_base_docs: knowledgeBase.value
    })
    result.value = response.designed_content
    ElMessage.success('教学内容已生成')
  } catch (error) {
    ElMessage.error('生成失败，请稍后再试')
    console.error('Design course failed:', error)
  } finally {
    loading.value = false
  }
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
.result-section .el-divider h3 {
  color: #555;
}
.result-card {
  min-height: 300px;
}
</style> 