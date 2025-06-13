<template>
  <div class="w-full">
    <div v-if="error" class="p-2 text-xs text-center text-red-800 border border-red-300 rounded-lg bg-red-50" role="alert">
      <p>Ошибка загрузки данных</p>
    </div>
    
    <div v-else class="px-1 py-3 border border-gray-300 rounded-lg">
      <div class="space-y-4">
        <div
          v-for="category in healthCategories"
          :key="category.key"
          class="space-y-1"
        >
          <div class="flex items-center justify-center">
            <h3 class="text-xs font-semibold">
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
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useFetch } from '../composables/utils.js';

const props = defineProps({
  sessionId: {
    type: String,
    required: true
  }
});

const apiBaseUrl = import.meta.env.VITE_APP_API_BASE_URL;
const { data: health, error: error_health, fetchData: fetchData_health } = useFetch(`${apiBaseUrl}/api/health/${props.sessionId}`);

const healthCategories = ref([
  { key: 'steps', label: 'Шаги (шт)', colors: ['#f3f4f6', '#f3f4f6', '#bbf7d0', '#4ade80', '#22c55e', '#15803d'], max: 20000 },
  { key: 'energy', label: 'Энергия (ккал)', colors: ['#f3f4f6', '#f3f4f6', '#bbf7d0', '#4ade80', '#22c55e', '#15803d'], max: 1000 },
  { key: 'water', label: 'Вода (мл)', colors: ['#f3f4f6', '#f3f4f6', '#bbf7d0', '#4ade80', '#22c55e', '#15803d'], max: 2000 },
  { key: 'sleep', label: 'Сон (ч)', colors: ['#f3f4f6', '#f3f4f6', '#bbf7d0', '#4ade80', '#22c55e', '#15803d'], max: 9 },
]);

const getCategoryData = (categoryKey) => {
  const data = [];

  health.value?.forEach((entry) => {
    const date = entry.date.split('T')[0];
    const count = entry[categoryKey];
    if (count !== undefined && count !== null) {
      data.push({ date, count });
    }
  });

  return data;
};

const endDate = computed(() => {
  const allDates = health.value?.map(entry => new Date(entry.date.split('T')[0])) || [];
  if (allDates.length > 0) {
    const latestDate = allDates.sort((a, b) => b - a)[0];
    latestDate.setDate(latestDate.getDate() + 1);
    return latestDate.toISOString().split('T')[0];
  }
  return null;
});

onMounted(() => {
  fetchData_health();
});
</script> 