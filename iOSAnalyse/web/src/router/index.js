import Vue from 'vue'
import Router from 'vue-router'
import Index from '@/views/index'
import Compare from '@/views/compare'
import Module from '@/views/module'
import Login from '@/views/login'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: 'v1',
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: Login
    }, {
      path: '/',
      name: 'Index',
      component: Index
    }, {
      path: '/compare',
      name: 'Compare',
      component: Compare
    }, {
      path: '/module',
      name: 'Module',
      component: Module
    }
  ]
})
