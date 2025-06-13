<template>
    <div class="min-h-screen bg-black font-montserrat w-full flex flex-col justify-center items-center p-4">
        <!-- Registration Form -->
        <div class="w-full max-w-md p-6 rounded-lg backdrop-blur-sm border border-white">
            <h2 class="text-lg font-semibold text-white text-center mb-4">
                Регистрация
            </h2>

            <div v-if="errorMessage" class="p-3 mb-4 text-sm text-red-400 border border-red-400/50 rounded-lg bg-red-400/10" role="alert">
                {{ formatErrorMessage(errorMessage) }}
            </div>

            <form @submit.prevent="handleRegister" class="space-y-4">
                <div>
                    <label for="email" class="block text-sm font-medium text-white/80">
                        Почта
                    </label>
                    <input
                        v-model="email"
                        id="email"
                        type="email"
                        required
                        placeholder="Введи почту"
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
                        placeholder="Введи пароль"
                        class="mt-1 w-full px-3 py-2 border bg-black border-white rounded-lg focus:outline-none focus:border-white/50 text-white placeholder:text-white/50"
                    />
                </div>

                <button
                    type="submit"
                    class="w-full px-4 py-2 rounded-lg border border-white text-white hover:bg-white/20 transition-all duration-300"
                >
                    Зарегистрироваться
                </button>
            </form>

            <div class="mt-4 text-center text-sm">
                <span class="text-white/60">Уже есть аккаунт? </span>
                <router-link to="/login" class="text-white underline hover:text-white/80">
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
</script>