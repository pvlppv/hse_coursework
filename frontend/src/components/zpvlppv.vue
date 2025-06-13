<template>
  <div class="p-6 sm:p-8 lg:p-12">
    <Navbar :sections="sections" />
    
    <div id="bio">
      <Bio />
    </div>

    <hr class="my-5 border-gray-300">

    <div id="activity-status">
      <ActivityStatus :lastActivityName="lastActivityName" class="my-5"/>
    </div>

    <div id="calendar">
      <Calendar @updateLastActivity="updateLastActivity" class="my-5"/>
    </div>

    <div id="projects">
      <Projects class="mt-5"/>
    </div>

    <div id="activity-heatmap">
      <ActivityHeatmap class="my-5"/>
    </div>

    <hr class="my-5 border-gray-300">

    <div id="society">
      <Contacts class="my-5"/>
    </div>

    <hr class="my-5 border-gray-300">

    <div id="health-status">
      <HealthStatus class="mt-5"/>
    </div>

    <div id="health-heatmap">
      <HealthHeatmap class="my-5"/>
    </div>

    <hr class="my-5 border-gray-300">

    <div id="blog">
      <Blog />
    </div>

    <hr class="my-5 border-gray-300">

    <div id="database">
      <Database />
    </div>

    <p class="text-xs sm:text-sm text-gray-600 text-center mt-5">
      Потихоньку добавляется...<br />
      Если есть идеи, что добавить – <a href="https://t.me/pvlppv" class="text-blue-600 hover:text-blue-800">пишите</a> :)
    </p>
  </div>
</template>  

<script setup>
import Navbar from './Navbar.vue';
import Bio from './Bio.vue';
import Blog from './Blog.vue';
import Calendar from './Calendar.vue';
import Projects from './Projects.vue';
import ActivityHeatmap from './ActivityHeatmap.vue';
import HealthHeatmap from './HealthHeatmap.vue';
import ActivityStatus from './ActivityStatus.vue';
import HealthStatus from './HealthStatus.vue';
import Database from './Database.vue';
import Contacts from './Contacts.vue';

import { ref } from 'vue';

const lastActivityName = ref(null);  // Store last activity's name

const updateLastActivity = (activityName) => {
  lastActivityName.value = activityName;
};

const sections = [
  { id: 'activity-status', name: 'Деятельность' },
  { id: 'society', name: 'Социум' },
  { id: 'health-status', name: 'Здоровье' },
  { id: 'blog', name: 'Блог' },
  { id: 'database', name: 'База данных' },
];
</script>

<style scoped>
</style>