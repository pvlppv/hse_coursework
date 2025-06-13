<template>
  <div v-if="loading" class="p-4 text-xs sm:text-xs text-center text-gray-500 border border-gray-300 rounded-lg bg-gray-50">
      Загрузка данных...
  </div>
  <div v-else-if="error" class="p-4 text-xs sm:text-xs text-center text-red-800 border border-red-300 rounded-lg bg-red-50" role="alert">
    <p>Не удалось загрузить данные для диаграммы потоков</p>
  </div>
  <div v-else-if="!sessionData || sessionData.length < 2" class="p-4 text-xs sm:text-sm text-center text-gray-600 border border-gray-300 rounded-lg bg-gray-50">
      Добавь минимум 2 записи, чтобы увидеть визуализацию
  </div>
  <div v-else class="p-4 border border-gray-200 rounded-lg">
    <v-chart class="chart" :option="option" autoresize />
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import { use } from 'echarts/core';
import { CanvasRenderer } from 'echarts/renderers';
import { SankeyChart } from 'echarts/charts';
import {
  TitleComponent,
  TooltipComponent,
} from 'echarts/components';
import VChart from 'vue-echarts';
import { useFetch } from '../composables/utils.js';

use([
  CanvasRenderer,
  SankeyChart,
  TitleComponent,
  TooltipComponent,
]);

const props = defineProps({
  session: {
    type: Object,
    required: true
  }
});

const apiBaseUrl = import.meta.env.VITE_APP_API_BASE_URL;
const error = ref(null);
const sessionData = ref([]);
const nodes = ref([]);
const links = ref([]);
const loading = ref(true);

const fetchData = async () => {
  if (!props.session?.id) {
    loading.value = false;
    return;
  }
  try {
    loading.value = true;
    error.value = null;
    const tableName = `session_${props.session.id}_data`;
    const { data: fetchedData, error: fetchError, fetchData: fetch } = useFetch(
      `${apiBaseUrl}/api/users/table/${tableName}/rows/`,
      { credentials: 'include' }
    );
    await fetch();

    if (fetchError.value) {
      console.error('Error fetching data for sankey:', fetchError.value);
      error.value = 'Не удалось загрузить данные';
      return;
    }
    sessionData.value = (fetchedData.value || []).reverse();
    processSankeyData();
  } catch (e) {
    console.error('Error in fetchData for sankey:', e);
    error.value = 'Произошла ошибка при загрузке данных';
  } finally {
    loading.value = false;
  }
};

const processSankeyData = () => {
  if (sessionData.value.length < 2) {
    nodes.value = [];
    links.value = [];
    return;
  }

  // 1. Aggregate link counts
  const linkCounts = new Map();
  for (let i = 0; i < sessionData.value.length - 1; i++) {
    const source = sessionData.value[i].value;
    const target = sessionData.value[i+1].value;
    const key = `${source} -> ${target}`;
    linkCounts.set(key, (linkCounts.get(key) || 0) + 1);
  }

  // 2. Build graph, breaking cycles as we go
  const finalNodes = new Map(); // 'A' -> { name: 'A', ... }
  const finalLinks = [];
  const adj = new Map(); // Adjacency list for cycle detection: 'A' -> ['B']
  
  // Helper for cycle detection (DFS)
  const hasPath = (source, target) => {
    const stack = [source];
    const visited = new Set();
    while (stack.length > 0) {
      const u = stack.pop();
      if (u === target) return true;
      if (visited.has(u)) continue;
      visited.add(u);
      const neighbors = adj.get(u) || [];
      for (const v of neighbors) {
        stack.push(v);
      }
    }
    return false;
  };

  const nameCounters = new Map();
  
  for (const [key, value] of linkCounts.entries()) {
    let [sourceName, targetName] = key.split(' -> ');

    // Ensure source node exists and is the latest version
    if (!finalNodes.has(sourceName)) {
      finalNodes.set(sourceName, { name: sourceName });
    }

    let targetNodeName = targetName;
    // If adding (source -> target) creates a path from target back to source, we have a cycle.
    if (hasPath(targetName, sourceName)) {
      // Break the cycle by creating a new version of the target node.
      const count = (nameCounters.get(targetName) || 0) + 1;
      nameCounters.set(targetName, count);
      targetNodeName = `${targetName} (${count})`;
    }
    
    if (!finalNodes.has(targetNodeName)) {
        finalNodes.set(targetNodeName, { name: targetNodeName, displayName: targetName });
    }

    // Add the link
    finalLinks.push({
      source: sourceName,
      target: targetNodeName,
      value: value
    });

    // Update adjacency list
    if (!adj.has(sourceName)) adj.set(sourceName, []);
    adj.get(sourceName).push(targetNodeName);
  }

  nodes.value = Array.from(finalNodes.values());
  links.value = finalLinks;
};

onMounted(fetchData);

watch(sessionData, processSankeyData, { deep: true });

const option = computed(() => ({
  color: [
    '#a7f3d0', '#bfdbfe', '#fecaca', '#fde68a', '#e9d5ff', '#c7d2fe', '#fbcfe8'
  ],
  tooltip: {
    trigger: 'item',
    triggerOn: 'mousemove',
    formatter: (params) => {
      if (params.dataType === 'node') {
        // Use displayName if it exists (for duplicated nodes), otherwise use name
        const { displayName, name } = params.data;
        return displayName || name;
      }
      if (params.dataType === 'edge') {
        // We can't easily get display names here, so just show the transition
        return `${params.data.source} → ${params.data.target}`;
      }
      return params.value;
    },
    textStyle: {
      color: '#4b5563',
      fontFamily: 'Montserrat',
      fontSize: 12,
      fontWeight: '400'
    }
  },
  series: [
    {
      type: 'sankey',
      data: nodes.value,
      links: links.value,
      emphasis: {
        focus: 'adjacency'
      },
      lineStyle: {
        color: 'gradient',
        curveness: 0.5
      },
      label: {
          color: '#4b5563',
          fontFamily: 'Montserrat',
          fontSize: 12,
          formatter: (params) => {
            return params.data.displayName || params.data.name;
          }
      },
      nodeWidth: 10,
      nodeGap: 8,
      left: '2%',
      right: '10%',
      top: '5%',
      bottom: '5%'  
    }
  ]
}));
</script>

<style scoped>
.chart {
  height: 400px;
  width: 100%;
}
</style> 