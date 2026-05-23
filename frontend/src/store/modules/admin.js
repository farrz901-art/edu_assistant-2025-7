import adminApi from '@/api/admin'

export default {
  namespaced: true,
  state: {
    stats: {},
    systemInfo: {},
    activityLogs: [],
    users: []
  },
  mutations: {
    SET_STATS(state, stats) {
      state.stats = stats
    },
    SET_SYSTEM_INFO(state, systemInfo) {
      state.systemInfo = systemInfo
    },
    SET_ACTIVITY_LOGS(state, logs) {
      state.activityLogs = logs
    },
    SET_USERS(state, users) {
      state.users = users
    },
    UPDATE_USER_STATUS(state, { userId, isActive }) {
      const user = state.users.find(u => u.id === userId)
      if (user) {
        user.is_active = isActive
      }
    }
  },
  actions: {
    async fetchUserStats({ commit }) {
      try {
        const response = await adminApi.getUserStats()
        commit('SET_STATS', response.data)
      } catch (error) {
        console.error('获取统计失败:', error)
      }
    },
    async fetchSystemInfo({ commit }) {
      try {
        const response = await adminApi.getSystemInfo()
        commit('SET_SYSTEM_INFO', response.data)
      } catch (error) {
        console.error('获取系统信息失败:', error)
      }
    },
    async fetchActivityLogs({ commit }) {
      try {
        const response = await adminApi.getActivityLogs()
        commit('SET_ACTIVITY_LOGS', response.data)
      } catch (error) {
        console.error('获取活动日志失败:', error)
      }
    },
    async fetchUsers({ commit }) {
      try {
        const response = await adminApi.getUsers()
        commit('SET_USERS', response.data)
      } catch (error) {
        console.error('获取用户列表失败:', error)
      }
    },
    async deactivateUser({ commit }, userId) {
      try {
        await adminApi.deactivateUser(userId)
        commit('UPDATE_USER_STATUS', { userId, isActive: false })
      } catch (error) {
        console.error('停用用户失败:', error)
        throw error
      }
    },
    async activateUser({ commit }, userId) {
      try {
        await adminApi.activateUser(userId)
        commit('UPDATE_USER_STATUS', { userId, isActive: true })
      } catch (error) {
        console.error('启用用户失败:', error)
        throw error
      }
    }
  }
}