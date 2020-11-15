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
    component: KeyWord
  },
  {
    path: '/Chart',
    name: 'Chart',
    component: Chart
  },
  {
    path: '/Tweet',
    name: 'Tweet',
    component: Tweet
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
