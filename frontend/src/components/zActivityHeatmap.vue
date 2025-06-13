<template>
  <div class="container mx-auto flex justify-center">
    <div class="max-w-sm sm:max-w-lg w-full space-y-5">
      
      <div v-if="error_activity" class="p-4 text-xs sm:text-sm text-center text-red-800 border border-red-300 rounded-lg bg-red-50" role="alert">
        <p>На сервере что-то сломалось, данные не достались из базы данных :(</p>
        <p><a href="https://t.me/pvlppv" class="text-blue-600 hover:text-blue-800">Напишите мне</a>, я починю.</p>
      </div>

      <div v-else class="px-1 py-4 sm:px-2 sm:py-5 border border-gray-300 rounded-lg">
        <div class="space-y-6">
          <div
            v-for="category in activityCategories"
            :key="category.key"
            class="space-y-1 sm:space-y-2 cursor-pointer"
            @click="openModal(category)"
          >
            <div class="flex items-center justify-center">
              <h3 class="text-xs sm:text-sm font-semibold">
                {{ category.label }}
              </h3>
            </div>
            <calendar-heatmap
              :values="getCategoryData(category.key)"
              :round="2"
              :end-date="endDate"
              :range-color="category.colors"
              :max="category.max"
              :tooltip="false"
              :tooltip-unit="category.key"
            />
          </div>
        </div>
        <Transition
            enter-active-class="transition duration-300"
            enter-from-class="opacity-0"
            enter-to-class="opacity-100"
            leave-active-class="transition duration-300"
            leave-from-class="opacity-100"
            leave-to-class="opacity-0"
        >
          <heatmap-modal
            v-if="selectedCategory"
            :is-open="isModalOpen"
            :title="selectedCategory.label"
            :values="getCategoryData(selectedCategory.key)"
            :round="2"
            :end-date="endDate"
            :range-color="selectedCategory.colors"
            :max="selectedCategory.max"
            :tooltip="true"
            :tooltip-unit="selectedCategory.key"
            @close="closeModal"
          />
        </Transition>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import HeatmapModal from './HeatmapModal.vue';
import { useFetch } from '../composables/utils.js';

const apiBaseUrl = import.meta.env.VITE_APP_API_BASE_URL;
const { data: activity, error: error_activity, fetchData: fetchData_activity } = useFetch(`${apiBaseUrl}/api/activity_count/`);

onMounted(() => {
  fetchData_activity();
});

const renderedActivity = computed(() => activity.value || []);

const activityCategories = ref([
  { key: 'Работа', label: 'Работал', colors: ['#f3f4f6', '#f3f4f6', '#22c55e'], max: 3 },
  { key: 'Учёба', label: 'Учился', colors: ['#f3f4f6', '#f3f4f6', '#22c55e'], max: 3 },
  { key: 'Спорт', label: 'Тренировался', colors: ['#f3f4f6', '#f3f4f6', '#22c55e'], max: 3 },
  { key: 'Хобби', label: 'Занимался хобби', colors: ['#f3f4f6', '#f3f4f6', '#22c55e'], max: 3 },
  { key: 'Болезнь', label: 'Болел', colors: ['#f3f4f6', '#f3f4f6', '#22c55e'], max: 3 },
]);

const getCategoryData = (categoryKey) => {
  const data = [];

  renderedActivity.value.forEach((entry) => {
    const date = entry.date.split('T')[0];
    const count = entry.activities[categoryKey];
    if (count !== undefined && count !== null) {
      data.push({ date, count: count ? 1 : 0 });
    }
  });

  return data;
};

const endDate = computed(() => {
  const allDates = renderedActivity.value.map(entry => new Date(entry.date.split('T')[0]));
  if (allDates.length > 0) {
    const latestDate = allDates.sort((a, b) => b - a)[0];
    latestDate.setDate(latestDate.getDate() + 1);
    return latestDate.toISOString().split('T')[0];
  }
  return null;
});

const isModalOpen = ref(false);
const selectedCategory = ref(null);

const openModal = (category) => {
  selectedCategory.value = category;
  isModalOpen.value = true;
};

const closeModal = () => {
  isModalOpen.value = false;
  selectedCategory.value = null;
};
</script>

<style scoped>
</style>