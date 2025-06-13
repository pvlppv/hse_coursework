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
        class="fixed inset-0 flex items-center justify-center p-4 z-[99999]"
      >
        <div 
          @click.stop
          class="bg-white rounded-lg p-4 sm:p-6 w-full max-w-[80%] sm:max-w-md max-h-[80vh] flex flex-col overflow-hidden"
        >
          <h3 class="text-sm sm:text-base font-medium mb-4">Продолжительность сеанса</h3>
          
          <div class="flex flex-col gap-4 mb-6">
            <div class="space-y-1">
              <input
                v-model="customDays"
                type="number"
                min="1"
                class="w-full p-2 text-xs sm:text-sm border rounded"
                placeholder="Дней"
              >
              <label class="text-xs text-gray-500">дней</label>
            </div>
            <div class="space-y-1">
              <input
                v-model="customWeeks"
                type="number"
                min="0"
                class="w-full p-2 text-xs sm:text-sm border rounded"
                placeholder="Недель"
              >
              <label class="text-xs text-gray-500">недель</label>
            </div>
            <div class="space-y-1">
              <input
                v-model="customMonths"
                type="number"
                min="0"
                class="w-full p-2 text-xs sm:text-sm border rounded"
                placeholder="Месяцев"
              >
              <label class="text-xs text-gray-500">месяцев</label>
            </div>
            <div class="space-y-1">
              <input
                v-model="customYears"
                type="number"
                min="0"
                class="w-full p-2 text-xs sm:text-sm border rounded"
                placeholder="Лет"
              >
              <label class="text-xs text-gray-500">лет</label>
            </div>
          </div>

          <div class="flex justify-center gap-3">
            <button
              @click="$emit('close')"
              class="px-4 py-2 text-xs sm:text-sm rounded-lg border hover:bg-gray-50"
            >
              Отменить
            </button>
            <button
              @click="applyDuration"
              class="px-4 py-2 text-xs sm:text-sm rounded-lg border border-gray-600 bg-gray-600 text-white hover:bg-gray-700 max-w-[200px]"
            >
              Применить
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref } from 'vue';

defineProps({
  show: {
    type: Boolean,
    required: true
  }
});

const emit = defineEmits(['close', 'apply']);

const customYears = ref(0);
const customMonths = ref(0);
const customWeeks = ref(0);
const customDays = ref(0);

const applyDuration = () => {
  // Ensure at least 1 day is selected
  if (!customDays.value && !customWeeks.value && !customMonths.value && !customYears.value) {
    customDays.value = 1;
  }

  emit('apply', {
    years: customYears.value,
    months: customMonths.value,
    weeks: customWeeks.value,
    days: customDays.value,
  });
  
  // Reset values
  customYears.value = 0;
  customMonths.value = 0;
  customWeeks.value = 0;
  customDays.value = 0;
  
  emit('close');
};
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
