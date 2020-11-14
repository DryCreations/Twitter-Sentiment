import Vue from 'vue'
import VueRouter from 'vue-router'
import Tweet from '../views/Tweet.vue'
import Chart from '../views/Chart.vue'
import KeyWord from '../views/KeyWord.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Tweet
  },
  {
    path: '/Chart',
    name: 'Chart',
    component: Chart
  },
  {
    path: '/KeyWord',
    name: 'KeyWord',
    component: KeyWord
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
