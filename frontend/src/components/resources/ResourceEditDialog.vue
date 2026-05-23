<template>
  <el-dialog v-model="visible" title="编辑资源">
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
      <el-button type="primary" @click="submitForm">保存</el-button>
    </template>
  </el-dialog>
</template>

<script>
import { ref, reactive, watch } from 'vue'
import { ElMessage } from 'element-plus'

export default {
  props: {
    modelValue: Boolean,
    resource: Object
  },
  emits: ['update:modelValue', 'success'],
  setup(props, { emit }) {
    const visible = ref(false)
    const resourceTypes = [
      { value: 'slide', label: '课件' },
      { value: 'exercise', label: '练习' },
      { value: 'reference', label: '参考资料' },
      { value: 'other', label: '其他' }
    ]

    const form = reactive({
      title: '',
      resource_type: 'slide',
      description: ''
    })

    watch(() => props.modelValue, (val) => {
      visible.value = val
      if (val && props.resource) {
        Object.assign(form, props.resource)
      }
    })

    watch(visible, (val) => {
      emit('update:modelValue', val)
    })

    const submitForm = () => {
      if (!form.title.trim()) {
        ElMessage.error('请填写资源标题')
        return
      }

      emit('success', form)
      visible.value = false
    }

    return {
      visible,
      form,
      resourceTypes,
      submitForm
    }
  }
}
</script>