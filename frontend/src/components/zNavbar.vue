<template>
  <nav class="fixed top-0 left-0 w-full z-50">
    <div class="flex justify-end px-6 py-4 sm:px-8 sm:py-6">
      <button @click="toggleMenu" class="p-1.5 sm:p-2 bg-white rounded-lg flex items-center border border-gray-300 justify-center transition-all duration-300 hover:border-gray-100 hover:bg-gray-100 focus:outline-none">
        <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
        </svg>
      </button>
    </div>

    <div 
      class="absolute top-16 right-6 sm:right-8 w-48 sm:w-56 bg-white bg-opacity-90 backdrop-blur-sm rounded-lg shadow-lg overflow-hidden transition-all duration-300 ease-in-out"
      :style="{ maxHeight: isOpen ? menuHeight : '0px' }"
    >
      <div class="py-2" ref="menuContent">
        <a 
          v-for="section in sections" 
          :key="section.id"
          @click="scrollToSection(section.id)"
          class="cursor-pointer text-black hover:bg-gray-100 block px-4 py-2 text-sm sm:text-base transition-colors duration-200"
        >
          {{ section.name }}
        </a>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, computed, onMounted, defineProps, nextTick } from 'vue';

const props = defineProps({
  sections: {
    type: Array,
    required: true
  }
});

const isOpen = ref(false);
const menuContent = ref(null);
const menuHeight = ref('0px');

const toggleMenu = () => {
  isOpen.value = !isOpen.value;
  if (isOpen.value) {
    nextTick(() => {
      menuHeight.value = `${menuContent.value.scrollHeight}px`;
    });
  } else {
    menuHeight.value = '0px';
  }
};

const scrollToSection = (sectionId) => {
  const element = document.getElementById(sectionId);
  if (element) {
    const navbarHeight = 16; // Reduced padding
    const elementPosition = element.getBoundingClientRect().top;
    const offsetPosition = elementPosition + window.scrollY - navbarHeight;

    window.scrollTo({
      top: offsetPosition,
      behavior: "smooth"
    });
  }
  isOpen.value = false;
  menuHeight.value = '0px';
};

onMounted(() => {
  window.addEventListener('resize', () => {
    if (isOpen.value) {
      menuHeight.value = `${menuContent.value.scrollHeight}px`;
    }
  });
});
</script>
