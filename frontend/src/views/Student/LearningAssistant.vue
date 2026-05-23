<template>
  <div class="assistant-container">
    <el-card class="chat-container">
      <div class="chat-history" ref="historyRef">
        <div v-for="(msg,idx) in msgs" :key="idx" :class="['msg',msg.role]">
          <div class="avatar">
            <el-avatar :icon="msg.role==='user'?User:ChatLineRound" />
          </div>
          <div class="content">
            <MarkdownView :content="msg.content" />
          </div>
        </div>
      </div>
      <div class="input-area">
        <el-input v-model="question" type="textarea" :rows="3" placeholder="输入问题..." @keyup.ctrl.enter="ask" />
        <el-button type="primary" :loading="loading" @click="ask" class="send-btn">提问</el-button>
      </div>
    </el-card>
  </div>
</template>
<script setup>
/* eslint-disable */
import { ref, watch,nextTick } from 'vue'
import { useStore } from 'vuex'
import { User,ChatLineRound } from '@element-plus/icons-vue'
import MarkdownView from '@/components/common/MarkdownView.vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'

const store = useStore()
const route = useRoute()
const courseId = route.params.courseId || null

const question = ref('')
const msgs = ref([])
const loading = ref(false)
const historyRef = ref(null)

watch(msgs,()=>nextTick(()=>{historyRef.value?.scrollTo({top:historyRef.value.scrollHeight,behavior:'smooth'})}))

const ask = async ()=>{
  if(!question.value.trim()||loading.value) return
  msgs.value.push({role:'user',content:question.value})
  const q=question.value
  question.value=''
  loading.value=true
  try{
    const res = await store.dispatch('ai/askQuestion',{ course_id: courseId, question:q })
    msgs.value.push({role:'assistant',content:res.answer})
  }catch(e){
    ElMessage.error('暂时无法回答，请稍后再试')
  }finally{loading.value=false}
}
</script>
<style scoped>
.assistant-container{height:100%;display:flex;flex-direction:column;}
.chat-container{flex:1;display:flex;flex-direction:column;}
.chat-history{flex:1;overflow-y:auto;padding:20px;background:#f5f7fa;}
.msg{display:flex;margin-bottom:20px;}
.msg.user{flex-direction:row-reverse;}
.avatar{margin:0 10px;}
.content{max-width:70%;padding:10px 15px;border-radius:5px;background:#fff;box-shadow:0 2px 4px rgba(0,0,0,.1);}
.user .content{background:#e6f7ff;}
.input-area{padding:20px;border-top:1px solid #ebeef5;background:#fff;}
.send-btn{margin-top:10px;width:100%;}
</style> 