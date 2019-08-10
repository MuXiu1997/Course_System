import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/schedule',
      name: 'schedule',
      meta: { login: true },
      component: () => import(/* webpackChunkName: "schedule" */'@/views/Schedule/index')
    },
    {
      path: '/login',
      alias: '/',
      name: 'login',
      meta: { login: false },
      component: () => import(/* webpackChunkName: "login" */'@/views/Login.vue')
    }
  ]
})
