<template>
  <div class="page-container">
    <div class="header">
      <el-page-header @back="$router.push('/student')">
        <template #content>
          <span class="text-large font-600 mr-3">
            在线学习助手{{ course.name ? ` - ${course.name}` : '' }}
          </span>
        </template>
      </el-page-header>
    </div>

    <div v-if="!courseId" class="no-course">
      <el-alert title="错误" type="error" description="未指定课程ID，请从课程列表进入。" show-icon :closable="false" />
    </div>

    <div v-else class="chat-wrapper">
      <div class="message-list" ref="messageListRef">
        <div v-for="(msg, index) in messages" :key="index" :class="['message-item', msg.role]">
          <div class="avatar">
            {{ msg.role === 'user' ? '我' : 'AI' }}
          </div>
          <div class="message-content">
            <MarkdownView :content="msg.content" />
          </div>
        </div>
        <div v-if="loading" class="message-item assistant">
          <div class="avatar">AI</div>
          <div class="message-content">
            <el-icon class="is-loading"><Loading /></el-icon>
            <span>正在思考中...</span>
          </div>
        </div>
      </div>
      <div class="input-area">
        <el-input
          v-model="question"
          placeholder="请输入您的问题..."
          @keyup.enter="sendMessage"
          :disabled="loading"
          size="large"
        >
          <template #append>
            <el-button @click="sendMessage" :disabled="loading || !question.trim()">发送</el-button>
          </template>
        </el-input>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, nextTick, onMounted, defineProps } from 'vue';
import { useStore } from 'vuex';
import { ElMessage } from 'element-plus';
import { Loading } from '@element-plus/icons-vue';
import MarkdownView from '@/components/common/MarkdownView.vue';

const props = defineProps({
  courseId: {
    type: String,
    required: true,
  },
});

const store = useStore();
const course = ref({});
const messages = reactive([]);
const question = ref('');
const loading = ref(false);
const messageListRef = ref(null);

onMounted(async () => {
  if (props.courseId) {
    try {
      const courseDetail = await store.dispatch('courses/fetchCourseDetails', props.courseId);
      course.value = courseDetail;
      messages.push({ role: 'assistant', content: `你好！你可以开始就《${course.value.name}》这门课向我提问了。` });
    } catch (error) {
      ElMessage.error('获取课程详情失败');
    }
  }
});

const scrollToBottom = () => {
  nextTick(() => {
    if (messageListRef.value) {
      messageListRef.value.scrollTop = messageListRef.value.scrollHeight;
    }
  });
};

const sendMessage = async () => {
  if (!question.value.trim() || loading.value) return;

  const userMessage = { role: 'user', content: question.value };
  messages.push(userMessage);
  const currentQuestion = question.value;
  question.value = '';
  loading.value = true;
  scrollToBottom();

  try {
    const response = await store.dispatch('ai/askQuestion', {
      course_id: props.courseId,
      question: currentQuestion,
    });
    messages.push({ role: 'assistant', content: response.answer });
  } catch (error) {
    ElMessage.error('提问失败，请稍后再试');
    messages.push({ role: 'assistant', content: '抱歉，我暂时无法回答你的问题。' });
  } finally {
    loading.value = false;
    scrollToBottom();
  }
};
</script>

<style scoped>
.page-container {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 40px);
  padding: 20px;
  background-color: #f0f2f5;
}
.header {
  background-color: #fff;
  padding: 10px 20px;
  border-radius: 8px;
  margin-bottom: 20px;
  flex-shrink: 0;
}
.no-course {
  padding: 20px;
}
.chat-wrapper {
  flex-grow: 1;
  background-color: #fff;
  border-radius: 8px;
  padding: 24px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
.message-list {
  flex-grow: 1;
  overflow-y: auto;
  padding: 20px 10px;
}
.message-item {
  display: flex;
  margin-bottom: 20px;
  max-width: 80%;
}
.message-item .avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  text-align: center;
  line-height: 40px;
  flex-shrink: 0;
  color: #fff;
}
.message-item .message-content {
  padding: 10px 15px;
  border-radius: 10px;
  margin: 0 10px;
}
/* User message */
.message-item.user {
  margin-left: auto;
  flex-direction: row-reverse;
}
.message-item.user .avatar {
  background-color: #409eff;
}
.message-item.user .message-content {
  background-color: #ecf5ff;
}
/* Assistant message */
.message-item.assistant .avatar {
  background-color: #67c23a;
}
.message-item.assistant .message-content {
  background-color: #f0f9eb;
}
.input-area {
  padding-top: 15px;
  border-top: 1px solid #eee;
  flex-shrink: 0;
}
</style>
 