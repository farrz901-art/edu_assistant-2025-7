import coursesApi from '@/api/courses'

export default {
  namespaced: true,
  state: {
    courses: [],
    currentCourse: null,
    courseResources: []
  },
  mutations: {
    SET_COURSES(state, courses) {
      state.courses = courses
    },
    SET_CURRENT_COURSE(state, course) {
      state.currentCourse = course
    },
    SET_COURSE_RESOURCES(state, resources) {
      state.courseResources = resources
    },
    ADD_COURSE_RESOURCE(state, resource) {
      state.courseResources.push(resource)
    }
  },
  actions: {
    // 获取课程列表
    async fetchCourses({ commit }) {
      try {
        const response = await coursesApi.getCourses()
        commit('SET_COURSES', response.results)
        return response
      } catch (error) {
        console.error('fetchCourses failed:', error)
        throw error
      }
    },

    // 获取课程详情
    async fetchCourseDetail({ commit }, courseId) {
      try {
        const response = await coursesApi.getCourseDetail(courseId)
        commit('SET_CURRENT_COURSE', response)
        return response
      } catch (error) {
        console.error('fetchCourseDetail failed:', error)
        throw error
      }
    },

    // 设计课程
    async designCourse(context, courseData) {
      try {
        const response = await coursesApi.designCourse(courseData)
        return response
      } catch (error) {
        console.error('designCourse failed:', error)
        throw error
      }
    },

    // 选课/退课
    async enrollCourse(context, { courseId, action }) {
      try {
        const response = await coursesApi.enrollCourse(courseId, action)
        return response
      } catch (error) {
        console.error('enrollCourse failed:', error)
        throw error
      }
    },

    // 获取课程资源
    async fetchCourseResources({ commit }, courseId) {
      try {
        const response = await coursesApi.getCourseResources(courseId)
        commit('SET_COURSE_RESOURCES', response)
        return response
      } catch (error) {
        console.error('fetchCourseResources failed:', error)
        throw error
      }
    },

    // 上传资源
    async uploadResource({ commit }, formData) {
      try {
        const response = await coursesApi.uploadResource(formData)
        commit('ADD_COURSE_RESOURCE', response)
        return response
      } catch (error) {
        console.error('uploadResource failed:', error)
        throw error
      }
    }
  }
}