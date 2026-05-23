/**
 * @module courses
 * @description Vuex module for managing course-related data and actions, including practice questions and AI evaluation.
 */
import coursesApi from '@/api/courses'

const state = {
  courses: [],
  currentCourse: null,
};

const mutations = {
  SET_COURSES(state, courses) {
    state.courses = courses;
  },
  SET_CURRENT_COURSE(state, course) {
    state.currentCourse = course;
  },
};

const actions = {
  /**
   * Fetches a list of all courses from the backend.
   * @param {object} context - Vuex action context.
   */
  async fetchCourses({ commit }) {
    try {
      const responseData = await coursesApi.getCourses();
      const courseList = responseData.results || responseData;
      commit('SET_COURSES', courseList);
      return courseList;
    } catch (error) {
      console.error('Error fetching courses:', error);
      // Re-throw the error to be caught by the component
      throw error;
    }
  },

  /**
   * Fetches the details of a single course by its ID.
   * @param {object} context - Vuex action context.
   * @param {string} courseId - The ID of the course to fetch.
   */
  async fetchCourseDetails({ commit }, courseId) {
    try {
      const responseData = await coursesApi.getCourseDetails(courseId);
      commit('SET_CURRENT_COURSE', responseData);
      return responseData;
    } catch (error) {
      console.error(`Error fetching course details for ID ${courseId}:`, error);
      throw error;
    }
  },

  /**
   * @action fetchPracticeQuestions
   * @description Dispatches a request to fetch practice questions for a course.
   * @param {object} context - Vuex action context.
   * @param {string} courseId - The ID of the course.
   * @returns {Promise<Array>} A promise that resolves with an array of practice questions.
   */
  async fetchPracticeQuestions(context, courseId) {
    return coursesApi.fetchPracticeQuestions(courseId);
  },

  /**
   * @action generatePracticeQuestions
   * @description Dispatches a request to generate new practice questions for a course using AI.
   * @param {object} context - Vuex action context.
   * @param {object} payload - Object containing courseId and count.
   * @param {string} payload.courseId - The ID of the course.
   * @param {number} payload.count - The number of questions to generate.
   * @returns {Promise<Array>} A promise that resolves with an array of generated practice questions.
   */
  async generatePracticeQuestions(context, payload) {
    return coursesApi.generatePracticeQuestions(payload);
  },

  /**
   * @action submitAnswer
   * @description Dispatches a request to submit a student's answer for AI evaluation.
   * @param {object} context - Vuex action context.
   * @param {object} payload - Object containing questionId and answer.
   * @param {string} payload.questionId - The ID of the question.
   * @param {string} payload.answer - The student's answer.
   * @returns {Promise<object>} A promise that resolves with the evaluation result.
   */
  async submitAnswer(context, payload) {
    return coursesApi.submitAnswer(payload);
  }
};

export default {
  namespaced: true,
  state,
  mutations,
  actions,
}; 