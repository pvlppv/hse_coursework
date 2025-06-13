<template>
  <div class="w-full">
    <div v-if="loading" class="p-4 text-xs sm:text-xs text-center text-gray-500 border border-gray-300 rounded-lg bg-gray-50">
      Загрузка данных...
    </div>
    <div v-else-if="error" class="p-4 text-xs sm:text-xs text-center text-red-800 border border-red-300 rounded-lg bg-red-50" role="alert">
      <p>На сервере что-то сломалось, данные не достались из базы данных :(</p>
      <p><a href="https://t.me/pvlppv" class="text-blue-600 hover:text-blue-800">Напишите мне</a>, я починю.</p>
    </div>
    <div v-else-if="!sessionData || sessionData.length === 0" class="p-4 text-xs sm:text-xs text-center text-gray-600 border border-gray-300 rounded-lg bg-gray-50">
      Добавь хоть одну запись, чтобы увидеть визуализацию
    </div>
    <div v-else class="px-4 py-4 sm:px-6 sm:py-5 border border-gray-300 rounded-lg">
      <div class="relative w-full mb-4">
        <!-- Dropdown button -->
        <button 
          @click="toggleDropdown"
          class="w-full text-xs sm:text-xs text-gray-600 py-1.5 px-3 border border-gray-300 rounded-md bg-white flex justify-between items-center"
        >
          {{ aggregationTypes[selectedAggregationType] }}
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" style="fill: rgba(0, 0, 0, 1);">
            <path d="M16.293 9.293 12 13.586 7.707 9.293l-1.414 1.414L12 16.414l5.707-5.707z"></path>
          </svg>
        </button>

        <!-- Dropdown options -->
        <ul v-if="dropdownOpen" class="absolute w-full bg-white border border-gray-300 rounded-md shadow-md z-10 mt-1">
          <li 
            v-for="(label, value) in aggregationTypes" 
            :key="value" 
            @click="selectAggregationType(value)"
            class="px-3 py-1.5 text-xs sm:text-xs text-gray-600 hover:bg-gray-100 cursor-pointer"
          >
            {{ label }}
          </li>
        </ul>
      </div>
      <v-chart class="chart" :option="option" autoresize />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { use } from 'echarts/core';
import { CanvasRenderer } from 'echarts/renderers';
import { HeatmapChart } from 'echarts/charts';
import {
  CalendarComponent,
  TooltipComponent,
  VisualMapComponent
} from 'echarts/components';
import VChart from 'vue-echarts';
import { useFetch } from '../composables/utils.js';

use([
  CanvasRenderer,
  HeatmapChart,
  CalendarComponent,
  TooltipComponent,
  VisualMapComponent
]);

const props = defineProps({
  sessionId: {
    type: [String, Number],
    required: true
  },
  userId: {
    type: [String, Number],
    required: true
  },
  aggregationType: {
    type: String,
    default: 'count',
    validator: (value) => ['count', 'sum'].includes(value)
  }
});

const STORAGE_KEY = `heatmap_aggregation_type_${props.sessionId}`;
const selectedAggregationType = ref(localStorage.getItem(STORAGE_KEY) || props.aggregationType);
const dropdownOpen = ref(false);

const aggregationTypes = {
  count: 'Количество записей',
  sum: 'Сумма значений'
};

const toggleDropdown = () => {
  dropdownOpen.value = !dropdownOpen.value;
};

const selectAggregationType = (value) => {
  selectedAggregationType.value = value;
  localStorage.setItem(STORAGE_KEY, value);
  dropdownOpen.value = false;
};

const apiBaseUrl = import.meta.env.VITE_APP_API_BASE_URL;
const error = ref(null);
const sessionData = ref([]);
const loading = ref(true);

const fetchData = async () => {
  try {
    error.value = null;
    loading.value = true;
    
    const tableName = `session_${props.sessionId}_data`;
    const { data: fetchedData, error: fetchError, fetchData: fetch } = useFetch(
      `${apiBaseUrl}/api/users/table/${tableName}/rows/`,
      { credentials: 'include' }
    );
    
    await fetch();
    
    if (fetchError.value) {
      console.error('Error fetching data:', fetchError.value);
      error.value = 'Не удалось загрузить данные';
      sessionData.value = [];
      return;
    }
    
    if (fetchedData.value) {
      sessionData.value = fetchedData.value;
    } else {
      sessionData.value = [];
    }
  } catch (e) {
    console.error('Error in fetchData:', e);
    error.value = 'Произошла ошибка при загрузке данных';
    sessionData.value = [];
  } finally {
    loading.value = false;
  }
};

onMounted(fetchData);

const chartData = computed(() => {
  if (!sessionData.value || sessionData.value.length === 0) {
    return [];
  }

  const dateValues = new Map();
  const today = new Date();
  const startDate = new Date();
  startDate.setMonth(today.getMonth() - 6);
  startDate.setDate(startDate.getDate() + 1);
  
  for (let d = new Date(startDate); d <= today; d.setDate(d.getDate() + 1)) {
    const dateStr = d.toISOString().split('T')[0];
    dateValues.set(dateStr, 0);
  }

  // Fill in actual values
  sessionData.value.forEach(entry => {
    let dtStr = entry.datetime.toString().replace(' ', 'T');
    if (!dtStr.endsWith('Z')) {
      dtStr += 'Z';
    }
    const d = new Date(dtStr);
    d.setUTCHours(d.getUTCHours() + 3); // Apply MSK timezone offset
    const date = d.toISOString().split('T')[0];
    
    if (dateValues.has(date)) {
      if (selectedAggregationType.value === 'sum') {
        const numericValue = parseFloat(entry.value);
        if (!isNaN(numericValue)) {
          const currentValue = dateValues.get(date) || 0;
          dateValues.set(date, currentValue + numericValue);
        }
      } else { // 'count'
        const currentValue = dateValues.get(date) || 0;
        dateValues.set(date, currentValue + 1);
      }
    }
  });

  return Array.from(dateValues.entries()).map(([date, value]) => [date, value]);
});

const calendarRange = computed(() => {
    const today = new Date();
    const endDate = today.toISOString().split('T')[0];
    const startDate = new Date();
    startDate.setMonth(startDate.getMonth() - 6);
    startDate.setDate(startDate.getDate() + 1);
    const startDateStr = startDate.toISOString().split('T')[0];
    return [startDateStr, endDate];
});

const maxValue = computed(() => {
  if (chartData.value.length === 0) return 5;
  const values = chartData.value.map(item => item[1]);
  return Math.max(...values, 5);
});

const minValue = computed(() => {
  if (chartData.value.length === 0) return 0;
  const values = chartData.value.map(item => item[1]).filter(v => v > 0);
  if (values.length === 0) return 0;
  return Math.min(...values);
});

const formatNumber = (num) => {
  if (num >= 1000 && num < 1000000) {
    return Math.round(num / 1000) + 'к';
  }
  else if (num >= 1000000) {
    return Math.round(num / 1000000) + 'м';
  }
  return num.toString();
};

const visualMapOption = computed(() => {
  if (selectedAggregationType.value === 'sum') {
    const max = maxValue.value;
    const min = minValue.value;
    const range = max - min;
    const step = range / 5; // Divide range into 5 steps for coloring

    return {
      type: 'piecewise',
      orient: 'horizontal',
      left: 'center',
      bottom: 0,
      pieces: [
        { min: min, max: min + step, color: '#bbf7d0', label: `${formatNumber(Math.round(min))}-${formatNumber(Math.round(min + step))}` },
        { min: min + step, max: min + step * 2, color: '#86efac', label: `${formatNumber(Math.round(min + step))}-${formatNumber(Math.round(min + step * 2))}` },
        { min: min + step * 2, max: min + step * 3, color: '#4ade80', label: `${formatNumber(Math.round(min + step * 2))}-${formatNumber(Math.round(min + step * 3))}` },
        { min: min + step * 3, max: min + step * 4, color: '#22c55e', label: `${formatNumber(Math.round(min + step * 3))}-${formatNumber(Math.round(min + step * 4))}` },
        { min: min + step * 4, max: max, color: '#15803d', label: `${formatNumber(Math.round(min + step * 4))}-${formatNumber(Math.round(max))}` }
      ],
      textStyle: {
        color: '#4b5563',
        fontFamily: 'Montserrat',
        fontSize: 10
      },
      itemWidth: 10,
      itemHeight: 10,
      itemGap: 8,
      textGap: 3
    };
  }
  // 'count'
  return {
    type: 'piecewise',
    orient: 'horizontal',
    left: 'center',
    bottom: 0,
    pieces: [
      { value: 1, color: '#bbf7d0' },
      { value: 2, color: '#86efac' },
      { value: 3, color: '#4ade80' },
      { value: 4, color: '#22c55e' },
      { gte: 5, color: '#15803d' }
    ],
    textStyle: {
      color: '#4b5563',
      fontFamily: 'Montserrat',
      fontSize: 10
    },
    itemWidth: 10,
    itemHeight: 10,
    itemGap: 8,
    textGap: 3
  };
});

const option = computed(() => {
  return {
    tooltip: {
      position: 'top',
      formatter: function (p) {
        const date = new Date(p.data[0]).toLocaleDateString('ru-RU');
        const value = p.data[1];
        if (selectedAggregationType.value === 'sum') {
          return `${date}: ${formatNumber(value)}`;
        }
        return `${date}: ${value} раз`;
      },
      textStyle: {
        color: '#4b5563',
        fontFamily: 'Montserrat',
        fontSize: 12,
        fontWeight: '400'
      }
    },
    visualMap: visualMapOption.value,
    calendar: {
      top: 30,
      left: 20,
      right: 10,
      bottom: 50,
      cellSize: ['auto', 13],
      range: calendarRange.value,
      itemStyle: {
        borderWidth: 0.5,
        borderColor: '#e5e7eb'
      },    
      dayLabel: { 
        nameMap: 'ru', 
        firstDay: 1, 
        margin: 5,
        color: '#4b5563',
        fontSize: 12,
        fontFamily: 'Montserrat'
      },
      monthLabel: { 
        nameMap: 'ru',
        color: '#4b5563',
        fontSize: 12,
        fontFamily: 'Montserrat'
      },
      splitLine: {
        show: true,
        lineStyle: {
          color: '#4b5563',
          borderWidth: 0.5
        }
      },
      yearLabel: { show: false }
    },
    series: {
      type: 'heatmap',
      coordinateSystem: 'calendar',
      data: chartData.value,
      itemStyle: {
        color: '#ffffff'
      }
    }
  };
});
</script>

<style scoped>
.chart {
  height: 180px;
  width: 100%;
}
</style> 