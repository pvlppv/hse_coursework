<template>
    <div class="container mx-auto flex justify-center">
        <div class="max-w-sm sm:max-w-lg w-full space-y-5">
            <a class="text-base sm:text-lg font-semibold p-2 rounded-lg border border-gray-300 transition-all duration-300 hover:border-gray-100 hover:bg-gray-100 flex items-center justify-center">
                База данных
            </a>

            <!-- Sheet Tabs -->
            <div class="flex space-x-1 border-b border-gray-200">
                <button
                    v-for="(sheet, index) in sheets"
                    :key="index"
                    @click="switchToSheet(index)"
                    class="px-4 py-2 text-sm rounded-t-lg transition-colors"
                    :class="[
                        activeSheetIndex === index 
                            ? 'bg-[#f3f4f6]' 
                            : 'bg-white hover:bg-[#f3f4f6]'
                    ]"
                >
                    {{ sheet.name }}
                </button>
            </div>

            <div v-if="error" class="p-4 text-xs sm:text-sm text-center text-red-800 border border-red-300 rounded-lg bg-red-50" role="alert">
                <p>На сервере что-то сломалось, данные не достались из базы данных :(</p>
                <p><a href="https://t.me/pvlppv" class="text-blue-600 hover:text-blue-800">Напишите мне</a>, я починю.</p>
            </div>

            <!-- Grid Container -->
            <div v-for="(sheet, index) in sheets" :key="index" v-show="activeSheetIndex === index">
                <ag-grid-vue
                    class="ag-theme-quartz h-[600px] w-full"
                    :columnDefs="sheet.colDefs"
                    :defaultColDef="defaultColDef"
                    rowModelType="infinite"
                    :cacheBlockSize="cacheBlockSize"
                    :maxConcurrentDatasourceRequests="2"
                    @gridReady="(params) => onGridReady(params, index)"
                    @cellValueChanged="(params) => onCellValueChanged(params, index)"
                />
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
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

const defaultColDef = {
    resizable: true,
    sortable: true,
    filter: true,
    flex: 1,
    minWidth: 100,
    suppressMovable: true
};

// Fetch table structure from backend
const fetchTableStructure = async () => {
    try {
        const { data, error: fetchError, fetchData } = useFetch(
            `${apiBaseUrl}/api/tables/structure`
        );
        await fetchData();

        if (fetchError.value) {
            error.value = fetchError.value;
            return;
        }

        // Transform backend table structure into sheet configuration
        sheets.value = data.value.map(table => ({
            name: formatTableName(table.name),
            type: table.name,
            colDefs: generateColumnDefs(table.columns)
        }));
    } catch (err) {
        console.error('Error fetching table structure:', err);
        error.value = err;
    }
};

// Helper to format table names for display
const formatTableName = (name) => {
    return name.charAt(0).toUpperCase() + name.slice(1);
};

// Generate column definitions from table structure
const generateColumnDefs = (columns) => {
    const dynamicColumns = columns.map(column => ({
        headerName: column.name.charAt(0).toUpperCase() + column.name.slice(1),
        field: column.name,
        editable: column.name !== 'id' ? true : false,
        width: column.type === 'date' ? 150 : null
    }));

    return [...dynamicColumns];
};

const switchToSheet = (index) => {
    activeSheetIndex.value = index;
};

// Create datasource for infinite scrolling
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

const onGridReady = (params, sheetIndex) => {
    gridApis.value[sheetIndex] = params.api;
    params.api.setGridOption('datasource', createDatasource(sheetIndex));
};

const onCellValueChanged = async (params, sheetIndex) => {
    try {
        const updatedData = params.data;
        console.log('Updating row with data:', updatedData);
        
        // Remove id from the update payload
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
        gridApis.value[sheetIndex].setGridOption('datasource', createDatasource(sheetIndex));
    } catch (err) {
        console.error('Error updating row:', err);
        error.value = err;
    }
};

const createRow = async (sheetIndex) => {
    try {
        const defaultValues = generateDefaultValues(sheets.value[sheetIndex].colDefs);
        const { fetchData: createData } = useFetch(
            `${apiBaseUrl}/api/${sheets.value[sheetIndex].type}`, 
            {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: defaultValues
            }
        );
        
        await createData();
        gridApis.value[sheetIndex].setGridOption('datasource', createDatasource(sheetIndex));
    } catch (err) {
        console.error('Error creating row:', err);
        error.value = err;
    }
};

const generateDefaultValues = (colDefs) => {
    const values = {};
    colDefs.forEach(col => {
        if (col.field !== 'id') {
            if (col.field === 'date') {
                values[col.field] = new Date().toISOString();
            } else {
                values[col.field] = '';
            }
        }
    });
    return values;
};

const deleteRow = async (id, sheetIndex) => {
    try {
        const { fetchData: deleteData } = useFetch(
            `${apiBaseUrl}/api/${sheets.value[sheetIndex].type}/${id}`, 
            {
                method: 'DELETE'
            }
        );
        
        await deleteData();
        gridApis.value[sheetIndex].setGridOption('datasource', createDatasource(sheetIndex));
    } catch (err) {
        console.error('Error deleting row:', err);
        error.value = err;
    }
};

// Fetch table structure when component mounts
onMounted(() => {
    fetchTableStructure();
});
</script>