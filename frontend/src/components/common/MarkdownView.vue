<template>
  <div class="markdown-view" v-html="compiledMarkdown"></div>
</template>

<script>
import { marked } from 'marked'
import { ref, watch } from 'vue'

export default {
  props: {
    content: {
      type: String,
      default: ''
    }
  },
  setup(props) {
    const compiledMarkdown = ref('')

    watch(() => props.content, (newContent) => {
      compiledMarkdown.value = marked(newContent || '')
    }, { immediate: true })

    return { compiledMarkdown }
  }
}
</script>

<style scoped>
.markdown-view {
  padding: 15px;
  border: 1px solid #ebeef5;
  border-radius: 4px;
  background-color: #fff;
}
</style>