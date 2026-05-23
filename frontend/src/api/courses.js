import service from '@/utils/request'

export default {
  // 获取课程列表
  getCourses() {
    return service.get('/courses/')
  },

  // 获取课程详情
  getCourseDetails(id) {
    return service.get(`/courses/${id}/`)
  },

  // 设计课程
  designCourse(data) {
    return service.post('/ai/design_course/', data)
  },

  // 选课/退课
  enrollCourse(courseId, action) {
    return service.post(`/courses/${courseId}/enroll/`, { action })
  },

  // 获取课程资源
  getCourseResources(courseId) {
    return service.get('/resources/', { params: { course_id: courseId } })
  },

  // 上传课程资源
  uploadResource(formData) {
    return service.post('/resources/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },

  /**
   * @function fetchPracticeQuestions
   * @description Fetches practice questions for a given course, potentially AI-generated.
   * @param {string} courseId - The ID of the course.
   * @returns {Promise<Array>} A promise that resolves with an array of practice questions.
   */
  fetchPracticeQuestions(courseId) {
    return service.post('/ai/practice/', { course_id: courseId });
  },

  /**
   * @function generatePracticeQuestions
   * @description Generates new practice questions using AI for a given course.
   * @param {object} data - Object containing courseId and count.
   * @param {string} data.courseId - The ID of the course.
   * @param {number} data.count - The number of questions to generate.
   * @returns {Promise<Array>} A promise that resolves with an array of generated practice questions.
   */
  generatePracticeQuestions(data) {
    return service.post('/ai/practice/', data);
  },

  /**
   * @function submitAnswer
   * @description Submits a student's answer for evaluation by AI.
   * @param {object} data - Object containing questionId and answer.
   * @param {string} data.questionId - The ID of the question.
   * @param {string} data.answer - The student's answer.
   * @returns {Promise<object>} A promise that resolves with the evaluation result.
   */
  submitAnswer(data) {
    return service.post('/ai/evaluate/', data);
  }
}