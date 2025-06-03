<!-- LandingPage.vue -->
<template>
    <div class="min-h-screen w-full overflow-hidden">
      <!-- Loading State with Transition -->
      <transition name="fade">
        <div v-if="isLoading" class="flex items-center justify-center h-screen">
          <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-white"></div>
        </div>
      </transition>
  
      <!-- Dynamic Content with Transition -->
      <transition name="fade">
        <template v-if="!isLoading">
          <Hero v-if="!isAuthenticated" />
          <Profile v-else />
        </template>
      </transition>
    </div>
  </template>
    
  <script setup>
  import { ref, onMounted } from 'vue'
  import { useFetch } from '../composables/utils.js'
  import Hero from './Hero.vue'
  import Profile from './Profile.vue'
  
  const apiBaseUrl = import.meta.env.VITE_APP_API_BASE_URL
  const isAuthenticated = ref(false)
  const isLoading = ref(true) // Add a loading state
  
  // Auth check logic
  const checkAuth = async () => {
    try {
      const { fetchData } = useFetch(`${apiBaseUrl}/api/users/me`, {
        credentials: 'include'
      })
      await fetchData()
      isAuthenticated.value = true
    } catch (error) {
      isAuthenticated.value = false
    } finally {
      isLoading.value = false // Ensure loading state is always turned off
    }
  }
  
  onMounted(async () => {
    await checkAuth()
  })
  </script>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>