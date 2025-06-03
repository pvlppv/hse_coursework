import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router';
import VueCalendarHeatmap from 'vue3-calendar-heatmap';
import 'vue3-calendar-heatmap/dist/style.css';

const app = createApp(App);
app.use(router);
app.use(VueCalendarHeatmap);
app.mount('#app');
