import { createRouter, createWebHistory } from 'vue-router'

// 导入布局组件
import TeacherLayout from '@/views/layouts/TeacherLayout.vue'
import StudentLayout from '@/views/layouts/StudentLayout.vue'
import AdminLayout from '@/views/layouts/AdminLayout.vue'

// 导入页面组件
import Home from '@/views/Home.vue'; // 新增导入 Home 页面
import Design from '@/views/Teacher/Design.vue'
import Practice from '@/views/Student/Practice.vue'
import AdminDashboard from '@/views/Admin/Dashboard.vue'
import UserManagement from '@/views/Admin/UserManagement.vue'
import SystemMonitor from '@/views/Admin/SystemMonitor.vue'
import TeacherHome from '@/views/Teacher/Home.vue'
import Assessment from '@/views/Teacher/Assessment.vue'
import StudentHome from '@/views/Student/Home.vue'
import Assistant from '@/views/Student/Assistant.vue'
import Analytics from '@/views/Teacher/Analytics.vue'

const routes = [
  {
    path: '/',
    name: 'Home', // 设置 Home 页面为根路径
    component: Home
  },
  {
    path: '/teacher',
    component: TeacherLayout,
    meta: { role: 'teacher' },
    redirect: '/teacher',
    children: [
      { path: '', name: 'TeacherHome', component: TeacherHome },
      { path: 'design', name: 'CourseDesign', component: Design },
      { path: 'assessment', name: 'Assessment', component: Assessment },
      { path: 'analytics', name: 'Analytics', component: Analytics }
    ]
  },
  {
    path: '/student',
    component: StudentLayout,
    meta: { role: 'student' },
    children: [
      { path: '', name: 'StudentHome', component: StudentHome },
      { path: 'assistant/:courseId?', name: 'StudentAssistant', component: Assistant, props: true },
      { path: 'practice/:courseId?', name: 'StudentPractice', component: Practice, props: true }
    ]
  },
  {
    path: '/admin',
    component: AdminLayout,
    meta: { role: 'admin' },
    children: [
      { path: '', name: 'AdminDashboard', component: AdminDashboard }, // 管理员默认页直接是 Dashboard
      { path: 'users', name: 'UserManagement', component: UserManagement },
      { path: 'system', name: 'SystemMonitor', component: SystemMonitor }
    ]
  },
  {
    path: '/:pathMatch(.*)*', // 保持未匹配路径重定向，可以重定向到 Home
    redirect: '/'
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router