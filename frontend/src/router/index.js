import { createRouter, createWebHistory } from 'vue-router';
import Login from '../components/Login.vue';
import Register from '../components/Register.vue';
import Profile from '../components/Profile.vue';
import Hero from '../components/Hero.vue';
import Main from '../components/Main.vue';

const routes = [
  { path: '/', component: Hero, name: 'Hero' },
  { path: '/profile', component: Profile, name: 'Profile' },
  { path: '/login', component: Login, name: 'Login' },
  { path: '/register', component: Register, name: 'Register' },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
