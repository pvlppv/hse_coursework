<template>
  <div class="w-full">
    <Blog 
      v-if="data"
      :data="data"
      :loading="loading"
      :error="error"
    />
    <div v-else-if="loading" class="w-full h-32 flex items-center justify-center">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
    </div>
    <div v-else-if="error" class="w-full h-32 flex items-center justify-center text-red-600 text-sm">
      {{ error }}
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useFetch } from '../composables/utils.js'
import Blog from './Blog.vue'

const props = defineProps({
  sessionId: {
    type: [String, Number],
    required: true
  }
})

const apiBaseUrl = import.meta.env.VITE_APP_API_BASE_URL
const data = ref(null)
const loading = ref(true)
const error = ref(null)

const fetchData = async () => {
  try {
    loading.value = true
    error.value = null
    
    const tableName = `session_${props.sessionId}_data`
    const { data: fetchData, error: fetchError, fetchData: fetch } = useFetch(
      `${apiBaseUrl}/api/users/table/${tableName}/rows/`,
      { credentials: 'include' }
    )
    
    await fetch()
    
    if (fetchError.value) {
      if (fetchError.value.includes('Failed to get table content')) {
        data.value = []
        return
      }
      throw new Error(fetchError.value)
    }
    
    data.value = (fetchData.value || []).map(item => ({
      id: item.id,
      date: item.date || new Date().toISOString().split('T')[0],
      value: item.value || '',
      time: item.time || '00:00'
    }))
  } catch (err) {
    console.error('Error fetching blog data:', err)
    error.value = err.message || 'Failed to load blog data'
  } finally {
    loading.value = false
  }
}

onMounted(fetchData)
</script> 