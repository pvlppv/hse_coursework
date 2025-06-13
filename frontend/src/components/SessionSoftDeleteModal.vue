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
        class="fixed inset-0 bg-black bg-opacity-50 z-[9998]"
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
        class="fixed inset-0 flex items-center justify-center p-2 sm:p-4 z-[9999]"
      >
        <div 
          @click.stop
          class="bg-white rounded-lg p-4 sm:p-6 w-full max-w-sm sm:max-w-lg max-h-[80vh] flex flex-col overflow-hidden"
        >
          <p class="text-center text-sm sm:text-base text-gray-600 mb-6 flex-shrink-0">
            Этот сеанс будет скрыт и перенесён ниже в неактивные сеансы. Вы сможете восстановить его в любой момент.
          </p>
          <div class="flex justify-center gap-3 mt-auto">
            <button
              @click="$emit('close')"
              class="px-3 sm:px-4 py-1.5 sm:py-2 text-xs sm:text-sm rounded-lg border border-gray-300 hover:bg-gray-50"
            >
              Отменить
            </button>
            <button
              @click="$emit('confirm')"
              class="px-3 sm:px-4 py-1.5 sm:py-2 text-xs sm:text-sm rounded-lg border border-red-200 bg-red-200 text-gray-600 hover:bg-red-300"
            >
              Скрыть
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
defineProps({
  show: {
    type: Boolean,
    required: true
  }
});

defineEmits(['close', 'confirm']);
</script>
