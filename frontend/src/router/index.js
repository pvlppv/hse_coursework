import { createRouter, createWebHistory } from 'vue-router';
import pvlppv from '../components/pvlppv.vue';
import BlogPage from '../components/BlogPage.vue';
import Post from '../components/Post.vue';
import Login from '../components/Login.vue';
import Register from '../components/Register.vue';
import DatabaseFull from '../components/DatabaseFull.vue';
import Profile from '../components/Profile.vue';
import Hero from '../components/Hero.vue';
import Main from '../components/Main.vue';

const routes = [
  { path: '/', component: Hero, name: 'Hero' },
  { path: '/profile', component: Profile, name: 'Profile' },
  { path: '/login', component: Login, name: 'Login' },
  { path: '/register', component: Register, name: 'Register' },

  { path: '/pvlppv', component: pvlppv, name: 'pvlppv' },
  { path: '/pvlppv/blog', component: BlogPage, name: 'BlogPage' },
  { path: '/pvlppv/blog/:id', component: Post, name: 'Post' },
  { path: '/pvlppv/database', component: DatabaseFull, name: 'Database' },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
