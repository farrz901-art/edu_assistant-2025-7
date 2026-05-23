<template>
  <div id="app">
    <!-- 顶部导航栏 -->
    <header v-if="isAuthenticated">
      <nav class="navbar">
        <div class="navbar-brand">
          <router-link to="/" class="logo">
            <img :src="logo" alt="教育助手" />
            <span>教学实训智能体平台</span>
          </router-link>
        </div>

        <div class="navbar-menu">
          <div class="navbar-start">
            <!-- 根据用户角色显示导航 -->
            <router-link
              v-if="isTeacher"
              to="/teacher"
              class="navbar-item"
            >
              教师中心
            </router-link>
            <router-link
              v-if="isStudent"
              to="/student"
              class="navbar-item"
            >
              学习中心
            </router-link>
            <router-link
              v-if="isAdmin"
              to="/admin"
              class="navbar-item"
            >
              系统管理
            </router-link>
          </div>

          <div class="navbar-end">
            <div class="navbar-item">
              <div class="user-info" v-if="isAuthenticated">
                <el-avatar :size="32" :src="userAvatar" />
                <span class="username">{{ userName }}</span>
                <el-dropdown>
                  <span class="el-dropdown-link">
                    <i class="el-icon-arrow-down el-icon--right"></i>
                  </span>
                  <template #dropdown>
                    <el-dropdown-menu>
                      <el-dropdown-item @click="goToProfile">个人中心</el-dropdown-item>
                      <el-dropdown-item divided @click="logout">退出登录</el-dropdown-item>
                    </el-dropdown-menu>
                  </template>
                </el-dropdown>
              </div>
              <router-link v-else to="/login" class="button is-light">登录</router-link>
            </div>
          </div>
        </div>
      </nav>
    </header>

    <!-- 主要内容区域 -->
    <main class="main-content">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <!-- 全局页脚 -->
    <footer class="app-footer">
      <div class="content has-text-centered">
        <p>
          <strong>教学实训智能体平台</strong> © 2025 版权所有
        </p>
        <p>技术支持: edu-support@example.com</p>
      </div>
    </footer>

    <!-- 全局加载指示器 -->
    <div v-if="globalLoading" class="global-loading">
      <el-icon class="is-loading" color="#409EFF" :size="40">
        <Loading />
      </el-icon>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { Loading } from '@element-plus/icons-vue'

export default {
  name: 'App',
  components: { Loading },
  setup() {
    const store = useStore()
    const router = useRouter()
    const globalLoading = ref(false)

    // 计算用户状态
    const isAuthenticated = computed(() => store.getters['auth/isAuthenticated'])
    const userRole = computed(() => store.getters['auth/userRole'])
    const userName = computed(() => store.getters['auth/userName'] || '用户')
    const userAvatar = computed(() => store.getters['auth/userAvatar'] || require('@/assets/default-avatar.png'))

    // 角色判断
    const isTeacher = computed(() => userRole.value === 'teacher')
    const isStudent = computed(() => userRole.value === 'student')
    const isAdmin = computed(() => userRole.value === 'admin')

    // 使用默认logo
    const logo = computed(() => require('@/assets/logo.png'))

    // 初始化用户状态
    onMounted(async () => {
      try {
        globalLoading.value = true
        await store.dispatch('auth/checkAuthStatus')
      } catch (error) {
        console.error('初始化认证状态失败:', error)
      } finally {
        globalLoading.value = false
      }
    })

    // 导航到个人中心
    const goToProfile = () => {
      router.push('/profile')
    }

    // 退出登录
    const logout = async () => {
      try {
        globalLoading.value = true
        await store.dispatch('auth/logout')
        router.push('/login')
      } catch (error) {
        console.error('退出登录失败:', error)
      } finally {
        globalLoading.value = false
      }
    }

    return {
      logo,
      isAuthenticated,
      isTeacher,
      isStudent,
      isAdmin,
      userName,
      userAvatar,
      globalLoading,
      goToProfile,
      logout
    }
  }
}
</script>

<style scoped>
/* 全局样式保持不变 */
#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  font-family: 'Helvetica Neue', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 2rem;
  background-color: #2c3e50;
  color: white;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.logo {
  display: flex;
  align-items: center;
  color: white;
  text-decoration: none;
  font-weight: bold;
  font-size: 1.2rem;
}

.logo img {
  height: 40px;
  margin-right: 10px;
}

.navbar-menu {
  display: flex;
  flex-grow: 1;
  justify-content: space-between;
}

.navbar-start, .navbar-end {
  display: flex;
  align-items: center;
}

.navbar-item {
  color: white;
  text-decoration: none;
  margin: 0 15px;
  padding: 5px 10px;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.navbar-item:hover {
  background-color: rgba(255,255,255,0.1);
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.username {
  font-weight: 500;
}

.main-content {
  flex: 1;
  padding: 20px;
}

.app-footer {
  padding: 20px;
  background-color: #f5f5f5;
  text-align: center;
  border-top: 1px solid #eaeaea;
}

/* 页面切换动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 全局加载指示器 */
.global-loading {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}
</style>