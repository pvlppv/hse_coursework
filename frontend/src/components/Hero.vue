<template>
  <div class="min-h-screen bg-black font-montserrat w-full overflow-hidden">
    <nav 
      class="fixed w-full top-0 z-50 border-white/10 backdrop-blur-sm transition-transform duration-300"
      :class="{'transform -translate-y-full': !isNavbarVisible}"
    >
      <div class="container mx-auto px-6 h-20 flex items-center justify-between">
        <img src="../assets/thoughty_logo.svg" alt="Соти" class="w-24 h-24 sm:w-32 sm:h-32">
        <router-link 
          to="/profile"
          class="border border-white px-5 py-1.5 rounded-lg text-white text-base sm:text-lg hover:bg-white/10 transition-colors duration-500 group"
        >
          <span class="relative z-10 flex items-center gap-2">
            Войти
            <svg class="w-5 h-5 transition-transform duration-500 group-hover:translate-x-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3"/>
            </svg>
          </span>
        </router-link>

      </div>
    </nav>

    <!-- Main Content -->
    <main class="w-full h-screen flex flex-col items-center justify-center relative">
      <!-- Glow Effect -->
      <div class="absolute inset-0 overflow-hidden z-0">
        <div class="absolute w-[400%] h-[400%] sm:w-[200%] sm:h-[200%] top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 opacity-10">
          <div class="animate-gradient-rotate bg-gradient-to-r from-white via-transparent to-white h-full w-full"></div>
        </div>
      </div>

      <!-- Text Content -->
      <div class="relative z-10 text-center space-y-6 sm:space-y-8">
        <!-- Glow Spot Behind Text -->
        <div class="absolute -inset-16 bg-white/10 blur-3xl rounded-full"></div>

        <h1 class="text-5xl sm:text-7xl font-bold text-white">
          Становись
        </h1>
        
        <div class="inline-block border-2 sm:border-4 border-white rounded-2xl sm:rounded-3xl px-8 sm:px-12 py-4 sm:py-6 backdrop-blur-sm">
          <h1 class="text-5xl sm:text-7xl font-bold text-white">
            Осознаннее
          </h1>
        </div>

        <h1 class="text-5xl sm:text-7xl font-bold text-white">
          с Соти
        </h1>
      </div>

      <!-- Animated Arrow -->
      <div class="absolute bottom-12 animate-bounce z-20">
        <svg class="w-12 h-12 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3"/>
        </svg>
      </div>
    </main>

    <!-- Registration Section -->
    <section class="min-h-screen w-full bg-black flex flex-col items-center justify-center px-4 sm:px-8 py-12">
      <!-- Hero Text -->
      <div class="max-w-lg text-center mb-8 sm:mb-14 px-4">
        <h1 class="text-2xl sm:text-3xl font-bold text-white">
          Привет ещё раз
        </h1>
        <p class="mt-4 text-sm sm:text-base text-white/80 leading-relaxed">
          Зарегистрируйся ниже и <a href="https://t.me/pvlppv" class="text-white underline">отпиши мне</a>, я приму тебя, а после переходи на свою <router-link to="/profile" class="text-white underline">личную страницу</router-link>, где ты уже сможешь настроить весь функционал
        </p>
      </div>

      <!-- Registration Form -->
      <div class="w-full max-w-md p-6 rounded-lg backdrop-blur-sm border border-white">
        <h2 class="text-lg font-semibold text-white text-center mb-4">
          Регистрация
        </h2>

        <form @submit.prevent="handleRegister" class="space-y-4">
          <!-- <div>
            <label for="username" class="block text-sm font-medium text-white/80">
              Имя пользователя
            </label>
            <input
              v-model="username"
              id="username"
              type="text"
              required
              placeholder="Введите имя пользователя"
              class="mt-1 w-full px-3 py-2 border bg-black border-white rounded-lg focus:outline-none focus:border-white/50 text-white placeholder:text-white/50"
            />
          </div> -->

          <div>
            <label for="email" class="block text-sm font-medium text-white/80">
              Почта
            </label>
            <input
              v-model="email"
              id="email"
              type="email"
              required
              placeholder="Введите почту"
              class="mt-1 w-full px-3 py-2 border bg-black border-white rounded-lg focus:outline-none focus:border-white/50 text-white placeholder:text-white/50"
            />
          </div>

          <div>
            <label for="password" class="block text-sm font-medium text-white/80">
              Пароль
            </label>
            <input
              v-model="password"
              id="password"
              type="password"
              required
              placeholder="Введите пароль"
              class="mt-1 w-full px-3 py-2 border bg-black border-white rounded-lg focus:outline-none focus:border-white/50 text-white placeholder:text-white/50"
            />
          </div>

          <button
            type="submit"
            class="w-full px-4 py-2 rounded-lg border border-white text-white hover:bg-white/20 transition-all duration-300"
          >
            Зарегестрироваться
          </button>
        </form>

        <div class="mt-4 text-center text-sm">
          <span class="text-white/60">Уже есть аккаунт? </span>
          <router-link to="/login" class="text-white underline hover:text-white/80">
            Войти
          </router-link>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useFetch } from '../composables/utils.js';
import { useRouter } from 'vue-router';

const apiBaseUrl = import.meta.env.VITE_APP_API_BASE_URL;
const email = ref('');
const password = ref('');
const username = ref('');
const errorMessage = ref(null);
const router = useRouter();
const isNavbarVisible = ref(true)
let lastScrollPosition = 0

const handleRegister = async () => {
    errorMessage.value = null;
    
    const { error, fetchData } = useFetch(`${apiBaseUrl}/api/auth/register`, {
        method: 'POST',
        headers: { 
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        body: {
            email: email.value,
            password: password.value,
            username: username.value,
            is_active: true,
            is_superuser: false,
            is_verified: false
        },
        credentials: 'include'
    });

    try {
        await fetchData();

        if (error.value) {
            errorMessage.value = error.value;
            return;
        }

        // After successful registration, log in automatically
        const { error: loginError, fetchData: loginFetch } = useFetch(`${apiBaseUrl}/api/auth/jwt/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: {
                username: email.value,
                password: password.value
            },
            credentials: 'include'
        });

        await loginFetch();

        if (loginError.value) {
            errorMessage.value = loginError.value;
            return;
        }

        router.push('/profile');
    } catch (error) {
        errorMessage.value = error.message;
    }
};
const handleScroll = () => {
  const currentScrollPosition = window.scrollY || document.documentElement.scrollTop
  
  if (currentScrollPosition < 0) return
  if (Math.abs(currentScrollPosition - lastScrollPosition) < 60) return
  
  isNavbarVisible.value = currentScrollPosition < lastScrollPosition
  lastScrollPosition = currentScrollPosition
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style>
@keyframes gradient-rotate {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.animate-gradient-rotate {
  animation: gradient-rotate 20s linear infinite;
}
</style>