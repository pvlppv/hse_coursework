<template>
  <div class="w-full">
    <div v-if="error" class="p-4 text-xs sm:text-sm text-center text-red-800 border border-red-300 rounded-lg bg-red-50" role="alert">
      <p>На сервере что-то сломалось, данные не достались из базы данных :(</p>
      <p><a href="https://t.me/pvlppv" class="text-blue-600 hover:text-blue-800">Напишите мне</a>, я починю.</p>
    </div>

    <div v-else class="px-1 py-4 sm:px-2 sm:py-5 border border-gray-300 rounded-lg">
      <div class="space-y-6">
        <div class="space-y-1 sm:space-y-2 cursor-pointer" @click="openModal">
          <calendar-heatmap
            :values="heatmapData"
            :round="2"
            :end-date="endDate"
            :range-color="['#f3f4f6', '#bbf7d0', '#4ade80', '#22c55e', '#166534']"
            :max="maxCount"
            :tooltip="false"
            tooltip-unit="записей"
          />
        </div>
      </div>
      <Transition
        enter-active-class="transition duration-300"
        enter-from-class="opacity-0"
        enter-to-class="opacity-100"
        leave-active-class="transition duration-300"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0"
      >
        <heatmap-modal
          v-if="isModalOpen"
          :is-open="isModalOpen"
          :values="heatmapData"
          :round="2"
          :end-date="endDate"
          :range-color="['#f3f4f6', '#bbf7d0', '#4ade80', '#22c55e', '#166534']"
          :max="maxCount"
          :tooltip="true"
          tooltip-unit="записей"
          @close="closeModal"
        />
      </Transition>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import HeatmapModal from './HeatmapModal.vue';
import { useFetch } from '../composables/utils.js';

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
const error = ref(null)
const sessionData = ref([])
const isModalOpen = ref(false)

// Process data for heatmap
const heatmapData = computed(() => {
  const dateCounts = new Map()

  // Count entries per day
  sessionData.value.forEach((entry) => {
    const date = new Date(entry.datetime).toISOString().split('T')[0]
    dateCounts.set(date, (dateCounts.get(date) || 0) + 1)
  })

  // Convert to heatmap format
  return Array.from(dateCounts.entries()).map(([date, count]) => ({
    date,
    count
  }))
})

// Calculate max count for proper scaling
const maxCount = computed(() => {
  if (heatmapData.value.length === 0) return 1
  return Math.max(...heatmapData.value.map(item => item.count), 5)
})

const endDate = computed(() => {
  if (sessionData.value.length === 0) return null

  const dates = sessionData.value.map(entry => new Date(entry.datetime))
  const latestDate = new Date(Math.max(...dates))
  latestDate.setDate(latestDate.getDate() + 1) // Add one day to include the last day
  return latestDate.toISOString().split('T')[0]
})

const openModal = () => {
  isModalOpen.value = true
}

const closeModal = () => {
  isModalOpen.value = false
}

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
      sessionData.value = []
      return
    }
    
    if (fetchData.value) {
      sessionData.value = fetchData.value
    } else {
      sessionData.value = []
    }
  } catch (error) {
    console.error('Error in fetchData:', error)
    error.value = 'Произошла ошибка при загрузке данных'
    sessionData.value = []
  }
}

onMounted(fetchData)
</script>

<style scoped>
</style>