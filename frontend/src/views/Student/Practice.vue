<template>
  <div class="page-container">
    <div class="header">
      <el-page-header @back="$router.push('/student')">
        <template #content>
          <span class="text-large font-600 mr-3">
            随练与评测{{ course.name ? ` - ${course.name}` : '' }}
          </span>
        </template>
      </el-page-header>
    </div>

    <div v-if="!props.courseId" class="no-course">
       <el-alert title="错误" type="error" description="未指定课程ID，请从课程列表进入。" show-icon :closable="false" />
    </div>

    <div v-else class="content-wrapper">
      <!-- Stage 1: Topic Selection -->
      <div v-if="stage === 'select'" class="stage-wrapper">
        <el-card shadow="never">
          <template #header><h3>第一步：选择练习主题</h3></template>
          <el-form label-width="100px">
            <el-form-item label="练习主题">
              <el-input v-model="topic" placeholder="例如：Python 循环语句" />
            </el-form-item>
            <el-form-item label="题目数量">
              <el-input-number v-model="count" :min="1" :max="10" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" :loading="loading" @click="generateQuestions">
                {{ loading ? '正在生成...' : '生成练习题' }}
              </el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </div>

      <!-- Stage 2: Answering Questions -->
      <div v-if="stage === 'answer'" class="stage-wrapper">
        <h3>第二步：回答问题 (第 {{ currentQuestionIndex + 1 }} / {{ questions.length }} 题)</h3>
        <el-card class="question-card">
           <template #header>
            <div class="question-header">
              <span>{{ currentQuestion.question_type }}</span>
              <el-tag size="small" type="info" style="margin-left: 10px;">{{ currentQuestion.difficulty }}</el-tag>
            </div>
          </template>
          <p>{{ currentQuestion.text }}</p>
          <div v-if="currentQuestion.options" class="options-group">
            <el-radio-group v-model="currentAnswer">
              <el-radio v-for="(option, key) in currentQuestion.options" :key="key" :label="key">{{ key }}. {{ option }}</el-radio>
            </el-radio-group>
          </div>
          <el-input
            v-else
            v-model="currentAnswer"
            type="textarea"
            :rows="5"
            placeholder="请输入您的答案..."
            class="answer-input"
          />
        </el-card>
        <div class="action-buttons">
          <el-button type="primary" :loading="loading" @click="evaluateAnswer">
            {{ loading ? '正在评测...' : '提交答案并评测' }}
          </el-button>
        </div>
      </div>
      
      <!-- Stage 3: Evaluation Result -->
      <div v-if="stage === 'result'" class="stage-wrapper">
        <h3>评测结果</h3>
        <el-card class="result-card" :body-style="{ padding: '0px' }">
          <el-descriptions :column="1" border>
            <el-descriptions-item label="得分"><el-tag :type="evaluationResult.score > 7 ? 'success' : 'warning'">{{ evaluationResult.score }} / 10</el-tag></el-descriptions-item>
            <el-descriptions-item label="AI 评语">{{ evaluationResult.feedback }}</el-descriptions-item>
            <el-descriptions-item label="改进建议">
              <ul>
                <li v-for="(suggestion, i) in evaluationResult.suggestions" :key="i">{{ suggestion }}</li>
              </ul>
            </el-descriptions-item>
          </el-descriptions>
        </el-card>
        <div class="action-buttons">
            <el-button v-if="currentQuestionIndex < questions.length - 1" @click="nextQuestion">下一题</el-button>
            <el-button v-else type="success" @click="finishPractice">完成练习</el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, defineProps } from 'vue';
import { useStore } from 'vuex';
import { ElMessage } from 'element-plus';

const props = defineProps({
  courseId: {
    type: String,
    required: true,
  },
});

const store = useStore();
const course = ref({});
const stage = ref('select'); // select, answer, result
const loading = ref(false);

// Stage 1
const topic = ref('Python 基础');
const count = ref(3);
const questions = ref([]);

// Stage 2
const currentQuestionIndex = ref(0);
const currentAnswer = ref('');
const currentQuestion = computed(() => questions.value[currentQuestionIndex.value] || {});

// Stage 3
const evaluationResult = ref({});

onMounted(async () => {
  if (props.courseId) {
    try {
      const courseDetail = await store.dispatch('courses/fetchCourseDetails', props.courseId);
      course.value = courseDetail;
    } catch (error) {
      ElMessage.error('获取课程详情失败');
    }
  }
});

const generateQuestions = async () => {
  if (!topic.value.trim()) {
    ElMessage.warning('练习主题不能为空');
    return;
  }
  loading.value = true;
  try {
    const res = await store.dispatch('ai/generatePractice', { 
      topic: topic.value, 
      count: count.value, 
      course_id: props.courseId 
    });
    
    if (res && res.questions && res.questions.length > 0) {
      questions.value = res.questions;
      stage.value = 'answer';
      ElMessage.success(`已生成 ${questions.value.length} 道题`);
    } else {
      ElMessage.error('未能生成题目，AI服务可能正忙，请更换主题或稍后再试');
    }
  } catch (error) {
    // error message is already shown by the interceptor in request.js
    console.error(error);
  } finally {
    loading.value = false;
  }
};

const evaluateAnswer = async () => {
  if (!currentAnswer.value.trim()) {
    ElMessage.warning('答案不能为空');
    return;
  }
  loading.value = true;
  try {
    const res = await store.dispatch('ai/evaluateAnswer', { 
      question_id: currentQuestion.value.id,
      answer: currentAnswer.value 
    });
    evaluationResult.value = res;
    stage.value = 'result';
  } catch (error) {
    console.error(error);
  } finally {
    loading.value = false;
  }
};

const nextQuestion = () => {
    currentQuestionIndex.value++;
    currentAnswer.value = '';
    evaluationResult.value = {};
    stage.value = 'answer';
}

const finishPractice = () => {
    ElMessage.success('恭喜你，已完成本次所有练习！');
    stage.value = 'select';
    questions.value = [];
    currentQuestionIndex.value = 0;
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
.no-course {
  padding: 20px;
}
.content-wrapper {
  background-color: #fff;
  padding: 24px;
  border-radius: 8px;
  max-width: 800px;
  margin: 0 auto;
}
.stage-wrapper {
  animation: fadeIn 0.5s ease-in-out;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
.question-card, .result-card {
  margin-top: 20px;
}
.answer-input {
  margin-top: 15px;
}
.action-buttons {
    margin-top: 20px;
    text-align: right;
}
.question-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 14px;
  color: #999;
}
.options-group {
    margin-top: 15px;
}
.el-radio-group {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
}
.el-radio {
    margin-bottom: 10px;
}
ul {
    padding-inline-start: 20px;
    margin: 0;
}
li {
    margin-bottom: 5px;
}
</style>