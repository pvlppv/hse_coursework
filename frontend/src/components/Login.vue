<template>
    <div class="min-h-screen w-full flex justify-center items-center">
        <div class="max-w-sm w-full space-y-5 p-6 bg-white rounded-lg shadow-lg mx-4">
            <div class="text-center text-lg font-semibold">
                Вход
            </div>
            
            <div v-if="errorMessage" class="p-4 text-sm text-red-800 border border-red-300 rounded-lg bg-red-50" role="alert">
                {{ errorMessage }}
            </div>

            <form @submit.prevent="handleLogin">
                <label for="email" class="block text-sm font-medium text-gray-700">Почта</label>
                <input
                    v-model="email"
                    id="email"
                    type="email"
                    required
                    class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-gray-600"
                />

                <label for="password" class="block text-sm font-medium text-gray-700 mt-4">Пароль</label>
                <input
                    v-model="password"
                    id="password"
                    type="password"
                    required
                    class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-gray-600"
                />

                <button
                    type="submit"
                    class="mt-6 w-full px-4 py-2 rounded-lg focus:outline-none border border-gray-300 transition-all duration-300 hover:border-gray-100 hover:bg-gray-100"
                >
                    Вход
                </button>
            </form>
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
