<template>
<div class="container mx-auto flex justify-center">
    <div class="max-w-sm sm:max-w-lg w-full space-y-5">
        
        <div class="text-base sm:text-lg font-semibold p-2 rounded-lg border border-gray-300 transition-all duration-300 hover:border-gray-100 hover:bg-gray-100 flex items-center justify-center">
            Деятельность
        </div>

        <div v-if="error_location" class="p-4 text-xs sm:text-sm text-center text-red-800 border border-red-300 rounded-lg bg-red-50" role="alert">
            <p>На сервере что-то сломалось, данные не достались из базы данных :(</p>
            <p><a href="https://t.me/pvlppv" class="text-blue-600 hover:text-blue-800">Напишите мне</a>, я починю.</p>
        </div>

        <div v-else class="px-6 py-4 sm:px-7 sm:py-5 border border-gray-300 rounded-lg">
            <div class="flex items-center justify-between space-x-3">
                <div class="flex items-center space-x-3">
                    <span class="relative flex h-3 w-3 ml-1.5">
                        <span class="animate-ping absolute h-full w-full rounded-full bg-green-500 opacity-75"></span>
                        <span class="relative rounded-full h-3 w-3 bg-green-500"></span>
                    </span>
                    <h1 class="text-xs sm:text-sm font-semibold">
                        Сейчас в {{ slicedLocation }}
                    </h1>
                </div>
                <span class="text-xs sm:text-sm text-gray-600 min-w-max">
                    {{ timeSince(renderedLocation.date) }}
                </span>
            </div>
            <div class="flex items-center mt-1 space-x-1">
                <svg class="v-5 h-5" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" style="fill: rgba(0, 0, 0, 1);">
                    <circle cx="12" cy="12" r="3"></circle>
                    <path d="M13 4.069V2h-2v2.069A8.008 8.008 0 0 0 4.069 11H2v2h2.069A8.007 8.007 0 0 0 11 19.931V22h2v-2.069A8.007 8.007 0 0 0 19.931 13H22v-2h-2.069A8.008 8.008 0 0 0 13 4.069zM12 18c-3.309 0-6-2.691-6-6s2.691-6 6-6 6 2.691 6 6-2.691 6-6 6z"></path>
                </svg>
                <p class="text-xs sm:text-sm">{{ statusMessage }}</p>
            </div>
            <div class="flex items-center mt-1 space-x-1">
                <svg class="v-5 h-5" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" style="fill: rgba(0, 0, 0, 1);">
                    <path d="M18.944 11.112C18.507 7.67 15.56 5 12 5 9.244 5 6.85 6.611 5.757 9.15 3.609 9.792 2 11.82 2 14c0 2.757 2.243 5 5 5h11c2.206 0 4-1.794 4-4a4.01 4.01 0 0 0-3.056-3.888zM18 17H7c-1.654 0-3-1.346-3-3 0-1.404 1.199-2.756 2.673-3.015l.581-.102.192-.558C8.149 8.274 9.895 7 12 7c2.757 0 5 2.243 5 5v1h1c1.103 0 2 .897 2 2s-.897 2-2 2z"></path>
                </svg>
                <p class="text-xs sm:text-sm">{{ renderedLocation.weather }}</p>
            </div>
            <div class="flex items-center mt-1 space-x-1">
                <svg class="v-5 h-5" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" style="fill: rgba(0, 0, 0, 1);">
                    <path d="M4 18h14c1.103 0 2-.897 2-2v-2h2v-4h-2V8c0-1.103-.897-2-2-2H4c-1.103 0-2 .897-2 2v8c0 1.103.897 2 2 2zM4 8h14l.002 8H4V8z"></path>
                </svg>
                <p class="text-xs sm:text-sm">На телефоне {{ renderedLocation.battery }}%</p>
            </div>
        </div>
    </div>
</div>
</template>

<script setup>
import { useFetch, timeSince } from '../composables/utils.js';
import { onMounted, computed } from 'vue';

const apiBaseUrl = import.meta.env.VITE_APP_API_BASE_URL;
const { data: location, error: error_location, fetchData: fetchData_location } = useFetch(`${apiBaseUrl}/api/location/`);

const props = defineProps({
    lastActivityName: String, // Receive the last activity name as a prop
});

const activityStatusMap = {
    'Работа': 'Работаю',
    'Учёба': 'Учусь',
    'Спорт': 'Тренируюсь',
    'Хобби': 'Занимаюсь хобби',
    'Люди': 'Общаюсь',
    'Быт': 'Занимаюсь бытом',
    'Дорога': 'В дороге',
    'Досуг': 'На досуге',
    'Тусовка': 'Тусуюсь',
    'Сон': 'Сплю',
    'Болезнь': 'Болею',
};

// Compute the status message based on the lastActivityName
const statusMessage = computed(() => {
    return activityStatusMap[props.lastActivityName];
});

onMounted(() => {
    fetchData_location();
});

const renderedLocation = computed(() => {
    return location.value ? location.value : {};
});

const slicedLocation = computed(() => {
    if (renderedLocation.value.location) {
        const parts = renderedLocation.value.location.split('\n');
        return parts.length >= 3 ? `${parts[0].trim()}, ${parts[2].trim()}` : renderedLocation.value.location;
    }
    return '';
});
</script>