<template>
  <div class="user-management">
    <el-card>
      <template #header>
        <div class="card-header">
          <h2>用户管理</h2>
          <div class="actions">
            <el-input
              v-model="searchKeyword"
              placeholder="搜索用户名或邮箱"
              clearable
              style="width: 300px;"
              @input="handleSearch"
            />
          </div>
        </div>
      </template>

      <el-table :data="filteredUsers" v-loading="loading">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="username" label="用户名" />
        <el-table-column prop="email" label="邮箱" />
        <el-table-column label="角色" width="120">
          <template #default="{ row }">
            <el-tag :type="roleTag(row.role)">{{ roleText(row.role) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="date_joined" label="注册时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.date_joined) }}
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.is_active ? 'success' : 'danger'">
              {{ row.is_active ? '活跃' : '停用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180">
          <template #default="{ row }">
            <el-button
              v-if="row.is_active"
              type="danger"
              size="small"
              @click="deactivateUser(row.id)"
              :disabled="row.id === currentUserId"
            >
              停用
            </el-button>
            <el-button
              v-else
              type="success"
              size="small"
              @click="activateUser(row.id)"
            >
              启用
            </el-button>
            <el-button
              type="primary"
              size="small"
              @click="showUserCourses(row)"
            >
              课程
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="coursesDialogVisible" :title="`${selectedUser?.username}的课程`">
      <el-table :data="userCourses" v-if="userCourses.length > 0">
        <el-table-column prop="title" label="课程名称" />
        <el-table-column prop="subject" label="学科" width="120" />
        <el-table-column label="创建时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
      </el-table>
      <el-empty v-else description="该用户未参加任何课程" />
    </el-dialog>
  </div>
</template>

<script>
import { ref,  onMounted } from 'vue'
import { useStore } from 'vuex'
import { ElMessage } from 'element-plus'

export default {
  setup() {
    const store = useStore()
    const users = ref([])
    const filteredUsers = ref([])
    const loading = ref(false)
    const searchKeyword = ref('')
    const coursesDialogVisible = ref(false)
    const userCourses = ref([])
    const selectedUser = ref(null)
    const currentUserId = ref(null) // 当前登录用户ID

    // 获取当前登录用户
    if (store.state.auth.user) {
      currentUserId.value = store.state.auth.user.id
    }

    const roleText = (role) => {
      const roles = {
        admin: '管理员',
        teacher: '教师',
        student: '学生'
      }
      return roles[role] || role
    }

    const roleTag = (role) => {
      const tags = {
        admin: 'danger',
        teacher: 'warning',
        student: 'success'
      }
      return tags[role] || ''
    }

    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleDateString()
    }

    const fetchUsers = async () => {
      loading.value = true
      try {
        await store.dispatch('admin/fetchUsers')
        users.value = store.state.admin.users
        filteredUsers.value = [...users.value]
      } catch (error) {
        ElMessage.error('加载用户列表失败')
      } finally {
        loading.value = false
      }
    }

    const deactivateUser = async (userId) => {
      if (userId === currentUserId.value) {
        ElMessage.warning('不能停用自己')
        return
      }

      try {
        await store.dispatch('admin/deactivateUser', userId)
        ElMessage.success('用户已停用')
      } catch (error) {
        ElMessage.error('停用用户失败')
      }
    }

    const activateUser = async (userId) => {
      try {
        await store.dispatch('admin/activateUser', userId)
        ElMessage.success('用户已启用')
      } catch (error) {
        ElMessage.error('启用用户失败')
      }
    }

    const showUserCourses = async (user) => {
      selectedUser.value = user
      try {
        // 实际项目中应调用API
        // const response = await adminApi.getUserCourses(user.id)
        // userCourses.value = response.data

        // 模拟数据
        userCourses.value = [
          { id: 1, title: '高等数学', subject: '数学', created_at: '2023-01-01' },
          { id: 2, title: '大学英语', subject: '英语', created_at: '2023-02-01' }
        ]
        coursesDialogVisible.value = true
      } catch (error) {
        ElMessage.error('获取用户课程失败')
      }
    }

    const handleSearch = () => {
      const keyword = searchKeyword.value.toLowerCase()
      if (!keyword) {
        filteredUsers.value = [...users.value]
        return
      }

      filteredUsers.value = users.value.filter(user =>
        user.username.toLowerCase().includes(keyword) ||
        (user.email && user.email.toLowerCase().includes(keyword)))
    }

    onMounted(fetchUsers)

    return {
      users,
      filteredUsers,
      loading,
      searchKeyword,
      coursesDialogVisible,
      userCourses,
      selectedUser,
      currentUserId,
      roleText,
      roleTag,
      formatDate,
      deactivateUser,
      activateUser,
      showUserCourses,
      handleSearch
    }
  }
}
</script>

<style scoped>
.user-management {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.actions {
  display: flex;
  gap: 10px;
}
</style>