<template>
  <div id="profile" class="p-6 sm:p-8 lg:p-12">
    <!-- <div class="max-w-sm sm:max-w-lg w-full mx-auto"> -->
      <Header 
        :email="data.email"
        :show-add-modal="showAddModal"
        :active-sessions="activeSessions"
      />
      <hr class="my-5 border-gray-300">
      <SessionsList 
        :user-id="data.id"
        @update:show-add-modal="showAddModal = $event"
        @update:active-sessions="activeSessions = $event"
      />
    <!-- </div> -->
  </div>
</template>

<script setup>
// Components
import Header from './Header.vue';
import SessionsList from './SessionsList.vue';

// Composables
import { computed, ref, watch } from 'vue';
import { useFetch } from '../composables/utils.js';
import { useRouter } from 'vue-router';

const apiBaseUrl = import.meta.env.VITE_APP_API_BASE_URL;
const router = useRouter();

// Session state
const showAddModal = ref(false);
const activeSessions = ref([]);

// State
const { data: userData, fetchData: userFetchData } = useFetch(`${apiBaseUrl}/api/users/me`);

// Fetch user data
const fetchUserData = async () => {
  await userFetchData();
  if (!userData.value) router.push('/');
};

// Watch for user data changes
watch(userData, (newData) => {
  if (!newData) {
    router.push('/');
  }
});

fetchUserData();

const data = computed(() => userData.value || {});
</script>

<style scoped>
</style>