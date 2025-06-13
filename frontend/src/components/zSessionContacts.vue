<template>
  <div class="w-full">
    <div v-if="error" class="p-2 text-xs text-center text-red-800 border border-red-300 rounded-lg bg-red-50" role="alert">
      <p>Ошибка загрузки данных</p>
    </div>

    <div v-else class="px-4 py-3 border border-gray-300 rounded-lg">
      <div v-if="!contacts.length" class="text-center text-xs text-gray-500">
        Нет контактов
      </div>
      <div v-else class="max-h-32 overflow-y-auto space-y-2">
        <div v-for="contact in validContacts" :key="contact.id" 
          class="flex justify-between items-center">
          <span class="text-xs font-semibold">{{ contact.name || 'Без имени' }}</span>
          <div class="flex space-x-0.5">
            <div
              v-for="n in 5"
              :key="n"
              class="w-4 h-4 flex items-center justify-center rounded text-white font-bold"
              :class="getColor(n, contact.score || 0)"
            >
              <span class="text-2xs">{{ n }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useFetch } from '../composables/utils.js';

const props = defineProps({
  sessionId: {
    type: String,
    required: true
  }
});

const apiBaseUrl = import.meta.env.VITE_APP_API_BASE_URL;
const contacts = ref([]);
const error = ref(null);

const validContacts = computed(() => {
  return contacts.value.filter(contact => contact && contact.id);
});

const { data, error: fetchError, fetchData } = useFetch(`${apiBaseUrl}/api/contact_score/${props.sessionId}`);

onMounted(async () => {
  await fetchData();
  if (data.value) {
    contacts.value = data.value;
  }
  if (fetchError.value) {
    error.value = fetchError.value;
  }
});

const getColor = (n, score) => {
  if (n <= score) {
    if (n === 5) return 'bg-[#15803d]';
    if (n === 4) return 'bg-[#22c55e]';
    if (n === 3) return 'bg-[#4ade80]';
    if (n === 2) return 'bg-[#86efac]';
    return 'bg-[#bbf7d0]';
  }
  return 'bg-gray-200 text-gray-400';
};
</script> 