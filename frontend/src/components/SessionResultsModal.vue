<template>
  <Teleport to="body">
    <Transition
      enter-active-class="transition duration-300"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition duration-300"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div
        v-if="show"
        class="fixed inset-0 bg-black bg-opacity-50 z-[9998]"
      />
    </Transition>
    <Transition
      enter-active-class="transition duration-300 ease-out"
      enter-from-class="opacity-0 scale-95"
      enter-to-class="opacity-100 scale-100"
      leave-active-class="transition duration-200 ease-in"
      leave-from-class="opacity-100 scale-100"
      leave-to-class="opacity-0 scale-95"
    >
      <div 
        v-if="show" 
        @click="$emit('close')"
        @wheel.prevent
        @scroll.prevent
        @touchmove.prevent
        class="fixed inset-0 flex items-center justify-center p-2 sm:p-4 z-[9999]"
      >
        <div 
          @click.stop
          class="bg-white rounded-lg p-4 sm:p-6 w-full max-w-sm sm:max-w-lg max-h-[80vh] flex flex-col overflow-hidden"
        >
          <h3 class="text-lg font-semibold mb-4 text-center">
            {{ session?.goal_type === 'observe' ? 'Статистика' : 'Результаты' }}: {{ session?.title }}
          </h3>

          <div v-if="results?.loading" class="text-center">
            <p>Подсчитываем результаты...</p>
          </div>

          <div v-else-if="results?.error" class="text-center text-red-600">
            <p>{{ results.error }}</p>
          </div>

          <div v-else-if="results" class="space-y-4">
            <div 
              v-if="results.success !== null"
              class="p-4 rounded-lg text-center" 
              :class="results.success ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'"
            >
              <p class="font-bold text-lg">{{ results.success ? 'Эксперимент успешен!' : 'Эксперимент не удался' }}</p>
            </div>

            <div v-if="results.metric" class="grid grid-cols-2 gap-4 text-center border-b pb-4">
              <div>
                <p class="text-sm text-gray-500">Цель</p>
                <p class="text-lg font-semibold">{{ formatMetric(results.metric) }}</p>
              </div>
              <div>
                <p class="text-sm text-gray-500">Результат</p>
                <p class="text-lg font-semibold">{{ results.actualValue }}</p>
              </div>
            </div>

            <!-- Statistics Section -->
            <div v-if="results.stats" class="space-y-3 pt-2">
              <h4 class="text-md font-semibold text-center text-gray-700">Статистика сессии</h4>
              
              <div class="grid grid-cols-2 gap-3 text-center text-sm">
                <div class="p-3 bg-gray-50 rounded-lg">
                  <p class="text-gray-500">Всего записей</p>
                  <p class="font-semibold text-base">{{ results.stats.totalRows }}</p>
                </div>

                <div v-if="results.stats.duration" class="p-3 bg-gray-50 rounded-lg">
                  <p class="text-gray-500">Длительность</p>
                  <p class="font-semibold text-base">{{ results.stats.duration }}</p>
                </div>

                <div v-if="results.stats.categoricalStats" class="p-3 bg-gray-50 rounded-lg">
                  <p class="text-gray-500">Совпадений</p>
                  <p class="font-semibold text-base">{{ results.stats.categoricalStats.matchingCount }}</p>
                </div>
              </div>

              <div v-if="results.stats.frequencyStats" class="grid grid-cols-2 gap-3 text-center text-sm">
                <div class="p-3 bg-gray-50 rounded-lg">
                  <p class="text-gray-500">Самое частое</p>
                  <p class="font-semibold text-base truncate" :title="results.stats.frequencyStats.mostFrequent.value">
                    {{ results.stats.frequencyStats.mostFrequent.value }} ({{ results.stats.frequencyStats.mostFrequent.count }} раз)
                  </p>
                </div>
                <div class="p-3 bg-gray-50 rounded-lg">
                  <p class="text-gray-500">Самое редкое</p>
                  <p class="font-semibold text-base truncate" :title="results.stats.frequencyStats.leastFrequent.value">
                    {{ results.stats.frequencyStats.leastFrequent.value }} ({{ results.stats.frequencyStats.leastFrequent.count }} раз)
                  </p>
                </div>
              </div>

              <div v-if="results.stats.numericStats" class="grid grid-cols-2 gap-3 text-center text-sm">
                <div class="p-3 bg-gray-50 rounded-lg">
                  <p class="text-gray-500">Мин. значение</p>
                  <p class="font-semibold text-base">{{ Math.round(results.stats.numericStats.min * 100) / 100 }}</p>
                </div>
                <div class="p-3 bg-gray-50 rounded-lg">
                  <p class="text-gray-500">Макс. значение</p>
                  <p class="font-semibold text-base">{{ Math.round(results.stats.numericStats.max * 100) / 100 }}</p>
                </div>
                <div class="p-3 bg-gray-50 rounded-lg">
                  <p class="text-gray-500">Сумма</p>
                  <p class="font-semibold text-base">{{ Math.round(results.stats.numericStats.sum * 100) / 100 }}</p>
                </div>
                <div class="p-3 bg-gray-50 rounded-lg">
                  <p class="text-gray-500">Среднее</p>
                  <p class="font-semibold text-base">{{ Math.round(results.stats.numericStats.average * 100) / 100 }}</p>
                </div>
              </div>
            </div>
          </div>

          <div class="flex justify-center gap-3 mt-6">
            <button
              @click="$emit('close')"
              class="px-4 py-2 text-sm rounded-lg border hover:bg-gray-50"
            >
              Закрыть
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, watch } from 'vue';
import { useFetch } from '../composables/utils.js';

const apiBaseUrl = import.meta.env.VITE_APP_API_BASE_URL;

const props = defineProps({
  show: {
    type: Boolean,
    required: true,
  },
  session: {
    type: Object,
    default: null
  }
});

defineEmits(['close']);

const results = ref(null);

const formatMetric = (metric) => {
  if (!metric) return '';
  
  const typeMap = {
    count: 'кол-во записей',
    average: 'среднее значение',
    sum: 'сумма значений'
  };

  const operatorMap = {
    '>=': '≥',
    '<=': '≤',
    '==': '='
  };

  let description = typeMap[metric.type] || '';
  if (metric.type === 'count' && metric.filterValue) {
    description += ` "${metric.filterValue}"`;
  }
  const operator = operatorMap[metric.operator] || '';
  const target = metric.targetValue;

  return `${description} ${operator} ${target}`;
};

const calculateResults = async () => {
  const isObserveSession = props.session?.goal_type === 'observe';

  if (!props.session) {
    results.value = { error: 'Сеанс не найден.' };
    return;
  }

  if (!isObserveSession && !props.session.metric) {
    results.value = { error: 'Метрика для этого сеанса не найдена.' };
    return;
  }

  const session = props.session;
  const metric = session.metric;
  results.value = { loading: true }; // Set loading state

  const calculateNumericStats = (rows) => {
    const numbers = rows.map(row => parseFloat(row.value)).filter(n => !isNaN(n));
    if (numbers.length > 0) {
      const sum = numbers.reduce((acc, val) => acc + val, 0);
      const avg = sum / numbers.length;
      return {
          min: Math.min(...numbers),
          max: Math.max(...numbers),
          sum: sum,
          average: avg,
          count: numbers.length
      };
    }
    return { min: 0, max: 0, sum: 0, average: 0, count: 0 };
  }

  try {
    const tableName = `session_${session.id}_data`;
    // Fetch all rows, not just a paginated list
    const { data, error: fetchError, fetchData } = useFetch(
      `${apiBaseUrl}/api/users/table/${tableName}/rows/`,
      { credentials: 'include' }
    );
    await fetchData();

    if (fetchError.value) {
      throw new Error(fetchError.value);
    }

    const rows = data.value || [];
    let actualValue = 0;
    
    const stats = {
      totalRows: rows.length,
      numericStats: null,
      categoricalStats: null,
      frequencyStats: null,
      duration: null
    };

    if (session.created_at && session.end_time) {
      const startDate = new Date(session.created_at);
      const endDate = new Date(session.end_time);
      if (!isNaN(startDate) && !isNaN(endDate)) {
        const diffInMs = Math.abs(endDate.getTime() - startDate.getTime());
        const diffInDays = Math.floor(diffInMs / (1000 * 60 * 60 * 24));
        if (diffInDays > 0) {
          stats.duration = `${diffInDays} д.`;
        } else {
          const diffInHours = Math.floor(diffInMs / (1000 * 60 * 60));
          if (diffInHours > 0) {
            stats.duration = `${diffInHours} ч.`;
          } else {
            const diffInMinutes = Math.floor(diffInMs / (1000 * 60));
            stats.duration = `${diffInMinutes} мин.`;
          }
        }
      }
    }

    if (rows.length > 0) {
      const frequency = rows.reduce((acc, row) => {
        const value = String(row.value).trim();
        if (value) {
            acc[value] = (acc[value] || 0) + 1;
        }
        return acc;
      }, {});

      const sortedFrequencies = Object.entries(frequency).sort((a, b) => b[1] - a[1]);

      if (sortedFrequencies.length > 0) {
        stats.frequencyStats = {
          mostFrequent: { value: sortedFrequencies[0][0], count: sortedFrequencies[0][1] },
          leastFrequent: { value: sortedFrequencies[sortedFrequencies.length - 1][0], count: sortedFrequencies[sortedFrequencies.length - 1][1] },
        };
      }
    }

    if (isObserveSession) {
      stats.numericStats = calculateNumericStats(rows);
      results.value = {
        success: null,
        metric: null,
        stats: stats,
      };
      return;
    }

    if (metric.type === 'average' || metric.type === 'sum') {
      const numStats = calculateNumericStats(rows);
      stats.numericStats = numStats;
      if (metric.type === 'sum') {
        actualValue = numStats.sum;
      } else { // average
        actualValue = numStats.average;
      }
    } else if (metric.type === 'count') {
      if (metric.filterValue) {
        const matchingRows = rows.filter(row => row.value === metric.filterValue);
        actualValue = matchingRows.length;
        stats.categoricalStats = {
            matchingCount: actualValue,
            totalCount: rows.length
        };
      } else {
        actualValue = rows.length;
      }
    }
    
    let success = false;
    switch (metric.operator) {
      case '>=': success = actualValue >= metric.targetValue; break;
      case '<=': success = actualValue <= metric.targetValue; break;
      case '==': success = actualValue == metric.targetValue; break;
    }

    results.value = {
      success,
      actualValue: Math.round(actualValue * 100) / 100, // round to 2 decimal places
      targetValue: metric.targetValue,
      metric: metric,
      stats: stats,
    };

  } catch (err) {
    results.value = { error: `Не удалось загрузить или рассчитать результаты: ${err.message}` };
  }
};

watch(() => props.show, (newValue) => {
  if (newValue) {
    results.value = null; // Reset previous results
    calculateResults();
  }
});

</script>
