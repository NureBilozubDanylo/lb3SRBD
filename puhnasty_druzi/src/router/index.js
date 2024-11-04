import { createRouter, createWebHistory } from 'vue-router'
import Main from '../components/Main.vue'
import Login from '../components/Login.vue'
import Register from '../components/Register.vue'
import Category from '../components/Category.vue'
import AddNew from '../components/AddNew.vue'
import Statistic from '../components/Statistic.vue'
const routes = [
  {
    path: '/',
    name: 'main',
    component: Main
  },
  {
    path: '/cart',
    name: 'cart',
    component: Main
  },
  {
    path: '/login',
    name: 'login',
    component: Login
  },
  {
    path: '/register',
    name: 'register',
    component: Register
  },
  {
    path: '/category:id',
    name: 'category',
    component: Category
  },
  {
    path: '/statistic',
    name: 'statistic',
    component: Statistic
  },
  {
    path: '/add',
    name: 'add',
    component: AddNew
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
