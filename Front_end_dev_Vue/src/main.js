import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

import VueCookie from 'vue-cookie'

import 'iview/dist/styles/iview.css'
import 'element-ui/lib/theme-chalk/index.css'

Vue.use(VueCookie)

Vue.config.productionTip = false

// noinspection JSUnusedGlobalSymbols
new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
