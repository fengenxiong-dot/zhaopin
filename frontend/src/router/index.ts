import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: () => import('@/views/WorkbenchView.vue'),
      meta: { title: '工作台' },
    },
    {
      path: '/demands',
      component: () => import('@/views/PlaceholderView.vue'),
      meta: { title: '招聘需求', description: '管理招聘目标、参与HR和交付进度' },
    },
    {
      path: '/candidates',
      component: () => import('@/views/PlaceholderView.vue'),
      meta: { title: '候选人', description: '管理候选人初试、复试、Offer及报到流程' },
    },
    {
      path: '/resume-workloads',
      component: () => import('@/views/PlaceholderView.vue'),
      meta: { title: '简历推荐', description: '按日期、需求、渠道录入推荐简历数字' },
    },
    {
      path: '/dashboard',
      component: () => import('@/views/PlaceholderView.vue'),
      meta: { title: '数据看板', description: '查看工作量、招聘漏斗和Out原因分析' },
    },
  ],
})

export default router

