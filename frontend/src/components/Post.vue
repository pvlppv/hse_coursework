<template>
  <div class="prose prose-sm sm:prose-lg mx-auto p-6 relative space-y-5">
    <div v-if="error" class="p-4 text-xs sm:text-sm text-center text-red-800 border border-red-300 rounded-lg bg-red-50" role="alert">
      <p>На сервере что-то сломалось, данные не достались из базы данных :(</p>
      <p><a href="https://t.me/pvlppv" class="text-blue-600 hover:text-blue-800">Напишите мне</a>, я починю.</p>
    </div>
    <div v-else>
      <h2>{{ renderedPost.title }}</h2>
      <p class="text-gray-500">{{ formatDate(renderedPost.date) }}</p>
    </div>
    <a href="/pvlppv/blog" class="p-2 rounded-lg border border-gray-300 transition-all duration-300 hover:border-gray-100 hover:bg-gray-100 flex items-center justify-center">
      <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3">
        <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
      </svg>
    </a>
    <div v-html="formattedText"></div>
  </div>

  <div class="fixed bottom-5 sm:bottom-10 left-0 right-0 mx-auto w-full max-w-xs sm:max-w-xl md:max-w-2xl lg:max-w-3xl">
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
import { onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useFetch, formatDate, useScrollToTop } from '../composables/utils.js'

const apiBaseUrl = import.meta.env.VITE_APP_API_BASE_URL;
const route = useRoute()
const { data: post, error, fetchData } = useFetch(`${apiBaseUrl}/api/posts/` + route.params.id);

onMounted(() => {
  fetchData();
});

const renderedPost = computed(() => {
  return post.value ? post.value : {};
});

const formattedText = computed(() => {
  return renderedPost.value.text ? renderedPost.value.text.replace(/\n/g, '<br>') : '';
});

// Scroll to the top
const { showScrollToTop, scrollToTop } = useScrollToTop();
</script>

<style scoped>
.prose h2 {
  margin-bottom: 0;
}
.prose p {
  margin-top: 0;
}
</style>
