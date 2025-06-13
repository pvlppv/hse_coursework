<template>
  <div class="w-full">
    <div v-if="error" class="p-2 text-xs text-center text-red-800 border border-red-300 rounded-lg bg-red-50" role="alert">
      <p>Ошибка загрузки данных</p>
    </div>

    <div v-else class="qalendar-wrapper is-light-mode">
      <Qalendar 
        v-if="!error && events.length" 
        :selected-date="new Date()" 
        :events="events" 
        :config="config"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useFetch } from '../composables/utils.js';
import { Qalendar } from 'qalendar';
import 'qalendar/dist/style.css';

const props = defineProps({
  sessionId: {
    type: String,
    required: true
  }
});

const apiBaseUrl = import.meta.env.VITE_APP_API_BASE_URL;
const events = ref([]);
const error = ref(null);

const { data: activities, error: fetchError, fetchData } = useFetch(`${apiBaseUrl}/api/activity/${props.sessionId}`);

const processEvents = (data) => {
  return data.map((activity) => {
    const startDate = new Date(activity.date);
    const start = `${startDate.getFullYear()}-${String(startDate.getMonth() + 1).padStart(2, '0')}-${String(startDate.getDate()).padStart(2, '0')} ${String(startDate.getHours()).padStart(2, '0')}:${String(startDate.getMinutes()).padStart(2, '0')}`;
    const end = `${start.split(' ')[0]} 23:59`;

    return {
      title: activity.name,
      time: { start, end },
      id: activity.id,
      isEditable: false,
    };
  });
};

const config = computed(() => ({
  week: {
    startsOn: 'monday',
    nDays: 1,
    scrollToHour: new Date().getHours(),
  },
  month: {
    showTrailingAndLeadingDates: false,
  },
  locale: 'ru-RU',
  style: {
    fontFamily: "'Montserrat', sans-serif",
  },
  defaultMode: 'day',
  isSilent: true,
  showCurrentTime: false,
  disableModes: ['month', 'week'],
  eventDialog: {
    isDisabled: true,
  },
  dayIntervals: {
    length: 60,
    height: 20,
  },
}));

onMounted(async () => {
  await fetchData();
  if (activities.value) {
    events.value = processEvents(activities.value);
  }
  if (fetchError.value) {
    error.value = fetchError.value;
  }
});
</script>

<style scoped>
.qalendar-wrapper {
  height: 200px;
}
</style> 