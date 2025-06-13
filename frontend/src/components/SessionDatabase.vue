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
        id="session-database-modal"
        @click="handleOverlayClick"
        @wheel.prevent
        @scroll.prevent
        @touchmove.prevent
        class="fixed inset-0 flex items-center justify-center p-2 sm:p-4 z-[9999]"
      >
        <div 
          @click.stop
          @wheel.stop
          @scroll.stop
          @touchmove.stop
          class="bg-white rounded-lg p-4 sm:p-6 w-full max-w-sm sm:max-w-lg max-h-[80vh] flex flex-col overflow-hidden"
        >
          <h3 class="text-sm sm:text-base font-semibold mb-4 text-center flex-shrink-0">База данных: {{ title }}</h3>
          <div class="flex-1 overflow-y-auto">
            <div class="container mx-auto flex justify-center relative">
              <div class="max-w-sm sm:max-w-lg w-full space-y-2">
                <div v-if="error" class="p-4 text-xs sm:text-sm text-center text-red-800 border border-red-300 rounded-lg bg-red-50" role="alert">
                  <p>На сервере что-то сломалось, данные не достались из базы данных :(</p>
                  <p><a href="https://t.me/pvlppv" class="text-blue-600 hover:text-blue-800">Напишите мне</a>, я починю.</p>
                </div>
                <div v-else>
                  <div v-if="rows.length === 0" class="h-[500px] sm:h-[600px] w-full flex items-center justify-center border border-gray-300 rounded-lg">
                    <div id="add-first-db-record-button-container" class="text-center space-y-4">
                      <button
                        @click="showAddRowModal = true"
                        id="add-first-db-record-button"
                        class="mx-auto flex items-center justify-center w-20 h-20 sm:w-24 sm:h-24 rounded-full bg-gray-200 hover:bg-gray-300 transition-colors duration-200"
                      >
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          width="24"
                          height="24"
                          viewBox="0 0 24 24"
                          class="w-10 h-10 sm:w-12 sm:h-12 text-white"
                        >
                          <path fill="currentColor" d="M19 11h-6V5h-2v6H5v2h6v6h2v-6h6z" />
                        </svg>
                      </button>
                      <p class="text-gray-600 text-sm sm:text-base font-medium">
                        Добавить запись
                      </p>
                    </div>
                  </div>
                  <div v-else>
                    <ag-grid-vue
                      id="session-database-grid"
                      class="ag-theme-quartz h-[500px] sm:h-[600px] w-full"
                      :columnDefs="colDefs"
                      :defaultColDef="defaultColDef"
                      :rowData="rows"
                      @cellValueChanged="onCellValueChanged"
                      @rowClicked="onRowClicked"
                      @selectionChanged="onSelectionChanged"
                    />
                  </div>
                </div>
              </div>
              <div v-if="rows.length > 0" class="absolute bottom-4 left-0 right-0 flex justify-center" style="z-index: 1000;">
                <button
                  id="db-action-button"
                  v-tippy="selectedRows.length ? 'Удалить запись' : 'Добавить запись'"
                  @click="selectedRows.length ? deleteSelectedRows() : showAddRowModal = true"
                  class="text-xs sm:text-sm p-1 rounded-md bg-white border border-gray-300 bg-opacity-85 transition-all duration-300 hover:bg-opacity-100 flex items-center justify-center w-[200px] sm:w-[250px] shadow-lg"
                >
                  <span v-if="!selectedRows.length">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" class="v-5 h-5 sm:w-6 sm:h-6 fill-current">
                      <path d="M19 11h-6V5h-2v6H5v2h6v6h2v-6h6z"></path>
                    </svg>
                  </span>
                  <span v-else>
                    <svg xmlns="http://www.w3.org/2400/svg" width="24" height="24" viewBox="0 0 24 24" class="v-5 h-5 sm:v-6 sm:h-6 fill-current">
                      <path d="m16.192 6.344-4.243 4.242-4.242-4.242-1.414 1.414L10.535 12l-4.242 4.242 1.414 1.414 4.242-4.242 4.243 4.242 1.414-1.414L13.364 12l4.242-4.242z"></path>
                    </svg>
                  </span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
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
        v-if="showAddRowModal"
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
        v-if="showAddRowModal" 
        @click="handleAddRowModalOverlayClick"
        @wheel.prevent
        @scroll.prevent
        @touchmove.prevent
        class="fixed inset-0 flex items-center justify-center p-2 sm:p-4 z-[99999]"
      >
        <div 
          id="add-db-record-modal"
          @click.stop
          class="bg-white rounded-lg p-4 sm:p-6 w-full max-w-[80%] sm:max-w-md max-h-[80vh] flex flex-col overflow-hidden"
        >
          <h3 class="text-sm sm:text-base font-semibold mb-4 text-center flex-shrink-0">Добавить запись</h3>
          
          <!-- Scrollable content area -->
          <div
            @wheel.stop
            @scroll.stop
            @touchmove.stop
            class="flex-1 overflow-y-auto"
          >
            <form @submit.prevent="handleAddRow" class="space-y-3">
              <div v-for="col in filteredColumns" :key="col.field" class="space-y-1">
                <input
                  :id="col.field"
                  v-model="newRowData[col.field]"
                  type="text"
                  class="w-full p-2 text-xs sm:text-sm border rounded-lg focus:border-gray-300 focus:ring-0"
                  :placeholder="col.headerName"
                >
              </div>
            </form>
          </div>

          <!-- Sticky footer for buttons -->
          <div class="mt-5 flex-shrink-0">
            <div class="flex justify-center gap-3">
              <button
                @click="showAddRowModal = false"
                :disabled="isOnboardingActive"
                class="px-3 sm:px-4 py-1.5 sm:py-2 text-xs sm:text-sm rounded-lg border border-gray-300 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Отменить
              </button>
              <button
                type="submit"
                @click="handleAddRow"
                id="add-db-record-submit-button"
                class="px-3 sm:px-4 py-1.5 sm:py-2 text-xs sm:text-sm rounded-lg border border-gray-600 bg-gray-600 text-white hover:bg-gray-700"
              >
                Добавить
              </button>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
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
        v-if="showDeleteConfirmModal"
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
        v-if="showDeleteConfirmModal" 
        @click="showDeleteConfirmModal = false"
        class="fixed inset-0 flex items-center justify-center p-2 sm:p-4 z-[99999]"
      >
        <div 
          @click.stop
          class="bg-white rounded-lg p-4 sm:p-6 w-full max-w-[80%] sm:max-w-md max-h-[80vh] flex flex-col overflow-hidden"
        >
          <p class="text-center text-sm sm:text-base text-gray-600 mb-6">Вы уверены, что хотите удалить эту запись?</p>
          <div class="flex justify-center gap-3 items-center">
            <button @click="showDeleteConfirmModal = false" class="px-3 sm:px-4 py-1.5 sm:py-2 text-xs sm:text-sm rounded-lg border border-gray-300 transition-all duration-300 hover:border-gray-100 hover:bg-gray-100">Отмена</button>
            <button @click="confirmDelete" class="px-3 sm:px-4 py-1.5 sm:py-2 text-xs sm:text-sm rounded-lg border border-gray-300 transition-all duration-300 hover:border-gray-100 hover:bg-gray-100">Удалить</button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
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
        v-if="showErrorModal"
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
        v-if="showErrorModal" 
        @click="showErrorModal = false"
        class="fixed inset-0 flex items-center justify-center p-2 sm:p-4 z-[9999]"
      >
        <div 
          @click.stop
          class="border border-red-300 rounded-lg bg-red-50 p-4 sm:p-6 w-full max-w-[80%] sm:max-w-md"
        >
          <p class="text-center text-sm sm:text-base text-red-800 mb-6">{{ errorMessage }}</p>
          <div class="flex justify-center">
            <button @click="showErrorModal = false" class="px-4 py-2 text-sm rounded-lg border text-red-800 border-red-300 bg-red-50 transition-all duration-300 hover:border-red-800 hover:bg-red-100">ОК</button>
          </div>
          <p class="text-red-800 text-center text-2xs sm:text-xs mt-4">Если не понятно, в чём ошибка, <a href="https://t.me/pvlppv" class="text-blue-600 hover:text-blue-800">напиши мне</a>, я починю.</p>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useFetch } from '../composables/utils.js';
import { AgGridVue } from 'ag-grid-vue3';
import "ag-grid-community/styles/ag-grid.css";
import "ag-grid-community/styles/ag-theme-quartz.css";
import { directive as VTippy } from 'vue-tippy';
import { isOnboardingActive, canCloseModalOverride } from '../composables/onboarding.js';

const props = defineProps({
  tableName: {
    type: String,
    required: true
  },
  show: {
    type: Boolean,
    required: true
  },
  title: {
    type: String,
    required: true
  }
});

const apiBaseUrl = import.meta.env.VITE_APP_API_BASE_URL;
const error = ref(null);
const loading = ref(true);
const rows = ref([]);
const showAddRowModal = ref(false);
const showDeleteConfirmModal = ref(false);
const newRowData = ref({});
const selectedRows = ref([]);
const showErrorModal = ref(false);
const errorMessage = ref('');
const emit = defineEmits(['data-updated', 'close']);

const colDefs = [
  { 
    headerName: 'ID', 
    field: 'id', 
    editable: false,
    width: 60,
    minWidth: 60,
    maxWidth: 60
  },
  { 
    headerName: 'Дата', 
    field: 'datetime', 
    editable: false,
    width: 170,
    minWidth: 170,
    maxWidth: 170,
    valueFormatter: (params) => {
      if (!params.value) return '';
      const date = new Date(params.value);
      // Convert to Moscow time (UTC+3)
      const moscowDate = new Date(date.getTime() + (3 * 60 * 60 * 1000));
      return moscowDate.toLocaleString('ru-RU', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: false
      }).replace(',', '');
    }
  },
  { headerName: 'Значение', field: 'value', editable: true }
];

const defaultColDef = {
  resizable: true,
  sortable: false,
  filter: false,
  flex: 1,
  minWidth: 80,
  suppressMovable: true
};

const filteredColumns = computed(() => {
  return [{ field: 'value', headerName: 'Значение' }];
});

const fetchRows = async () => {
  if (!props.tableName) return; // Don't fetch if no table name is provided
  
  try {
    loading.value = true;
    error.value = null;
    const { data, error: fetchError, fetchData } = useFetch(
      `${apiBaseUrl}/api/users/table/${props.tableName}/rows/`
    );
    await fetchData();
    if (fetchError.value) {
      error.value = fetchError.value;
      return;
    }
    rows.value = data.value || [];
  } catch (err) {
    error.value = err.message || 'Ошибка при получении данных';
  } finally {
    loading.value = false;
  }
};

// Add a watch on tableName to refetch when it changes
watch(() => props.tableName, (newTableName) => {
  if (newTableName) {
    fetchRows();
  } else {
    rows.value = [];
    error.value = null;
  }
});

const handleAddRow = async () => {
  if (!newRowData.value.value) {
    showError('Значение не может быть пустым');
    return;
  }

  try {
    const { data, error: fetchError, fetchData: createData } = useFetch(
      `${apiBaseUrl}/api/users/table/${props.tableName}/rows/`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: { value: newRowData.value.value },
        credentials: 'include'
      }
    );
    await createData();
    if (fetchError.value) {
      showError(fetchError.value || 'Добавить запись не получилось');
      return;
    }
    showAddRowModal.value = false;
    newRowData.value = {};
    await fetchRows();
    
    // Get updated session data and emit it
    const sessionId = props.tableName.split('_')[1];
    const { data: sessionData, fetchData: fetchSession } = useFetch(
      `${apiBaseUrl}/api/users/sessions/${sessionId}/get`,
      { credentials: 'include' }
    );
    await fetchSession();
    if (sessionData.value) {
      emit('data-updated', sessionData.value);
    }
  } catch (err) {
    showError(err.message || 'Добавить запись не получилось');
  }
};

const deleteRow = async (id) => {
  try {
    const { data, error: fetchError, fetchData: deleteData } = useFetch(
      `${apiBaseUrl}/api/users/table/${props.tableName}/rows/${id}/`,
      { method: 'DELETE' }
    );
    await deleteData();
    if (fetchError.value) {
      showError(fetchError.value || 'Удалить запись не получилось');
      return;
    }
    await fetchRows();
    
    // Get updated session data and emit it
    const sessionId = props.tableName.split('_')[1];
    const { data: sessionData, fetchData: fetchSession } = useFetch(
      `${apiBaseUrl}/api/users/sessions/${sessionId}/get`,
      { credentials: 'include' }
    );
    await fetchSession();
    if (sessionData.value) {
      emit('data-updated', sessionData.value);
    }
  } catch (err) {
    showError(err.message || 'Удалить запись не получилось');
  }
};

const onCellValueChanged = async (params) => {
  if (params.column.colDef.field !== 'value') return;
  try {
    const updatedData = params.data;
    const { data, error: fetchError, fetchData: updateData } = useFetch(
      `${apiBaseUrl}/api/users/table/${props.tableName}/rows/${updatedData.id}/`,
      {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: { value: updatedData.value }
      }
    );
    await updateData();
    if (fetchError.value) {
      showError(fetchError.value || 'Обновить запись не получилось');
      return;
    }
    
    // Get updated session data and emit it
    const sessionId = props.tableName.split('_')[1];
    const { data: sessionData, fetchData: fetchSession } = useFetch(
      `${apiBaseUrl}/api/users/sessions/${sessionId}/get`,
      { credentials: 'include' }
    );
    await fetchSession();
    if (sessionData.value) {
      emit('data-updated', sessionData.value);
    }
  } catch (err) {
    showError(err.message || 'Обновить запись не получилось');
  }
};

const onRowClicked = (event) => {
  // Prevent selection if cell is being edited
  if (event.api.getEditingCells().length > 0) {
    return;
  }
  
  const node = event.node;
    if (node.isSelected()) {
        node.setSelected(false);
    } else {
        node.setSelected(true);
    }
};

const onSelectionChanged = (params) => {
  selectedRows.value = params.api.getSelectedRows();
};

const deleteSelectedRows = async () => {
  if (!selectedRows.value.length) return;
  showDeleteConfirmModal.value = true;
};

const confirmDelete = async () => {
  try {
    const row = selectedRows.value[0];
    await deleteRow(row.id);
    selectedRows.value = [];
    showDeleteConfirmModal.value = false;
  } catch (err) {
    showError(err.message || 'Удалить запись не получилось');
  }
};

const showError = (message) => {
  errorMessage.value = message;
  showErrorModal.value = true;
};

const handleOverlayClick = () => {
  if (!isOnboardingActive.value || canCloseModalOverride.value) {
    emit('close');
  }
};

const handleAddRowModalOverlayClick = () => {
  if (!isOnboardingActive.value) {
    showAddRowModal.value = false;
  }
};
</script>

<style scoped>
.dropdown-enter-active,
.dropdown-leave-active {
  transition: all 0.2s ease;
}
.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style> 