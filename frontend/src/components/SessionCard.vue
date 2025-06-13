<template>
  <div
    id="session-card-inner"
    class="group relative border border-gray-300 rounded-lg p-4 hover:shadow-lg transition-all duration-200 bg-white mb-5"
    :class="{ 'opacity-50': !session.is_active || session.is_paused }"
  >
    <div class="flex justify-between items-start mb-2">
      <div>
        <div class="flex items-center gap-2">
          <span class="relative flex h-3 w-3 ml-2">
            <span 
              v-if="session.is_active && !session.is_paused"
              class="animate-ping absolute h-full w-full rounded-full bg-green-200 opacity-75"
            ></span>
            <span 
              class="relative rounded-full h-3 w-3"
              :class="{
                'bg-green-200': session.is_active && !session.is_paused,
                'bg-yellow-200': session.is_active && session.is_paused,
                'bg-red-200': !session.is_active
              }"
            ></span>
          </span>
          <h3 class="text-sm sm:text-sm font-semibold text-black">{{ session.title }}</h3>
        </div>
        <div class="text-xs sm:text-xs text-gray-500 mt-1">
           <span v-if="session.is_paused && !isActiveCard" class="px-2 py-1 bg-yellow-200 text-gray-600 rounded-full">
            На паузе
          </span>
          <span v-if="!session.is_active && !session.is_paused && session.time_remaining <= 0" class="px-2 py-1 bg-red-200 text-gray-600 rounded-full">
            Сеанс закончен
          </span>
        </div>
        <div v-if="session.goal_type" id="session-card-goal" class="text-xs sm:text-xs text-gray-600 mt-1">
          <p><span class="font-medium">Цель: </span> 
            <span>{{ session.goal_type === 'observe' ? 'понаблюдать и понять' : 'провести эксперимент' }}</span>
            <span v-if="session.goal_type === 'experiment' && session.metric"> ({{ formatMetric(session.metric) }}) </span>
          </p>
        </div>
        <p v-if="session.is_active && !session.is_paused" id="session-card-time-remaining" class="text-xs sm:text-xs text-gray-600 mt-1">
          <span class="font-medium">Осталось:</span> {{ formatDurationRemaining(session.time_remaining) }}
        </p>
      </div>
      <div id="session-card-controls" class="flex gap-1">
        <!-- Buttons for Active Session Card -->
        <template v-if="isActiveCard">
          <button
            v-tippy="session.is_paused ? 'Возобновить сеанс' : 'Поставить сеанс на паузу'"
            @click.stop="$emit('pause', session.id, !session.is_paused)"
            class="p-1 hover:bg-gray-100 rounded-full"
            >
            <svg class="w-4 h-4 text-gray-600" viewBox="0 0 24 24">
              <path d="M12 2C6.486 2 2 6.486 2 12s4.486 10 10 10 10-4.486 10-10S17.514 2 12 2zm0 18c-4.411 0-8-3.589-8-8s3.589-8 8-8 8 3.589 8 8-3.589 8-8 8z"/>
              <path d='M9 9h2v6H9zm4 0h2v6h-2z'/>
            </svg>
          </button>
          <button
            v-tippy="'Редактировать сеанс'"
            @click.stop="$emit('edit', session)"
            class="p-1 hover:bg-gray-100 rounded-full">
            <svg class="w-4 h-4 text-gray-600" viewBox="0 0 24 24">
              <path d="M12 2C6.486 2 2 6.486 2 12s4.486 10 10 10 10-4.486 10-10S17.514 2 12 2zm0 18c-4.411 0-8-3.589-8-8s3.589-8 8-8 8 3.589 8 8-3.589 8-8 8z"/>
              <path d="M11 11h2v6h-2zm0-4h2v2h-2z"/>
            </svg>
          </button>
          <button
            v-tippy="'Скрыть сеанс'"
              @click.stop="$emit('soft-delete', session)"
              class="p-1 hover:bg-gray-100 rounded-full text-gray-400 hover:text-red-600 transition-colors"
            >
            <svg class="w-4 h-4" viewBox="0 0 24 24">
              <path d="M9.172 16.242L12 13.414l2.828 2.828 1.414-1.414L13.414 12l2.828-2.828-1.414-1.414L12 10.586 9.172 7.758 7.758 9.172 10.586 12l-2.828 2.828z"/>
              <path d="M12 22c5.514 0 10-4.486 10-10S17.514 2 12 2 2 6.486 2 12s4.486 10 10 10zm0-18c4.411 0 8 3.589 8 8s-3.589 8-8 8-8-3.589-8-8 3.589-8 8-8z"/>
            </svg>
          </button>
        </template>
        <!-- Buttons for Inactive Session Card -->
        <template v-else>
            <button
              v-tippy="session.is_paused ? 'Возобновить сеанс' : 'Восстановить сеанс'"
              @click.stop="session.is_active ? $emit('pause', session.id, !session.is_paused) : $emit('restore', session.id)"
              class="p-1 hover:bg-gray-100 rounded-full"
              >
              <svg 
                class="w-4 h-4" 
                :class="{
                  'text-gray-600': session.is_active,
                  'text-green-600': !session.is_active
                }"
                viewBox="0 0 24 24"
              >
                <path d="M12 2C6.486 2 2 6.486 2 12s4.486 10 10 10 10-4.486 10-10S17.514 2 12 2zm0 18c-4.411 0-8-3.589-8-8s3.589-8 8-8 8 3.589 8 8-3.589 8-8 8z"/>
                <path v-if="session.is_active" d='m9 17 8-5-8-5z'/>
                <path v-else d="m6.293 13.293 1.414 1.414L12 10.414l4.293 4.293 1.414-1.414L12 7.586z"/>
              </svg>
            </button>
            <button
              v-tippy="'Редактировать сеанс'"
              @click.stop="$emit('edit', session)"
              class="p-1 hover:bg-gray-100 rounded-full">
              <svg class="w-4 h-4 text-gray-600" viewBox="0 0 24 24">
                <path d="M12 2C6.486 2 2 6.486 2 12s4.486 10 10 10 10-4.486 10-10S17.514 2 12 2zm0 18c-4.411 0-8-3.589-8-8s3.589-8 8-8 8 3.589 8 8-3.589 8-8 8z"/>
                <path d="M11 11h2v6h-2zm0-4h2v2h-2z"/>
              </svg>
            </button>
            <button
              v-tippy="'Удалить сеанс'"
              @click.stop="$emit('delete', session)"
              class="p-1 hover:bg-gray-100 rounded-full text-gray-400 hover:text-red-600 transition-colors"
            >
              <svg class="w-4 h-4" viewBox="0 0 24 24">
                <path d="M9.172 16.242L12 13.414l2.828 2.828 1.414-1.414L13.414 12l2.828-2.828-1.414-1.414L12 10.586 9.172 7.758 7.758 9.172 10.586 12l-2.828 2.828z"/>
                <path d="M12 22c5.514 0 10-4.486 10-10S17.514 2 12 2 2 6.486 2 12s4.486 10 10 10zm0-18c4.411 0 8 3.589 8 8s-3.589 8-8 8-8-3.589-8-8 3.589-8 8-8z"/>
              </svg>
            </button>
        </template>
      </div>
    </div>
    <button 
      v-if="isActiveCard"
      id="session-card-database-button"
      @click="$emit('open-database', session.id)"
      class="w-full p-2 border-2 border-dashed border-gray-300 rounded-lg hover:border-gray-400 transition-colors duration-200 flex flex-col items-center justify-center"
    >
      <div class="w-6 h-6 bg-gray-200 rounded-full flex items-center justify-center">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          viewBox="0 0 24 24"
          class="w-4 h-4 text-white"
        >
          <path fill="currentColor" d="M19 11h-6V5h-2v6H5v2h6v6h2v-6h6z"/>
        </svg>
      </div>
      <p class="text-xs text-gray-600 mt-1">
        Добавить данные
      </p>
    </button>

    <button 
      v-if="!isActiveCard && session.goal_type === 'experiment' && !session.is_active && session.time_remaining <= 0"
      @click.stop="$emit('open-results', session)"
      class="w-full mt-4 p-2 border border-gray-300 rounded-lg bg-blue-50 hover:bg-blue-100 text-blue-700 transition-colors duration-200 flex items-center justify-center text-xs sm:text-sm"
    >
      Показать результаты
    </button>

    <button 
      v-if="!isActiveCard && session.goal_type === 'observe' && !session.is_active && session.time_remaining <= 0"
      @click.stop="$emit('open-results', session)"
      class="w-full mt-4 p-2 border border-gray-300 rounded-lg bg-blue-50 hover:bg-blue-100 text-blue-700 transition-colors duration-200 flex items-center justify-center text-xs sm:text-sm"
    >
      Показать статистику
    </button>

    <div v-if="isActiveCard && session?.visualization_preferences?.length" id="session-card-visualization-area" class="mt-4">
      <div class="space-y-4">
        <component 
          v-for="vizId in session.visualization_preferences"
          :key="`${session.id}-${vizId}-${Date.now()}`"
          :is="getVisualizationComponent(vizId)"
          :session-id="session.id"
          :user-id="userId"
          :session="session"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { directive as VTippy } from 'vue-tippy';
import { declineWord } from '../composables/utils.js';
import SessionVizRating from './SessionVizRating.vue'
import SessionVizCalendar from './SessionVizCalendar.vue'
import SessionVizProgress from './SessionVizProgress.vue'
import SessionVizScatter from './SessionVizScatter.vue'
import SessionVizSankey from './SessionVizSankey.vue'
import SessionVizBoxplot from './SessionVizBoxplot.vue'
import SessionVizHeatmap from './SessionVizHeatmap.vue'

const props = defineProps({
  session: {
    type: Object,
    required: true
  },
  isActiveCard: {
    type: Boolean,
    default: true
  },
  userId: {
    type: String,
    required: true
  }
});

defineEmits(['pause', 'edit', 'soft-delete', 'delete', 'restore', 'open-database', 'open-results']);

const getVisualizationComponent = (type) => {
  const vizId = String(type);
  switch (vizId) {
    case '1': // activity heatmap
      return SessionVizHeatmap
    case '2': // contacts
      return SessionVizRating
    case '3': // calendar
      return SessionVizCalendar
    case '4': // goal progress gauge
      return SessionVizProgress
    case '5': // correlation scatter plot
      return SessionVizScatter
    case '6': // behavioral flow sankey
      return SessionVizSankey
    case '7': // Data Distribution Boxplot
      return SessionVizBoxplot
    default:
      return null
  }
}

const formatDurationRemaining = (seconds) => {
  if (!seconds || seconds <= 0) return '0 дней';
  
  const YEAR_SEC = 365 * 24 * 60 * 60;
  const MONTH_SEC = 30 * 24 * 60 * 60;
  const WEEK_SEC = 7 * 24 * 60 * 60;
  const DAY_SEC = 24 * 60 * 60;
  const HOUR_SEC = 60 * 60;
  const MINUTE_SEC = 60;

  const years = Math.floor(seconds / YEAR_SEC);
  seconds %= YEAR_SEC;
  
  const months = Math.floor(seconds / MONTH_SEC);
  seconds %= MONTH_SEC;
  
  const weeks = Math.floor(seconds / WEEK_SEC);
  seconds %= WEEK_SEC;
  
  const days = Math.floor(seconds / DAY_SEC);
  seconds %= DAY_SEC;
  
  const hours = Math.floor(seconds / HOUR_SEC);
  seconds %= HOUR_SEC;
  
  const minutes = Math.floor(seconds / MINUTE_SEC);

  const parts = [];
  
  if (years > 0) {
    parts.push(`${years} ${declineWord(years, ['год', 'года', 'лет'])}`);
    if (months > 0) parts.push(`${months} ${declineWord(months, ['месяц', 'месяца', 'месяцев'])}`);
    if (weeks > 0) parts.push(`${weeks} ${declineWord(weeks, ['неделя', 'недели', 'недель'])}`);
    if (days > 0) parts.push(`${days} ${declineWord(days, ['день', 'дня', 'дней'])}`);
  } 
  else if (months > 0) {
    parts.push(`${months} ${declineWord(months, ['месяц', 'месяца', 'месяцев'])}`);
    if (weeks > 0) parts.push(`${weeks} ${declineWord(weeks, ['неделя', 'недели', 'недель'])}`);
    if (days > 0) parts.push(`${days} ${declineWord(days, ['день', 'дня', 'дней'])}`);
  } 
  else if (weeks > 0) {
    parts.push(`${weeks} ${declineWord(weeks, ['неделя', 'недели', 'недель'])}`);
    if (days > 0) parts.push(`${days} ${declineWord(days, ['день', 'дня', 'дней'])}`);
  } 
  else if (days > 0) {
    parts.push(`${days} ${declineWord(days, ['день', 'дня', 'дней'])}`);
    if (hours > 0) parts.push(`${hours} ${declineWord(hours, ['час', 'часа', 'часов'])}`);
  } 
  else if (hours > 0) {
    parts.push(`${hours} ${declineWord(hours, ['час', 'часа', 'часов'])}`);
    if (minutes > 0) parts.push(`${minutes} ${declineWord(minutes, ['минута', 'минуты', 'минут'])}`);
  } 
  else {
    parts.push(`${minutes} ${declineWord(minutes, ['минута', 'минуты', 'минут'])}`);
  }

  return parts.length > 0 ? parts.join(' ') : 'меньше минуты';
};

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
</script>
