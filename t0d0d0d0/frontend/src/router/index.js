import { createRouter, createWebHistory } from 'vue-router'
// import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import SignupView from '../views/SignupView.vue'
import OverView from '../views/OverView.vue'
import ProjectsView from '../views/ProjectsView.vue'
import TaskView from '../views/TaskView.vue'
import SettingsView from '../views/SettingsView.vue'
import LandingView from '../views/LandingView.vue'
// import test from '../views/test.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },    
    {
      path: '/signup',
      name: 'signup',
      component: SignupView
    },
    {
      path: '/overview',
      name: 'overview',
      component: OverView
    },
    {
      path: '/projects',
      name: 'projects',
      component: ProjectsView
    },
    {
      path: '/tasks',
      name: 'tasks',
      component: TaskView
    },
    {
      path: '/settings',
      name: 'settings',
      component: SettingsView
    },
    {
      path: '/',
      name: 'general',
      component: LandingView
    },

    // {
    //   path: '/about',
    //   name: 'about',
    //   // route level code-splitting
    //   // this generates a separate chunk (About.[hash].js) for this route
    //   // which is lazy-loaded when the route is visited.
    //   component: () => import('../views/AboutView.vue')
    // }
  ]
})

export default router
