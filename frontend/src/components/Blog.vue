<template>
  <div class="container mx-auto flex justify-center">
    <div class="max-w-sm sm:max-w-lg w-full space-y-5">

      <router-link to="/pvlppv/blog" class="block">
        <div class="text-base sm:text-lg font-semibold p-2 rounded-lg border border-gray-300 transition-all duration-300 hover:border-gray-100 hover:bg-gray-100 flex items-center justify-center">
          Блог
        </div>
      </router-link>

      <div v-if="error" class="p-4 text-xs sm:text-sm text-center text-red-800 border border-red-300 rounded-lg bg-red-50" role="alert">
        <p>На сервере что-то сломалось, данные не достались из базы данных :(</p>
        <p><a href="https://t.me/pvlppv" class="text-blue-600 hover:text-blue-800">Напишите мне</a>, я починю.</p>
      </div>

      <ul v-else class="space-y-5">
        <li v-for="post in renderedPosts" :key="post.id">
          <a :href="`/pvlppv/blog/${post.id}`" class="block text-left">
            <div class="flex justify-between items-center">
              <h2 class="text-xs sm:text-sm font-semibold">{{ post.title }}</h2>
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
</template>

<script setup>
import { computed, onMounted } from 'vue';
import { useFetch, timeSince } from '../composables/utils.js';

const apiBaseUrl = import.meta.env.VITE_APP_API_BASE_URL;
const { data: posts, error, fetchData } = useFetch(`${apiBaseUrl}/api/posts/?skip=0&limit=3`);

onMounted(() => {
  fetchData();
});

const renderedPosts = computed(() => {
  return posts.value ? posts.value : {};
});
</script>