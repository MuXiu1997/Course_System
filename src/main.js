import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

import './axios'

import {
  Table,
  DatePicker,
  Select,
  Option,
  Drawer
} from 'iview'
import 'iview/dist/styles/iview.css'

import { InputNumber } from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'

Vue.component('Table', Table)
Vue.component('DatePicker', DatePicker)
Vue.component('Select', Select)
Vue.component('Option', Option)
Vue.component('Drawer', Drawer)

Vue.use(InputNumber)

Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
