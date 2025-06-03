<template>
    <div class="container mx-auto flex justify-center">
      <div class="max-w-sm sm:max-w-lg w-full space-y-5">
        
        <div class="text-base sm:text-lg font-semibold p-2 rounded-lg border border-gray-300 transition-all duration-300 hover:border-gray-100 hover:bg-gray-100 flex items-center justify-center">
            Статистика
        </div>

        <div v-if="error_location || error_health" class="p-4 text-xs sm:text-sm text-center text-red-800 border border-red-300 rounded-lg bg-red-50" role="alert">
            <p>На сервере что-то сломалось, данные не достались из базы данных :(</p>
            <p><a href="https://t.me/pvlppv" class="text-blue-600 hover:text-blue-800">Напишите мне</a>, я починю.</p>
        </div>

        <div v-else class="space-y-5">
            
            <!-- Status Card -->
            <div class="px-6 py-4 sm:px-7 sm:py-5 border border-gray-300 rounded-lg">
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

            <!-- Health Card -->
            <div class="px-6 py-4 sm:px-7 sm:py-5 border border-gray-300 rounded-lg">
                <div class="flex items-center justify-between space-x-3">
                    <div class="flex items-center mt-1 space-x-1">
                        <svg class="v-5 h-5" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" style="fill: rgba(0, 0, 0, 1);">
                            <circle cx="12" cy="4" r="2"></circle>
                            <path d="M15 22V9h5V7H4v2h5v13h2v-7h2v7z"></path>
                        </svg>
                        <p class="text-xs sm:text-sm">{{ renderedHealth.height }} см, {{ renderedHealth.weight }} кг</p>
                    </div>
                    <span class="text-xs sm:text-sm text-gray-600 min-w-max">
                        {{ timeSince(renderedHealth.date) }}
                    </span>
                </div>
                <div class="flex items-center mt-1 space-x-1">
                    <svg class="v-5 h-5" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" style="fill: rgba(0, 0, 0, 1);">
                        <path d="M16.97 4.757a.999.999 0 0 0-1.918-.073l-3.186 9.554-2.952-6.644a1.002 1.002 0 0 0-1.843.034L5.323 12H2v2h3.323c.823 0 1.552-.494 1.856-1.257l.869-2.172 3.037 6.835c.162.363.521.594.915.594l.048-.001a.998.998 0 0 0 .9-.683l2.914-8.742.979 3.911A1.995 1.995 0 0 0 18.781 14H22v-2h-3.22l-1.81-7.243z"></path>
                    </svg>
                    <p class="text-xs sm:text-sm">{{ renderedHealth.heart_rate }} уд/мин в среднем</p>
                </div>
                <div class="flex items-center mt-1 space-x-1">
                    <svg class="v-5 h-5" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" style="fill: rgba(0, 0, 0, 1);">
                        <path d="M20.98 11.802a.995.995 0 0 0-.738-.771l-6.86-1.716 2.537-5.921a.998.998 0 0 0-.317-1.192.996.996 0 0 0-1.234.024l-11 9a1 1 0 0 0 .39 1.744l6.719 1.681-3.345 5.854A1.001 1.001 0 0 0 8 22a.995.995 0 0 0 .6-.2l12-9a1 1 0 0 0 .38-.998z"></path>
                    </svg>
                    <p class="text-xs sm:text-sm">{{ renderedHealth.energy }} ккал</p>
                </div>
                <div class="flex items-center mt-1 space-x-1">
                    <svg class="v-5 h-5" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" style="fill: rgba(0, 0, 0, 1);">
                        <circle cx="13" cy="4" r="2"></circle>
                        <path d="M13.978 12.27c.245.368.611.647 1.031.787l2.675.892.633-1.896-2.675-.892-1.663-2.495a2.016 2.016 0 0 0-.769-.679l-1.434-.717a1.989 1.989 0 0 0-1.378-.149l-3.193.797a2.002 2.002 0 0 0-1.306 1.046l-1.794 3.589 1.789.895 1.794-3.589 2.223-.556-1.804 8.346-3.674 2.527 1.133 1.648 3.675-2.528c.421-.29.713-.725.82-1.225l.517-2.388 2.517 1.888.925 4.625 1.961-.393-.925-4.627a2 2 0 0 0-.762-1.206l-2.171-1.628.647-3.885 1.208 1.813z"></path>
                    </svg>
                    <p class="text-xs sm:text-sm">{{ renderedHealth.steps }} шагов</p>
                </div>
                <div class="flex items-center mt-1 space-x-1">
                    <svg class="v-5 h-5" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" style="fill: rgba(0, 0, 0, 1);">
                        <path d="M5.996 9c1.413 0 2.16-.747 2.705-1.293.49-.49.731-.707 1.292-.707s.802.217 1.292.707C11.83 8.253 12.577 9 13.991 9c1.415 0 2.163-.747 2.71-1.293.491-.49.732-.707 1.295-.707s.804.217 1.295.707C19.837 8.253 20.585 9 22 9V7c-.563 0-.804-.217-1.295-.707C20.159 5.747 19.411 5 17.996 5s-2.162.747-2.709 1.292c-.491.491-.731.708-1.296.708-.562 0-.802-.217-1.292-.707C12.154 5.747 11.407 5 9.993 5s-2.161.747-2.706 1.293c-.49.49-.73.707-1.291.707s-.801-.217-1.291-.707C4.16 5.747 3.413 5 2 5v2c.561 0 .801.217 1.291.707C3.836 8.253 4.583 9 5.996 9zm0 5c1.413 0 2.16-.747 2.705-1.293.49-.49.731-.707 1.292-.707s.802.217 1.292.707c.545.546 1.292 1.293 2.706 1.293 1.415 0 2.163-.747 2.71-1.293.491-.49.732-.707 1.295-.707s.804.217 1.295.707C19.837 13.253 20.585 14 22 14v-2c-.563 0-.804-.217-1.295-.707-.546-.546-1.294-1.293-2.709-1.293s-2.162.747-2.709 1.292c-.491.491-.731.708-1.296.708-.562 0-.802-.217-1.292-.707C12.154 10.747 11.407 10 9.993 10s-2.161.747-2.706 1.293c-.49.49-.73.707-1.291.707s-.801-.217-1.291-.707C4.16 10.747 3.413 10 2 10v2c.561 0 .801.217 1.291.707C3.836 13.253 4.583 14 5.996 14zm0 5c1.413 0 2.16-.747 2.705-1.293.49-.49.731-.707 1.292-.707s.802.217 1.292.707c.545.546 1.292 1.293 2.706 1.293 1.415 0 2.163-.747 2.71-1.293.491-.49.732-.707 1.295-.707s.804.217 1.295.707C19.837 18.253 20.585 19 22 19v-2c-.563 0-.804-.217-1.295-.707-.546-.546-1.294-1.293-2.709-1.293s-2.162.747-2.709 1.292c-.491.491-.731.708-1.296.708-.562 0-.802-.217-1.292-.707C12.154 15.747 11.407 15 9.993 15s-2.161.747-2.706 1.293c-.49.49-.73.707-1.291.707s-.801-.217-1.291-.707C4.16 15.747 3.413 15 2 15v2c.561 0 .801.217 1.291.707C3.836 18.253 4.583 19 5.996 19z"></path>
                    </svg>
                    <p class="text-xs sm:text-sm">{{ renderedHealth.water }} мл</p>
                </div>
                <div class="flex items-center mt-1 space-x-1">
                    <svg class="v-5 h-5" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" style="fill: rgba(0, 0, 0, 1);">
                        <path d="M20.742 13.045a8.088 8.088 0 0 1-2.077.271c-2.135 0-4.14-.83-5.646-2.336a8.025 8.025 0 0 1-2.064-7.723A1 1 0 0 0 9.73 2.034a10.014 10.014 0 0 0-4.489 2.582c-3.898 3.898-3.898 10.243 0 14.143a9.937 9.937 0 0 0 7.072 2.93 9.93 9.93 0 0 0 7.07-2.929 10.007 10.007 0 0 0 2.583-4.491 1.001 1.001 0 0 0-1.224-1.224zm-2.772 4.301a7.947 7.947 0 0 1-5.656 2.343 7.953 7.953 0 0 1-5.658-2.344c-3.118-3.119-3.118-8.195 0-11.314a7.923 7.923 0 0 1 2.06-1.483 10.027 10.027 0 0 0 2.89 7.848 9.972 9.972 0 0 0 7.848 2.891 8.036 8.036 0 0 1-1.484 2.059z"></path>
                    </svg>
                    <p class="text-xs sm:text-sm">{{ formatSleepDuration(renderedHealth.sleep) }}</p>
                </div>
            </div>
            
        </div>
      </div>
    </div>
</template>
    
<script setup>
import { useFetch, timeSince, formatSleepDuration } from '../composables/utils.js';
import { onMounted, computed } from 'vue';

const apiBaseUrl = import.meta.env.VITE_APP_API_BASE_URL;
const { data: location, error: error_location, fetchData: fetchData_location } = useFetch(`${apiBaseUrl}/api/location/`);
const { data: health, error: error_health, fetchData: fetchData_health } = useFetch(`${apiBaseUrl}/api/health/`);

const props = defineProps({
    lastActivityName: String,  // Receive the last activity name as a prop
});

const activityStatusMap = {
    'Работа': 'Работаю',
    'Учёба': 'Учусь',
    'Спорт': 'Тренируюсь',
    'Досуг': 'На досуге',
    'Люди': 'Общаюсь',
    'Тусовка': 'Тусуюсь',
    'Быт': 'Занимаюсь бытом',
    'Дорога': 'В дороге',
    'Сон': 'Сплю',
    'Болезнь': 'Болею',
};

// Compute the status message based on the lastActivityName
const statusMessage = computed(() => {
    return activityStatusMap[props.lastActivityName] || 'Чем-то занимаюсь';  // Default message
});

onMounted(() => {
    fetchData_location();
    fetchData_health();
});

const renderedLocation = computed(() => {
    return location.value ? location.value : {};
});

const renderedHealth = computed(() => {
    return health.value ? health.value : {};
});

const slicedLocation = computed(() => {
  if (renderedLocation && renderedLocation.value.location) {
    const parts = renderedLocation.value.location.split('\n');
    return parts.length >= 3 ? `${parts[0].trim()}, ${parts[2].trim()}` : renderedLocation.value.location;
  }
  return '';
});
</script>

