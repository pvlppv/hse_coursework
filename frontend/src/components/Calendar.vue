<template>
    <div class="container mx-auto flex justify-center">
        <div class="max-w-lg w-full space-y-5">

            <div v-if="error"class="p-4 text-xs sm:text-sm text-center text-red-800 border border-red-300 rounded-lg bg-red-50" role="alert">
                <p>На сервере что-то сломалось, данные не достались из базы данных :(</p>
                <p><a href="https://t.me/pvlppv" class="text-blue-600 hover:text-blue-800">Напишите мне</a>, я починю.</p>
            </div>
    
            <div v-else class="qalendar-wrapper is-light-mode">
                <Qalendar v-if="!error && events.length" :selected-date="new Date()" :events="events" :config="config"/>
            </div>
            
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, watch, computed, nextTick } from 'vue';
import { useFetch } from '../composables/utils.js';
import { Qalendar } from 'qalendar';
import 'qalendar/dist/style.css';
  
const apiBaseUrl = import.meta.env.VITE_APP_API_BASE_URL;
const events = ref([]);
const error = ref(null);
const lastActivity = ref(null);  // Store the last activity
const emit = defineEmits(['updateLastActivity']);  // Define emit for last activity

const { data: activities, error: fetchError, fetchData } = useFetch(`${apiBaseUrl}/api/activity/`);

// Process activities into the Qalendar-compatible format
const processEvents = (data) => {
    const sortedActivities = data.sort((a, b) => new Date(a.date) - new Date(b.date));
    lastActivity.value = sortedActivities[sortedActivities.length - 1];

    return sortedActivities.map((activity, index) => {
        // Parse the date string and format it, preserving the timezone
        const startDate = new Date(activity.date);
        const start = `${startDate.getFullYear()}-${String(startDate.getMonth() + 1).padStart(2, '0')}-${String(startDate.getDate()).padStart(2, '0')} ${String(startDate.getHours()).padStart(2, '0')}:${String(startDate.getMinutes()).padStart(2, '0')}`;

        let end;
        if (index === sortedActivities.length - 1 || 
            new Date(sortedActivities[index + 1].date).toDateString() !== startDate.toDateString()) {
            // Last activity of the day, stretch to 23:59
            end = `${start.split(' ')[0]} 23:59`;
        } else {
            // Set end time to the start time of the next activity
            const nextStartDate = new Date(sortedActivities[index + 1].date);
            end = `${nextStartDate.getFullYear()}-${String(nextStartDate.getMonth() + 1).padStart(2, '0')}-${String(nextStartDate.getDate()).padStart(2, '0')} ${String(nextStartDate.getHours()).padStart(2, '0')}:${String(nextStartDate.getMinutes()).padStart(2, '0')}`;
        }

        return {
            title: activity.name,
            time: { start, end },
            id: activity.id,
            isEditable: false,
        };
    });
};

// Calendar configuration (basic setup)
const config = computed(() => ({
    week: {
        // Takes the value 'sunday' or 'monday'
        // However, if startsOn is set to 'sunday' and nDays to 5, the week displayed will be Monday - Friday
        startsOn: 'monday',
        // Takes the values 5 or 7.
        nDays: 7,
        // Scroll to a certain hour on mounting a week. Takes any value from 0 to 23.
        // This option is not compatible with the 'dayBoundaries'-option, and will simply be ignored if custom day boundaries are set.
        scrollToHour: lastActivity.value ? new Date(lastActivity.value.date).getHours() : new Date().getHours(),
    },
    month: {
        // Hide leading and trailing dates in the month view (defaults to true when not set)
        showTrailingAndLeadingDates: false,
    },
    // Takes any valid locale that the browser understands. However, not all locales have been thorougly tested in Qalendar
    // If no locale is set, the preferred browser locale will be used
    locale: 'ru-RU',
    style: {
        // When adding a custom font, please also set the fallback(s) yourself
        fontFamily: "'Montserrat', sans-serif",
    },
    // if not set, the mode defaults to 'week'. The three available options are 'month', 'week' and 'day'
    // Please note, that only day and month modes are available for the calendar in mobile-sized wrappers (~700px wide or less, depending on your root font-size)
    defaultMode: 'day',
    // The silent flag can be added, to disable the development warnings. This will also bring a slight performance boost
    isSilent: true,
    showCurrentTime: true, // Display a line indicating the current time 
    disableModes: ['month'], // Disable the month mode
    eventDialog: {
        isDisabled: true, // Disable the event dialog
    },
    dayIntervals: {
        length: 30, // Length in minutes of each interval. Accepts values 15, 30 and 60 (the latter is the default)
        height: 30, // The height of each interval
    },
}));

onMounted(() => {
    fetchData();
    setupEndTimeObserver();
});
  
// Watch for changes in fetched data and errors
watch([activities, fetchError], () => {
    if (fetchError.value) {
        error.value = fetchError.value;
    } else if (activities.value) {
        events.value = processEvents(activities.value);
        
        if (lastActivity.value && lastActivity.value.name) {
            emit('updateLastActivity', lastActivity.value.name);
        }

        nextTick(() => {
            replaceEndTime();
        });
    }
});

function setupEndTimeObserver() {
    const targetNode = document.querySelector('.qalendar-wrapper');
    if (!targetNode) return;

    const config = { childList: true, subtree: true };

    const callback = function(mutationsList, observer) {
        for(let mutation of mutationsList) {
            if (mutation.type === 'childList') {
                replaceEndTime();
            }
        }
    };

    const observer = new MutationObserver(callback);
    observer.observe(targetNode, config);
}

function replaceEndTime() {
    const timeElements = document.querySelectorAll('.calendar-week__event-row.is-time span, .calendar-day__event-row.is-time span');
    timeElements.forEach(el => {
        if (el.textContent.endsWith('23:59')) {
            el.textContent = el.textContent.replace('23:59', '...');
        }
    });
}
</script>
  
<style scoped>
.qalendar-wrapper {
    height: 500px;
}
</style>
