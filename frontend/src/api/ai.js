// frontend/src/api/ai.js
import service from '@/utils/request'

export default {
  askQuestion(data) {
    return service.post('/ai/ask/', data)
  },
  evaluateAnswer(data) {
    return service.post('/ai/evaluate/', data)
  },
  generatePractice(data) {
    return service.post('/ai/practice/', data)
  },
  /**
   * @function designCourse
   * @description Calls the AI service to design course content based on syllabus and knowledge base.
   * @param {object} data - Object containing syllabus and knowledge_base_docs.
   * @param {string} data.syllabus - The course syllabus content.
   * @param {string} data.knowledge_base_docs - The knowledge base documents content.
   * @returns {Promise<object>} A promise that resolves with the designed course content.
   */
  designCourse(data) {
    return service.post('/ai/design_course/', data);
  },
  /**
   * @function generateAssessment
   * @description Calls the AI service to generate assessment questions based on teaching content.
   * @param {object} data - Object containing teaching_content.
   * @param {string} data.teaching_content - The teaching content for assessment generation.
   * @returns {Promise<object>} A promise that resolves with generated assessment questions.
   */
  generateAssessment(data) {
    return service.post('/ai/generate_assessment/', data);
  },
  /**
   * @function analyzeLearningData
   * @description Calls the AI service to analyze student learning data.
   * @param {object} data - Object containing student_practice_history.
   * @param {string} data.student_practice_history - The student's practice history data.
   * @returns {Promise<object>} A promise that resolves with learning analytics summary and suggestions.
   */
  analyzeLearningData(data) {
    return service.post('/ai/analyze_learning_data/', data);
  }
}