<template>
    <div class="container mx-auto flex justify-center relative">
      <div id="sessions-list" class="max-w-sm sm:max-w-lg w-full space-y-2">

        <!-- Error message -->
        <div v-if="error" class="p-4 text-xs sm:text-sm text-center text-red-800 border border-red-300 rounded-lg bg-red-50" role="alert">
            {{ error }}
            <p>На сервере что-то сломалось, данные не достались из базы данных :(</p>
            <p><a href="https://t.me/pvlppv" class="text-blue-600 hover:text-blue-800">Напишите мне</a>, я починю.</p>
        </div>
        

        <!-- Sessions List -->
        <div v-else class="space-y-4">
           <div v-if="activeSessions.length" id="active-sessions-list-container">
            <div 
              v-for="session in sortedActiveSessions"
              :key="session.id"
              class="group relative border border-gray-300 rounded-lg p-4 hover:shadow-lg transition-all duration-200 bg-white"
            >
            <div class="flex justify-between items-start mb-2">
              <div>
                <div class="flex items-center gap-2">
                  <span class="relative flex h-3 w-3 ml-2">
                    <span 
                      v-if="session.is_active && !session.is_paused"
                      class="animate-ping absolute h-full w-full rounded-full bg-green-500 opacity-75"
                    ></span>
                    <span 
                      class="relative rounded-full h-3 w-3"
                      :class="{
                        'bg-green-500': session.is_active && !session.is_paused,
                        'bg-yellow-500': session.is_active && session.is_paused,
                        'bg-red-500': !session.is_active
                      }"
                    ></span>
                  </span>
                  <h3 class="text-sm sm:text-sm font-semibold text-black">{{ session.title }}</h3>
                </div>
                <p class="text-xs sm:text-xs text-gray-500 mt-1">
                  Осталось {{ formatDurationRemaining(session.time_remaining) }}
                </p>
              </div>
              <div class="flex gap-1">
                <Tooltip :text="session.is_paused ? 'Возобновить сеанс' : 'Поставить сеанс на паузу'">
                  <button
                    @click.stop="pauseSession(session.id, !session.is_paused)"
                    class="p-1 hover:bg-gray-100 rounded-full"
                    >
                    <svg class="w-4 h-4 text-gray-600" viewBox="0 0 24 24">
                      <path d="M12 2C6.486 2 2 6.486 2 12s4.486 10 10 10 10-4.486 10-10S17.514 2 12 2zm0 18c-4.411 0-8-3.589-8-8s3.589-8 8-8 8 3.589 8 8-3.589 8-8 8z"/>
                      <path d='M9 9h2v6H9zm4 0h2v6h-2z'/>
                    </svg>
                  </button>
                </Tooltip>
                <Tooltip text="Редактировать сеанс">
                  <button
                    @click.stop="openEditModal(session)"
                    class="p-1 hover:bg-gray-100 rounded-full">
                    <svg class="w-4 h-4 text-gray-600" viewBox="0 0 24 24">
                      <path d="M12 2C6.486 2 2 6.486 2 12s4.486 10 10 10 10-4.486 10-10S17.514 2 12 2zm0 18c-4.411 0-8-3.589-8-8s3.589-8 8-8 8 3.589 8 8-3.589 8-8 8z"/>
                      <path d="M11 11h2v6h-2zm0-4h2v2h-2z"/>
                    </svg>
                  </button>
                </Tooltip>
                <Tooltip text="Скрыть сеанс">
                  <button
                    @click.stop="openSoftDeleteModal(session)"
                    class="p-1 hover:bg-gray-100 rounded-full text-gray-400 hover:text-red-600 transition-colors"
                  >
                  <svg class="w-4 h-4" viewBox="0 0 24 24">
                    <path d="M9.172 16.242L12 13.414l2.828 2.828 1.414-1.414L13.414 12l2.828-2.828-1.414-1.414L12 10.586 9.172 7.758 7.758 9.172 10.586 12l-2.828 2.828z"/>
                    <path d="M12 22c5.514 0 10-4.486 10-10S17.514 2 12 2 2 6.486 2 12s4.486 10 10 10zm0-18c4.411 0 8 3.589 8 8s-3.589 8-8 8-8-3.589-8-8 3.589-8 8-8z"/>
                  </svg>
                  </button>
                </Tooltip>
              </div>
            </div>
            <button 
              @click="openDatabaseModal(session.id)"
              class="w-full p-2 border-2 border-dashed border-gray-300 rounded-lg hover:border-gray-400 transition-colors duration-200 flex flex-col items-center justify-center"
            >
              <div class="w-6 h-6 bg-gray-200 rounded-full flex items-center justify-center">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="24"
                  height="24"
                  viewBox="0 0 24 24"
                  class="w-4 h-4 text-white"
                >
                  <path fill="currentColor" d="M19 11h-6V5h-2v6H5v2h6v6h2v-6h6z"/>
                </svg>
              </div>
              <p class="text-xs text-gray-600 mt-1">
                Добавить данные
              </p>
            </button>

            <div v-if="session?.visualization_preferences?.length" class="mt-4">
              <!-- Commented out expand/collapse functionality for future use
              <button 
                @click="expandedSessionId = expandedSessionId === session.id ? null : session.id"
                class="w-full flex items-center justify-center p-2 text-gray-600 hover:bg-gray-50 rounded-lg transition-colors"
              >
                <svg 
                  class="w-6 h-6 transform transition-transform" 
                  :class="{'rotate-180': expandedSessionId === session.id}"
                  viewBox="0 0 24 24"
                >
                  <path fill="currentColor" d="M7.41 8.59L12 13.17l4.59-4.58L18 10l-6 6-6-6 1.41-1.41z"/>
                </svg>
              </button>
              <div v-if="expandedSessionId === session.id" class="mt-4 space-y-4">
                <component 
                  v-for="vizId in session.visualization_preferences"
                  :key="`${session.id}-${vizId}-${Date.now()}`"
                  :is="getVisualizationComponent(vizId)"
                  :session-id="session.id"
                  :user-id="userId"
                />
              </div>
              -->
              <div class="space-y-4">
                <component 
                  v-for="vizId in session.visualization_preferences"
                  :key="`${session.id}-${vizId}-${Date.now()}`"
                  :is="getVisualizationComponent(vizId)"
                  :session-id="session.id"
                  :user-id="userId"
                />
              </div>
            </div>
          </div>
        </div>
          <!-- Add Session Button -->
          <button
            id="add-session-button"
            @click="showAddModal = true"
            class="w-full p-4 border-2 border-dashed border-gray-300 rounded-lg hover:border-gray-400 transition-colors duration-200 flex flex-col items-center justify-center"
          >
            <div class="w-8 h-8 bg-gray-200 rounded-full flex items-center justify-center">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                viewBox="0 0 24 24"
                class="w-5 h-5 text-white"
              >
                <path fill="currentColor" d="M19 11h-6V5h-2v6H5v2h6v6h2v-6h6z"/>
              </svg>
            </div>
            <p class="text-xs sm:text-sm text-gray-600 mt-2">
              Начать новый сеанс
            </p>
          </button>

          <!-- Show/Hide Archived Sessions -->
          <button 
            id="show-inactive-button"
            @click="showInactive || fetchSessions(false); showInactive = !showInactive"
            class="w-full flex items-center justify-center gap-2 px-4 py-3 text-xs sm:text-sm hover:bg-gray-50 text-gray-700 rounded-lg transition-colors border border-gray-200 mt-4"
          >
            <span>{{ showInactive ? 'Скрыть неактивные сеансы' : 'Показать неактивные сеансы' }}</span>
            <svg class="w-4 h-4 transform transition-transform" :class="{'rotate-180': showInactive}" viewBox="0 0 24 24">
              <path fill="currentColor" d="M7.41 8.59L12 13.17l4.59-4.58L18 10l-6 6-6-6 1.41-1.41z"/>
            </svg>
          </button>

          <!-- Inactive Sessions List -->
          <p 
            v-if="showInactive && !inactiveSessions.length" 
            class="text-xs sm:text-sm text-gray-600 mt-4 text-center bg-gray-50 rounded-lg py-8 px-4"
          >
            Неактивных сеансов нет
          </p>
          <div 
            v-for="session in sortedInactiveSessions"
            v-if="showInactive && inactiveSessions.length"
            v-show="showInactive"
            :key="session.id"
            class="group relative border border-gray-300 rounded-lg p-4 hover:shadow-lg transition-all duration-200 bg-white opacity-50"
          >
            <div class="flex justify-between items-start mb-2">
              <div>
                <div class="flex items-center gap-2">
                  <span class="relative flex h-3 w-3 ml-2">
                    <span 
                      class="relative rounded-full h-3 w-3"
                      :class="{
                        'bg-yellow-500': session.is_active && session.is_paused,
                        'bg-red-500': !session.is_active
                      }"
                    ></span>
                  </span>
                  <h3 class="text-xs sm:text-sm font-semibold text-black">{{ session.title }}</h3>
                  <span v-if="session.is_paused" class="text-xs sm:text-xs px-2 py-1 bg-yellow-100 text-yellow-800 rounded-full">
                    На паузе
                  </span>
                </div>
                <p class="text-xs sm:text-xs text-gray-500 mt-1">
                  Осталось {{ formatDurationRemaining(session.time_remaining) }}
                </p>
              </div>
              <div class="flex gap-1">
                <Tooltip text="Возобновить сеанс">
                  <button
                    @click.stop="session.is_active ? pauseSession(session.id, !session.is_paused) : restoreSession(session.id)"
                    class="p-1 hover:bg-gray-100 rounded-full"
                    >
                    <svg 
                      class="w-4 h-4" 
                      :class="{
                        'text-gray-600': session.is_active,
                        'text-green-600': !session.is_active
                      }"
                      viewBox="0 0 24 24"
                    >
                      <path d="M12 2C6.486 2 2 6.486 2 12s4.486 10 10 10 10-4.486 10-10S17.514 2 12 2zm0 18c-4.411 0-8-3.589-8-8s3.589-8 8-8 8 3.589 8 8-3.589 8-8 8z"/>
                      <path v-if="session.is_active" d='m9 17 8-5-8-5z'/>
                      <path v-else d="m6.293 13.293 1.414 1.414L12 10.414l4.293 4.293 1.414-1.414L12 7.586z"/>
                    </svg>
                  </button>
                </Tooltip>
                <Tooltip text="Редактировать сеанс">
                  <button
                    @click.stop="openEditModal(session)"
                    class="p-1 hover:bg-gray-100 rounded-full">
                    <svg class="w-4 h-4 text-gray-600" viewBox="0 0 24 24">
                      <path d="M12 2C6.486 2 2 6.486 2 12s4.486 10 10 10 10-4.486 10-10S17.514 2 12 2zm0 18c-4.411 0-8-3.589-8-8s3.589-8 8-8 8 3.589 8 8-3.589 8-8 8z"/>
                      <path d="M11 11h2v6h-2zm0-4h2v2h-2z"/>
                    </svg>
                  </button>
                </Tooltip>
                <Tooltip text="Удалить сеанс">
                  <button
                    @click.stop="openDeleteModal(session)"
                    class="p-1 hover:bg-gray-100 rounded-full text-gray-400 hover:text-red-600 transition-colors"
                  >
                  <svg class="w-4 h-4" viewBox="0 0 24 24">
                    <path d="M9.172 16.242L12 13.414l2.828 2.828 1.414-1.414L13.414 12l2.828-2.828-1.414-1.414L12 10.586 9.172 7.758 7.758 9.172 10.586 12l-2.828 2.828z"/>
                    <path d="M12 22c5.514 0 10-4.486 10-10S17.514 2 12 2 2 6.486 2 12s4.486 10 10 10zm0-18c4.411 0 8 3.589 8 8s-3.589 8-8 8-8-3.589-8-8 3.589-8 8-8z"/>
                  </svg>
                  </button>
                </Tooltip>
              </div>
            </div>
        </div>
      </div>
    </div>
  
    <!-- Edit Session Modal -->
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
          v-if="showEditModal" 
          @click="showEditModal = false"
          @wheel.prevent
          @scroll.prevent
          @touchmove.prevent
          class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-2 sm:p-4 z-[9999] overflow-hidden"
        >
          <div 
            @click.stop
            class="bg-white rounded-lg p-4 sm:p-6 w-full max-w-sm sm:max-w-lg max-h-[80vh] flex flex-col overflow-hidden"
          >
            <h3 class="text-sm sm:text-base font-semibold mb-4 text-center flex-shrink-0">Редактирование сеанса</h3>
            
            <!-- Scrollable content area -->
            <div
              @wheel.stop
              @scroll.stop
              @touchmove.stop
              class="flex-1 overflow-y-auto overflow-x-hidden px-2 pb-4"
            >
              <form @submit.prevent="saveSession" class="space-y-4">
                <div class="space-y-1">
                  <label class="text-sm sm:text-base font-medium flex items-center gap-2">
                    <span class="flex items-center justify-center w-6 h-6 rounded-full bg-gray-100 text-gray-600 text-sm">1</span>
                    Что отслеживаем?
                    <button 
                      type="button"
                      @click.stop="showTitleHelp"
                      class="text-gray-400 hover:text-gray-600"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24">
                        <path d="M12 2C6.486 2 2 6.486 2 12s4.486 10 10 10 10-4.486 10-10S17.514 2 12 2zm0 18c-4.411 0-8-3.589-8-8s3.589-8 8-8 8 3.589 8 8-3.589 8-8 8z"/>
                        <path d="M11 11h2v6h-2zm0-4h2v2h-2z"/>
                      </svg>
                    </button>
                  </label>
                  <input
                    v-model="editableSession.title"
                    type="text"
                    class="w-full p-2 text-xs sm:text-sm border rounded-lg focus:border-gray-300 focus:ring-0"
                    required
                    placeholder="Название сеанса"
                  >
                </div>
                
                <div class="space-y-1">
                  <label class="text-sm sm:text-base font-medium flex items-center gap-2">
                    <span class="flex items-center justify-center w-6 h-6 rounded-full bg-gray-100 text-gray-600 text-sm">2</span>
                    Сколько по времени отслеживаем?
                    <button 
                      type="button"
                      @click="showDurationHelp"
                      class="text-gray-400 hover:text-gray-600"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24">
                        <path d="M12 2C6.486 2 2 6.486 2 12s4.486 10 10 10 10-4.486 10-10S17.514 2 12 2zm0 18c-4.411 0-8-3.589-8-8s3.589-8 8-8 8 3.589 8 8-3.589 8-8 8z"/>
                        <path d="M11 11h2v6h-2zm0-4h2v2h-2z"/>
                      </svg>
                    </button>
                  </label>
                  
                  <div class="space-y-4">
                    <input
                      :value="formatDuration(editableSession.end_time)"
                      type="text"
                      readonly
                      @click="showDurationPicker = true"
                      class="w-full p-2 text-xs sm:text-sm border rounded-lg focus:border-gray-300 focus:ring-0 cursor-pointer"
                      required
                      placeholder="Выбрать продолжительность"
                    >
                    
                    <div class="flex flex-wrap gap-2">
                      <button
                        v-for="preset in durationPresets"
                        :key="preset.label"
                        type="button"
                        @click="applyPresetDuration(preset)"
                        class="px-3 py-1 text-xs rounded-full border hover:bg-gray-50"
                      >
                        {{ preset.label }}
                      </button>
                    </div>
                  </div>
                </div>

                <div class="space-y-1">
                  <label class="text-sm sm:text-base font-medium flex items-center gap-2">
                    <span class="flex items-center justify-center w-6 h-6 rounded-full bg-gray-100 text-gray-600 text-sm">3</span>
                    Как собираем данные?
                  </label>
                  <div class="flex flex-col gap-4">
                    <div class="flex gap-6">
                      <button
                        type="button"
                        @click="editableSession.data_collection_methods = ['manual']"
                        class="flex-1 p-2 text-xs sm:text-sm border rounded-lg hover:bg-gray-50 relative"
                        :class="{ 'border-gray-500 bg-gray-50': editableSession.data_collection_methods.includes('manual') }"
                      >
                        Вручную
                      </button>
                      <div class="flex-1 relative">
                        <button
                          type="button"
                          disabled
                          class="w-full p-2 text-xs sm:text-sm border rounded-lg opacity-50 cursor-not-allowed relative group"
                        >
                          Автоматически
                          <div class="absolute inset-0 flex items-center justify-center bg-white bg-opacity-50">
                            <svg class="w-4 h-4" viewBox="0 0 24 24">
                              <path d="M12 2C9.243 2 7 4.243 7 7v3H6c-1.103 0-2 .897-2 2v8c0 1.103.897 2 2 2h12c1.103 0 2-.897 2-2v-8c0-1.103-.897-2-2-2h-1V7c0-2.757-2.243-5-5-5zm6 10 .002 8H6v-8h12zm-9-2V7c0-1.654 1.346-3 3-3s3 1.346 3 3v3H9z"/>
                            </svg>
                          </div>
                          <div class="absolute inset-0 flex items-center justify-center p-2">
                            <img src="../assets/apple_health.svg" class="w-6 h-6 absolute -top-2 -left-2 -rotate-12" alt="Apple Health" />
                            <img src="../assets/google_calendar.png" class="w-6 h-6 absolute -top-2 -right-2 rotate-12" alt="Google Calendar" />
                            <img src="../assets/notion.png" class="w-6 h-6 absolute -bottom-2 -left-2 -rotate-12" alt="Notion" />
                            <img src="../assets/telegram.png" class="w-6 h-6 absolute -bottom-2 -right-2 rotate-12" alt="Telegram" />
                          </div>
                          <div class="absolute inset-0 rounded-lg shadow-[0_0_15px_rgba(168,85,247,0.5)]"></div>
                        </button>
                      </div>
                    </div>
                  </div>
                </div>

                <div class="space-y-1">
                  <label class="text-sm sm:text-base font-medium flex items-center gap-2">
                    <span class="flex items-center justify-center w-6 h-6 rounded-full bg-gray-100 text-gray-600 text-sm">4</span>
                    Как визуализируем данные?
                  </label>
                  <div class="grid grid-cols-2 gap-4">
                    <div 
                      v-for="(viz, index) in visualizations" 
                      :key="index"
                      class="relative group cursor-pointer border border-gray-300 rounded-lg overflow-hidden"
                      :class="{
                        'border-gray-300': !editableSession.visualization_preferences.includes(viz.id.toString()),
                        'border-gray-600': editableSession.visualization_preferences.includes(viz.id.toString())
                      }"
                      @click="selectVizForEdit(viz)"
                    >
                      <img 
                        :src="viz.image" 
                        :alt="viz.title"
                        class="w-full h-32 object-cover transition-opacity duration-200 group-hover:opacity-75"
                        :class="{ 'ring-2 ring-gray-500': editableSession.visualization_preferences.includes(viz.id.toString()) }"
                      />
                      <div class="absolute top-2 right-2">
                        <div 
                          class="w-6 h-6 rounded-full border-2 flex items-center justify-center"
                          :class="{
                            'bg-gray-600 border-gray-600': editableSession.visualization_preferences.includes(viz.id.toString()),
                            'bg-white border-gray-300': !editableSession.visualization_preferences.includes(viz.id.toString())
                          }"
                        >
                          <svg 
                            v-if="editableSession.visualization_preferences.includes(viz.id.toString())"
                            class="w-4 h-4 text-white" 
                            viewBox="0 0 24 24"
                          >
                            <path fill="currentColor" d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41L9 16.17z"/>
                          </svg>
                        </div>
                      </div>
                      <div 
                        v-if="editableSession.visualization_preferences.includes(viz.id.toString())"
                        class="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-200"
                      >
                        <div class="flex gap-2">
                          <button 
                            @click.stop="openVizModal(viz, $event)"
                            class="p-1.5 bg-white rounded-full shadow-lg hover:bg-gray-50 border border-gray-300"
                          >
                            <svg class="w-4 h-4" viewBox="0 0 24 24">
                              <path d="M12 10c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm6 0c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zM6 10c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z"/>
                            </svg>
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <div class="space-y-1">
                  <label class="text-sm sm:text-base font-medium flex items-center gap-2">
                    <span class="flex items-center justify-center w-6 h-6 rounded-full bg-gray-100 text-gray-600 text-sm">5</span>
                    Как анализируем данные?
                  </label>
                  <div class="flex flex-col gap-4">
                    <div class="flex gap-6">
                      <div class="flex-1 relative">
                        <button
                          type="button"
                          disabled
                          class="w-full p-2 text-xs sm:text-sm border rounded-lg opacity-50 cursor-not-allowed relative group"
                        >
                          Через инструменты
                          <div class="absolute inset-0 flex items-center justify-center bg-white bg-opacity-50">
                            <svg class="w-4 h-4" viewBox="0 0 24 24">
                              <path d="M12 2C9.243 2 7 4.243 7 7v3H6c-1.103 0-2 .897-2 2v8c0 1.103.897 2 2 2h12c1.103 0 2-.897 2-2v-8c0-1.103-.897-2-2-2h-1V7c0-2.757-2.243-5-5-5zm6 10 .002 8H6v-8h12zm-9-2V7c0-1.654 1.346-3 3-3s3 1.346 3 3v3H9z"/>
                            </svg>
                          </div>
                        </button>
                      </div>
                      <div class="flex-1 relative">
                        <button
                          type="button"
                          disabled
                          class="w-full p-2 text-xs sm:text-sm border rounded-lg opacity-50 cursor-not-allowed relative group"
                        >
                          Через ИИ
                          <div class="absolute inset-0 flex items-center justify-center bg-white bg-opacity-50">
                            <svg class="w-4 h-4" viewBox="0 0 24 24">
                              <path d="M12 2C9.243 2 7 4.243 7 7v3H6c-1.103 0-2 .897-2 2v8c0 1.103.897 2 2 2h12c1.103 0 2-.897 2-2v-8c0-1.103-.897-2-2-2h-1V7c0-2.757-2.243-5-5-5zm6 10 .002 8H6v-8h12zm-9-2V7c0-1.654 1.346-3 3-3s3 1.346 3 3v3H9z"/>
                            </svg>
                          </div>
                          <svg class="w-6 h-6 absolute -top-2 -right-2" viewBox="0 0 24 24" transform="scale(-1, 1)">
                            <path d="m11 4-.5-1-.5 1-1 .125.834.708L9.5 6l1-.666 1 .666-.334-1.167.834-.708zm8.334 10.666L18.5 13l-.834 1.666-1.666.209 1.389 1.181L16.834 18l1.666-1.111L20.166 18l-.555-1.944L21 14.875zM6.667 6.333 6 5l-.667 1.333L4 6.5l1.111.944L4.667 9 6 8.111 7.333 9l-.444-1.556L8 6.5zM3.414 17c0 .534.208 1.036.586 1.414L5.586 20c.378.378.88.586 1.414.586s1.036-.208 1.414-.586L20 8.414c.378-.378.586-.88.586-1.414S20.378 5.964 20 5.586L18.414 4c-.756-.756-2.072-.756-2.828 0L4 15.586c-.378.378-.586.88-.586 1.414zM17 5.414 18.586 7 15 10.586 13.414 9 17 5.414z"/>
                          </svg>
                          <div class="absolute inset-0 rounded-lg shadow-[0_0_15px_rgba(168,85,247,0.5)]"></div>
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </form>
            </div>

            <!-- Sticky footer for buttons -->
            <div class="mt-5 mb-2 flex-shrink-0">
              <div class="flex justify-center gap-3">
                <button
                  type="button"
                  @click="showEditModal = false"
                  class="px-3 sm:px-4 py-1.5 sm:py-2 text-xs sm:text-sm rounded-lg border border-gray-300 hover:bg-gray-50"
                >
                  Отменить
                </button>
                <button
                  type="submit"
                  @click="saveSession"
                  :disabled="!editableSession.title || !editableSession.end_time || editableSession.visualization_preferences.length === 0"
                  class="px-3 sm:px-4 py-1.5 sm:py-2 text-xs sm:text-sm rounded-lg border border-gray-600 bg-gray-600 text-white hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed flex-1 max-w-[200px]"
                >
                  Сохранить
                </button>
              </div>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>

    <!-- Add Session Modal -->
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
          v-if="showAddModal" 
          @click="showAddModal = false"
          @wheel.prevent
          @scroll.prevent
          @touchmove.prevent
          class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-2 sm:p-4 z-[9999] overflow-hidden"
        >
          <div 
            id="add-session-modal"
            @click.stop
            class="bg-white rounded-lg p-4 sm:p-6 w-full max-w-sm sm:max-w-lg max-h-[80vh] flex flex-col overflow-hidden"
          >
            <h3 class="text-base sm:text-lg font-semibold mb-4 text-center flex-shrink-0">Создание сеанса</h3>
            
            <!-- Scrollable content area -->
            <div
              @wheel.stop
              @scroll.stop
              @touchmove.stop
              class="flex-1 overflow-y-auto overflow-x-hidden px-2 pb-4"
            >
              <form @submit.prevent="addSession" class="space-y-4">
                <div class="space-y-1" id="new-session-title-input">
                  <label class="text-sm sm:text-base font-medium flex items-center gap-2">
                    <span class="flex items-center justify-center w-6 h-6 rounded-full bg-gray-100 text-gray-600 text-sm">1</span>
                    Что будем отслеживать?
                    <button 
                      type="button"
                      @click.stop="showTitleHelp"
                      class="text-gray-400 hover:text-gray-600"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24">
                        <path d="M12 2C6.486 2 2 6.486 2 12s4.486 10 10 10 10-4.486 10-10S17.514 2 12 2zm0 18c-4.411 0-8-3.589-8-8s3.589-8 8-8 8 3.589 8 8-3.589 8-8 8z"/>
                        <path d="M11 11h2v6h-2zm0-4h2v2h-2z"/>
                      </svg>
                    </button>
                  </label>
                  <input
                    v-model="newSession.title"
                    type="text"
                    class="w-full p-2 text-xs sm:text-sm border rounded-lg focus:border-gray-300 focus:ring-0"
                    required
                    placeholder="Название сеанса"
                  >
                </div>
                
                <div class="space-y-1" id="new-session-duration-input">
                  <label class="text-sm sm:text-base font-medium flex items-center gap-2">
                    <span class="flex items-center justify-center w-6 h-6 rounded-full bg-gray-100 text-gray-600 text-sm">2</span>
                    Сколько по времени будем отслеживать?
                    <button 
                      type="button"
                      @click="showDurationHelp"
                      class="text-gray-400 hover:text-gray-600"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24">
                        <path d="M12 2C6.486 2 2 6.486 2 12s4.486 10 10 10 10-4.486 10-10S17.514 2 12 2zm0 18c-4.411 0-8-3.589-8-8s3.589-8 8-8 8 3.589 8 8-3.589 8-8 8z"/>
                        <path d="M11 11h2v6h-2zm0-4h2v2h-2z"/>
                      </svg>
                    </button>
                  </label>
                  
                  <div class="space-y-4">
                    <input
                      :value="formatDuration(newSession.end_time)"
                      type="text"
                      readonly
                      @click="showDurationPicker = true"
                      class="w-full p-2 text-xs sm:text-sm border rounded-lg focus:border-gray-300 focus:ring-0 cursor-pointer"
                      required
                      placeholder="Выбрать продолжительность"
                    >
                    
                    <div class="flex flex-wrap gap-2">
                      <button
                        v-for="preset in durationPresets"
                        :key="preset.label"
                        type="button"
                        @click="applyPresetDuration(preset)"
                        class="px-3 py-1 text-xs rounded-full border hover:bg-gray-50"
                      >
                        {{ preset.label }}
                      </button>
                    </div>
                  </div>
                </div>

                <div class="space-y-1" id="new-session-data-collection-methods-input">
                  <label class="text-sm sm:text-base font-medium flex items-center gap-2">
                    <span class="flex items-center justify-center w-6 h-6 rounded-full bg-gray-100 text-gray-600 text-sm">3</span>
                    Как будем собирать данные?
                  </label>
                  <div class="flex flex-col gap-4">
                    <div class="flex gap-6">
                      <button
                        type="button"
                        @click="newSession.data_collection_methods = ['manual']"
                        class="flex-1 p-2 text-xs sm:text-sm border rounded-lg hover:bg-gray-50 relative"
                        :class="{ 'border-gray-500 bg-gray-50': newSession.data_collection_methods.includes('manual') }"
                      >
                        Вручную
                      </button>
                      <div class="flex-1 relative">
                        <button
                          type="button"
                          disabled
                          class="w-full p-2 text-xs sm:text-sm border rounded-lg opacity-50 cursor-not-allowed relative group"
                        >
                          Автоматически
                          <div class="absolute inset-0 flex items-center justify-center bg-white bg-opacity-50">
                            <svg class="w-4 h-4" viewBox="0 0 24 24">
                              <path d="M12 2C9.243 2 7 4.243 7 7v3H6c-1.103 0-2 .897-2 2v8c0 1.103.897 2 2 2h12c1.103 0 2-.897 2-2v-8c0-1.103-.897-2-2-2h-1V7c0-2.757-2.243-5-5-5zm6 10 .002 8H6v-8h12zm-9-2V7c0-1.654 1.346-3 3-3s3 1.346 3 3v3H9z"/>
                            </svg>
                          </div>
                          <div class="absolute inset-0 flex items-center justify-center p-2">
                            <img src="../assets/apple_health.svg" class="w-6 h-6 absolute -top-2 -left-2 -rotate-12" alt="Apple Health" />
                            <img src="../assets/google_calendar.png" class="w-6 h-6 absolute -top-2 -right-2 rotate-12" alt="Google Calendar" />
                            <img src="../assets/notion.png" class="w-6 h-6 absolute -bottom-2 -left-2 -rotate-12" alt="Notion" />
                            <img src="../assets/telegram.png" class="w-6 h-6 absolute -bottom-2 -right-2 rotate-12" alt="Telegram" />
                          </div>
                          <div class="absolute inset-0 rounded-lg shadow-[0_0_15px_rgba(168,85,247,0.5)]"></div>
                        </button>
                      </div>
                    </div>
                  </div>
                </div>

                <div class="space-y-1" id="new-session-visualization-preferences-input">
                  <label class="text-sm sm:text-base font-medium flex items-center gap-2">
                    <span class="flex items-center justify-center w-6 h-6 rounded-full bg-gray-100 text-gray-600 text-sm">4</span>
                    Как будем визуализировать данные?
                  </label>
                  <div class="grid grid-cols-2 gap-4">
                    <div 
                      v-for="(viz, index) in visualizations" 
                      :key="index"
                      class="relative group cursor-pointer border border-gray-300 rounded-lg overflow-hidden"
                      :class="{
                        'border-gray-300': !newSession.visualization_preferences.includes(viz.id.toString()),
                        'border-gray-600': newSession.visualization_preferences.includes(viz.id.toString())
                      }"
                      @click="selectViz(viz)"
                    >
                      <img 
                        :src="viz.image" 
                        :alt="viz.title"
                        class="w-full h-32 object-cover transition-opacity duration-200 group-hover:opacity-75"
                        :class="{ 'ring-2 ring-gray-500': newSession.visualization_preferences.includes(viz.id.toString()) }"
                      />
                      <div class="absolute top-2 right-2">
                        <div 
                          class="w-6 h-6 rounded-full border-2 flex items-center justify-center"
                          :class="{
                            'bg-gray-600 border-gray-600': newSession.visualization_preferences.includes(viz.id.toString()),
                            'bg-white border-gray-300': !newSession.visualization_preferences.includes(viz.id.toString())
                          }"
                        >
                          <Tooltip text="Посмотреть описание визуализации">
                            <svg 
                              v-if="newSession.visualization_preferences.includes(viz.id.toString())"
                              class="w-4 h-4 text-white" 
                              viewBox="0 0 24 24"
                            >
                              <path fill="currentColor" d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41L9 16.17z"/>
                            </svg>
                          </Tooltip>
                        </div>
                      </div>
                      <div 
                        v-if="newSession.visualization_preferences.includes(viz.id.toString())"
                        class="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-200"
                      >
                        <div class="flex gap-2">
                          <button 
                            @click.stop="openVizModal(viz, $event)"
                            class="p-1.5 bg-white rounded-full shadow-lg hover:bg-gray-50 border border-gray-300"
                          >
                            <svg class="w-4 h-4" viewBox="0 0 24 24">
                              <path d="M12 10c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm6 0c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zM6 10c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z"/>
                            </svg>
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <div class="space-y-1" id="new-session-analysis-methods-input">
                  <label class="text-sm sm:text-base font-medium flex items-center gap-2">
                    <span class="flex items-center justify-center w-6 h-6 rounded-full bg-gray-100 text-gray-600 text-sm">5</span>
                    Как будем анализировать данные?
                  </label>
                  <div class="flex flex-col gap-4">
                    <div class="flex gap-6">
                      <div class="flex-1 relative">
                        <button
                          type="button"
                          disabled
                          class="w-full p-2 text-xs sm:text-sm border rounded-lg opacity-50 cursor-not-allowed relative group"
                        >
                          Через инструменты
                          <div class="absolute inset-0 flex items-center justify-center bg-white bg-opacity-50">
                            <svg class="w-4 h-4" viewBox="0 0 24 24">
                              <path d="M12 2C9.243 2 7 4.243 7 7v3H6c-1.103 0-2 .897-2 2v8c0 1.103.897 2 2 2h12c1.103 0 2-.897 2-2v-8c0-1.103-.897-2-2-2h-1V7c0-2.757-2.243-5-5-5zm6 10 .002 8H6v-8h12zm-9-2V7c0-1.654 1.346-3 3-3s3 1.346 3 3v3H9z"/>
                            </svg>
                          </div>
                        </button>
                      </div>
                      <div class="flex-1 relative">
                        <button
                          type="button"
                          disabled
                          class="w-full p-2 text-xs sm:text-sm border rounded-lg opacity-50 cursor-not-allowed relative group"
                        >
                          Через ИИ
                          <div class="absolute inset-0 flex items-center justify-center bg-white bg-opacity-50">
                            <svg class="w-4 h-4" viewBox="0 0 24 24">
                              <path d="M12 2C9.243 2 7 4.243 7 7v3H6c-1.103 0-2 .897-2 2v8c0 1.103.897 2 2 2h12c1.103 0 2-.897 2-2v-8c0-1.103-.897-2-2-2h-1V7c0-2.757-2.243-5-5-5zm6 10 .002 8H6v-8h12zm-9-2V7c0-1.654 1.346-3 3-3s3 1.346 3 3v3H9z"/>
                            </svg>
                          </div>
                          <svg class="w-6 h-6 absolute -top-2 -right-2" viewBox="0 0 24 24" transform="scale(-1, 1)">
                            <path d="m11 4-.5-1-.5 1-1 .125.834.708L9.5 6l1-.666 1 .666-.334-1.167.834-.708zm8.334 10.666L18.5 13l-.834 1.666-1.666.209 1.389 1.181L16.834 18l1.666-1.111L20.166 18l-.555-1.944L21 14.875zM6.667 6.333 6 5l-.667 1.333L4 6.5l1.111.944L4.667 9 6 8.111 7.333 9l-.444-1.556L8 6.5zM3.414 17c0 .534.208 1.036.586 1.414L5.586 20c.378.378.88.586 1.414.586s1.036-.208 1.414-.586L20 8.414c.378-.378.586-.88.586-1.414S20.378 5.964 20 5.586L18.414 4c-.756-.756-2.072-.756-2.828 0L4 15.586c-.378.378-.586.88-.586 1.414zM17 5.414 18.586 7 15 10.586 13.414 9 17 5.414z"/>
                          </svg>
                          <div class="absolute inset-0 rounded-lg shadow-[0_0_15px_rgba(168,85,247,0.5)]"></div>
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </form>
            </div>

            <!-- Sticky footer for buttons -->
            <div class="mt-5 mb-2 flex-shrink-0">
              <div class="flex justify-center gap-3" id="new-session-submit-button">
                <button
                  type="button"
                  @click="showAddModal = false"
                  class="px-3 sm:px-4 py-1.5 sm:py-2 text-xs sm:text-sm rounded-lg border border-gray-300 hover:bg-gray-50"
                >
                  Отменить
                </button>
                <button
                  type="submit"
                  @click="addSession"
                  :disabled="!newSession.title || !newSession.end_time || !newSession.visualization_preferences.length"
                  class="px-3 sm:px-4 py-1.5 sm:py-2 text-xs sm:text-sm rounded-lg border border-gray-600 bg-gray-600 text-white hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed flex-1 max-w-[200px]"
                >
                  Начать
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
        <div 
          v-if="showDeleteModal" 
          @click="showDeleteModal = false"
          @wheel.prevent
          @scroll.prevent
          @touchmove.prevent
          class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-2 sm:p-4 z-[9999]"
        >
          <div 
            @click.stop
            class="bg-white rounded-lg p-4 sm:p-6 w-full max-w-sm sm:max-w-lg max-h-[80vh] flex flex-col overflow-hidden"
          >
            <p class="text-center text-sm sm:text-base text-gray-600 mb-6 flex-shrink-0">
              Этот сеанс будет безвозвратно удалён. Вы уверены, что хотите удалить его?
            </p>
            <div class="flex justify-center gap-3 mt-auto">
              <button
                @click="showDeleteModal = false"
                class="px-3 sm:px-4 py-1.5 sm:py-2 text-xs sm:text-sm rounded-lg border border-gray-300 hover:bg-gray-50"
              >
                Отменить
              </button>
              <button
                @click="deleteSession()"
                class="px-3 sm:px-4 py-1.5 sm:py-2 text-xs sm:text-sm rounded-lg border border-red-300 bg-red-300 text-red-600 hover:bg-red-400"
              >
                Удалить
              </button>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>

    <!-- Soft Delete Confirmation Modal -->
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
          v-if="showSoftDeleteModal" 
          @click="showSoftDeleteModal = false"
          @wheel.prevent
          @scroll.prevent
          @touchmove.prevent
          class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-2 sm:p-4 z-[9999]"
        >
          <div 
            @click.stop
            class="bg-white rounded-lg p-4 sm:p-6 w-full max-w-sm sm:max-w-lg max-h-[80vh] flex flex-col overflow-hidden"
          >
            <p class="text-center text-sm sm:text-base text-gray-600 mb-6 flex-shrink-0">
              Этот сеанс будет скрыт и перенесён ниже в неактивные сеансы. Вы сможете восстановить его в любой момент.
            </p>
            <div class="flex justify-center gap-3 mt-auto">
              <button
                @click="showSoftDeleteModal = false"
                class="px-3 sm:px-4 py-1.5 sm:py-2 text-xs sm:text-sm rounded-lg border border-gray-300 hover:bg-gray-50"
              >
                Отменить
              </button>
              <button
                @click="softDeleteSession(deleteTargetId)"
                class="px-3 sm:px-4 py-1.5 sm:py-2 text-xs sm:text-sm rounded-lg border border-red-300 bg-red-300 text-red-600 hover:bg-red-400"
              >
                Скрыть
              </button>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>

    <!-- Add Duration Picker Modal -->
    <Teleport to="body">
      <Transition name="fade">
        <div 
          v-if="showDurationPicker" 
          @click="showDurationPicker = false"
          class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-[10001]"
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
                  min="0"
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
                @click="showDurationPicker = false"
                class="px-4 py-2 text-xs sm:text-sm rounded-lg border hover:bg-gray-50"
              >
                Отменить
              </button>
              <button
                @click="applyCustomDuration"
                class="px-4 py-2 text-xs sm:text-sm rounded-lg border border-gray-600 bg-gray-600 text-white hover:bg-gray-700 max-w-[200px]"
              >
                Применить
              </button>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>

    <!-- Visualization Details Modal -->
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
          v-if="showVizModal" 
          @click="showVizModal = false"
          @wheel.prevent
          @scroll.prevent
          @touchmove.prevent
          class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-2 sm:p-4 z-[10001]"
        >
          <div 
            @click.stop
            class="bg-white rounded-lg p-4 sm:p-6 w-full max-w-[80%] sm:max-w-md max-h-[80vh] flex flex-col overflow-hidden"
          >            
            <!-- Scrollable content area -->
            <div
              @wheel.stop
              @scroll.stop
              @touchmove.stop
              class="flex-1 overflow-y-auto"
            >
              <img 
                :src="selectedViz?.image" 
                :alt="selectedViz?.title"
                class="w-full h-48 sm:h-64 object-cover rounded-lg mb-3"
              />
              <h3 class="text-sm sm:text-base font-semibold mb-1.5">{{ selectedViz?.title }}</h3>
              <p class="text-xs sm:text-sm text-gray-600 mb-4">{{ selectedViz?.description }}</p>
            </div>

            <!-- Sticky footer for buttons -->
            <div class="mt-5 flex-shrink-0">
              <div class="flex justify-center gap-3">
                <button
                  @click="showVizModal = false"
                  class="px-3 sm:px-4 py-1.5 sm:py-2 text-xs sm:text-sm rounded-lg border border-gray-300 hover:bg-gray-50"
                >
                  Отменить
                </button>
                <button
                  @click="confirmVizSelection"
                  class="px-3 sm:px-4 py-1.5 sm:py-2 text-xs sm:text-sm rounded-lg border border-gray-600 bg-gray-600 text-white hover:bg-gray-700"
                >
                  Выбрать
                </button>
              </div>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>

    <!-- InfoPopup Modal -->
    <InfoPopup
      ref="infoPopupRef"
      title="Как понять, сколько по времени отслеживать сеанс?"
      text="Выберите период, который вам кажется подходящим для достижения вашей цели."
      @close="infoPopupRef?.hide()"
    />

    <!-- Title InfoPopup Modal -->
    <InfoPopup
      ref="titleInfoPopupRef"
      title="Как понять, как назвать сеанс?"
      text="Название должно отражать то, что вы хотите отслеживать. Например: часы сна, количество свиданий, частота посещения магазинов и т.д."
      @close="titleInfoPopupRef?.hide()"
    />

    <!-- SessionDatabase Modal -->
    <Teleport to="body">
      <Transition enter-active-class="transition duration-300" enter-from-class="opacity-0" enter-to-class="opacity-100" leave-active-class="transition duration-300" leave-from-class="opacity-100" leave-to-class="opacity-0">
        <div 
          v-if="showDatabaseModal" 
          @click="closeDatabaseModal"
          @wheel.prevent
          @scroll.prevent
          @touchmove.prevent
          class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-2 sm:p-4 z-[9999]"
        >
          <div 
            @click.stop
            @wheel.stop
            @scroll.stop
            @touchmove.stop
            class="bg-white rounded-lg p-4 sm:p-6 w-full max-w-sm sm:max-w-lg max-h-[80vh] flex flex-col overflow-hidden"
          >
            <h3 class="text-sm sm:text-base font-semibold mb-4 text-center flex-shrink-0">{{ getSessionTitle(currentDatabaseTableName) }}</h3>
            <div class="flex-1 overflow-y-auto">
              <SessionDatabase 
                v-if="currentDatabaseTableName" 
                :tableName="currentDatabaseTableName"
                @data-updated="handleDatabaseUpdate"
              />
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>
  
<script setup>
import { ref, reactive, onMounted, computed, watch } from 'vue'
import { useFetch, declineWord } from '../composables/utils.js';
import InfoPopup from './InfoPopup.vue'
import SessionContactsDisplay from './SessionContactsDisplay.vue'
import SessionActivityHeatmapDisplay from './SessionActivityHeatmapDisplay.vue'
import SessionCalendarDisplay from './SessionCalendarDisplay.vue'
import SessionBlogDisplay from './SessionBlogDisplay.vue'
import SessionDatabase from './SessionDatabase.vue'
import Tooltip from './Tooltip.vue'

const apiBaseUrl = import.meta.env.VITE_APP_API_BASE_URL;

const props = defineProps({
  userId: {
    type: String,
    required: true
  }
})

// State
const activeSessions = ref([])
const inactiveSessions = ref([])
const loading = ref(true)
const error = ref(null)
const showAddModal = ref(false)
const showEditModal = ref(false)
const showDeleteModal = ref(false)
const showSoftDeleteModal = ref(false)
const editableSession = ref({
  id: null,
  title: '',
  end_time: null,
  data_collection_methods: ['manual'],
  visualization_preferences: []
})
const deleteTargetId = ref(null)

const newSession = ref({
  title: '',
  end_time: null,
  data_collection_methods: ['manual'],
  visualization_preferences: []
})
const showInactive = ref(false)
const sortedActiveSessions = computed(() => {
  return [...activeSessions.value].sort((a, b) => a.time_remaining - b.time_remaining)
})
const sortedInactiveSessions = computed(() => {
  return [...inactiveSessions.value].sort((a, b) => new Date(b.updated_at) - new Date(a.updated_at))
})

// Add these to your existing script setup
const customYears = ref(0)
const customMonths = ref(0)
const customWeeks = ref(0)
const customDays = ref(0)
const showDurationPicker = ref(false)

const durationPresets = [
  { label: '1 неделю', days: 7 },
  { label: '1 месяц', days: 30 },
  { label: '3 месяца', days: 90 },
  { label: '6 месяцев', days: 180 },
  { label: '1 год', days: 365 },
]

const formatDuration = (dateString) => {
  if (!dateString) return '';
  
  const end = new Date(dateString);
  const now = new Date();
  const diffTime = end - now;
  let diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24)); // Округляем вверх
  
  if (diffDays <= 0) return '0 дней';

  // Константы для конвертации (фиксированные значения)
  const YEARS = 365;
  const MONTHS = 30;
  const WEEKS = 7;

  // Разбиваем дни на составные части
  const years = Math.floor(diffDays / YEARS);
  diffDays %= YEARS;
  
  const months = Math.floor(diffDays / MONTHS);
  diffDays %= MONTHS;
  
  const weeks = Math.floor(diffDays / WEEKS);
  const days = diffDays % WEEKS;

  // Формируем части строки
  const parts = [];
  if (years > 0) parts.push(`${years} ${declineWord(years, ['год', 'года', 'лет'])}`);
  if (months > 0) parts.push(`${months} ${declineWord(months, ['месяц', 'месяца', 'месяцев'])}`);
  if (weeks > 0) parts.push(`${weeks} ${declineWord(weeks, ['неделя', 'недели', 'недель'])}`);
  if (days > 0) parts.push(`${days} ${declineWord(days, ['день', 'дня', 'дней'])}`);

  return parts.join(', ') || '0 дней';
};

const formatDurationRemaining = (seconds) => {
  if (!seconds || seconds <= 0) return '0 дней';
  
  // Фиксированные интервалы (в секундах)
  const YEAR_SEC = 365 * 24 * 60 * 60;  // 365 дней
  const MONTH_SEC = 30 * 24 * 60 * 60;  // 30 дней
  const WEEK_SEC = 7 * 24 * 60 * 60;    // 7 дней
  const DAY_SEC = 24 * 60 * 60;
  const HOUR_SEC = 60 * 60;
  const MINUTE_SEC = 60;

  // Рассчитываем все единицы времени
  const years = Math.floor(seconds / YEAR_SEC);
  seconds %= YEAR_SEC;
  
  const months = Math.floor(seconds / MONTH_SEC);
  seconds %= MONTH_SEC;
  
  const weeks = Math.floor(seconds / WEEK_SEC);
  seconds %= WEEK_SEC;
  
  const days = Math.floor(seconds / DAY_SEC);
  seconds %= DAY_SEC;
  
  const hours = Math.floor(seconds / HOUR_SEC);
  seconds %= HOUR_SEC;
  
  const minutes = Math.floor(seconds / MINUTE_SEC);

  // Формируем результат в зависимости от старшей единицы
  const parts = [];
  
  if (years > 0) {
    parts.push(`${years} ${declineWord(years, ['год', 'года', 'лет'])}`);
    if (months > 0) parts.push(`${months} ${declineWord(months, ['месяц', 'месяца', 'месяцев'])}`);
    if (weeks > 0) parts.push(`${weeks} ${declineWord(weeks, ['неделя', 'недели', 'недель'])}`);
    if (days > 0) parts.push(`${days} ${declineWord(days, ['день', 'дня', 'дней'])}`);
  } 
  else if (months > 0) {
    parts.push(`${months} ${declineWord(months, ['месяц', 'месяца', 'месяцев'])}`);
    if (weeks > 0) parts.push(`${weeks} ${declineWord(weeks, ['неделя', 'недели', 'недель'])}`);
    if (days > 0) parts.push(`${days} ${declineWord(days, ['день', 'дня', 'дней'])}`);
  } 
  else if (weeks > 0) {
    parts.push(`${weeks} ${declineWord(weeks, ['неделя', 'недели', 'недель'])}`);
    if (days > 0) parts.push(`${days} ${declineWord(days, ['день', 'дня', 'дней'])}`);
  } 
  else if (days > 0) {
    parts.push(`${days} ${declineWord(days, ['день', 'дня', 'дней'])}`);
    if (hours > 0) parts.push(`${hours} ${declineWord(hours, ['час', 'часа', 'часов'])}`);
  } 
  else if (hours > 0) {
    parts.push(`${hours} ${declineWord(hours, ['час', 'часа', 'часов'])}`);
    if (minutes > 0) parts.push(`${minutes} ${declineWord(minutes, ['минута', 'минуты', 'минут'])}`);
  } 
  else {
    parts.push(`${minutes} ${declineWord(minutes, ['минута', 'минуты', 'минут'])}`);
  }

  return parts.join(', ') || '0 дней';
};

// UI Handlers
const openEditModal = (session) => {
  if (!session) return
  editableSession.value = { 
    id: session.id,
    title: session.title || '',
    end_time: session.end_time ? new Date(session.end_time).toISOString().slice(0, 16) : '',
    data_collection_methods: [...(session.data_collection_methods || [])],
    visualization_preferences: [...(session.visualization_preferences || [])]
  }
  showEditModal.value = true
}

const openDeleteModal = (session) => {
  deleteTargetId.value = session.id
  showDeleteModal.value = true
}

const openSoftDeleteModal = (session) => {
  deleteTargetId.value = session.id
  showSoftDeleteModal.value = true
}

const saveSession = async () => {
  await updateSession(editableSession.value.id, {
    title: editableSession.value.title,
    end_time: editableSession.value.end_time,
    data_collection_methods: editableSession.value.data_collection_methods,
    visualization_preferences: editableSession.value.visualization_preferences
  })    
  showEditModal.value = false
}

const addSession = async () => {
  try {
    await createSession({
      title: newSession.value.title,
      end_time: newSession.value.end_time,
      data_collection_methods: newSession.value.data_collection_methods,
      visualization_preferences: newSession.value.visualization_preferences
    })
    showAddModal.value = false
    // Reset form
    newSession.value = {
      title: '',
      end_time: null,
      data_collection_methods: ['manual'],
      visualization_preferences: []
    }
  } catch (err) {
    error.value = err.message || 'Не удалось создать сеанс'
    throw err
  }
}

// Session operations with proper endpoint alignment
const fetchSessions = async (activeOnly = true) => {
  try {
    loading.value = true
    const url = new URL(`${apiBaseUrl}/api/users/sessions/get`)
    url.searchParams.set('active_only', activeOnly)
    
    const { data, error: fetchError, fetchData } = useFetch(
      url.toString(),
      { credentials: 'include' }
    )
    await fetchData()

    if (fetchError.value) throw fetchError.value
    if (activeOnly) {
        activeSessions.value = data.value || []
      } else {
        inactiveSessions.value = data.value || []
      }
    return data.value
  } catch (err) {
    error.value = err.message || 'Не удалось получить сеансы'
    throw err
  } finally {
    loading.value = false
  }
}

// Modify the createVizTable function to create a single table
const createVizTable = async (sessionId) => {
  try {
    const tableName = `session_${sessionId}_data`
    const { error: fetchError, fetchData } = useFetch(
      `${apiBaseUrl}/api/users/table/`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: { 
          table_name: tableName,
          schema: {
            id: 'INTEGER PRIMARY KEY AUTOINCREMENT',
            value: 'TEXT',
            date: 'TEXT',
            time: 'TEXT'
          }
        },
        credentials: 'include'
      }
    )

    await fetchData()

    if (fetchError.value) {
      console.error('Error creating session data table:', fetchError.value)
      throw new Error(fetchError.value || 'Failed to create session data table')
    }
  } catch (err) {
    console.error('Error creating session data table:', err)
    throw err
  }
}

// TODO: add user_id to the table name
const deleteVizTable = async (sessionId) => {
  try {
    const tableName = `session_${sessionId}_data` 
    const { data, error: fetchError, fetchData: deleteTable } = useFetch(
      `${apiBaseUrl}/api/users/table/${tableName}/`,
      {
        method: 'DELETE',
        credentials: 'include'
      }
    )

    await deleteTable()

    if (fetchError.value) {
      console.error('Error deleting session data table:', fetchError.value)
      // Don't throw error here, just log it
      // This way session deletion can continue even if table deletion fails
    }
  } catch (err) {
    console.error('Error deleting session data table:', err)
    // Don't throw error here, just log it
    // This way session deletion can continue even if table deletion fails
  }
}

// Modify the createSession function to create only one table
const createSession = async (sessionData) => {
  try {
    const { data, error: fetchError, fetchData } = useFetch(
      `${apiBaseUrl}/api/users/sessions/create`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: sessionData,
        credentials: 'include'
      }
    )
    await fetchData()

    if (fetchError.value) throw fetchError.value

    const newSession = data.value
    activeSessions.value.push(newSession)

    // Create a single table for all visualizations
    if (newSession.visualization_preferences.length > 0) {
      await createVizTable(newSession.id)
    }

    return newSession
  } catch (err) {
    error.value = err.message || 'Failed to create session'
    throw err
  }
}

// Modify the updateSession function to create table only if it doesn't exist
const updateSession = async (sessionId, updateData) => {
  try {
    // Get the current session to compare visualizations
    const currentSession = activeSessions.value.find(s => s.id === sessionId) || 
                         inactiveSessions.value.find(s => s.id === sessionId)
    
    const { data, error: fetchError, fetchData } = useFetch(
      `${apiBaseUrl}/api/users/sessions/${sessionId}/edit`,
      {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: updateData,
        credentials: 'include'
      }
    )
    await fetchData()

    if (fetchError.value) throw fetchError.value

    const updatedSession = data.value
    
    // Check if the session has ended
    const now = new Date()
    const endTime = new Date(updatedSession.end_time)
    if (endTime <= now) {
      // If session has ended, soft delete it
      deleteTargetId.value = sessionId
      await softDeleteSession(sessionId)
      return
    }

    // Create table if it's a new session with visualizations
    if (currentSession && 
        updatedSession.visualization_preferences.length > 0 && 
        !currentSession.visualization_preferences.length) {
      await createVizTable(sessionId)
    }

    // Update only the specific session in the appropriate list
    const isActive = updatedSession.is_active && !updatedSession.is_paused
    if (isActive) {
      const index = activeSessions.value.findIndex(s => s.id === sessionId)
      if (index > -1) {
        activeSessions.value[index] = updatedSession
      }
    } else {
      const index = inactiveSessions.value.findIndex(s => s.id === sessionId)
      if (index > -1) {
        inactiveSessions.value[index] = updatedSession
      }
    }
    return updatedSession
  } catch (err) {
    error.value = err.message || 'Failed to update session'
    throw err
  }
}

// Update the deleteSession function to handle table deletion errors
const deleteSession = async () => {
  try {
    // First delete the session's data table
    try {
      await deleteVizTable(deleteTargetId.value)
    } catch (err) {
      console.error('Error deleting session data table:', err)
      // Continue with session deletion even if table deletion fails
    }

    // Then delete the session
    const { error: fetchError, fetchData } = useFetch(
      `${apiBaseUrl}/api/users/sessions/${deleteTargetId.value}/delete`,
      { 
        method: 'DELETE',
        credentials: 'include' 
      }
    )
    await fetchData()

    if (fetchError.value) throw fetchError.value
    
    // Refresh both lists and close modal
    await Promise.all([
      fetchSessions(true),
      showInactive.value == true && fetchSessions(false)
    ])
    showDeleteModal.value = false
    deleteTargetId.value = null
  } catch (err) {
    error.value = err.message || 'Не удалось удаление сеанса'
    throw err
  }
}

// Update the softDeleteSession function to handle table deletion errors
const softDeleteSession = async (sessionId) => {
  if (!sessionId) {
    error.value = 'Не удалось перенести сеанс в неактивные: отсутствует ID сеанса'
    return
  }

  try {
    const { error: fetchError, fetchData } = useFetch(
      `${apiBaseUrl}/api/users/sessions/${sessionId}/soft_delete`,
      { 
        method: 'DELETE',
        credentials: 'include' 
      }
    )
    await fetchData()

    if (fetchError.value) throw fetchError.value
    
    // Show inactive sessions
    showInactive.value = true
    
    // Refresh both lists and close modal
    await Promise.all([
      fetchSessions(true),
      fetchSessions(false)
    ])
    showSoftDeleteModal.value = false
    deleteTargetId.value = null
  } catch (err) {
    error.value = err.message || 'Не удалось перенести сеанс в неактивные'
  }
}

const pauseSession = async (sessionId, isPaused) => {
  try {    
    const { data, error: fetchError, fetchData } = useFetch(
      `${apiBaseUrl}/api/users/sessions/${sessionId}/pause`,
      {
        method: 'PATCH',
        headers: { 
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: { is_paused: isPaused },
        credentials: 'include'
      }
    )
    
    await fetchData()

    if (fetchError.value) throw fetchError.value

    // Show inactive sessions if we're pausing
    if (isPaused) {
      showInactive.value = true
    }

    // Refresh both active and inactive lists
    await Promise.all([
      fetchSessions(true),  // Refresh active sessions
      fetchSessions(false)  // Always refresh inactive sessions
    ])

  } catch (err) {
    error.value = err.message || 'Не удалось обновить статус паузы'
    throw err
  }
}

const restoreSession = async (sessionId) => {
  try {
    const { data, error: fetchError, fetchData } = useFetch(
      `${apiBaseUrl}/api/users/sessions/${sessionId}/restore`,
      {
        method: 'PATCH',
        credentials: 'include'
      }
    )
    await fetchData()

    if (fetchError.value) throw fetchError.value

    // Hide inactive sessions when restoring
    showInactive.value = false

    await Promise.all([
      fetchSessions(true),
      fetchSessions(false)
    ])
  } catch (err) {
    error.value = err.message || 'Не удалось восстановить сеанс'
    throw err
  }
}

// Initial load
onMounted(async () => {
  await fetchSessions()
})

const visualizations = [
  {
    id: 1,
    title: 'График дня',
    description: 'Заносите данные и отслеживайте, сколько времени они занимают',
    image: new URL('../assets/viz3.png', import.meta.url).href
  },
  {
    id: 2,
    title: 'Частота',
    description: 'Заносите данные и отслеживайте, какие из них самые активные',
    image: new URL('../assets/viz2.png', import.meta.url).href
  },
  {
    id: 3,
    title: 'График года',
    description: 'Заносите данные и отслеживайте, как часто они происходят в течение года',
    image: new URL('../assets/viz1.png', import.meta.url).href
  }
]

const showVizModal = ref(false)
const selectedViz = ref(null)
const tempSelectedViz = ref(null)

const openVizModal = (viz, event) => {
  event.preventDefault()
  event.stopPropagation()
  selectedViz.value = viz
  tempSelectedViz.value = viz
  showVizModal.value = true
}

const selectViz = (viz) => {
  const vizId = viz.id.toString()
  const index = newSession.value.visualization_preferences.indexOf(vizId)
  if (index === -1) {
    newSession.value.visualization_preferences.push(vizId)
  } else {
    newSession.value.visualization_preferences.splice(index, 1)
  }
}

const confirmVizSelection = () => {
  if (tempSelectedViz.value) {
    newSession.value.visualization_preferences = [tempSelectedViz.value.id.toString()]
  }
  showVizModal.value = false
  tempSelectedViz.value = null
}

// Update the showDurationHelp function to use InfoPopup
const infoPopupRef = ref(null)

const showDurationHelp = () => {
  infoPopupRef.value?.show()
}

const showHelp = ref(false)
const currentHelpContent = ref(null)

const closeHelp = () => {
  showHelp.value = false
  currentHelpContent.value = null
}

const applyCustomDuration = () => {
  const date = new Date();
  
  // Добавляем фиксированные интервалы (в днях)
  let totalDays = 0;
  
  if (customYears.value) {
    totalDays += Number(customYears.value) * 365; // 1 год = 365 дней
  }
  
  if (customMonths.value) {
    totalDays += Number(customMonths.value) * 30; // 1 месяц = 30 дней
  }
  
  if (customWeeks.value) {
    totalDays += Number(customWeeks.value) * 7; // 1 неделя = 7 дней
  }
  
  if (customDays.value) {
    totalDays += Number(customDays.value);
  }
  
  // Устанавливаем новую дату
  date.setDate(date.getDate() + totalDays);
  
  // Обновляем end_time (как в оригинале)
  if (showEditModal.value) {
    editableSession.value.end_time = date.toISOString().slice(0, 16);
  } else {
    newSession.value.end_time = date.toISOString().slice(0, 16);
  }
  
  // Сброс значений
  customYears.value = 0;
  customMonths.value = 0;
  customWeeks.value = 0;
  customDays.value = 0;
  showDurationPicker.value = false;
}

const applyPresetDuration = (preset) => {
  const date = new Date()
  date.setDate(date.getDate() + preset.days)
  
  if (showEditModal.value) {
    editableSession.value.end_time = date.toISOString().slice(0, 16)
  } else {
    newSession.value.end_time = date.toISOString().slice(0, 16)
  }
}

// Add this function for edit modal
const selectVizForEdit = (viz) => {
  const vizId = viz.id.toString()
  const index = editableSession.value.visualization_preferences.indexOf(vizId)
  if (index === -1) {
    editableSession.value.visualization_preferences.push(vizId)
  } else {
    editableSession.value.visualization_preferences.splice(index, 1)
  }
}

const getVisualizationComponent = (type) => {
  switch (type) {
    case '1': // activity heatmap
      return SessionActivityHeatmapDisplay
    case '2': // contacts
      return SessionContactsDisplay
    case '3': // calendar
      return SessionCalendarDisplay
    case '4': // blog
      return SessionBlogDisplay
    default:
      return null
  }
}

// Add state for managing which viz's data modal is open
const showDatabaseModal = ref(false)
const currentDatabaseTableName = ref('')

const openDatabaseModal = (sessionId) => {
  currentDatabaseTableName.value = `session_${sessionId}_data`
  showDatabaseModal.value = true
}
const closeDatabaseModal = async () => {
  const tableName = currentDatabaseTableName.value;
  showDatabaseModal.value = false;
  currentDatabaseTableName.value = '';
};

const handleDatabaseUpdate = (updatedSession) => {
  if (!updatedSession) return;
  
  // Update the session in the array using splice, exactly like in updateSession
  const isActive = updatedSession.is_active && !updatedSession.is_paused;
  if (isActive) {
    const index = activeSessions.value.findIndex(s => s.id === updatedSession.id);
    if (index > -1) {
      activeSessions.value.splice(index, 1, updatedSession);
    }
  } else {
    const index = inactiveSessions.value.findIndex(s => s.id === updatedSession.id);
    if (index > -1) {
      inactiveSessions.value.splice(index, 1, updatedSession);
    }
  }
};

// Helper to get display name for a viz id
const getVizDisplayName = (vizId) => {
  const found = visualizations.find(v => v.id.toString() === vizId)
  return found ? found.title : vizId
}

const expandedSessionId = ref(null)

// Add these functions to the script section
const getSessionTitle = (tableName) => {
  if (!tableName) return '';
  const sessionId = parseInt(tableName.split('_')[1], 10);
  const session = activeSessions.value.find(s => s.id === sessionId) || 
                 inactiveSessions.value.find(s => s.id === sessionId);
  return session ? session.title : '';
};

const emit = defineEmits(['update:show-add-modal', 'update:active-sessions'])

// Watch for changes in showAddModal and activeSessions to emit updates
watch(showAddModal, (newValue) => {
  emit('update:show-add-modal', newValue)
})

watch(activeSessions, (newValue) => {
  emit('update:active-sessions', newValue)
}, { deep: true })

const titleInfoPopupRef = ref(null)

const showTitleHelp = () => {
  titleInfoPopupRef.value?.show()
}

</script>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>