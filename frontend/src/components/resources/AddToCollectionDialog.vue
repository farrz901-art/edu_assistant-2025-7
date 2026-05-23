<template>
  <el-dialog v-model="visible" title="添加到集合">
    <el-form label-width="80px">
      <el-form-item label="选择集合">
        <el-select v-model="selectedCollection" placeholder="请选择集合">
          <el-option
            v-for="collection in collections"
            :key="collection.id"
            :label="collection.name"
            :value="collection.id"
          />
        </el-select>
      </el-form-item>

      <el-form-item label="新建集合">
        <el-input
          v-model="newCollectionName"
          placeholder="输入新集合名称"
          @keyup.enter="createCollection"
        />
        <el-button
          type="primary"
          plain
          @click="createCollection"
          :disabled="!newCollectionName.trim()"
        >
          创建
        </el-button>
      </el-form-item>
    </el-form>

    <template #footer>
      <el-button @click="visible = false">取消</el-button>
      <el-button type="primary" @click="addToCollection">确定</el-button>
    </template>
  </el-dialog>
</template>

<script>
import { ref, watch } from 'vue'
import { ElMessage } from 'element-plus'

export default {
  props: {
    modelValue: Boolean,
    resourceIds: Array
  },
  emits: ['update:modelValue', 'success'],
  setup(props, { emit }) {
    const visible = ref(false)
    const selectedCollection = ref(null)
    const newCollectionName = ref('')
    const collections = ref([
      { id: 1, name: '数学课程资源' },
      { id: 2, name: '英语课程资源' }
    ])

    watch(() => props.modelValue, (val) => {
      visible.value = val
    })

    watch(visible, (val) => {
      emit('update:modelValue', val)
    })

    const createCollection = () => {
      if (!newCollectionName.value.trim()) return

      const newCollection = {
        id: Date.now(),
        name: newCollectionName.value
      }

      collections.value.push(newCollection)
      selectedCollection.value = newCollection.id
      newCollectionName.value = ''

      ElMessage.success(`集合"${newCollection.name}"创建成功`)
    }

    const addToCollection = () => {
      if (!selectedCollection.value) {
        ElMessage.error('请选择集合')
        return
      }

      const collection = collections.value.find(c => c.id === selectedCollection.value)
      ElMessage.success(`已添加到集合"${collection.name}"`)

      emit('success')
      visible.value = false
    }

    return {
      visible,
      selectedCollection,
      newCollectionName,
      collections,
      createCollection,
      addToCollection
    }
  }
}
</script>