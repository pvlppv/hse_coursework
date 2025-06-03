<template>
    <div class="container mx-auto p-4">
        <div class="w-full space-y-2">
            <div class="flex justify-between items-center mb-4">
                <h1 class="text-xl sm:text-2xl font-semibold">База данных</h1>
                <router-link to="/pvlppv" class="text-sm text-gray-600 hover:text-gray-800">
                    Вернуться назад
                </router-link>
            </div>
            
            <!-- Reuse the same database component structure but with full-width layout -->
            <div v-if="error" class="p-4 text-sm text-center text-red-800 border border-red-300 rounded-lg bg-red-50" role="alert">
                <p>На сервере что-то сломалось, данные не достались из базы данных :(</p>
                <p><a href="https://t.me/pvlppv" class="text-blue-600 hover:text-blue-800">Напишите мне</a>, я починю.</p>
            </div>

            <div>
                <!-- Sheet Tabs -->
                <div class="flex space-x-1 overflow-x-auto">
                    <button
                        v-for="(sheet, index) in sheets"
                        :key="index"
                        @click="switchToSheet(index)"
                        class="px-4 py-2 text-sm rounded-t-lg transition-colors whitespace-nowrap"
                        :class="[
                            activeSheetIndex === index 
                                ? 'bg-[#f3f4f6]' 
                                : 'bg-white hover:bg-[#f3f4f6]'
                        ]"
                    >
                        {{ sheet.name }}
                    </button>
                </div>

                <!-- Grid Container with full height -->
                <div v-for="(sheet, index) in sheets" :key="index" v-show="activeSheetIndex === index">
                    <ag-grid-vue
                        class="ag-theme-quartz h-[calc(100vh-200px)] w-full"
                        :columnDefs="sheet.colDefs"
                        :defaultColDef="defaultColDef"
                        :undoRedoCellEditing="true"
                        :undoRedoCellEditingLimit="20"
                        rowModelType="infinite"
                        :cacheBlockSize="cacheBlockSize"
                        :maxConcurrentDatasourceRequests="2"
                        @gridReady="(params) => onGridReady(params, index)"
                        @cellValueChanged="(params) => onCellValueChanged(params, index)"
                        @rowClicked="onRowClicked"
                        @selectionChanged="onSelectionChanged"
                    />
                </div>
            </div>
        </div>

        <!-- Floating Action Button -->
        <div v-if="isLoggedIn" 
            class="absolute bottom-12 sm:bottom-16 left-0 right-0 flex justify-center"
            style="z-index: 1000;">
            <button
                @click="selectedRows.length ? deleteSelectedRows() : showAddRowModal = true"
                class="text-xs sm:text-sm p-1 rounded-md bg-white border border-gray-300 bg-opacity-85 transition-all duration-300 hover:bg-opacity-100 flex items-center justify-center w-full max-w-[200px] sm:max-w-[250px] shadow-lg"
            >
                <span v-if="!selectedRows.length">
                    <!-- Plus Icon -->
                    <svg xmlns="http://www.w3.org/2000/svg" 
                        width="24" height="24" viewBox="0 0 24 24" 
                        class="v-5 h-5 sm:w-6 sm:h-6 fill-current">
                        <path d="M19 11h-6V5h-2v6H5v2h6v6h2v-6h6z"></path>
                    </svg>
                </span>
                <span v-else>
                    <!-- Remove Icon -->
                    <svg xmlns="http://www.w3.org/2400/svg" 
                        width="24" height="24" viewBox="0 0 24 24" 
                        class="v-5 h-5 sm:v-6 sm:h-6 fill-current">
                        <path d="m16.192 6.344-4.243 4.242-4.242-4.242-1.414 1.414L10.535 12l-4.242 4.242 1.414 1.414 4.242-4.242 4.243 4.242 1.414-1.414L13.364 12l4.242-4.242z"></path>
                    </svg>
                </span>
            </button>
        </div>
    </div>

    <!-- Add Row Modal -->
    <Teleport to="body">
        <Transition
            enter-active-class="transition duration-300"
            enter-from-class="opacity-0"
            enter-to-class="opacity-100"
            leave-active-class="transition duration-300"
            leave-from-class="opacity-100"
            leave-to-class="opacity-0"
            >
            <div v-if="showAddRowModal" 
                @click="showAddRowModal = false"
                @wheel.prevent
                @scroll.prevent
                @touchmove.prevent
                class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-2 sm:p-4 z-[9999]">
                <div 
                    @click.stop
                    class="bg-white rounded-lg p-4 sm:p-6 w-full max-w-[80%] sm:max-w-md max-h-[80vh] flex flex-col overflow-hidden">
                    <h3 class="text-sm sm:text-base font-semibold mb-4 text-center flex-shrink-0">Добавить новую запись</h3>
                    
                    <!-- Scrollable content area -->
                    <div
                        @wheel.stop
                        @scroll.stop
                        @touchmove.stop
                        class="flex-1 overflow-y-auto">
                        <form @submit.prevent="handleAddRow" class="space-y-3">
                            <div v-for="col in filteredColumns" :key="col.field" class="space-y-1">
                                <label :for="col.field" class="text-xs sm:text-sm font-medium">
                                    {{ col.headerName }}
                                </label>
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
                                type="button"
                                @click="showAddRowModal = false"
                                class="px-3 sm:px-4 py-1.5 sm:py-2 text-xs sm:text-sm rounded-lg border border-gray-300 transition-all duration-300 hover:border-gray-100 hover:bg-gray-100"
                            >
                                Отмена
                            </button>
                            <button
                                type="submit"
                                @click="handleAddRow"
                                class="px-3 sm:px-4 py-1.5 sm:py-2 text-xs sm:text-sm rounded-lg border border-gray-300 transition-all duration-300 hover:border-gray-100 hover:bg-gray-100"
                            >
                                Добавить
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </Transition>
    </Teleport>

    <!-- Delete Confirmation Modal -->
    <Teleport to="body">
        <Transition
            enter-active-class="transition duration-300"
            enter-from-class="opacity-0"
            enter-to-class="opacity-100"
            leave-active-class="transition duration-300"
            leave-from-class="opacity-100"
            leave-to-class="opacity-0"
        >
            <div v-if="showDeleteConfirmModal" @wheel.prevent @touchmove.prevent @scroll.prevent @click="showDeleteConfirmModal = false"
                 class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-2 sm:p-4 z-[9999]">
                <div @click.stop class="bg-white rounded-lg p-4 sm:p-6 w-full max-w-[80%] sm:max-w-md">
                    <p class="text-center text-sm sm:text-base text-gray-600 mb-6">
                        Вы уверены, что хотите удалить эту запись?
                    </p>
                    <div class="flex justify-center gap-3 items-center">
                        <button
                            @click="showDeleteConfirmModal = false"
                            class="px-3 sm:px-4 py-1.5 sm:py-2 text-xs sm:text-sm rounded-lg border border-gray-300 transition-all duration-300 hover:border-gray-100 hover:bg-gray-100"
                        >
                            Отмена
                        </button>
                        <button
                            @click="confirmDelete"
                            class="px-3 sm:px-4 py-1.5 sm:py-2 text-xs sm:text-sm rounded-lg border border-gray-300 transition-all duration-300 hover:border-gray-100 hover:bg-gray-100"
                        >
                            Удалить
                        </button>
                    </div>
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

const apiBaseUrl = import.meta.env.VITE_APP_API_BASE_URL;
const error = ref(null);
const cacheBlockSize = 20;
const activeSheetIndex = ref(0);
const gridApis = ref([]);
const sheets = ref([]);
const showAddRowModal = ref(false);
const newRowData = ref({});

// Authentication
const isLoggedIn = ref(false);
const { data: userData, fetchData: userFetchData } = useFetch(`${apiBaseUrl}/api/users/me`);

// Update refs
const selectedRows = ref([]);
const showDeleteConfirmModal = ref(false);

// Update defaultColDef
const defaultColDef = {
    resizable: true,
    sortable: false,
    filter: false,
    flex: 1,
    minWidth: 80,
    suppressMovable: true,
    editable: false // Set default to false
};

const fetchTableStructure = async () => {
    try {
        const { data, error: fetchError, fetchData } = useFetch(
            `${apiBaseUrl}/api/tables/structure/`
        );
        await fetchData();

        if (fetchError.value) {
            error.value = fetchError.value;
            return;
        }

        sheets.value = data.value.map(table => ({
            name: table.name.charAt(0).toUpperCase() + table.name.slice(1),
            type: table.name,
            colDefs: generateColumnDefs(table.columns)
        }));
    } catch (err) {
        console.error('Error fetching table structure:', err);
        error.value = err;
    }
};

// Update generateColumnDefs to handle editability
const generateColumnDefs = (columns) => {
    return columns.map(column => ({
        headerName: column.name.charAt(0).toUpperCase() + column.name.slice(1),
        field: column.name,
        editable: isLoggedIn.value // Only editable if logged in
    }));
};

const getCurrentSheetColumns = computed(() => {
    if (!sheets.value[activeSheetIndex.value]) return [];
    return sheets.value[activeSheetIndex.value].colDefs.filter(col => col.field !== 'actions');
});

const switchToSheet = (index) => {
    activeSheetIndex.value = index;
    newRowData.value = {};
};

const createDatasource = (sheetIndex) => {
    return {
        getRows: async (params) => {
            const { startRow, endRow, successCallback, failCallback } = params;
            
            try {
                const { data, error: fetchError, fetchData } = useFetch(
                    `${apiBaseUrl}/api/${sheets.value[sheetIndex].type}/latest/?skip=${startRow}&limit=${endRow - startRow}`
                );
                
                await fetchData();

                if (fetchError.value) {
                    failCallback();
                    return;
                }

                const lastRow = data.value && data.value.length < (endRow - startRow) 
                    ? startRow + data.value.length 
                    : undefined;
                
                successCallback(data.value || [], lastRow);
            } catch (err) {
                console.error('Error fetching data:', err);
                failCallback();
            }
        }
    };
};

const deleteRow = async (id, sheetIndex) => {
    try {
        const { fetchData: deleteData } = useFetch(
            `${apiBaseUrl}/api/${sheets.value[sheetIndex].type}/${id}`,
            { method: 'DELETE' }
        );

        await deleteData();
        gridApis.value[sheetIndex].setGridOption('datasource', createDatasource(sheetIndex));
    } catch (err) {
        console.error('Error deleting row:', err);
        error.value = err;
    }
};

const handleAddRow = async () => {
    try {
        const currentSheet = sheets.value[activeSheetIndex.value];
        const { fetchData: createData } = useFetch(
            `${apiBaseUrl}/api/${currentSheet.type}/`,
            {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: newRowData.value,
                credentials: 'include'
            }
        );
        
        await createData();
        showAddRowModal.value = false;
        newRowData.value = {};
        gridApis.value[activeSheetIndex.value].setGridOption('datasource', createDatasource(activeSheetIndex.value));
    } catch (err) {
        console.error('Error creating row:', err);
        error.value = err;
    }
};

// Update selection handler
const onSelectionChanged = (params) => {
    selectedRows.value = params.api.getSelectedRows();
};

// Add method to delete selected rows
const deleteSelectedRows = async () => {
    if (!selectedRows.value.length) return;
    showDeleteConfirmModal.value = true;
};

// Add confirmation method
const confirmDelete = async () => {
    try {
        const row = selectedRows.value[0];
        await deleteRow(row.id, activeSheetIndex.value);
        selectedRows.value = [];
        showDeleteConfirmModal.value = false;
    } catch (err) {
        console.error('Error deleting row:', err);
        error.value = err;
    }
};

// Update onGridReady to include pinned row handling
const onGridReady = (params, sheetIndex) => {
    gridApis.value[sheetIndex] = params.api;
    params.api.setGridOption('datasource', createDatasource(sheetIndex));
};

const onCellValueChanged = async (params, sheetIndex) => {
    try {
        const updatedData = params.data;
        const { id, ...updatePayload } = updatedData;
        
        const { fetchData: updateData } = useFetch(
            `${apiBaseUrl}/api/${sheets.value[sheetIndex].type}/${id}`, 
            {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: updatePayload
            }
        );

        await updateData();
    } catch (err) {
        console.error('Error updating row:', err);
        error.value = err;
    }
};

const onRowClicked = (event) => {
    if (!isLoggedIn.value) return;

    if (event.api.getEditingCells().length > 0) return;
    
    const node = event.node;
    if (node.isSelected()) {
        node.setSelected(false);
    } else {
        node.setSelected(true);
    }
};

onMounted(async () => {
    await userFetchData();
    isLoggedIn.value = !!userData.value;
    await fetchTableStructure();
    
    // Update column definitions to reflect auth state
    sheets.value.forEach((sheet, index) => {
        if (gridApis.value[index]) {
            const updatedColDefs = generateColumnDefs(sheet.colDefs);
            gridApis.value[index].setColumnDefs(updatedColDefs);
        }
    });
});

// Add computed property for filtered columns
const filteredColumns = computed(() => {
    if (!sheets.value[activeSheetIndex.value]) return [];
    return sheets.value[activeSheetIndex.value].colDefs.filter(col => 
        !['id', 'date', 'actions'].includes(col.field)
    );
});
</script>
