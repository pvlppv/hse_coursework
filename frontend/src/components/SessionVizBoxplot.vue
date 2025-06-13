<template>
  <div v-if="loading" class="p-4 text-xs sm:text-xs text-center text-gray-500 border border-gray-300 rounded-lg bg-gray-50">
      Загрузка данных...
  </div>
  <div v-else-if="error" class="p-4 text-xs sm:text-xs text-center text-red-800 border border-red-300 rounded-lg bg-red-50" role="alert">
    <p>Не удалось загрузить данные для диаграммы распределения.</p>
  </div>
   <div v-else-if="!sessionData || sessionData.length < 5" class="p-4 text-xs sm:text-sm text-center text-gray-600 border border-gray-300 rounded-lg bg-gray-50">
      Добавь минимум 5 записей с числовыми значениями, чтобы увидеть визуализацию
  </div>
  <div v-else-if="boxplotData.boxData.length > 0" class="p-4 border border-gray-200 rounded-lg">
    <v-chart class="chart" :option="option" autoresize />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { use } from 'echarts/core';
import { CanvasRenderer } from 'echarts/renderers';
import { BoxplotChart, ScatterChart } from 'echarts/charts';
import {
  GridComponent,
  TooltipComponent,
  LegendComponent,
  TitleComponent,
  DataZoomComponent,
} from 'echarts/components';
import VChart from 'vue-echarts';
import { useFetch } from '../composables/utils.js';

use([
  CanvasRenderer,
  BoxplotChart,
  ScatterChart,
  GridComponent,
  TooltipComponent,
  LegendComponent,
  TitleComponent,
  DataZoomComponent
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
      console.error('Error fetching data for boxplot:', fetchError.value);
      error.value = 'Не удалось загрузить данные';
      sessionData.value = [];
      return;
    }
    sessionData.value = fetchedData.value || [];
  } catch (e) {
    console.error('Error in fetchData for boxplot:', e);
    error.value = 'Произошла ошибка при загрузке данных';
    sessionData.value = [];
  } finally {
    loading.value = false;
  }
};

onMounted(fetchData);

// --- Data processing for Boxplot ---

function getWeekKey(dateStr) {
  let dtStr = dateStr.toString().replace(' ', 'T');
  if (!dtStr.endsWith('Z')) {
    dtStr += 'Z';
  }
  const utcDate = new Date(dtStr);
  
  // Apply MSK offset
  const mskDate = new Date(utcDate.getTime());
  mskDate.setUTCHours(mskDate.getUTCHours() + 3);

  // Now calculate week number based on MSK date using UTC methods
  const d = new Date(Date.UTC(mskDate.getUTCFullYear(), mskDate.getUTCMonth(), mskDate.getUTCDate()));
  const dayNum = d.getUTCDay() || 7;
  d.setUTCDate(d.getUTCDate() + 4 - dayNum);
  const yearStart = new Date(Date.UTC(d.getUTCFullYear(), 0, 1));
  const weekNo = Math.ceil((((d.getTime() - yearStart.getTime()) / 86400000) + 1) / 7);
  return `${d.getUTCFullYear()}-W${String(weekNo).padStart(2, '0')}`;
}

const boxplotData = computed(() => {
  // Convert the data to the format we need, ensuring proper numeric conversion
  const numericData = sessionData.value
    .map(item => ({
      date: item.date || item.datetime, // handle both date and datetime fields
      value: Number(item.value) // ensure numeric conversion
    }))
    .filter(item => item.date && !isNaN(item.value));

  if (numericData.length < 5) {
    return { axisData: [], boxData: [], outliers: [] };
  }

  // Group data by week
  const dataByWeek = numericData.reduce((acc, item) => {
    const weekKey = getWeekKey(item.date);
    if (!acc[weekKey]) {
      acc[weekKey] = [];
    }
    acc[weekKey].push(item.value);
    return acc;
  }, {});

  const sortedWeeks = Object.keys(dataByWeek).sort();
  const axisData = [];
  const boxData = [];
  const outliers = [];

  function getQuantiles(arr) {
    const sorted = [...arr].sort((a, b) => a - b);

    const getMedian = (subArr) => {
        if (subArr.length === 0) return 0;
        const mid = Math.floor(subArr.length / 2);
        return subArr.length % 2 === 1 ? subArr[mid] : (subArr[mid - 1] + subArr[mid]) / 2;
    };
    
    const median = getMedian(sorted);
    const midPoint = Math.floor(sorted.length / 2);

    let lowerHalf, upperHalf;
    if (sorted.length % 2 === 1) {
        lowerHalf = sorted.slice(0, midPoint);
        upperHalf = sorted.slice(midPoint + 1);
    } else {
        lowerHalf = sorted.slice(0, midPoint);
        upperHalf = sorted.slice(midPoint);
    }

    const q1 = getMedian(lowerHalf);
    const q3 = getMedian(upperHalf);
    
    const iqr = q3 - q1;
    
    const lowerBound = q1 - 1.5 * iqr;
    const upperBound = q3 + 1.5 * iqr;
    
    const inliers = sorted.filter(v => v >= lowerBound && v <= upperBound);
    const boxplotMin = inliers.length > 0 ? inliers[0] : q1;
    const boxplotMax = inliers.length > 0 ? inliers[inliers.length - 1] : q3;

    return { q1, median, q3, boxplotMin, boxplotMax, lowerBound, upperBound };
  }
  
  // Process each week's data
  for (const weekKey of sortedWeeks) {
    const weekValues = dataByWeek[weekKey];

    axisData.push(weekKey);
    const stats = getQuantiles(weekValues);
    boxData.push([stats.boxplotMin, stats.q1, stats.median, stats.q3, stats.boxplotMax]);
    
    const weekIndex = axisData.length - 1;
    weekValues.forEach(value => {
      if (value < stats.lowerBound || value > stats.upperBound) {
        outliers.push([weekIndex, value]);
      }
    });
  }

  return { axisData, boxData, outliers };
});


const option = computed(() => ({
  // title: {
  //   text: 'Распределение данных по неделям',
  //   left: 'center',
  //   textStyle: {
  //     fontSize: 12,
  //     fontWeight: 'normal',
  //     fontFamily: 'Montserrat',
  //     color: '#4b5563'
  //   }
  // },
  tooltip: {
    trigger: 'item',
    axisPointer: {
      type: 'shadow'
    },
    formatter: function (params) {
      if (params.seriesType === 'boxplot') {
        if (params.dataIndex === undefined || !boxplotData.value.boxData?.[params.dataIndex]) {
          return '';
        }
        
        const data = boxplotData.value.boxData[params.dataIndex];
        
        return [
          `<b>${params.name}</b>`,
          `Максимум: ${data[4].toFixed(2)}`,
          `Перцентиль 75: ${data[3].toFixed(2)}`,
          `Медиана: ${data[2].toFixed(2)}`,
          `Перцентиль 25: ${data[1].toFixed(2)}`,
          `Минимум: ${data[0].toFixed(2)}`,
        ].join('<br/>');
      }
      if (params.seriesType === 'scatter') {
        // Good practice to also add a check for the scatter plot data.
        if (!params.value || !Array.isArray(params.value) || params.value.length < 2) {
            return '';
        }
        return `${params.marker} Выброс<br/>Значение: ${params.value[1].toFixed(2)}`;
      }
      return '';
    },
    textStyle: {
      color: '#4b5563',
      fontFamily: 'Montserrat',
      fontSize: 12,
      fontWeight: '400'
    }
  },
  grid: {
    left: '10%',
    right: '10%',
  },
  xAxis: {
    type: 'category',
    data: boxplotData.value.axisData,
    boundaryGap: true,
    nameGap: 30,
    splitArea: { show: false },
    splitLine: { show: false },
    axisLabel: {
      fontFamily: 'Montserrat',
      rotate: 45
    }
  },
  yAxis: {
    type: 'value',
    splitArea: { show: false },
    axisLabel: {
      fontFamily: 'Montserrat',
      formatter: function(value) {
        return value.toFixed(0);
      }
    }
  },
  dataZoom: [
    {
      type: 'inside',
      start: 0,
      end: 100
    },
    {
      show: true,
      type: 'slider',
      top: '90%',
      start: 0,
      end: 100
    }
  ],
  series: [
    {
      name: 'BoxPlot',
      type: 'boxplot',
      data: boxplotData.value.boxData,
      itemStyle: {
        color: '#bbf7d0',
        borderColor: '#4ade80'
      }
    },
    {
      name: 'Outliers',
      type: 'scatter',
      data: boxplotData.value.outliers,
      itemStyle: {
        color: '#f87171'
      }
    }
  ]
}));
</script>

<style scoped>
.chart {
  height: 350px;
  width: 100%;
}
</style>