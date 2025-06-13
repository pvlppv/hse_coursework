<template>
  <div v-if="loading" class="p-4 text-xs sm:text-xs text-center text-gray-500 border border-gray-300 rounded-lg bg-gray-50">
      Загрузка данных...
  </div>
  <div v-else-if="error" class="p-4 text-xs sm:text-xs text-center text-red-800 border border-red-300 rounded-lg bg-red-50" role="alert">
    <p>Не удалось загрузить данные для графика.</p>
  </div>
  <div v-else-if="!sessionData || sessionData.length === 0" class="p-4 text-xs sm:text-sm text-center text-gray-600 border border-gray-300 rounded-lg bg-gray-50">
      Добавь хоть одну запись, чтобы увидеть визуализацию
  </div>
  <div v-else class="p-4 border border-gray-200 rounded-lg">
    <v-chart class="chart" :option="option" autoresize />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { use } from 'echarts/core';
import { CanvasRenderer } from 'echarts/renderers';
import { ScatterChart } from 'echarts/charts';
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent
} from 'echarts/components';
import VChart from 'vue-echarts';
import { useFetch } from '../composables/utils.js';

use([
  CanvasRenderer,
  ScatterChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent
]);

const props = defineProps({
  session: {
    type: Object,
    required: true
  }
});

const apiBaseUrl = import.meta.env.VITE_APP_API_BASE_URL;
const error = ref(null);
const sessionData = ref([]);
const loading = ref(true);

const fetchData = async () => {
  if (!props.session?.id) {
    loading.value = false;
    return;
  }
  try {
    loading.value = true;
    error.value = null;
    const tableName = `session_${props.session.id}_data`;
    const { data: fetchedData, error: fetchError, fetchData: fetch } = useFetch(
      `${apiBaseUrl}/api/users/table/${tableName}/rows/`,
      { credentials: 'include' }
    );
    await fetch();

    if (fetchError.value) {
      console.error('Error fetching data for scatter plot:', fetchError.value);
      error.value = 'Не удалось загрузить данные';
      sessionData.value = [];
      return;
    }
    sessionData.value = fetchedData.value || [];
  } catch (e) {
    console.error('Error in fetchData for scatter plot:', e);
    error.value = 'Произошла ошибка при загрузке данных';
    sessionData.value = [];
  } finally {
    loading.value = false;
  }
};

onMounted(fetchData);

const seriesData = computed(() => {
  if (!sessionData.value || sessionData.value.length === 0) {
    return [];
  }

  // Group by value type first
  const dataByValue = sessionData.value.reduce((acc, item) => {
    const value = item.value;
    if (!acc[value]) {
      acc[value] = [];
    }
    acc[value].push(item);
    return acc;
  }, {});

  // For each value type, count occurrences per day
  return Object.entries(dataByValue).map(([value, items]) => {
    const countsByDay = items.reduce((acc, item) => {
      let dtStr = item.datetime.toString().replace(' ', 'T');
      if (!dtStr.endsWith('Z')) {
        dtStr += 'Z';
      }
      const date = new Date(dtStr);
      // Convert to MSK
      date.setUTCHours(date.getUTCHours() + 3);
      // Set time to midnight (00:00:00)
      date.setHours(0, 0, 0, 0);
      const day = date.toISOString();
      acc[day] = (acc[day] || 0) + 1;
      return acc;
    }, {});

    // Convert to array of [timestamp, count] pairs
    const chartData = Object.entries(countsByDay).map(([day, count]) => [
      new Date(day).getTime(), // Convert to timestamp
      count
    ]);

    return {
      name: value,
      type: 'scatter',
      symbolSize: 15,
      data: chartData,
    };
  });
});

const axisRange = computed(() => {
  if (!seriesData.value || seriesData.value.length === 0) {
    return { min: null, max: null };
  }
  let min = Infinity;
  let max = -Infinity;
  seriesData.value.forEach(series => {
    series.data.forEach(point => {
      if (point[0] < min) min = point[0];
      if (point[0] > max) max = point[0];
    });
  });
  // Add some padding to the range
  const oneDay = 3600 * 1000 * 24;
  return {
    min: min - oneDay,
    max: max + oneDay
  };
});

const option = computed(() => {
  const colorPalette = [
    '#a7f3d0', '#bfdbfe', '#fecaca', '#fde68a', '#e9d5ff', '#c7d2fe', '#fbcfe8'
  ];

  return {
    color: colorPalette,
    grid: {
      left: '2%',
      right: '2%',
      bottom: '15%',
      top: '10%',
      containLabel: true
    },
    legend: {
      show: true,
      bottom: 0,
      type: 'scroll',
      textStyle: {
        fontSize: 12,
        color: '#4b5563',
        fontFamily: 'Montserrat'
      }
    },
    tooltip: {
      position: 'top',
      formatter: function (params) {
        const date = new Date(params.value[0]).toLocaleDateString('ru-RU');
        return `${params.seriesName}: ${params.value[1]} раз <br/> ${date}`;
      },
      textStyle: {
        color: '#4b5563',
        fontFamily: 'Montserrat',
        fontSize: 12,
        fontWeight: '400'
      }
    },
    xAxis: {
      type: 'time',
    //   name: 'Дата',
    //   nameGap: 20,
    //   nameLocation: 'middle',
    //   nameTextStyle: {
    //     fontFamily: 'Montserrat',
    //     fontSize: 12,
    //     color: '#4b5563'
    //   },
        min: axisRange.value.min,
        max: axisRange.value.max,
        minInterval: 3600 * 1000 * 24, // Ensure ticks are at least 1 day apart
      axisLabel: {
        formatter: function (value) {
          const date = new Date(value);
          const day = date.getDate().toString().padStart(2, '0');
          const month = (date.getMonth() + 1).toString().padStart(2, '0');
          return `${day}.${month}`;
        }
      },
      splitLine: {
        show: true,
        lineStyle: {
          type: 'dashed',
          color: '#E0E0E0'
        }
      }
    },
    yAxis: {
      type: 'value',
    //   name: 'Количество',
    //   nameLocation: 'middle',
    //   nameGap: 30,
    //   nameTextStyle: {
    //     fontFamily: 'Montserrat',
    //     fontSize: 12,
    //     color: '#4b5563'
    //   },
      splitLine: {
        show: true,
        lineStyle: {
          type: 'dashed',
          color: '#E0E0E0'
        }
      },
      minInterval: 1,
      interval: 1
    },
    series: seriesData.value
  };
});

</script>

<style scoped>
.chart {
  height: 250px;
  width: 100%;
}
</style> 