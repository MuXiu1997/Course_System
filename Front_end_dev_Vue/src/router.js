import Vue from 'vue'
import Router from 'vue-router'
import store from './store'
import VueCookie from 'vue-cookie'
import { postToken } from './api'

Vue.use(Router)

const router = new Router({
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

router.beforeEach(async (to, from, next) => {
  if (store.getters.getToken === null) {
    let userName = VueCookie.get('userName')
    let password = VueCookie.get('password')
    if (userName && password) {
      let response = await postToken({
        userName: userName,
        password: password
      })
      await store.dispatch('setToken', response.data.token)
      VueCookie.set('token', response.data.token, 1)
      next()
    } else {
      next()
    }
  } else {
    next()
  }
})

router.beforeEach((to, from, next) => {
  if (store.getters.getToken !== null) {
    if (to.name === 'login') {
      next({ name: 'schedule' })
    } else {
      next()
    }
  } else {
    if (to.meta.login) {
      next({ name: 'login' })
    } else {
      next()
    }
  }
})

export default router
