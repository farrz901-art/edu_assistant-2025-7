import axios from 'axios'

const service = axios.create({
  baseURL: process.env.VUE_APP_API_BASE_URL,
  timeout: 30000
})

// 请求拦截器
service.interceptors.request.use(
  config => {
    // 添加请求ID用于跟踪
    config.headers['X-Request-ID'] = Date.now()

    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  response => {
    // 处理标准响应
    return response.data
  },
  error => {
    // 处理HTTP错误
    if (error.response) {
      // {{ edit_1 }}
      const { data } = error.response // 移除对 'status' 的解构赋值

      if (data && data.error) {
        return Promise.reject(new Error(data.error))
      }
    }

    return Promise.reject(error)
  }
)

// API模块 - 根据后端调整更新
const api = {
  courses: {
    list: () => service.get('/courses/'),
    detail: (id) => service.get(`/courses/${id}/`),
    design: (data) => service.post('/courses/design/', data),
    exercises: (courseId) => service.get(`/courses/${courseId}/exercises/`),
    teacherCourses: () => service.get('/courses/teacher/')
  },
  ai: {
    ask: (data) => service.post('/ai/ask/', data),
    evaluate: (data) => service.post('/ai/evaluate/', data),
    practice:  (data) => service.post('/ai/practice/', data),
    generatePractice: (data) => service.post('/ai/practice/', data),
  },
  analytics: {
    get: (courseId) => service.get(`/analytics/?course_id=${courseId}`)
  },
  resources: {
    list:    (params) => service.get('/resources/', { params }),
    upload:  (formData) => service.post('/resources/', formData, { headers: { 'Content-Type': 'multipart/form-data' } }),
    download:(id) => service.get(`/resources/${id}/download/`, { responseType: 'blob' }),
    export:  (ids) => service.post('/resources/export/', { ids }, { responseType: 'blob' })
  },
  admin: {
    systemInfo: () => service.get('/admin/system/'),
  }

}

export default api