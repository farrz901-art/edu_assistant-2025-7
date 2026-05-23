// frontend/src/store/modules/analytics.js
import analyticsApi from '@/api/analytics'

export default {
  namespaced: true,
  state: {
    analytics: null
  },
  mutations: {
    setAnalytics(state, analytics) {
      state.analytics = analytics
    }
  },
  actions: {
    async fetchCourseAnalytics({ commit }, courseId) {
      const response = await analyticsApi.getAnalytics(courseId)
      commit('setAnalytics', response.data)
      return response.data
    }
  }
}