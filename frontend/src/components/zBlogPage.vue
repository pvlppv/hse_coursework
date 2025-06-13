<template>
  <div class="container mx-auto flex justify-center">
    <div class="max-w-lg w-full space-y-5">
      <h1 class="text-lg sm:text-xl font-semibold text-center">Блог</h1>
      <a href="/pvlppv" class="p-2 rounded-lg border border-gray-300 transition-all duration-300 hover:border-gray-100 hover:bg-gray-100 flex items-center justify-center">
        <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3">
          <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
        </svg>
      </a>

      <!-- Loading message -->
      <div v-if="loading" class="text-center text-gray-600">
        Загрузка...
      </div>

      <!-- Error message -->
      <div v-if="error && !loading" class="p-4 text-xs sm:text-sm text-center text-red-800 border border-red-300 rounded-lg bg-red-50" role="alert">
        <p>На сервере что-то сломалось, данные не достались из базы данных :(</p>
        <p><a href="https://t.me/pvlppv" class="text-blue-600 hover:text-blue-800">Напишите мне</a>, я починю.</p>
      </div>

      <!-- Post list -->
      <ul v-else-if="!loading && !error" class="space-y-5">
        <li v-for="post in renderedPosts" :key="post.id">
          <a :href="`/pvlppv/blog/${post.id}`" class="block text-left">
            <div class="flex justify-between items-center">
              <h3 class="text-sm sm:text-base font-semibold">{{ post.title }}</h3>
              <span class="text-xs sm:text-sm text-gray-600">
                #{{ post.id }} · {{ timeSince(post.date) }}
              </span>
            </div>
            <p class="text-xs sm:text-sm text-gray-600 mt-1">{{ post.text.split(' ').slice(0, 30).join(' ') + '...' }}</p>
          </a>
        </li>
      </ul>
    </div>
  </div>

  <div class="fixed bottom-5 left-0 right-0 mx-auto w-full max-w-lg px-4 sm:px-0">
    <button 
      v-show="showScrollToTop" 
      @click="scrollToTop" 
      class="p-2 w-full rounded-lg bg-white border border-solid border-gray-300 transition-all duration-300 hover:border-gray-100 hover:bg-gray-100 flex items-center justify-center"
    >
      <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3">
        <path stroke-linecap="round" stroke-linejoin="round" d="M19 15l-7-7-7 7" />
      </svg>
    </button>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useFetch, timeSince, useScrollToTop } from '../composables/utils.js';

const posts = ref([]);
const error = ref(null);
const loading = ref(true);

const apiBaseUrl = import.meta.env.VITE_APP_API_BASE_URL;
const fetchPosts = async () => {
  const { data, error: fetchError, fetchData } = useFetch(`${apiBaseUrl}/api/posts/?skip=0&limit=99999999`);
  
  try {
    await fetchData();
    if (fetchError.value) {
      error.value = fetchError.value;
    } else {
      posts.value = data.value || [];
    }
  } catch (err) {
    console.error(err);
    error.value = 'Error fetching posts';
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchPosts();
});

const renderedPosts = computed(() => {
  return posts.value ? posts.value : [];
});

// Scroll to the top
const { showScrollToTop, scrollToTop } = useScrollToTop();
</script>
