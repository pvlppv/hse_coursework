<template>
  <div class="container mx-auto flex justify-center relative">
    <div id="sessions-list" class="max-w-sm sm:max-w-lg w-full space-y-2">
      <!-- Error message -->
      <div v-if="error" class="p-4 text-xs sm:text-sm text-center text-red-800 border border-red-300 rounded-lg bg-red-50" role="alert">
        {{ error }}
        <p>На сервере что-то сломалось, данные не достались из базы данных :(</p>
        <p><a href="https://t.me/pvlppv" class="text-blue-600 hover:text-blue-800">Напишите мне</a>, я починю.</p>
      </div>
      
      <!-- Sessions List -->
      <div v-else>
        <div v-if="activeSessions.length" id="active-sessions-list-container">
          <SessionCard
            v-for="session in sortedActiveSessions"
            :key="session.id"
            :session="session"
            :is-active-card="true"
            :user-id="userId"
            @pause="pauseSession"
            @edit="openEditModal"
            @soft-delete="openSoftDeleteModal"
            @open-database="openDatabaseModal"
          />
        </div>
        
        <!-- Add Session Button -->
        <button
          id="add-session-button"
          @click="showAddModal = true"
          class="w-full p-4 border-2 border-dashed border-gray-300 rounded-lg hover:border-gray-400 transition-colors duration-200 flex flex-col items-center justify-center"
        >
          <div class="w-8 h-8 bg-gray-200 rounded-full flex items-center justify-center">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="24"
              height="24"
              viewBox="0 0 24 24"
              class="w-5 h-5 text-white"
            >
              <path fill="currentColor" d="M19 11h-6V5h-2v6H5v2h6v6h2v-6h6z"/>
            </svg>
          </div>
          <p class="text-xs sm:text-sm text-gray-600 mt-2">
            Начать новый сеанс
          </p>
        </button>

        <!-- Show/Hide Archived Sessions -->
        <button 
          id="show-inactive-button"
          @click="showInactive || fetchSessions(false); showInactive = !showInactive"
          class="w-full flex items-center justify-center gap-2 px-4 py-3 text-xs sm:text-sm hover:bg-gray-50 text-gray-700 rounded-lg transition-colors border border-gray-200 mt-4"
        >
          <span>{{ showInactive ? 'Скрыть неактивные сеансы' : 'Показать неактивные сеансы' }}</span>
          <svg class="w-4 h-4 transform transition-transform" :class="{'rotate-180': showInactive}" viewBox="0 0 24 24">
            <path fill="currentColor" d="M7.41 8.59L12 13.17l4.59-4.58L18 10l-6 6-6-6 1.41-1.41z"/>
          </svg>
        </button>

        <!-- Inactive Sessions List -->
        <p 
          v-if="showInactive && !inactiveSessions.length" 
          class="text-xs sm:text-sm text-gray-600 mt-4 text-center bg-gray-50 rounded-lg py-8 px-4"
        >
          Неактивных сеансов нет
        </p>
        <div v-if="showInactive && inactiveSessions.length" class="mt-4">
            <SessionCard
              v-for="session in sortedInactiveSessions"
              :key="session.id"
              :session="session"
              :is-active-card="false"
              :user-id="userId"
              @restore="restoreSession"
              @pause="pauseSession"
              @edit="openEditModal"
              @delete="openDeleteModal"
              @open-results="openResultsModal"
            />
        </div>
      </div>
    </div>

    <!-- Modals -->
    <SessionAddModal
      :show="showAddModal"
      :visualizations="visualizations"
      :duration-presets="durationPresets"
      @close="showAddModal = false"
      @add="addSession"
    />
    <SessionEditModal
      :show="showEditModal"
      :session="editableSession"
      :visualizations="visualizations"
      :duration-presets="durationPresets"
      @close="showEditModal = false"
      @save="saveSession"
    />
    <SessionDeleteModal
      :show="showDeleteModal"
      @close="showDeleteModal = false"
      @confirm="deleteSession"
    />
    <SessionSoftDeleteModal
      :show="showSoftDeleteModal"
      @close="showSoftDeleteModal = false"
      @confirm="softDeleteSession(deleteTargetId)"
    />
    <SessionResultsModal
      :show="showResultsModal"
      :session="sessionForResults"
      @close="showResultsModal = false"
    />
    <SessionDatabase 
      :show="showDatabaseModal"
      :tableName="currentDatabaseTableName"
      :title="getSessionTitle(currentDatabaseTableName)"
      @close="closeDatabaseModal"
      @data-updated="handleDatabaseUpdate"
    />
    <SessionPauseModal
      :show="showPauseModal"
      :is-paused="!pauseTargetState"
      @close="showPauseModal = false"
      @confirm="confirmPause"
    />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed, watch } from 'vue'
import { useFetch } from '../composables/utils.js';
import SessionDatabase from './SessionDatabase.vue'
import SessionCard from './SessionCard.vue'
import SessionAddModal from './SessionAddModal.vue'
import SessionEditModal from './SessionEditModal.vue'
import SessionDeleteModal from './SessionDeleteModal.vue'
import SessionSoftDeleteModal from './SessionSoftDeleteModal.vue'
import SessionResultsModal from './SessionResultsModal.vue'
import SessionPauseModal from './SessionPauseModal.vue'

const apiBaseUrl = import.meta.env.VITE_APP_API_BASE_URL;

const props = defineProps({
  userId: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['update:show-add-modal', 'update:active-sessions'])

// State
const activeSessions = ref([])
const inactiveSessions = ref([])
const loading = ref(true)
const error = ref(null)
const showAddModal = ref(false)
const showEditModal = ref(false)
const showDeleteModal = ref(false)
const showSoftDeleteModal = ref(false)
const showPauseModal = ref(false)
const pauseTargetId = ref(null)
const pauseTargetState = ref(false)
const editableSession = ref(null);
const deleteTargetId = ref(null)

const showInactive = ref(false)
const sortedActiveSessions = computed(() => {
  return [...activeSessions.value].sort((a, b) => a.time_remaining - b.time_remaining)
})
const sortedInactiveSessions = computed(() => {
  return [...inactiveSessions.value].sort((a, b) => new Date(b.updated_at) - new Date(a.updated_at))
})

const durationPresets = [
  { label: '1 неделю', days: 7 },
  { label: '1 месяц', days: 30 },
  { label: '3 месяца', days: 90 },
  { label: '6 месяцев', days: 180 },
  { label: '1 год', days: 365 },
]

// UI Handlers
const openEditModal = (session) => {
  editableSession.value = session;
  showEditModal.value = true
}

const openDeleteModal = (session) => {
  deleteTargetId.value = session.id
  showDeleteModal.value = true
}

const openSoftDeleteModal = (session) => {
  deleteTargetId.value = session.id
  showSoftDeleteModal.value = true
}

const saveSession = async (sessionData) => {
  await updateSession(sessionData.id, {
    title: sessionData.title,
    end_time: sessionData.end_time,
    data_collection_methods: sessionData.data_collection_methods,
    visualization_preferences: sessionData.visualization_preferences,
    goal_type: sessionData.goalType,
    metric: sessionData.metric
  })    
  showEditModal.value = false
}

const addSession = async (sessionData) => {
  try {
    await createSession(sessionData)
    showAddModal.value = false
  } catch (err) {
    error.value = err.message || 'Не удалось создать сеанс'
    throw err
  }
}

// Session operations with proper endpoint alignment
const fetchSessions = async (activeOnly = true) => {
  try {
    loading.value = true
    const url = new URL(`${apiBaseUrl}/api/users/sessions/get`)
    url.searchParams.set('active_only', activeOnly)
    
    const { data, error: fetchError, fetchData } = useFetch(
      url.toString(),
      { credentials: 'include' }
    )
    await fetchData()

    if (fetchError.value) throw fetchError.value

    const now = new Date();
    const sessions = data.value || [];
    
    // Filter and update sessions based on their end time
    const processedSessions = sessions.map(session => {
      const endTime = new Date(session.end_time);
      const isEnded = endTime <= now;
      
      // If session has ended, update its status
      if (isEnded && session.is_active) {
        session.is_active = false;
        session.is_paused = false;
      }
      
      return session;
    });

    if (activeOnly) {
      activeSessions.value = processedSessions.filter(s => s.is_active && !s.is_paused);
    } else {
      inactiveSessions.value = processedSessions.filter(s => !s.is_active || s.is_paused);
    }
    
    return processedSessions;
  } catch (err) {
    error.value = err.message || 'Не удалось получить сеансы'
    throw err
  } finally {
    loading.value = false
  }
}

const createVizTable = async (sessionId) => {
  try {
    const tableName = `session_${sessionId}_data`
    const { error: fetchError, fetchData } = useFetch(
      `${apiBaseUrl}/api/users/table/`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: { 
          table_name: tableName,
          schema: {
            id: 'INTEGER PRIMARY KEY AUTOINCREMENT',
            value: 'TEXT',
            date: 'TEXT',
            time: 'TEXT'
          }
        },
        credentials: 'include'
      }
    )

    await fetchData()

    if (fetchError.value) {
      console.error('Error creating session data table:', fetchError.value)
      throw new Error(fetchError.value || 'Failed to create session data table')
    }
  } catch (err) {
    console.error('Error creating session data table:', err)
    throw err
  }
}

const deleteVizTable = async (sessionId) => {
  try {
    const tableName = `session_${sessionId}_data` 
    const { data, error: fetchError, fetchData: deleteTable } = useFetch(
      `${apiBaseUrl}/api/users/table/${tableName}/`,
      {
        method: 'DELETE',
        credentials: 'include'
      }
    )

    await deleteTable()

    if (fetchError.value) {
      console.error('Error deleting session data table:', fetchError.value)
    }
  } catch (err) {
    console.error('Error deleting session data table:', err)
  }
}

const createSession = async (sessionData) => {
  try {
    const { data, error: fetchError, fetchData } = useFetch(
      `${apiBaseUrl}/api/users/sessions/create`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: sessionData,
        credentials: 'include'
      }
    )
    await fetchData()

    if (fetchError.value) throw fetchError.value

    const newSession = data.value

    if (newSession.visualization_preferences.length > 0) {
      await createVizTable(newSession.id)
    }

    activeSessions.value.push(newSession)

    return newSession
  } catch (err) {
    error.value = err.message || 'Failed to create session'
    throw err
  }
}

const updateSession = async (sessionId, updateData) => {
  try {
    const currentSession = activeSessions.value.find(s => s.id === sessionId) || 
                         inactiveSessions.value.find(s => s.id === sessionId)
    
    const { data, error: fetchError, fetchData } = useFetch(
      `${apiBaseUrl}/api/users/sessions/${sessionId}/edit`,
      {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: updateData,
        credentials: 'include'
      }
    )
    await fetchData()

    if (fetchError.value) throw fetchError.value

    const updatedSession = data.value
    
    const now = new Date()
    const endTime = new Date(updatedSession.end_time)
    if (endTime <= now) {
      deleteTargetId.value = sessionId
      await softDeleteSession(sessionId)
      return
    }

    if (currentSession && 
        updatedSession.visualization_preferences.length > 0 && 
        !currentSession.visualization_preferences.length) {
      await createVizTable(sessionId)
    }

    const isActive = updatedSession.is_active && !updatedSession.is_paused
    if (isActive) {
      const index = activeSessions.value.findIndex(s => s.id === sessionId)
      if (index > -1) {
        activeSessions.value[index] = updatedSession
      }
    } else {
      const index = inactiveSessions.value.findIndex(s => s.id === sessionId)
      if (index > -1) {
        inactiveSessions.value[index] = updatedSession
      }
    }
    return updatedSession
  } catch (err) {
    error.value = err.message || 'Failed to update session'
    throw err
  }
}

const deleteSession = async () => {
  try {
    try {
      await deleteVizTable(deleteTargetId.value)
    } catch (err) {
      console.error('Error deleting session data table:', err)
    }

    const { error: fetchError, fetchData } = useFetch(
      `${apiBaseUrl}/api/users/sessions/${deleteTargetId.value}/delete`,
      { 
        method: 'DELETE',
        credentials: 'include' 
      }
    )
    await fetchData()

    if (fetchError.value) throw fetchError.value
    
    await Promise.all([
      fetchSessions(true),
      showInactive.value == true && fetchSessions(false)
    ])
    showDeleteModal.value = false
    deleteTargetId.value = null
  } catch (err) {
    error.value = err.message || 'Не удалось удаление сеанса'
    throw err
  }
}

const softDeleteSession = async (sessionId) => {
  if (!sessionId) {
    error.value = 'Не удалось перенести сеанс в неактивные: отсутствует ID сеанса'
    return
  }

  try {
    const { error: fetchError, fetchData } = useFetch(
      `${apiBaseUrl}/api/users/sessions/${sessionId}/soft_delete`,
      { 
        method: 'DELETE',
        credentials: 'include' 
      }
    )
    await fetchData()

    if (fetchError.value) throw fetchError.value
    
    showInactive.value = true
    
    await Promise.all([
      fetchSessions(true),
      fetchSessions(false)
    ])
    showSoftDeleteModal.value = false
    deleteTargetId.value = null
  } catch (err) {
    error.value = err.message || 'Не удалось перенести сеанс в неактивные'
  }
}

const pauseSession = async (sessionId, isPaused) => {
  pauseTargetId.value = sessionId
  pauseTargetState.value = isPaused
  showPauseModal.value = true
}

const confirmPause = async () => {
  try {    
    const { data, error: fetchError, fetchData } = useFetch(
      `${apiBaseUrl}/api/users/sessions/${pauseTargetId.value}/pause`,
      {
        method: 'PATCH',
        headers: { 
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: { is_paused: pauseTargetState.value },
        credentials: 'include'
      }
    )
    
    await fetchData()

    if (fetchError.value) throw fetchError.value

    if (pauseTargetState.value) {
      showInactive.value = true
    }

    await Promise.all([
      fetchSessions(true),
      fetchSessions(false)
    ])

    showPauseModal.value = false
    pauseTargetId.value = null
    pauseTargetState.value = false
  } catch (err) {
    error.value = err.message || 'Не удалось обновить статус паузы'
    throw err
  }
}

const restoreSession = async (sessionId) => {
  try {
    const { data, error: fetchError, fetchData } = useFetch(
      `${apiBaseUrl}/api/users/sessions/${sessionId}/restore`,
      {
        method: 'PATCH',
        headers: { 
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        credentials: 'include'
      }
    )
    await fetchData()

    if (fetchError.value) throw fetchError.value

    await Promise.all([
      fetchSessions(true),
      fetchSessions(false)
    ])
  } catch (err) {
    error.value = err.message || 'Не удалось восстановить сеанс'
    throw err
  }
}

onMounted(async () => {
  await fetchSessions()
})

watch(showAddModal, (newValue) => {
  emit('update:show-add-modal', newValue)
})

watch(activeSessions, (newValue) => {
  emit('update:active-sessions', newValue);
})

const visualizations = [
  {
    id: 1,
    title: 'Интенсивность',
    description: 'Визуализация показывает, как часто происходит событие. Идеально для отслеживания одной повторяющейся привычки или активности. Подходит для отслеживания одного события.',
    image: new URL('../assets/heatmap.png', import.meta.url).href,
    goalType: ['observe', 'experiment']
  },
  {
    id: 2,
    title: 'Рейтинг',
    description: 'Визуализация показывает, какие из событий происходят чаще всего, а какие реже. Идеально для ранжирования нескольких событий. Подходит для отслеживания нескольких событий.',
    image: new URL('../assets/rating.png', import.meta.url).href,
    goalType: ['observe', 'experiment']
  },
  {
    id: 3,
    title: 'Календарь',
    description: 'Визуализация показывает, когда именно происходят события, и сколько они длятся по времени. Подходит для отслеживания одного или нескольких событий.',
    image: new URL('../assets/calendar.png', import.meta.url).href,
    goalType: ['observe', 'experiment']
  },
  {
    id: 4,
    title: 'Прогресс',
    description: 'Визуализация показывает прогресс в достижении экспериментальной цели. Подходит для отслеживаний одного или нескольких событий.',
    image: new URL('../assets/progress.png', import.meta.url).href,
    goalType: ['experiment']
  },
  { 
    id: 5, 
    title: 'Корреляция', 
    description: 'Визуализация показывает взаимосвязь между частотой происхождения нескольких событий. Идеально для проверки гипотез вроде "влияет ли одно на другое". Подходит для отслеживания нескольких событий.',
    image: new URL('../assets/scatter.png', import.meta.url).href,
    goalType: ['observe', 'experiment']
  },
  {
    id: 6,
    title: 'Поток',
    description: 'Визуализация показывает, как часто происходят события друг за другом. Идеально для отслеживания последовательности событий. Подходит для отслеживания одного или нескольких событий.',
    image: new URL('../assets/sankey.png', import.meta.url).href,
    goalType: ['observe', 'experiment']
  },
  {
    id: 7,
    title: 'Распределение данных',
    description: 'Визуализация показывает распределение числовых данных по времени. Помогает понять диапазон, стабильность и выявить выбросы. Подходит для отслеживания одного или нескольких событий.',
    image: new URL('../assets/boxplot.png', import.meta.url).href,
    goalType: ['observe', 'experiment']
  }
]

const showDatabaseModal = ref(false)
const currentDatabaseTableName = ref('')

const openDatabaseModal = (sessionId) => {
  currentDatabaseTableName.value = `session_${sessionId}_data`
  showDatabaseModal.value = true
}
const closeDatabaseModal = () => {
  showDatabaseModal.value = false;
  currentDatabaseTableName.value = '';
};

const handleDatabaseUpdate = (updatedSession) => {
  if (!updatedSession) return;
  
  const isActive = updatedSession.is_active && !updatedSession.is_paused;
  if (isActive) {
    const index = activeSessions.value.findIndex(s => s.id === updatedSession.id);
    if (index > -1) {
      activeSessions.value.splice(index, 1, updatedSession);
    }
  } else {
    const index = inactiveSessions.value.findIndex(s => s.id === updatedSession.id);
    if (index > -1) {
      inactiveSessions.value.splice(index, 1, updatedSession);
    }
  }
};

const getSessionTitle = (tableName) => {
  if (!tableName) return '';
  const sessionId = parseInt(tableName.split('_')[1], 10);
  const session = activeSessions.value.find(s => s.id === sessionId) || 
                 inactiveSessions.value.find(s => s.id === sessionId);
  return session ? session.title : '';
};

const showResultsModal = ref(false)
const sessionForResults = ref(null)

const openResultsModal = (session) => {
  sessionForResults.value = session;
  showResultsModal.value = true;
};

</script>
