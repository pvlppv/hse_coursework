<template>
  <!-- Add Session Modal -->
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
        @click="handleOverlayClick"
        @wheel.prevent
        @scroll.prevent
        @touchmove.prevent
        class="fixed inset-0 flex items-center justify-center p-2 sm:p-4 z-[9999] overflow-hidden"
      >
        <div 
          id="add-session-modal"
          @click.stop
          class="bg-white rounded-lg p-4 sm:p-6 w-full max-w-sm sm:max-w-lg max-h-[80vh] flex flex-col overflow-hidden"
        >
          <h3 class="text-base sm:text-lg font-semibold mb-4 text-center flex-shrink-0">Создание сеанса</h3>
          
          <!-- Scrollable content area -->
          <div
            id="session-add-modal-scroll-container"
            @wheel.stop
            @scroll.stop
            @touchmove.stop
            class="flex-1 overflow-y-auto overflow-x-hidden px-2 pb-4"
          >
            <form @submit.prevent="add" class="space-y-4">
              <div class="space-y-1" id="new-session-title-input">
                <label @click.stop.prevent class="text-sm sm:text-base font-medium flex items-center gap-2">
                  <span class="flex items-center justify-center w-6 h-6 rounded-full bg-gray-100 text-gray-600 text-sm">1</span>
                  Что будем отслеживать?
                  <button 
                    type="button"
                    v-tippy="'Название сеанса может отображать, например, общую тему событий, которые ты хочешь отследить, или вопросы, на которые хочешь ответить, в целом всё, что угодно твоей потребности или воображению'"
                    @click.stop
                    class="text-gray-400 hover:text-gray-600"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24">
                      <path d="M12 2C6.486 2 2 6.486 2 12s4.486 10 10 10 10-4.486 10-10S17.514 2 12 2zm0 18c-4.411 0-8-3.589-8-8s3.589-8 8-8 8 3.589 8 8-3.589 8-8 8z"/>
                      <path d="M11 11h2v6h-2zm0-4h2v2h-2z"/>
                    </svg>
                  </button>
                </label>
                <input
                  v-model="newSession.title"
                  type="text"
                  class="w-full p-2 text-xs sm:text-sm border rounded-lg focus:border-gray-300 focus:ring-0"
                  required
                  placeholder="Название сеанса"
                >
              </div>
              
              <div class="space-y-1" id="new-session-duration-input">
                <label @click.stop.prevent class="text-sm sm:text-base font-medium flex items-center gap-2">
                  <span class="flex items-center justify-center w-6 h-6 rounded-full bg-gray-100 text-gray-600 text-sm">2</span>
                  Сколько по времени будем отслеживать?
                  <button 
                    v-tippy="'Продолжительность сеанса можно задать, например, такой, которой тебе, кажется, хватит для достижения цели отслеживания'"
                    @click.stop
                    type="button"
                    class="text-gray-400 hover:text-gray-600"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24">
                      <path d="M12 2C6.486 2 2 6.486 2 12s4.486 10 10 10 10-4.486 10-10S17.514 2 12 2zm0 18c-4.411 0-8-3.589-8-8s3.589-8 8-8 8 3.589 8 8-3.589 8-8 8z"/>
                      <path d="M11 11h2v6h-2zm0-4h2v2h-2z"/>
                    </svg>
                  </button>
                </label>
                
                <div class="space-y-2">
                  <input
                    id="new-session-duration-input-input"
                    :value="formatDuration(newSession.end_time)"
                    type="text"
                    readonly
                    @click="showDurationPicker = true"
                    class="w-full p-2 text-xs sm:text-sm border rounded-lg focus:border-gray-300 focus:ring-0 cursor-pointer"
                    required
                    placeholder="Выбрать продолжительность"
                  >
                  
                  <div class="flex flex-wrap gap-2">
                    <button
                      v-for="preset in durationPresets"
                      :key="preset.label"
                      type="button"
                      @click="applyPresetDuration(preset)"
                      class="px-3 py-1 text-xs rounded-full border hover:bg-gray-50"
                    >
                      {{ preset.label }}
                    </button>
                  </div>
                </div>
              </div>

              <div class="space-y-1" id="new-session-goal-input">
                <label @click.stop.prevent class="text-sm sm:text-base font-medium flex items-center gap-2">
                  <span class="flex items-center justify-center w-6 h-6 rounded-full bg-gray-100 text-gray-600 text-sm">3</span>
                  С какой целью будем отслеживать?
                  <button 
                    type="button"
                    v-tippy="'Цель отслеживания исходит из твоего желания либо просто понаблюдать и понять, что происходит, либо провести эксперимент и проверить свою гипотезу о том, что происходит'"
                    @click.stop
                    class="text-gray-400 hover:text-gray-600"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24">
                      <path d="M12 2C6.486 2 2 6.486 2 12s4.486 10 10 10 10-4.486 10-10S17.514 2 12 2zm0 18c-4.411 0-8-3.589-8-8s3.589-8 8-8 8 3.589 8 8-3.589 8-8 8z"/>
                      <path d="M11 11h2v6h-2zm0-4h2v2h-2z"/>
                    </svg>
                  </button>
                </label>
                <div class="flex flex-col gap-4">
                  <div class="flex gap-4">
                    <button
                      id="new-session-observe-button"
                      type="button"
                      @click="newSession.goalType = 'observe'"
                      class="flex-1 p-2 text-xs sm:text-sm border rounded-lg hover:bg-gray-50 relative text-center"
                      :class="{ 'border-gray-500 bg-gray-50': newSession.goalType === 'observe' }"
                    >
                      Понаблюдать и понять
                    </button>
                    <button
                      id="new-session-experiment-button"
                      type="button"
                      @click="newSession.goalType = 'experiment'"
                      class="flex-1 p-2 text-xs sm:text-sm border rounded-lg hover:bg-gray-50 relative text-center"
                      :class="{ 'border-gray-500 bg-gray-50': newSession.goalType === 'experiment' }"
                    >
                      Провести эксперимент
                    </button>
                  </div>
                </div>
                <!-- Metric Configuration Block -->
                <div v-if="newSession.goalType === 'experiment' && newSession.metric" id="new-session-experiment-metric-input" class="space-y-2 mt-4 p-3 border rounded-lg bg-gray-50">
                  <label class="text-xs sm:text-sm font-medium text-gray-700">Эксперимент успешен, если...</label>
                  <div class="grid grid-cols-1 sm:grid-cols-3 gap-2 items-center">
                    <select v-model="newSession.metric.type" class="w-full p-2 text-xs sm:text-sm border rounded-lg focus:border-gray-300 focus:ring-0">
                      <option value="count">Количество записей</option>
                      <option value="average">Среднее значение</option>
                      <option value="sum">Сумма значений</option>
                    </select>
                    <select v-model="newSession.metric.operator" class="w-full p-2 text-xs sm:text-sm border rounded-lg focus:border-gray-300 focus:ring-0">
                      <option value=">=">&ge;</option>
                      <option value="<=">&le;</option>
                      <option value="==">=</option>
                    </select>
                    <input type="number" v-model.number="newSession.metric.targetValue" placeholder="Цель" class="w-full p-2 text-xs sm:text-sm border rounded-lg focus:border-gray-300 focus:ring-0"/>
                  </div>
                  <div v-if="newSession.metric.type === 'count'">
                    <input type="text" v-model="newSession.metric.filterValue" placeholder="Определённого значения (необязательно)" class="w-full p-2 text-xs sm:text-sm border rounded-lg focus:border-gray-300 focus:ring-0"/>
                  </div>
                  <p v-if="newSession.metric.type === 'average' || newSession.metric.type === 'sum'" class="text-xs text-gray-500">
                    Имей в виду, что эта метрика будет работать только на числовых значениях
                  </p>
                </div>
              </div>

              <div class="space-y-1" id="new-session-data-collection-methods-input">
                <label class="text-sm sm:text-base font-medium flex items-center gap-2">
                  <span class="flex items-center justify-center w-6 h-6 rounded-full bg-gray-100 text-gray-600 text-sm">4</span>
                  Как будем собирать данные?
                </label>
                <div class="flex flex-col gap-4" id="data-collection-buttons">
                  <div class="flex gap-4">
                    <div class="flex-1 relative">
                      <button
                        type="button"
                        @click="newSession.data_collection_methods = ['manual']"
                        class="w-full p-2 text-xs sm:text-sm border rounded-lg hover:bg-gray-50 relative"
                        :class="{ 'border-gray-500 bg-gray-50': newSession.data_collection_methods.includes('manual') }"
                      >
                        Вручную
                      </button>
                    </div>
                    <div class="flex-1 relative">
                      <div class="flex-1 relative" v-tippy="'Скоро будет доступен автоматический сбор данных с сторонних сервисов'">
                        <button
                          type="button"
                          disabled
                          class="w-full p-2 text-xs sm:text-sm border rounded-lg opacity-50 cursor-not-allowed relative group"
                        >
                          Автоматически
                          <div class="absolute inset-0 flex items-center justify-center bg-white bg-opacity-50">
                            <svg class="w-4 h-4" viewBox="0 0 24 24">
                              <path d="M12 2C9.243 2 7 4.243 7 7v3H6c-1.103 0-2 .897-2 2v8c0 1.103.897 2 2 2h12c1.103 0 2-.897 2-2v-8c0-1.103-.897-2-2-2h-1V7c0-2.757-2.243-5-5-5zm6 10 .002 8H6v-8h12zm-9-2V7c0-1.654 1.346-3 3-3s3 1.346 3 3v3H9z"/>
                            </svg>
                          </div>
                          <div class="absolute inset-0 flex items-center justify-center p-2">
                            <img src="../assets/apple_health.svg" class="w-6 h-6 absolute -top-2 -left-2 -rotate-12" alt="Apple Health" />
                            <img src="../assets/google_calendar.png" class="w-6 h-6 absolute -top-2 -right-2 rotate-12" alt="Google Calendar" />
                            <img src="../assets/notion.png" class="w-6 h-6 absolute -bottom-2 -left-2 -rotate-12" alt="Notion" />
                            <img src="../assets/telegram.png" class="w-6 h-6 absolute -bottom-2 -right-2 rotate-12" alt="Telegram" />
                          </div>
                          <!-- <div class="absolute inset-0 rounded-lg shadow-[0_0_15px_rgba(168,85,247,0.5)]"></div> -->
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div class="space-y-1" id="new-session-visualization-preferences-input">
                <label class="text-sm sm:text-base font-medium flex items-center gap-2" id="visualization-label">
                  <span class="flex items-center justify-center w-6 h-6 rounded-full bg-gray-100 text-gray-600 text-sm">5</span>
                  Как будем визуализировать данные?
                </label>
                <div class="grid grid-cols-2 gap-4">
                  <div 
                    v-for="(viz, index) in filteredVisualizations" 
                    :key="index"
                    class="relative group cursor-pointer border border-gray-300 rounded-lg overflow-hidden"
                    :class="{
                      'border-gray-300': !newSession.visualization_preferences.includes(viz.id.toString()),
                      'border-gray-600': newSession.visualization_preferences.includes(viz.id.toString())
                    }"
                    @click="selectViz(viz)"
                  >
                    <img 
                      :src="viz.image" 
                      :alt="viz.title"
                      class="w-full h-32 object-cover transition-opacity duration-200 group-hover:opacity-75"
                      :class="{ 'ring-2 ring-gray-500': newSession.visualization_preferences.includes(viz.id.toString()) }"
                    />
                    <div class="absolute top-2 right-2">
                      <div 
                        class="w-6 h-6 rounded-full border-2 flex items-center justify-center"
                        :class="{
                          'bg-gray-600 border-gray-600': newSession.visualization_preferences.includes(viz.id.toString()),
                          'bg-white border-gray-300': !newSession.visualization_preferences.includes(viz.id.toString())
                        }"
                      >
                        <svg 
                          v-if="newSession.visualization_preferences.includes(viz.id.toString())"
                          class="w-4 h-4 text-white" 
                          viewBox="0 0 24 24"
                        >
                          <path fill="currentColor" d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41L9 16.17z"/>
                        </svg>
                      </div>
                    </div>
                    <div 
                      class="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-200"
                    >
                      <div class="flex gap-2">
                        <button
                          v-tippy="'Посмотреть описание графика'"
                          @click.stop="openVizModal(viz, $event)"
                          class="p-1.5 bg-white rounded-full shadow-lg hover:bg-gray-50 border border-gray-300"
                        >
                          <svg class="w-4 h-4" viewBox="0 0 24 24">
                            <path d="M12 10c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm6 0c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zM6 10c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z"/>
                          </svg>
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div class="space-y-1" id="new-session-analysis-methods-input">
                <label class="text-sm sm:text-base font-medium flex items-center gap-2">
                  <span class="flex items-center justify-center w-6 h-6 rounded-full bg-gray-100 text-gray-600 text-sm">6</span>
                  Как будем анализировать данные?
                </label>
                <div class="flex flex-col gap-4" id="analysis-buttons">
                  <div class="flex gap-4">
                    <div class="flex-1 relative">
                      <div class="flex-1 relative" v-tippy="'Скоро будет доступен анализ данных с помощью аналитических инструментов'">
                        <button
                          type="button"
                          disabled
                          class="w-full p-2 text-xs sm:text-sm border rounded-lg opacity-50 cursor-not-allowed relative group"
                        >
                          Через инструменты
                          <div class="absolute inset-0 flex items-center justify-center bg-white bg-opacity-50">
                            <svg class="w-4 h-4" viewBox="0 0 24 24">
                              <path d="M12 2C9.243 2 7 4.243 7 7v3H6c-1.103 0-2 .897-2 2v8c0 1.103.897 2 2 2h12c1.103 0 2-.897 2-2v-8c0-1.103-.897-2-2-2h-1V7c0-2.757-2.243-5-5-5zm6 10 .002 8H6v-8h12zm-9-2V7c0-1.654 1.346-3 3-3s3 1.346 3 3v3H9z"/>
                            </svg>
                          </div>
                        </button>
                      </div>
                    </div>
                    <div class="flex-1 relative">
                      <div class="flex-1 relative" v-tippy="'Скоро будет доступен анализ данных с помощью ИИ'">
                        <button
                          type="button"
                          disabled
                          class="w-full p-2 text-xs sm:text-sm border rounded-lg opacity-50 cursor-not-allowed relative group"
                        >
                          Через ИИ
                          <div class="absolute inset-0 flex items-center justify-center bg-white bg-opacity-50">
                            <svg class="w-4 h-4" viewBox="0 0 24 24">
                              <path d="M12 2C9.243 2 7 4.243 7 7v3H6c-1.103 0-2 .897-2 2v8c0 1.103.897 2 2 2h12c1.103 0 2-.897 2-2v-8c0-1.103-.897-2-2-2h-1V7c0-2.757-2.243-5-5-5zm6 10 .002 8H6v-8h12zm-9-2V7c0-1.654 1.346-3 3-3s3 1.346 3 3v3H9z"/>
                            </svg>
                          </div>
                          <svg class="w-6 h-6 absolute -top-2 -right-2" viewBox="0 0 24 24" transform="scale(-1, 1)">
                            <path d="m11 4-.5-1-.5 1-1 .125.834.708L9.5 6l1-.666 1 .666-.334-1.167.834-.708zm8.334 10.666L18.5 13l-.834 1.666-1.666.209 1.389 1.181L16.834 18l1.666-1.111L20.166 18l-.555-1.944L21 14.875zM6.667 6.333 6 5l-.667 1.333L4 6.5l1.111.944L4.667 9 6 8.111 7.333 9l-.444-1.556L8 6.5zM3.414 17c0 .534.208 1.036.586 1.414L5.586 20c.378.378.88.586 1.414.586s1.036-.208 1.414-.586L20 8.414c.378-.378.586-.88.586-1.414S20.378 5.964 20 5.586L18.414 4c-.756-.756-2.072-.756-2.828 0L4 15.586c-.378.378-.586.88-.586 1.414zM17 5.414 18.586 7 15 10.586 13.414 9 17 5.414z"/>
                          </svg>
                          <!-- <div class="absolute inset-0 rounded-lg shadow-[0_0_15px_rgba(168,85,247,0.5)]"></div> -->
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </form>
          </div>

          <!-- Sticky footer for buttons -->
          <div class="mt-5 mb-2 flex-shrink-0">
            <div class="flex justify-center gap-3" id="new-session-submit-button">
              <button
                type="button"
                @click="$emit('close')"
                :disabled="isOnboardingActive"
                class="px-3 sm:px-4 py-1.5 sm:py-2 text-xs sm:text-sm rounded-lg border border-gray-300 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Отменить
              </button>
              <button
                type="submit"
                @click="add"
                :disabled="!newSession.title || !newSession.end_time || !newSession.visualization_preferences.length || !newSession.goalType"
                class="px-3 sm:px-4 py-1.5 sm:py-2 text-xs sm:text-sm rounded-lg border border-gray-600 bg-gray-600 text-white hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed flex-1 max-w-[200px]"
              >
                Начать
              </button>
            </div>
          </div>
        </div>
      </div>
    </Transition>
    <SessionDurationPicker 
      :show="showDurationPicker"
      @close="showDurationPicker = false"
      @apply="applyCustomDuration"
    />
    <SessionVisualizationPicker
      :show="showVizModal"
      :visualization="selectedViz"
      @close="showVizModal = false"
      @confirm="confirmVizSelection"
    />
  </Teleport>
</template>

<script setup>
import { ref, watch, reactive, computed } from 'vue';
import { directive as VTippy } from 'vue-tippy';
import { declineWord } from '../composables/utils.js';
import SessionDurationPicker from './SessionDurationPicker.vue';
import SessionVisualizationPicker from './SessionVisualizationPicker.vue';
import { isOnboardingActive, canCloseModalOverride } from '../composables/onboarding.js';

const props = defineProps({
  show: {
    type: Boolean,
    required: true,
  },
  visualizations: {
    type: Array,
    default: () => []
  },
  durationPresets: {
    type: Array,
    default: () => []
  }
});

const emit = defineEmits(['close', 'add']);

const handleOverlayClick = () => {
  if (!isOnboardingActive.value || canCloseModalOverride.value) {
    emit('close');
  }
};

const newSession = reactive({
  title: '',
  end_time: null,
  data_collection_methods: ['manual'],
  visualization_preferences: [],
  goalType: null,
  metric: null
});

watch(() => newSession.goalType, (newGoalType) => {
  if (newGoalType === 'experiment') {
    newSession.metric = {
      type: 'count',
      operator: '>=',
      targetValue: 1,
      filterValue: ''
    };
  } else if (newGoalType === 'observe') {
    newSession.metric = null;
  }

  // Filter selected visualizations based on the new goal type
  if (newGoalType) {
    const availableVizIds = props.visualizations
      .filter(v => v.goalType.includes(newGoalType))
      .map(v => v.id.toString());
    
    newSession.visualization_preferences = newSession.visualization_preferences.filter(
      id => availableVizIds.includes(id)
    );
  }
});

const filteredVisualizations = computed(() => {
  if (!newSession.goalType) {
    return props.visualizations;
  }
  return props.visualizations.filter(v => v.goalType.includes(newSession.goalType));
});

const formatDuration = (dateString) => {
  if (!dateString) return '';
  
  const end = new Date(dateString);
  const now = new Date();
  const diffTime = end - now;
  let diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

  if (diffDays <= 0) return '0 дней';

  const YEARS = 365;
  const MONTHS = 30;
  const WEEKS = 7;

  const years = Math.floor(diffDays / YEARS);
  diffDays %= YEARS;
  
  const months = Math.floor(diffDays / MONTHS);
  diffDays %= MONTHS;
  
  const weeks = Math.floor(diffDays / WEEKS);
  const days = diffDays % WEEKS;

  const parts = [];
  if (years > 0) parts.push(`${years} ${declineWord(years, ['год', 'года', 'лет'])}`);
  if (months > 0) parts.push(`${months} ${declineWord(months, ['месяц', 'месяца', 'месяцев'])}`);
  if (weeks > 0) parts.push(`${weeks} ${declineWord(weeks, ['неделя', 'недели', 'недель'])}`);
  if (days > 0) parts.push(`${days} ${declineWord(days, ['день', 'дня', 'дней'])}`);

  return parts.join(', ') || '0 дней';
};

const showDurationPicker = ref(false);

const applyCustomDuration = (duration) => {
  const date = new Date();
  
  let totalDays = 0;
  if (duration.years) totalDays += Number(duration.years) * 365;
  if (duration.months) totalDays += Number(duration.months) * 30;
  if (duration.weeks) totalDays += Number(duration.weeks) * 7;
  if (duration.days) totalDays += Number(duration.days);
  
  date.setDate(date.getDate() + totalDays);
  
  newSession.end_time = date.toISOString().slice(0, 16);
  showDurationPicker.value = false;
}

const applyPresetDuration = (preset) => {
  const date = new Date();
  date.setDate(date.getDate() + preset.days);
  newSession.end_time = date.toISOString().slice(0, 16);
}

const selectViz = (viz) => {
  const vizId = viz.id.toString();
  const index = newSession.visualization_preferences.indexOf(vizId);
  if (index === -1) {
    newSession.visualization_preferences.push(vizId);
  } else {
    newSession.visualization_preferences.splice(index, 1);
  }
}

const showVizModal = ref(false);
const selectedViz = ref(null);

const openVizModal = (viz, event) => {
  event.preventDefault();
  event.stopPropagation();
  selectedViz.value = viz;
  showVizModal.value = true;
}

const confirmVizSelection = () => {
  if (selectedViz.value) {
    const vizId = selectedViz.value.id.toString();
    if (!newSession.visualization_preferences.includes(vizId)) {
        newSession.visualization_preferences.push(vizId);
    }
  }
  showVizModal.value = false;
  selectedViz.value = null;
}

const add = () => {
    const sessionData = {
        title: newSession.title,
        end_time: newSession.end_time,
        data_collection_methods: newSession.data_collection_methods,
        visualization_preferences: newSession.visualization_preferences,
        goal_type: newSession.goalType,
        metric: newSession.metric,
    };
    emit('add', sessionData);

    // Reset form
    Object.assign(newSession, {
        title: '',
        end_time: null,
        data_collection_methods: ['manual'],
        visualization_preferences: [],
        goalType: null,
        metric: null
    });
};
</script>
<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
