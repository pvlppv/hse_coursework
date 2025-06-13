<template>
  <div class="w-full">
    <div v-if="error" class="p-2 text-xs text-center text-red-800 border border-red-300 rounded-lg bg-red-50" role="alert">
      <p>Ошибка загрузки данных</p>
    </div>

    <div v-else class="px-4 py-3 border border-gray-300 rounded-lg">
      <div v-if="posts.length === 0" class="text-center text-xs text-gray-500">
        Нет записей
      </div>
      <div v-else class="max-h-32 overflow-y-auto space-y-2">
        <div v-for="post in posts" :key="post.id" class="text-left">
          <div class="flex justify-between items-center">
            <h3 class="text-xs font-semibold">{{ post.title }}</h3>
            <span class="text-2xs text-gray-600">
              #{{ post.id }} · {{ timeSince(post.date) }}
            </span>
          </div>
          <p class="text-2xs text-gray-600 mt-1">{{ post.text.split(' ').slice(0, 15).join(' ') + '...' }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useFetch, timeSince } from '../composables/utils.js';

const props = defineProps({
  sessionId: {
    type: String,
    required: true
  }
});

const apiBaseUrl = import.meta.env.VITE_APP_API_BASE_URL;
const posts = ref([]);
const error = ref(null);

const { data, error: fetchError, fetchData } = useFetch(`${apiBaseUrl}/api/posts/${props.sessionId}`);

onMounted(async () => {
  await fetchData();
  if (data.value) {
    posts.value = data.value;
  }
  if (fetchError.value) {
    error.value = fetchError.value;
  }
});
</script> 