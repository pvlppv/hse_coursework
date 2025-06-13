<template>
    <div @wheel.prevent @touchmove.prevent @scroll.prevent @click="close" v-if="isOpen" class="fixed inset-0 z-50 flex flex-col items-center justify-center bg-black bg-opacity-50 space-y-5 cursor-pointer">
        <div @click.stop class="bg-white rounded-lg w-full max-w-xs relative flex flex-col cursor-default">
            <p class="text-lg sm:text-xl font-semibold text-center m-5">{{ title }}</p>
            <div class="overflow-hidden justify-center items-center">
                <calendar-heatmap
                    vertical
                    :values="values"
                    :round="round"
                    :end-date="endDate"
                    :range-color="rangeColor"
                    :max="max"
                    :tooltip="tooltip"
                    :tooltip-unit="tooltipUnit"
                    class="w-full h-full max-h-[calc(100vh-14rem)] sm:max-h-[calc(100vh-14rem)] ml-3"
                />
            </div>
        </div>
        <div class="w-full max-w-xs">
            <button @click="close" class="p-3 w-full rounded-lg bg-white border border-gray-300 transition-all duration-300 hover:border-gray-100 hover:bg-gray-100 flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
                </svg>
            </button>
        </div>
    </div>
</template>

<script setup>
const emit = defineEmits(['close']);

const props = defineProps({
    isOpen: Boolean,
    title: String,
    values: Array,
    round: Number,
    endDate: String,
    rangeColor: Array,
    max: Number,
    tooltip: Boolean,
    tooltipUnit: String,
});

const close = () => {
    emit('close');
};
</script>

<style scoped>
</style>
