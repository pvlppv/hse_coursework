<template>
    <div class="container mx-auto flex justify-center relative">
        <div class="max-w-sm sm:max-w-lg w-full space-y-2">
            <!-- <router-link to="/database" class="block"> -->
            <div class="text-base sm:text-lg font-semibold p-2 rounded-lg border border-gray-300 transition-all duration-300 hover:border-gray-100 hover:bg-gray-100 flex items-center justify-center">
                База данных
            </div>
            <!-- </router-link> -->
            
            <div v-if="error" class="p-4 text-xs sm:text-sm text-center text-red-800 border border-red-300 rounded-lg bg-red-50" role="alert">
                <p>На сервере что-то сломалось, данные не достались из базы данных :(</p>
                <p><a href="https://t.me/pvlppv" class="text-blue-600 hover:text-blue-800">Напишите мне</a>, я починю.</p>
            </div>

            <div v-else>
                <!-- Sheet Tabs -->
                <div v-if="sheets.length > 0" class="flex space-x-1 overflow-x-auto relative">
                    <div
                        v-for="(sheet, index) in sheets"
                        :key="index"
                        class="flex items-center space-x-1 group"
                    >
                        <!-- Tab Button with Dropdown Arrow -->
                        <div class="relative flex items-center">
                            <button
                                :ref="(el) => setTabRef(el, index)"
                                @click="switchToSheet(index)"
                                class="px-2 sm:px-4 py-2 text-xs sm:text-sm rounded-t-lg transition-colors whitespace-nowrap flex items-center"
                                :class="[
                                    activeSheetIndex === index 
                                        ? 'bg-[#f3f4f6]' 
                                        : 'bg-white hover:bg-[#f3f4f6]'
                                ]"
                            >
                                {{ sheet.name }}
                                <!-- Dropdown Arrow -->
                                <button
                                    v-if="activeSheetIndex === index"
                                    @click.stop="toggleMenu(index)"
                                    class="ml-1.5 hover:bg-gray-200 rounded-full flex items-center justify-center"
                                >
                                    <svg class="w-4 h-4 sm:w-5 sm:h-5 text-gray-600" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
                                        <path d="M16.293 9.293 12 13.586 7.707 9.293l-1.414 1.414L12 16.414l5.707-5.707z"></path>
                                    </svg>
                                </button>
                            </button>

                            <!-- Dropdown Menu with Fixed Positioning -->
                            <Teleport to="body">
                                <div 
                                    v-if="openedMenuIndex === index"
                                    @click="openedMenuIndex = null"
                                    class="fixed z-50 bg-white border border-gray-200 rounded-lg shadow-lg"
                                    :style="{
                                        top: `${dropdownTop}px`,
                                        left: `${dropdownLeft}px`
                                    }"
                                    data-dropdown-menu 
                                >
                                    <div class="py-1" @click.stop>
                                        <button
                                            @click="startRenamingTable(index)"
                                            class="w-full px-3 py-2 text-left text-xs sm:text-sm hover:bg-gray-100"
                                        >
                                            Переименовать
                                        </button>
                                        <button
                                            @click="deleteTable(sheets[index].fullName, index)"
                                            class="w-full px-3 py-2 text-left text-xs sm:text-sm text-red-600 hover:bg-gray-100"
                                        >
                                            Удалить
                                        </button>
                                    </div>
                                </div>
                            </Teleport>
                        </div>
                    </div>

                    <!-- Add Table Button -->
                    <button
                        @click="showAddTableModal = true"
                        class="px-2 sm:px-4 py-2 text-xs sm:text-sm rounded-t-lg transition-colors whitespace-nowrap bg-white hover:bg-[#f3f4f6] flex items-center"
                        >
                        <!-- Plus Icon -->
                        <svg xmlns="http://www.w3.org/2000/svg" 
                            width="24" height="24" viewBox="0 0 24 24" 
                            class="h-4 w-4 sm:h-5 sm:w-5">
                            <path d="M19 11h-6V5h-2v6H5v2h6v6h2v-6h6z"></path>
                        </svg>
                    </button>
                </div>

                <!-- Empty State -->
                <div v-if="sheets.length === 0" class="h-[500px] sm:h-[600px] w-full flex items-center justify-center border border-gray-300 rounded-lg">
                    <div class="text-center space-y-4">
                        <!-- Giant white plus icon in gray circle -->
                        <button
                        @click="showAddTableModal = true"
                        class="mx-auto flex items-center justify-center w-20 h-20 sm:w-24 sm:h-24 rounded-full bg-gray-200 hover:bg-gray-300 transition-colors duration-200"
                        >
                            <!-- Plus icon -->
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

                        <!-- Text below -->
                        <p class="text-gray-600 text-sm sm:text-base font-medium">
                            Создать таблицу
                        </p>
                    </div>
                </div>    

                <!-- Grid Container -->
                <div v-else v-for="(sheet, index) in sheets" :key="index" v-show="activeSheetIndex === index">
                    <ag-grid-vue
                        class="ag-theme-quartz h-[500px] sm:h-[600px] w-full"
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
        <div v-if="sheets.length > 0" 
            class="absolute bottom-4 left-0 right-0 flex justify-center"
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
                                Отменить
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

    <!-- Add/Rename Table Modal -->
    <Teleport to="body">
        <Transition
            enter-active-class="transition duration-300"
            enter-from-class="opacity-0"
            enter-to-class="opacity-100"
            leave-active-class="transition duration-300"
            leave-from-class="opacity-100"
            leave-to-class="opacity-0"
        >
            <div v-if="showAddTableModal" 
                @click="showAddTableModal = false"
                @wheel.prevent
                @scroll.prevent
                @touchmove.prevent
                class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-2 sm:p-4 z-[9999]">
                <div 
                    @click.stop
                    class="bg-white rounded-lg p-4 sm:p-6 w-full max-w-[80%] sm:max-w-md max-h-[80vh] flex flex-col overflow-hidden">
                    <h3 class="text-sm sm:text-base font-semibold mb-4 text-center flex-shrink-0">
                        {{ isRenaming ? 'Переименовать таблицу' : 'Создать новую таблицу' }}
                    </h3>
                    
                    <!-- Scrollable content area -->
                    <div
                        @wheel.stop
                        @scroll.stop
                        @touchmove.stop
                        class="flex-1 overflow-y-auto">
                        <form @submit.prevent="isRenaming ? handleRenameTable() : handleAddTable()" class="space-y-3">
                            <div class="space-y-1">
                                <label for="tableName" class="text-xs sm:text-sm font-medium">
                                    Название таблицы
                                </label>
                                <input
                                    id="tableName"
                                    v-model="newTableName"
                                    type="text"
                                    class="w-full p-2 text-xs sm:text-sm border rounded-lg focus:border-gray-300 focus:ring-0"
                                    placeholder="Введи название таблицы"
                                >
                            </div>
                        </form>
                    </div>

                    <!-- Sticky footer for buttons -->
                    <div class="mt-5 flex-shrink-0">
                        <div class="flex justify-center gap-3">
                            <button
                                type="button"
                                @click="showAddTableModal = false; isRenaming = false"
                                class="px-3 sm:px-4 py-1.5 sm:py-2 text-xs sm:text-sm rounded-lg border border-gray-300 transition-all duration-300 hover:border-gray-100 hover:bg-gray-100"
                            >
                                Отменить
                            </button>
                            <button
                                type="submit"
                                @click="isRenaming ? handleRenameTable() : handleAddTable()"
                                class="px-3 sm:px-4 py-1.5 sm:py-2 text-xs sm:text-sm rounded-lg border border-gray-300 transition-all duration-300 hover:border-gray-100 hover:bg-gray-100"
                            >
                                {{ isRenaming ? 'Переименовать' : 'Добавить' }}
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </Transition>
    </Teleport>
    
    <!-- Error Modal -->
    <Teleport to="body">
        <Transition
            enter-active-class="transition duration-300"
            enter-from-class="opacity-0"
            enter-to-class="opacity-100"
            leave-active-class="transition duration-300"
            leave-from-class="opacity-100"
            leave-to-class="opacity-0"
        >
            <div v-if="showErrorModal" @wheel.prevent @touchmove.prevent @scroll.prevent @click="showErrorModal = false"
                class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-2 sm:p-4 z-[9999]">
                <div @click.stop class="border border-red-300 rounded-lg bg-red-50 p-4 sm:p-6 w-full max-w-[80%] sm:max-w-md">
                    <!-- Error Message -->
                    <p class="text-center text-sm sm:text-base text-red-800 mb-6">
                        {{ errorMessage }}
                    </p>
                    <!-- OK Button -->
                    <div class="flex justify-center">
                        <button
                            @click="showErrorModal = false"
                            class="px-4 py-2 text-sm rounded-lg border text-red-800 border-red-300 bg-red-50 transition-all duration-300 hover:border-red-800 hover:bg-red-100"
                        >
                            ОК
                        </button>
                    </div>
                    <p class="text-red-800 text-center text-2xs sm:text-xs mt-4">Если не понятно, в чём ошибка, <a href="https://t.me/pvlppv" class="text-blue-600 hover:text-blue-800">напиши мне</a>, я починю.</p>
                </div>
            </div>
        </Transition>
    </Teleport>
</template>

<script setup>
import { ref, computed, onMounted, watch, onBeforeUnmount } from 'vue';
import { useFetch } from '../composables/utils.js';
import { AgGridVue } from 'ag-grid-vue3';
import "ag-grid-community/styles/ag-grid.css";
import "ag-grid-community/styles/ag-theme-quartz.css";

const apiBaseUrl = import.meta.env.VITE_APP_API_BASE_URL;
const error = ref(null);
const loading = ref(true);
const cacheBlockSize = 20;
const activeSheetIndex = ref(0);
const gridApis = ref([]);
const sheets = ref([]);
const showAddRowModal = ref(false);
const showAddTableModal = ref(false);
const showDeleteConfirmModal = ref(false);
const newRowData = ref({});
const newTableName = ref('');
const selectedRows = ref([]);
const isRenaming = ref(false);
const renamingIndex = ref(null); // Store the index of the table being renamed
const showErrorModal = ref(false);
const errorMessage = ref('');
const openedMenuIndex = ref(null);
const dropdownTop = ref(0)
const dropdownLeft = ref(0)
const tabRefs = ref([])

// Method to set tab references
const setTabRef = (el, index) => {
    if (el) {
        tabRefs.value[index] = el
    }
}

// Toggle dropdown menu
const toggleMenu = (index) => {
    // If the menu is already open for this tab, close it
    if (openedMenuIndex.value === index) {
        openedMenuIndex.value = null
        return
    }

    // Find the button that was clicked
    const tabButton = tabRefs.value[index]
    
    if (tabButton) {
        // Get the button's position
        const rect = tabButton.getBoundingClientRect()

        // Position the dropdown just below the button
        dropdownTop.value = rect.bottom
        dropdownLeft.value = rect.left

        // Open the menu for this specific tab
        openedMenuIndex.value = index
    }
}

// Function to show the error modal
const showError = (message) => {
    errorMessage.value = message;
    showErrorModal.value = true;
};

// Close dropdown menu
const closeMenu = () => {
    openedMenuIndex.value = null;
};

const handleClickOutside = (event) => {
  if (openedMenuIndex.value === null) return;

  // Get current dropdown menu and trigger button
  const dropdownMenu = document.querySelector('[data-dropdown-menu]');
  const triggerButton = tabRefs.value[openedMenuIndex.value];

  // Check if click is outside both elements
  if (!dropdownMenu?.contains(event.target) && !triggerButton?.contains(event.target)) {
    openedMenuIndex.value = null;
  }
};

// Fixed column definitions since all tables have the same structure
const generateColumnDefs = () => [
    { headerName: 'ID', field: 'id', editable: false },
    { headerName: 'Value', field: 'value', editable: true },
    { headerName: 'Date', field: 'date', editable: true }
];

// AG Grid configuration
const defaultColDef = {
    resizable: true,
    sortable: false,
    filter: false,
    flex: 1,
    minWidth: 80,
    suppressMovable: true
};

// Table management functions
const fetchUserTables = async () => {
    try {
        const { data, error: fetchError, fetchData } = useFetch(
            `${apiBaseUrl}/api/users/table/`
        );
        await fetchData();

        if (fetchError.value) {
            error.value = fetchError.value;
            return;
        }

        sheets.value = data.value.map(tableName => ({
            name: tableName.split('_').slice(2).join('_'), // Remove user_{id}_ prefix
            fullName: tableName,
            colDefs: generateColumnDefs()
        }));
    } catch (err) {
        console.error('Error fetching user tables:', err);
        error.value = err;
    } finally {
        loading.value = false;
    }
};

// Table operations
const handleAddTable = async () => {
    if (!validateTableName(newTableName.value)) return;

    try {
        const { data, error: fetchError, fetchData: createTable } = useFetch(
            `${apiBaseUrl}/api/users/table/`,
            {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: { table_name: newTableName.value },
                credentials: 'include'
            }
        );
        
        await createTable();
        
        if (fetchError.value) {
            showError(fetchError.value || 'Создать таблицу не получилось');
            return;
        }

        showAddTableModal.value = false;
        newTableName.value = '';
        await fetchUserTables();
        activeSheetIndex.value = sheets.value.length - 1;
    } catch (err) {
        console.error('Error creating table:', err);
        showError(err.message || 'Создать таблицу не получилось');
    }
};

// Row operations
const createDatasource = (sheetIndex) => {
    return {
        getRows: async (params) => {
            const { startRow, endRow, successCallback, failCallback } = params;
            
            try {
                const { data, error: fetchError, fetchData } = useFetch(
                    `${apiBaseUrl}/api/users/table/${sheets.value[sheetIndex].fullName}/rows/?skip=${startRow}&limit=${endRow - startRow}`
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

const handleAddRow = async () => {
    try {
        const currentSheet = sheets.value[activeSheetIndex.value];
        const { data, error: fetchError, fetchData: createData } = useFetch(
            `${apiBaseUrl}/api/users/table/${currentSheet.fullName}/rows/`,
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
        gridApis.value[activeSheetIndex.value].setGridOption('datasource', createDatasource(activeSheetIndex.value));
    } catch (err) {
        console.error('Error creating row:', err);
        showError(err.message || 'Добавить запись не получилось');
    }
};

const deleteRow = async (id, sheetIndex) => {
    try {
        const { data, error: fetchError, fetchData: deleteData } = useFetch(
            `${apiBaseUrl}/api/users/table/${sheets.value[sheetIndex].fullName}/rows/${id}/`,
            { method: 'DELETE' }
        );

        await deleteData();

        if (fetchError.value) {
            showError(fetchError.value || 'Удалить запись не получилось');
            return;
        }

        gridApis.value[sheetIndex].setGridOption('datasource', createDatasource(sheetIndex));
    } catch (err) {
        console.error('Error deleting row:', err);
        showError(err.message || 'Удалить запись не получилось');
    }
};

// Grid event handlers
const onGridReady = (params, sheetIndex) => {
    gridApis.value[sheetIndex] = params.api;
    params.api.setGridOption('datasource', createDatasource(sheetIndex));
};

const onCellValueChanged = async (params, sheetIndex) => {
    if (params.column.colDef.field !== 'value') return;
    
    try {
        const updatedData = params.data;
        const { data, error: fetchError, fetchData: updateData } = useFetch(
            `${apiBaseUrl}/api/users/table/${sheets.value[sheetIndex].fullName}/rows/${updatedData.id}/`, 
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
    } catch (err) {
        console.error('Error updating row:', err);
        showError(err.message || 'Обновить запись не получилось');
    }
};

const onRowClicked = (event) => {
    if (event.api.getEditingCells().length > 0) return;
    const node = event.node;
    node.setSelected(!node.isSelected());
};

const onSelectionChanged = (params) => {
    selectedRows.value = params.api.getSelectedRows();
};

// UI handlers
const switchToSheet = (index) => {
    activeSheetIndex.value = index;
    newRowData.value = {}; // Clear the new row data
    gridApis.value[index].setGridOption('datasource', createDatasource(index)); // Refresh the datasource
};

const deleteSelectedRows = async () => {
    if (!selectedRows.value.length) return;
    showDeleteConfirmModal.value = true;
};

const confirmDelete = async () => {
    try {
        const row = selectedRows.value[0];
        await deleteRow(row.id, activeSheetIndex.value);
        selectedRows.value = [];
        showDeleteConfirmModal.value = false;
    } catch (err) {
        console.error('Error deleting row:', err);
        showError(err.message || 'Удалить запись не получилось');
    }
};

// Computed properties
const filteredColumns = computed(() => {
    return [{ field: 'value', headerName: 'Value' }];
});

// Function to delete a table
const deleteTable = async (tableName, index) => {
    closeMenu();
    try {
        const { data, error: fetchError, fetchData: deleteTable } = useFetch(
        `${apiBaseUrl}/api/users/table/${tableName}/`,
        {
            method: 'DELETE',
            credentials: 'include'
        }
        );

        await deleteTable();

        if (fetchError.value) {
            showError(fetchError.value || 'Удалить таблицу не получилось');
            return;
        }

        sheets.value.splice(index, 1);
        if (activeSheetIndex.value >= sheets.value.length) {
            activeSheetIndex.value = sheets.value.length - 1;
        }
    } catch (err) {
        console.error('Error deleting table:', err);
    }
};

const startRenamingTable = (index) => {
    isRenaming.value = true;
    renamingIndex.value = index;
    newTableName.value = sheets.value[index].name; // Pre-fill the input with the current table name
    showAddTableModal.value = true;
    closeMenu();
};

const handleRenameTable = async () => {
    if (!validateTableName(newTableName.value)) return;

    try {
        const { data, error: fetchError, fetchData: renameTable } = useFetch(
            `${apiBaseUrl}/api/users/table/${sheets.value[renamingIndex.value].fullName}/rename`,
            {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: { new_name: newTableName.value },
                credentials: 'include'
            }
        );

        await renameTable();
        
        if (fetchError.value) {
            showError(fetchError.value || 'Переименовать таблицу не получилось');
            return;
        }

        showAddTableModal.value = false;
        isRenaming.value = false;
        await fetchUserTables(); // Refresh the table list
    } catch (err) {
        console.error('Error renaming table:', err);
        showError(fetchError.value || 'Переименовать таблицу не получилось');
    }
};

const validateTableName = (name) => {
    if (!name.trim()) {
        showError('Таблица не может быть пустой.');
        return false;
    }
    if (name.length > 50) {
        showError('Имя таблицы превышает 50 символов.');
        return false;
    }
    return true;
};

watch(openedMenuIndex, (newIndex) => {
  if (newIndex !== null) {
    document.addEventListener('click', handleClickOutside);
  } else {
    document.removeEventListener('click', handleClickOutside);
  }
});

// Cleanup listener
onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside);
});

// Initial setup
onMounted(async () => {
    await fetchUserTables();
});
</script>

<style scoped>
/* Dropdown Menu Animation */
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