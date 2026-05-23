// frontend/src/api/analytics.js
import service from '@/utils/request'

export default {
  getAnalytics(courseId) {
    return service.get(`/analytics/?course_id=${courseId}`)
  }
}