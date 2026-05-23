import service from '@/utils/request'

export default {
  getUserStats() {
    return service.get('/admin/stats/')
  },
  getSystemInfo() {
    return service.get('/admin/system/')
  },
  getActivityLogs() {
    return service.get('/admin/activity-logs/')
  },
  deactivateUser(userId) {
    return service.post(`/admin/users/${userId}/deactivate/`)
  },
  activateUser(userId) {
    return service.post(`/admin/users/${userId}/activate/`)
  },
  getUserCourses(userId) {
    return service.get(`/admin/users/${userId}/enrolled_courses/`)
  },
  getUsers() {
    return service.get('/admin/users/')
  }
}