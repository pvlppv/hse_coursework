<template>
    <div class="min-h-screen bg-black font-montserrat w-full flex justify-center items-center p-4">
        <div class="max-w-sm w-full space-y-5 p-6 backdrop-blur-sm border border-white rounded-lg">
            <div class="text-center text-lg font-semibold text-white">
                Вход
            </div>
            
            <div v-if="errorMessage" class="p-3 text-sm text-red-400 border border-red-400/50 rounded-lg bg-red-400/10" role="alert">
                {{ formatErrorMessage(errorMessage) }}
            </div>

            <form @submit.prevent="handleLogin" class="space-y-4">
                <div>
                    <label for="email" class="block text-sm font-medium text-white/80">Почта</label>
                    <input
                        v-model="email"
                        id="email"
                        type="email"
                        required
                        placeholder="Введи почту"
                        class="mt-1 block w-full px-3 py-2 border bg-black border-white rounded-lg focus:outline-none focus:border-white/50 text-white placeholder:text-white/50"
                    />
                </div>

                <div>
                    <label for="password" class="block text-sm font-medium text-white/80 mt-4">Пароль</label>
                    <input
                        v-model="password"
                        id="password"
                        type="password"
                        required
                        placeholder="Введи пароль"
                        class="mt-1 block w-full px-3 py-2 border bg-black border-white rounded-lg focus:outline-none focus:border-white/50 text-white placeholder:text-white/50"
                    />
                </div>

                <button
                    type="submit"
                    class="mt-6 w-full px-4 py-2 rounded-lg border border-white text-white hover:bg-white/20 transition-all duration-300"
                >
                    Вход
                </button>
            </form>

            <div class="mt-4 text-center text-sm">
                <span class="text-white/60">Нет аккаунта? </span>
                <router-link to="/register" class="text-white underline hover:text-white/80">
                    Зарегистрироваться
                </router-link>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useFetch } from '../composables/utils.js';
import { useRouter } from 'vue-router';

const apiBaseUrl = import.meta.env.VITE_APP_API_BASE_URL;
const email = ref('');
const password = ref('');
const errorMessage = ref(null);
const router = useRouter();

const formatErrorMessage = (error) => {
    if (typeof error === 'string') {
        return error;
    }
    if (error && error.detail) {
        if (typeof error.detail === 'string') {
            switch (error.detail) {
                case 'REGISTER_USER_ALREADY_EXISTS':
                    return 'Пользователь с такой почтой уже существует.';
                case 'LOGIN_BAD_CREDENTIALS':
                case 'AUTH_COOKIE_NOT_FOUND':
                    return 'Неверная почта или пароль.';
                default:
                    return error.detail;
            }
        } else if (Array.isArray(error.detail)) {
            return error.detail.map(d => `${d.loc.join(' -> ')}: ${d.msg}`).join('; ');
        }
    }
    return 'Произошла неизвестная ошибка.';
};

onMounted(async () => {
    const { data: userData, fetchData: checkAuth } = useFetch(`${apiBaseUrl}/api/users/me`);
    await checkAuth();
    if (userData.value) {
        router.push('/profile');
    }
});

const handleLogin = async () => {
    errorMessage.value = null;

    const { error, fetchData } = useFetch(`${apiBaseUrl}/api/auth/jwt/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: {
            username: email.value,
            password: password.value
        },
        credentials: 'include'
    });

    await fetchData();

    if (error.value) {
        errorMessage.value = error.value;
        return;
    }

    router.push('/profile');
};

</script>
