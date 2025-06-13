<template>
  <Teleport to="body">
    <Transition
      enter-active-class="transition duration-300"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition duration-300"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div
        v-if="show"
        class="fixed inset-0 bg-black bg-opacity-50 z-[99998]"
      />
    </Transition>
    <Transition
      enter-active-class="transition duration-300 ease-out"
      enter-from-class="opacity-0 scale-95"
      enter-to-class="opacity-100 scale-100"
      leave-active-class="transition duration-200 ease-in"
      leave-from-class="opacity-100 scale-100"
      leave-to-class="opacity-0 scale-95"
    >
      <div 
        v-if="show" 
        @click="$emit('close')"
        @wheel.prevent
        @scroll.prevent
        @touchmove.prevent
        class="fixed inset-0 flex items-center justify-center p-2 sm:p-4 z-[99999]"
      >
        <div 
          @click.stop
          class="bg-white rounded-lg p-4 sm:p-6 w-full max-w-[80%] sm:max-w-md max-h-[80vh] flex flex-col overflow-hidden"
        >            
          <!-- Scrollable content area -->
          <div
            @wheel.stop
            @scroll.stop
            @touchmove.stop
            class="flex-1 overflow-y-auto"
          >
            <img 
              :src="visualization?.image" 
              :alt="visualization?.title"
              class="w-full h-48 sm:h-64 object-cover rounded-lg mb-3"
            />
            <h3 class="text-sm sm:text-base font-semibold mb-1.5">{{ visualization?.title }}</h3>
            <p class="text-xs sm:text-sm text-gray-600 mb-4">{{ visualization?.description }}</p>
          </div>

          <!-- Sticky footer for buttons -->
          <div class="mt-5 flex-shrink-0">
            <div class="flex justify-center gap-3">
              <button
                @click="$emit('close')"
                class="px-3 sm:px-4 py-1.5 sm:py-2 text-xs sm:text-sm rounded-lg border border-gray-300 hover:bg-gray-50"
              >
                Отменить
              </button>
              <button
                @click="handleConfirm"
                class="px-3 sm:px-4 py-1.5 sm:py-2 text-xs sm:text-sm rounded-lg border border-gray-600 bg-gray-600 text-white hover:bg-gray-700"
              >
                Выбрать
              </button>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { onMounted, onUnmounted } from 'vue';

defineProps({
  show: {
    type: Boolean,
    required: true,
  },
  visualization: {
    type: Object,
    default: null
  }
});

const emit = defineEmits(['close', 'confirm']);

const handleConfirm = () => {
  // Dispatch custom event when visualization is selected
  window.dispatchEvent(new CustomEvent('visualization-selected'));
  emit('confirm');
};

onMounted(() => {
  // Add global event listener
  window.addEventListener('visualization-selected', () => {
    // This will be handled by the onboarding component
  });
});

onUnmounted(() => {
  // Clean up event listener
  window.removeEventListener('visualization-selected', () => {});
});
</script>
