<template>
  <div class="w-full">
    <div v-if="error" class="p-4 text-xs sm:text-sm text-center text-red-800 border border-red-300 rounded-lg bg-red-50" role="alert">
      <p>На сервере что-то сломалось, данные не достались из базы данных :(</p>
      <p><a href="https://t.me/pvlppv" class="text-blue-600 hover:text-blue-800">Напишите мне</a>, я починю.</p>
    </div>
    <div v-else class="qalendar-wrapper is-light-mode">
      <Qalendar :selected-date="new Date()" :events="events" :config="config"/>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed, nextTick } from 'vue'
import { useFetch } from '../composables/utils.js'
import { Qalendar } from 'qalendar'
import 'qalendar/dist/style.css'

const props = defineProps({
  sessionId: {
    type: [String, Number],
    required: true
  },
  userId: {
    type: [String, Number],
    required: true
  }
})

const apiBaseUrl = import.meta.env.VITE_APP_API_BASE_URL
const events = ref([])
const error = ref(null)
const lastActivity = ref(null)

// Process session data into Qalendar-compatible format
const processEvents = (data) => {
  if (!data || !Array.isArray(data)) return []
  
  const sortedData = data.sort((a, b) => new Date(a.datetime) - new Date(b.datetime))
  lastActivity.value = sortedData[sortedData.length - 1]

  return sortedData.map((item, index) => {
    // Parse the datetime string and format it
    const startDate = new Date(item.datetime)
    // Adjust for Moscow timezone (UTC+3)
    const moscowOffset = 3 * 60 * 60 * 1000 // 3 hours in milliseconds
    const moscowTime = new Date(startDate.getTime() + moscowOffset)
    
    const start = `${moscowTime.getFullYear()}-${String(moscowTime.getMonth() + 1).padStart(2, '0')}-${String(moscowTime.getDate()).padStart(2, '0')} ${String(moscowTime.getHours()).padStart(2, '0')}:${String(moscowTime.getMinutes()).padStart(2, '0')}`

    let end
    if (index === sortedData.length - 1 || 
        new Date(sortedData[index + 1].datetime).toDateString() !== startDate.toDateString()) {
      // Last activity of the day, stretch to 23:59
      end = `${start.split(' ')[0]} 23:59`
    } else {
      // Set end time to the start time of the next activity
      const nextStartDate = new Date(sortedData[index + 1].datetime)
      const nextMoscowTime = new Date(nextStartDate.getTime() + moscowOffset)
      end = `${nextMoscowTime.getFullYear()}-${String(nextMoscowTime.getMonth() + 1).padStart(2, '0')}-${String(nextMoscowTime.getDate()).padStart(2, '0')} ${String(nextMoscowTime.getHours()).padStart(2, '0')}:${String(nextMoscowTime.getMinutes()).padStart(2, '0')}`
    }

    return {
      title: item.value,
      time: { start, end },
      id: item.id,
      isEditable: false,
    }
  })
}

// Calendar configuration
const config = computed(() => ({
  week: {
    startsOn: 'monday',
    nDays: 7,
    scrollToHour: lastActivity.value ? new Date(lastActivity.value.datetime).getHours() : new Date().getHours(),
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
  showCurrentTime: true,
  disableModes: ['month'],
  eventDialog: {
    isDisabled: true,
  },
  dayIntervals: {
    length: 30,
    height: 30,
  },
}))

const fetchData = async () => {
  try {
    error.value = null
    
    const tableName = `session_${props.sessionId}_data`
    const { data: fetchData, error: fetchError, fetchData: fetch } = useFetch(
      `${apiBaseUrl}/api/users/table/${tableName}/rows/`,
      { credentials: 'include' }
    )
    
    await fetch()
    
    if (fetchError.value) {
      console.error('Error fetching data:', fetchError.value)
      error.value = 'Не удалось загрузить данные'
      events.value = []
      return
    }
    
    if (fetchData.value) {
      events.value = processEvents(fetchData.value)
    } else {
      events.value = []
    }
  } catch (error) {
    console.error('Error in fetchData:', error)
    error.value = 'Произошла ошибка при загрузке данных'
    events.value = []
  }
}

onMounted(() => {
  fetchData()
  setupEndTimeObserver()
})

function setupEndTimeObserver() {
  const targetNode = document.querySelector('.qalendar-wrapper')
  if (!targetNode) return

  const config = { childList: true, subtree: true }

  const callback = function(mutationsList, observer) {
    for(let mutation of mutationsList) {
      if (mutation.type === 'childList') {
        replaceEndTime()
      }
    }
  }

  const observer = new MutationObserver(callback)
  observer.observe(targetNode, config)
}

function replaceEndTime() {
  const timeElements = document.querySelectorAll('.calendar-week__event-row.is-time span, .calendar-day__event-row.is-time span')
  timeElements.forEach(el => {
    if (el.textContent.endsWith('23:59')) {
      el.textContent = el.textContent.replace('23:59', '...')
    }
  })
}
</script>

<style scoped>
.qalendar-wrapper {
  height: 500px;
}
</style> 