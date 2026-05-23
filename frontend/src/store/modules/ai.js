// frontend/src/store/modules/ai.js
import aiApi from '@/api/ai'

export default {
  namespaced: true,
  actions: {
    askQuestion(context, payload) {
      return aiApi.askQuestion(payload)
    },
    evaluateAnswer(context, payload) {
      return aiApi.evaluateAnswer(payload)
    },
    generatePractice(context, payload) {
      return aiApi.generatePractice(payload)
    },
    /**
     * @action designCourse
     * @description Dispatches a request to the AI service to design course content.
     * @param {object} context - Vuex action context.
     * @param {object} payload - Object containing syllabus and knowledge_base_docs.
     * @returns {Promise<object>} A promise that resolves with the designed course content.
     */
    async designCourse(context, payload) {
      return aiApi.designCourse(payload);
    },
    /**
     * @action generateAssessment
     * @description Dispatches a request to the AI service to generate assessment questions.
     * @param {object} context - Vuex action context.
     * @param {object} payload - Object containing teaching_content.
     * @returns {Promise<object>} A promise that resolves with generated assessment questions.
     */
    async generateAssessment(context, payload) {
      return aiApi.generateAssessment(payload);
    },
    /**
     * @action analyzeLearningData
     * @description Dispatches a request to the AI service to analyze student learning data.
     * @param {object} context - Vuex action context.
     * @param {object} payload - Object containing student_practice_history.
     * @returns {Promise<object>} A promise that resolves with learning analytics summary and suggestions.
     */
    async analyzeLearningData(context, payload) {
      return aiApi.analyzeLearningData(payload);
    }
  }
}