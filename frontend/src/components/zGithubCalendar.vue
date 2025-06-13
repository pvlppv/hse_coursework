<template>
    <div>
      <!-- Prepare a container for your calendar -->
      <div class="calendar">
        Loading the data just for you...
      </div>
    </div>
</template>

<script setup>
import { onMounted } from 'vue';

onMounted(() => {
const script = document.createElement('script');
script.src = 'https://unpkg.com/github-calendar@latest/dist/github-calendar.min.js';
document.body.appendChild(script);

script.onload = () => {
    GitHubCalendar('.calendar', 'pvlppv', { responsive: true });
};
});
</script>

<style>
@import url('https://unpkg.com/github-calendar@latest/dist/github-calendar-responsive.css');
</style>
  