import { createRouter, createWebHashHistory } from 'vue-router'

const routes = [
  { 
    path: '/',
    name: 'home',
    component: () => import('../views/Home.vue')
  },
  {
    path: '/search/:q',
    name:'search',
    component: () => import('../views/Search.vue'),
    props: true
  },
  {
    path: '/play/:songid/:title/:artist/:album/:cover/:publishTime',
    name: 'play',
    component: () => import('../views/Play.vue'),
    props: true
  }
]

const router = createRouter({
  history: createWebHashHistory(process.env.BASE_URL),
  routes,
})

export default router
