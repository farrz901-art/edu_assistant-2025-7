<template>
  <el-dialog v-model="visible" title="上传资源">
    <el-form :model="form" label-width="80px">
      <el-form-item label="资源标题" required>
        <el-input v-model="form.title" placeholder="输入资源标题" />
      </el-form-item>

      <el-form-item label="资源类型">
        <el-select v-model="form.resource_type" placeholder="选择类型">
          <el-option
            v-for="type in resourceTypes"
            :key="type.value"
            :label="type.label"
            :value="type.value"
          />
        </el-select>
      </el-form-item>

      <el-form-item label="所属课程">
        <el-select v-model="form.course" placeholder="选择课程">
          <el-option
            v-for="course in courses"
            :key="course.id"
            :label="course.title"
            :value="course.id"
          />
        </el-select>
      </el-form-item>

      <el-form-item label="文件" required>
        <el-upload
          class="upload-demo"
          :auto-upload="false"
          :on-change="handleFileChange"
          :show-file-list="false"
        >
          <el-button type="primary">选择文件</el-button>
          <div v-if="file" class="file-info">
            {{ file.name }} ({{ formatFileSize(file.size) }})
          </div>
        </el-upload>
      </el-form-item>

      <el-form-item label="描述">
        <el-input
          v-model="form.description"
          type="textarea"
          :rows="3"
          placeholder="输入资源描述"
        />
      </el-form-item>
    </el-form>

    <template #footer>
      <el-button @click="visible = false">取消</el-button>
      <el-button
        type="primary"
        @click="submitForm"
        :loading="loading"
        :disabled="!form.title || !file || !form.course"
      >
        上传
      </el-button>
    </template>
  </el-dialog>
</template>

<script>
import { ref, reactive } from 'vue'
import { useStore } from 'vuex'
import { ElMessage } from 'element-plus'

export default {
  props: {
    courses: {
      type: Array,
      default: () => []
    }
  },
  emits: ['success'],
  setup(props, { emit }) {
    const store = useStore()
    const visible = ref(false)
    const loading = ref(false)
    const file = ref(null)

    const resourceTypes = [
      { value: 'slide', label: '课件' },
      { value: 'exercise', label: '练习' },
      { value: 'reference', label: '参考资料' },
      { value: 'other', label: '其他' }
    ]

    const form = reactive({
      title: '',
      resource_type: 'slide',
      course: null,
      description: ''
    })

    const handleFileChange = (uploadFile) => {
      file.value = uploadFile.raw
    }

    const formatFileSize = (bytes) => {
      if (bytes === 0) return '0 Bytes'
      const k = 1024
      const sizes = ['Bytes', 'KB', 'MB', 'GB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
    }

    const submitForm = async () => {
      if (!form.title.trim()) {
        ElMessage.error('请填写资源标题')
        return
      }

      if (!file.value) {
        ElMessage.error('请选择文件')
        return
      }

      if (!form.course) {
        ElMessage.error('请选择所属课程')
        return
      }

      loading.value = true

      try {
        const formData = new FormData()
        formData.append('title', form.title)
        formData.append('resource_type', form.resource_type)
        formData.append('course_id', form.course)
        formData.append('description', form.description)
        formData.append('file', file.value)

        await store.dispatch('resource/uploadResource', formData)

        ElMessage.success('资源上传成功')
        // 重置表单
        form.title = ''
        form.description = ''
        file.value = null
        emit('success')
        visible.value = false
      } catch (error) {
        ElMessage.error(`上传失败: ${error.message}`)
      } finally {
        loading.value = false
      }
    }

    return {
      visible,
      loading,
      file,
      form,
      resourceTypes,
      handleFileChange,
      formatFileSize,
      submitForm
    }
  }
}
</script>

<style scoped>
.file-info {
  margin-top: 8px;
  font-size: 14px;
  color: #606266;
}
</style>