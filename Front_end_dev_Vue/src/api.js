import axios from 'axios'

import store from './store'

let request = axios.create()

export function postToken (data, time) {
  return request({
    url: `/api/tokens/${time}`,
    method: 'post',
    data: data
  })
}

export function getWorkdays () {
  return request({
    url: '/api/workdays',
    method: 'get',
    headers: {
      'Authorization': store.getters.getToken
    }
  })
}

export function getSchedules () {
  return request({
    url: '/api/schedules',
    method: 'get',
    headers: {
      'Authorization': store.getters.getToken
    }
  })
}

export function postNewClassName (newClassName) {
  return request({
    url: `/api/schedules/${newClassName}`,
    method: 'post',
    headers: {
      'Authorization': store.getters.getToken
    }
  })
}

export function postSchedules (data) {
  return request({
    url: '/api/schedules',
    method: 'post',
    data: data,
    headers: {
      'Authorization': store.getters.getToken
    }
  })
}

export function postXlsx (data) {
  return request({
    url: '/xlsx',
    method: 'post',
    data: data,
    responseType: 'blob',
    headers: {
      'Authorization': store.getters.getToken
    }
  })
}
