<template>
  <div v-if="session.metric">
    <div v-if="loading" class="p-4 text-xs sm:text-xs text-center text-gray-500 border border-gray-300 rounded-lg bg-gray-50">
        Загрузка данных...
    </div>
    <div v-else-if="error" class="p-4 text-xs sm:text-xs text-center text-red-800 border border-red-300 rounded-lg bg-red-50" role="alert">
        <p>Не удалось загрузить данные для индикатора</p>
    </div>
    <div v-else-if="!sessionData || sessionData.length === 0" class="p-4 text-xs sm:text-xs text-center text-gray-600 border border-gray-300 rounded-lg bg-gray-50">
        Добавь хоть одну запись, чтобы увидеть визуализацию
    </div>
    <div v-else class="p-4 border border-gray-200 rounded-lg">
      <v-chart class="chart" :option="option" autoresize />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import { use } from 'echarts/core';
import { CanvasRenderer } from 'echarts/renderers';
import { GaugeChart } from 'echarts/charts';
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent
} from 'echarts/components';
import VChart from 'vue-echarts';
import { useFetch } from '../composables/utils.js';

use([
  CanvasRenderer,
  GaugeChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent
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
      console.error('Error fetching data for gauge:', fetchError.value);
      error.value = 'Не удалось загрузить данные';
      sessionData.value = [];
      return;
    }
    sessionData.value = fetchedData.value || [];
  } catch (e) {
    console.error('Error in fetchData for gauge:', e);
    error.value = 'Произошла ошибка при загрузке данных';
    sessionData.value = [];
  } finally {
    loading.value = false;
  }
};

onMounted(fetchData);

const calculateProgress = () => {
  if (!props.session.metric || !sessionData.value) {
    return 0;
  }

  const { type, filterValue } = props.session.metric;
  let values = sessionData.value.map(item => item.value);

  switch (type) {
    case 'count':
      if (filterValue) {
        return values.filter(v => v.toString().toLowerCase() === filterValue.toString().toLowerCase()).length;
      }
      return values.length;
    case 'average':
      const numericValues = values.map(Number).filter(n => !isNaN(n));
      if (numericValues.length === 0) return 0;
      const sum = numericValues.reduce((a, b) => a + b, 0);
      return sum / numericValues.length;
    case 'sum':
      return values.map(Number).filter(n => !isNaN(n)).reduce((a, b) => a + b, 0);
    default:
      return 0;
  }
};

const progressValue = ref(0);

watch(sessionData, () => {
  progressValue.value = calculateProgress();
}, { deep: true, immediate: true });


const progressPercentage = computed(() => {
  if (!props.session.metric || !props.session.metric.targetValue || props.session.metric.targetValue === 0) {
    return 0;
  }
  const currentValue = progressValue.value;
  const targetValue = props.session.metric.targetValue;

  const operator = props.session.metric.operator;
  let percentage = 0;

  if (operator.includes('<')) {
    if (currentValue === 0) { // Avoid division by zero, assume goal is met if current is 0 for a <= goal
        percentage = 100;
    } else if (currentValue <= targetValue) {
        // If current is better than or equal to target, progress is 100% or more
        percentage = (targetValue / currentValue) * 100;
    } else {
        // If current is worse than target, show how close it is
        percentage = (targetValue / currentValue) * 100;
    }
  } else { // >= or ==
    percentage = (currentValue / targetValue) * 100;
  }

  return Math.floor(Math.min(percentage, 100)); // Cap at 100% and floor it
});

const option = computed(() => {
  const gaugeData = [
    {
      value: progressPercentage.value,
      name: 'Прогресс по цели',
      title: {
        offsetCenter: ['0%', '20%']
      },
      detail: {
        valueAnimation: true,
        offsetCenter: ['0%', '-10%']
      }
    }
  ];

  return {
    series: [
        {
            type: 'gauge',
            startAngle: 90,
            endAngle: -270,
            pointer: {
                show: false
            },
            progress: {
                show: true,
                overlap: false,
                roundCap: true,
                clip: false,
                itemStyle: {
                    color: '#bbf7d0',
                    borderWidth: 1,
                    borderColor: '#f3f4f6'
                }
            },
            axisLine: {
                lineStyle: {
                    width: 20,
                    color: [['1', '#f3f4f6']]
                }
            },
            splitLine: {
                show: false,
                distance: 0,
                length: 10
            },
            axisTick: {
                show: false
            },
            axisLabel: {
                show: false,
                distance: 50
            },
            data: gaugeData,
            title: {
                fontSize: 12,
                color: '#4b5563',
                fontFamily: 'Montserrat'
            },
            detail: {
                width: 50,
                height: 14,
                fontSize: 12,
                color: '#4b5563',
                borderColor: '#4b5563',
                borderRadius: 20,
                borderWidth: 0.5,
                formatter: '{value}%',
                fontWeight: '400',
                fontFamily: 'Montserrat'
            }
        }
    ],
    media: [
      {
        query: {
          maxWidth: 768 // Apply this on mobile screens
        },
        option: {
          series: [
            {
              title: {
                fontSize: 12
              },
              detail: {
                fontSize: 12
              }
            }
          ]
        }
      }
    ]
  };
});

</script>

<style scoped>
.chart {
  height: 250px;
  width: 100%;
}
</style> 