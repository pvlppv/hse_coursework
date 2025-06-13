import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router';
import VueCalendarHeatmap from 'vue3-calendar-heatmap';
import 'vue3-calendar-heatmap/dist/style.css';
import VueTippy from 'vue-tippy'

const app = createApp(App);
app.use(router);
app.use(VueCalendarHeatmap);
app.use(
    VueTippy,
    // optional
    {
      directive: 'tippy', // => v-tippy
      component: 'tippy', // => <tippy/>
    }
  )
app.mount('#app');
