<template>
    <div class="h-screen w-full flex flex-col justify-center items-center">
        <!-- Hero Text -->
        <div class="max-w-lg text-center mb-14 px-4">
            <h1 class="text-2xl sm:text-3xl font-bold text-gray-800">
                Привет ещё раз ахаха
            </h1>
            <p class="mt-4 text-sm sm:text-base text-gray-600 leading-relaxed">
                Зарегистрируйся ниже и отпиши мне, я приму тебя, а после переходи в логин (pvlppv.ru/login), логинься, и тебя перекинет на твою личную страницу, где ты уже сможешь настроить весь функционал.
            </p>
        </div>

        <!-- Registration Form -->
        <div class="w-full max-w-md bg-white p-6 rounded-lg shadow-lg">
            <h2 class="text-lg font-semibold text-gray-800 text-center mb-4">
                Регистрация
            </h2>

            <form @submit.prevent="handleRegister" class="space-y-4">
                <!-- <div>
                    <label for="username" class="block text-sm font-medium text-gray-700">
                        Имя пользователя
                    </label>
                    <input
                        v-model="username"
                        id="username"
                        type="text"
                        required
                        placeholder="Введите имя пользователя"
                        class="mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-gray-600"
                    />
                </div> -->

                <div>
                    <label for="email" class="block text-sm font-medium text-gray-700">
                        Почта
                    </label>
                    <input
                        v-model="email"
                        id="email"
                        type="email"
                        required
                        placeholder="Введите почту"
                        class="mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-gray-600"
                    />
                </div>

                <div>
                    <label for="password" class="block text-sm font-medium text-gray-700">
                        Пароль
                    </label>
                    <input
                        v-model="password"
                        id="password"
                        type="password"
                        required
                        placeholder="Введите пароль"
                        class="mt-1 w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-gray-600"
                    />
                </div>

                <button
                    type="submit"
                    class="w-full px-4 py-2 rounded-lg border border-gray-300 transition-all duration-300 hover:border-gray-100 hover:bg-gray-100"
                >
                    Регистрация
                </button>
            </form>

            <div class="mt-4 text-center text-sm">
                <span class="text-gray-600">Уже есть аккаунт? </span>
                <router-link to="/login" class="text-gray-600 underline">
                    Войти
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
const username = ref('');
const errorMessage = ref(null);
const router = useRouter();

onMounted(async () => {
    const { data: userData, fetchData: checkAuth } = useFetch(`${apiBaseUrl}/api/users/me`);
    await checkAuth();
    if (userData.value) {
        router.push('/profile');
    }
});

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

        router.push('/login');
    } catch (error) {
        errorMessage.value = error.message;
    }
};
</script>