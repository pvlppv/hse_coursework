<template>
  <div class="w-full">
    <div v-if="error" class="p-4 text-xs sm:text-sm text-center text-red-800 border border-red-300 rounded-lg bg-red-50" role="alert">
      <p>На сервере что-то сломалось, данные не достались из базы данных :(</p>
      <p><a href="https://t.me/pvlppv" class="text-blue-600 hover:text-blue-800">Напишите мне</a>, я починю.</p>
    </div>

    <div v-else class="px-4 py-4 sm:px-6 sm:py-5 border border-gray-300 rounded-lg">
      <div class="space-y-4">
        <div class="relative w-full">
          <!-- Dropdown button -->
          <button 
            @click="toggleDropdown"
            class="w-full text-xs sm:text-sm text-gray-600 py-1.5 px-3 border border-gray-300 rounded-md bg-white flex justify-between items-center"
          >
            {{ timeRanges[selectedRange] }}
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" style="fill: rgba(0, 0, 0, 1);">
              <path d="M16.293 9.293 12 13.586 7.707 9.293l-1.414 1.414L12 16.414l5.707-5.707z"></path>
            </svg>
          </button>

          <!-- Dropdown options -->
          <ul v-if="dropdownOpen" class="absolute w-full bg-white border border-gray-300 rounded-md shadow-md z-10 mt-1">
            <li 
              v-for="(label, value) in timeRanges" 
              :key="value" 
              @click="selectRange(value)"
              class="px-3 py-1.5 text-xs sm:text-sm text-gray-600 hover:bg-gray-100 cursor-pointer"
            >
              {{ label }}
            </li>
          </ul>
        </div>

        <div v-if="contacts.length === 0" class="text-center text-xs sm:text-sm text-gray-500">
          {{ `${timeRanges[selectedRange]} нет записей` }}
        </div>
        <div v-else class="max-h-60 overflow-y-auto space-y-2.5">
          <div v-for="contact in contacts" :key="contact.id" 
            class="flex justify-between items-center">
            <span class="text-xs sm:text-sm font-semibold">{{ contact.name }}</span>
            <div class="flex space-x-0.5 sm:space-x-1">
              <div
                v-for="n in 5"
                :key="n"
                class="w-4 h-4 sm:w-5 sm:h-5 flex items-center justify-center rounded text-white font-bold"
                :class="getColor(n, contact.score)"
              >
                <span class="text-2xs sm:text-xs">{{ n }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
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
});

const apiBaseUrl = import.meta.env.VITE_APP_API_BASE_URL;
const error = ref(null);
const sessionData = ref([]);
const dropdownOpen = ref(false);

// State for selected time range
const selectedRange = ref('today');

// Time range options
const timeRanges = {
  today: 'За сегодня',
  week: 'За неделю',
  month: 'За месяц',
  year: 'За год',
  all: 'За всё время',
};

// Process data for contacts
const contacts = computed(() => {
  const now = new Date();
  const filteredData = sessionData.value.filter(entry => {
    const entryDate = new Date(entry.datetime);
    switch (selectedRange.value) {
      case 'today':
        return entryDate.toDateString() === now.toDateString();
      case 'week':
        const weekAgo = new Date(now.setDate(now.getDate() - 7));
        return entryDate >= weekAgo;
      case 'month':
        const monthAgo = new Date(now.setMonth(now.getMonth() - 1));
        return entryDate >= monthAgo;
      case 'year':
        const yearAgo = new Date(now.setFullYear(now.getFullYear() - 1));
        return entryDate >= yearAgo;
      default: // 'all'
        return true;
    }
  });

  // Group by contact name and calculate score
  const contactMap = new Map();
  filteredData.forEach(entry => {
    const name = entry.value;
    if (!contactMap.has(name)) {
      contactMap.set(name, { name, count: 0 });
    }
    contactMap.get(name).count++;
  });

  // Convert to array and calculate scores
  return Array.from(contactMap.values())
    .map(contact => ({
      id: contact.name, // Using name as ID since we don't have contact IDs
      name: contact.name,
      score: Math.min(Math.ceil(contact.count / 2), 5), // Score 1-5 based on frequency
      count: contact.count // Keep the count for sorting
    }))
    .sort((a, b) => b.count - a.count) // Sort by count in descending order
    .map(({ id, name, score }) => ({ id, name, score })); // Remove count from final output
});

// Function to calculate badge color
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

const toggleDropdown = () => {
  dropdownOpen.value = !dropdownOpen.value;
};

const selectRange = (value) => {
  selectedRange.value = value;
  dropdownOpen.value = false;
};

const fetchData = async () => {
  try {
    error.value = null;
    
    const tableName = `session_${props.sessionId}_data`;
    const { data: fetchData, error: fetchError, fetchData: fetch } = useFetch(
      `${apiBaseUrl}/api/users/table/${tableName}/rows/`,
      { credentials: 'include' }
    );
    
    await fetch();
    
    if (fetchError.value) {
      console.error('Error fetching data:', fetchError.value);
      error.value = 'Не удалось загрузить данные';
      sessionData.value = [];
      return;
    }
    
    if (fetchData.value) {
      sessionData.value = fetchData.value;
    } else {
      sessionData.value = [];
    }
  } catch (error) {
    console.error('Error in fetchData:', error);
    error.value = 'Произошла ошибка при загрузке данных';
    sessionData.value = [];
  }
};

onMounted(fetchData);
</script>

<style scoped>
</style> 