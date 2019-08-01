import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

import axios from 'axios'

import VueCookie from 'vue-cookie'

import 'iview/dist/styles/iview.css'
import 'element-ui/lib/theme-chalk/index.css'

// noinspection JSUnusedGlobalSymbols
Vue.prototype.$axios = axios

Vue.use(VueCookie)

Vue.config.productionTip = false

let token = VueCookie.get('Token')

store.dispatch('setToken', token).then()

router.beforeEach((to, from, next) => {
  if (store.getters.getToken) {
    if (to.path === '/login') {
      next({ path: '/' })
    } else {
      next()
    }
  } else {
    if (to.meta.login) {
      next('/login')
    } else {
      next()
    }
  }
})

// noinspection JSUnusedGlobalSymbols
new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
