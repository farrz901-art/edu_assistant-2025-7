import { createStore } from 'vuex'
import users from './modules/users'
import courses from './modules/courses'
import ai from './modules/ai'
import resource from './modules/resources'
import admin from './modules/admin'
import analytics from './modules/analytics'

export default createStore({
  modules: {
    users,
    ai,
    resource,
    admin,
    analytics,
    courses
  }
})