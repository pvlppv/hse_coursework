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
        v-if="isOpen"
        @click="onClose"
        @wheel.prevent
        @scroll.prevent
        @touchmove.prevent
        class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-2 sm:p-4 z-[10001]"
      >
        <div 
          @click.stop
          class="bg-white rounded-lg p-4 sm:p-6 w-full max-w-[80%] sm:max-w-md max-h-[80vh] flex flex-col overflow-hidden"
        >
          <h3 v-if="title" class="text-sm sm:text-base font-semibold mb-4">{{ title }}</h3>
          <div v-if="text" class="text-xs sm:text-sm space-y-4">
            {{ text }}
          </div>
          <slot></slot>
          <div v-if="!$slots.default" class="mt-5 flex-shrink-0">
            <button
              @click="onClose"
              class="w-full px-3 sm:px-4 py-1.5 sm:py-2 text-xs sm:text-sm rounded-lg border border-gray-300 hover:bg-gray-50"
            >
              {{ buttonText }}
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  title: {
    type: String,
    default: ''
  },
  text: {
    type: String,
    default: ''
  },
  buttonText: {
    type: String,
    default: 'Понятно'
  }
})

const emit = defineEmits(['close'])
const isOpen = ref(false)

const onClose = () => {
  isOpen.value = false
  emit('close')
}

defineExpose({
  show: () => isOpen.value = true,
  hide: () => isOpen.value = false
})
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style> 