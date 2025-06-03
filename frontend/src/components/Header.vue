<template>
    <div class="container mx-auto flex justify-center relative">
        <VOnboardingWrapper ref="wrapper" :steps="steps">
          <template #default="{ previous, next, step, exit, isFirst, isLast, index }">
            <VOnboardingStep>
              <div class="bg-white rounded-lg shadow-lg">
                <div class="p-4 sm:p-6">
                  <!-- Close button in top right corner -->
                  <button 
                    @click="customFinishTour" 
                    class="absolute top-2 right-2 p-1.5 rounded-lg hover:bg-gray-100 transition-colors"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-gray-600" viewBox="0 0 24 24">
                      <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
                    </svg>
                  </button>

                  <!-- Content -->
                  <div class="flex flex-col">
                    <div v-if="step.content" class="mb-4">
                      <h3 v-if="step.content.title" class="text-sm sm:text-base font-semibold text-black">{{ step.content.title }}</h3>
                      <div v-if="step.content.description" class="mt-2 text-xs sm:text-sm text-gray-500">
                        <p>{{ step.content.description }}</p>
                      </div>
                    </div>
                    <div class="flex justify-between items-end">
                      <span class="text-gray-600 font-medium text-xs">{{ `${index + 1}/${steps.length}` }}</span>
                      <div class="flex gap-2">
                        <template v-if="!isFirst">
                          <button 
                            @click="previous" 
                            type="button" 
                            class="inline-flex items-center justify-center rounded-lg border border-gray-300 px-3 py-1.5 text-xs sm:text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
                          >
                            Назад
                          </button>
                        </template>
                        <button 
                          @click="next" 
                          type="button" 
                          class="inline-flex items-center rounded-lg border border-transparent bg-[#f3f4f6] px-3 py-1.5 text-xs sm:text-sm font-medium text-gray-700 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
                        >
                          {{ isLast ? 'Закончить' : 'Вперед' }}
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </VOnboardingStep>
          </template>
        </VOnboardingWrapper>

        <div class="max-w-lg space-y-3 sm:space-y-4 text-center">
            <div class="w-28 h-28 sm:w-32 sm:h-32 rounded-full mx-auto bg-gray-100 flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="w-16 h-16 sm:w-20 sm:h-20 text-gray-400" viewBox="0 0 24 24">
                    <path d="M7.5 6.5C7.5 8.981 9.519 11 12 11s4.5-2.019 4.5-4.5S14.481 2 12 2 7.5 4.019 7.5 6.5zM20 21h1v-1c0-3.859-3.141-7-7-7h-4c-3.86 0-7 3.141-7 7v1h17z"></path>
                </svg>
            </div>
            <h1 class="text-lg sm:text-xl font-semibold">{{ email.split('@')[0] }}</h1>
        </div>

        <!-- Settings Icon -->
        <div class="absolute top-2 right-2 sm:top-4 sm:right-4">
          <Tooltip text="Настройки">
            <button 
                @click="showSettings = true"
                class="p-1.5 sm:p-2 hover:bg-gray-100 rounded-full transition-colors"
            >
                <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 sm:w-6 sm:h-6 text-gray-600" viewBox="0 0 24 24">
                    <path d="M12 16c2.206 0 4-1.794 4-4s-1.794-4-4-4-4 1.794-4 4 1.794 4 4 4zm0-6c1.084 0 2 .916 2 2s-.916 2-2 2-2-.916-2-2 .916-2 2-2z"></path>
                    <path d="m2.845 16.136 1 1.73c.531.917 1.809 1.261 2.73.73l.529-.306A8.1 8.1 0 0 0 9 19.402V20c0 1.103.897 2 2 2h2c1.103 0 2-.897 2-2v-.598a8.132 8.132 0 0 0 1.896-1.111l.529.306c.923.53 2.198.188 2.731-.731l.999-1.729a2.001 2.001 0 0 0-.731-2.732l-.505-.292a7.718 7.718 0 0 0 0-2.224l.505-.292a2.002 2.002 0 0 0 .731-2.732l-.999-1.729c-.531-.92-1.808-1.265-2.731-.732l-.529.306A8.1 8.1 0 0 0 15 4.598V4c0-1.103-.897-2-2-2h-2c-1.103 0-2 .897-2 2v.598a8.132 8.132 0 0 0-1.896 1.111l-.529-.306c-.924-.531-2.2-.187-2.731.732l-.999 1.729a2.001 2.001 0 0 0 .731 2.732l.505.292a7.683 7.683 0 0 0 0 2.223l-.505.292a2.003 2.003 0 0 0-.731 2.733zm3.326-2.758A5.703 5.703 0 0 1 6 12c0-.462.058-.926.17-1.378a.999.999 0 0 0-.47-1.108l-1.123-.65.998-1.729 1.145.662a.997.997 0 0 0 1.188-.142 6.071 6.071 0 0 1 2.384-1.399A1 1 0 0 0 11 5.3V4h2v1.3a1 1 0 0 0 .708.956 6.083 6.083 0 0 1 2.384 1.399.999.999 0 0 0 1.188.142l1.144-.661 1 1.729-1.124.649a1 1 0 0 0-.47 1.108c.112.452.17.916.17 1.378 0 .461-.058.925-.171 1.378a1 1 0 0 0 .471 1.108l1.123.649-.998 1.729-1.145-.661a.996.996 0 0 0-1.188.142 6.071 6.071 0 0 1-2.384 1.399A1 1 0 0 0 13 18.7l.002 1.3H11v-1.3a1 1 0 0 0-.708-.956 6.083 6.083 0 0 1-2.384-1.399.992.992 0 0 0-1.188-.141l-1.144.662-1-1.729 1.124-.651a1 1 0 0 0 .471-1.108z"></path>
                </svg>
            </button>
          </Tooltip>
        </div>

        <!-- Settings Modal -->
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
                    v-if="showSettings" 
                    @click="showSettings = false"
                    class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-[9999]"
                >
                    <div 
                        @click.stop
                        class="bg-white rounded-lg p-6 w-full max-w-md"
                    >
                        <!-- Header -->
                        <div class="flex items-center justify-between mb-6">
                            <div class="flex items-center gap-3">
                                <h2 class="text-xl font-semibold text-black">Настройки</h2>
                            </div>
                            <button 
                                @click="showSettings = false"
                                class="p-2 hover:bg-gray-100 rounded-full transition-colors"
                            >
                                <svg class="w-5 h-5 text-gray-600" viewBox="0 0 24 24">
                                    <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
                                </svg>
                            </button>
                        </div>

                        <!-- Content -->
                        <div class="space-y-4">
                            <button
                                @click="restartOnboarding"
                                class="w-full flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50 transition-colors"
                            >
                                <div class="flex items-center gap-3">
                                    <svg class="w-5 h-5 text-gray-600" viewBox="0 0 24 24">
                                        <path d="M12 2C6.486 2 2 6.486 2 12s4.486 10 10 10 10-4.486 10-10S17.514 2 12 2zm0 18c-4.411 0-8-3.589-8-8s3.589-8 8-8 8 3.589 8 8-3.589 8-8 8z"/>
                                        <path d="M13 7h-2v5.414l3.293 3.293 1.414-1.414L13 11.586z"/>
                                    </svg>
                                    <span class="text-gray-700">Начать обучение заново</span>
                                </div>
                                <svg class="w-5 h-5 text-gray-400" viewBox="0 0 24 24">
                                    <path d="M8.59 16.59L13.17 12 8.59 7.41 10 6l6 6-6 6-1.41-1.41z"/>
                                </svg>
                            </button>
                        </div>
                    </div>
                </div>
            </Transition>
        </Teleport>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { VOnboardingWrapper, VOnboardingStep, useVOnboarding } from 'v-onboarding';
import Tooltip from './Tooltip.vue';

const props = defineProps({
    email: String,
    activeSessions: Array,
});

const emit = defineEmits(['update:show-add-modal']);

const wrapper = ref(null);
const { start, goToStep, finish: originalFinish, next, activeStepIndex } = useVOnboarding(wrapper);

const showSettings = ref(false);

const modalCloseDetectorInterval = ref(null);

const stopModalCloseDetection = () => {
  if (modalCloseDetectorInterval.value) {
    clearInterval(modalCloseDetectorInterval.value);
    modalCloseDetectorInterval.value = null;
  }
};

const customFinishTour = () => {
  stopModalCloseDetection();
  originalFinish();
};

const restartOnboarding = () => {
    customFinishTour();
    start();
    showSettings.value = false;
};

const startModalCloseDetection = () => {
  stopModalCloseDetection(); 
  modalCloseDetectorInterval.value = setInterval(() => {
    if (activeStepIndex?.value !== undefined && isInModalFlowSteps(activeStepIndex.value) && !isModalDomVisible()) {
      stopModalCloseDetection();
      goToStep(2);
    }
  }, 250);
};

const isModalDomVisible = () => {
  const modal = document.querySelector('#add-session-modal');
  return modal && window.getComputedStyle(modal).display !== 'none';
};

const closeModal = () => {
  emit('update:show-add-modal', false);
};

const openModal = () => {
  emit('update:show-add-modal', true);
};

const isInModalFlowSteps = (stepIndex) => {
  return stepIndex >= 3 && stepIndex <= 8;
};

const waitForCondition = (conditionFn, timeout = 5000, errorMessage = 'VOnboarding: Timeout waiting for condition.') => {
  return new Promise((resolve, reject) => {
    if (conditionFn()) {
      resolve();
      return;
    }
    const startTime = Date.now();
    const interval = setInterval(() => {
      if (conditionFn()) {
        clearInterval(interval);
        resolve();
      } else if (Date.now() - startTime > timeout) {
        clearInterval(interval);
        console.warn(errorMessage);
        reject(new Error(errorMessage.replace('VOnboarding: ', '')));
      }
    }, 100);
  });
};

const waitForAddModalOpenAndReady = async () => {
  return waitForCondition(
    () => isModalDomVisible() && document.querySelector('#new-session-title-input'),
    5000,
    'VOnboarding: Timed out waiting for add modal to open and be ready. Please click "Начать новый сеанс".'
  );
};

const waitForAddModalCloseAndSessionCreated = async () => {
  return waitForCondition(
    () => !isModalDomVisible() && document.querySelector('#active-sessions-list-container > .group:first-child'),
    10000, 
    'VOnboarding: Timed out waiting for session creation and modal close. Please complete creating the session.'
  );
};

const ensureFirstSessionCardExists = async () => {
  return waitForCondition(
    () => document.querySelector('#active-sessions-list-container > .group:first-child') !== null,
    5000,
    'VOnboarding: First session card not found.'
  );
};

const ensureFirstSessionCardVizArea = async () => {
  return waitForCondition(
    () => {
      const cardEl = document.querySelector('#active-sessions-list-container > .group:first-child');
      if (!cardEl) return false;
      const vizAreaEl = cardEl.querySelector(':scope > div.mt-4 > div.space-y-4');
      return vizAreaEl && vizAreaEl.children.length > 0;
    },
    7000,
    'VOnboarding: Session card visualization area not found or empty. Please ensure you selected a visualization.'
  );
};

const handleOpenModalAndProceed = () => {
  openModal();
  requestAnimationFrame(() => {
    if (isModalDomVisible()) {
      next();
    }
  });
};

async function modalStepBeforeLogic(elementSelector, stepNameForLog) {
  if (!isModalDomVisible()) {
    goToStep(2); 
    return false; 
  }
  try {
    await waitForCondition(() => document.querySelector(elementSelector), 2000, `VOnboarding: Element ${elementSelector} for step '${stepNameForLog}' not found.`);
    return true; 
  } catch (error) {
    console.warn(error.message); 
    goToStep(2); 
    return false; 
  }
}

const commonModalStepOptions = { 
  overlay: { preventOverlayInteraction: false, padding: 20, borderRadius: 10 }
};

const commonModalAfterStepLogic = ({ isBackward }) => {
  return true;
};

const steps = [
  {
    attachTo: { element: '#profile' },
    content: { 
      title: "Что такое Соти?", 
      description: "Соти - это призыв повышать осознанность. Это приложение создано, чтобы сделать этот процесс нагляднее и удобнее. Вот из чего оно состоит:" 
    },
    options: { overlay: { padding: 20, borderRadius: 10 } }
  },
  {
    attachTo: { element: '#sessions-list' },
    content: { 
      title: "Лента сеансов", 
      description: "Повышение осознанности сопровождается отслеживанием тех или иных событий в жизни, эти отслеживания фиксируются сеансами, здесь они будут храниться." 
    },
    options: { overlay: { padding: 20, borderRadius: 10 } }
  },
  {
    attachTo: { element: '#add-session-button' },
    content: { 
      title: "Создание сеанса", 
      description: 'Чтобы создать первый сеанс, нажми на кнопку "Начать новый сеанс".' 
    },
    options: { 
      overlay: { 
        preventOverlayInteraction: false, 
        padding: 20, 
        borderRadius: 10 
      }
    },
    on: {
      beforeStep: () => {
        if (isModalDomVisible()) {
          closeModal();
        }
        const button = document.querySelector('#add-session-button');
        if (button) {
          button.removeEventListener('click', handleOpenModalAndProceed);
          button.addEventListener('click', handleOpenModalAndProceed, { once: true });
        }
      },
      afterStep: ({ isForward }) => {
        if (isForward && !isModalDomVisible()) {
          return false;
        }
        return true;
      }
    }
  },
  {
    attachTo: { element: '#new-session-title-input' },
    content: { 
      title: "Название сеанса", 
      description: "Напиши, что бы ты хотел отслеживать в этом сеансе. Например: часы сна, количество свиданий, частота посещения магазинов и т.п." 
    },
    options: { 
      overlay: { 
        preventOverlayInteraction: false, 
        padding: 20, 
        borderRadius: 10 
      }
    },
    on: {
      beforeStep: () => {
        if (!isModalDomVisible()) {
          goToStep(2);
          return false;
        }
        return true;
      },
      afterStep: ({ isBackward }) => {
        if (isBackward) {
          closeModal();
        }
      }
    }
  },
  {
    attachTo: { element: '#new-session-duration-input' },
    content: { 
      title: "Продолжительность сеанса", 
      description: "Выбери, сколько по времени ты бы хотел вести сеанс." 
    },
    options: { 
      overlay: { 
        preventOverlayInteraction: false, 
        padding: 20, 
        borderRadius: 10 
      }
    },
    on: {
      beforeStep: () => {
        if (!isModalDomVisible()) {
          goToStep(2);
          return false;
        }
        return true;
      }
    }
  },
  {
    attachTo: { element: '#new-session-data-collection-methods-input' },
    content: { 
      title: "Сбор данных", 
      description: "Выбери, как бы ты хотел собирать данные для этого сеанса. Обрати внимание, что в будущих обновлениях их можно будет собирать автоматически через внешние сервисы." 
    },
    options: { 
      overlay: { 
        preventOverlayInteraction: false, 
        padding: 20, 
        borderRadius: 10 
      }
    },
    on: {
      beforeStep: () => {
        if (!isModalDomVisible()) {
          goToStep(2);
          return false;
        }
        return true;
      }
    }
  },
  {
    attachTo: { element: '#new-session-visualization-preferences-input' },
    content: { 
      title: "Визуализация данных", 
      description: "Выбери, как бы ты хотел визуализировать собранные данные. Учти, что визуализаций будет намного больше в следующих обновлениях." 
    },
    options: { 
      overlay: { 
        preventOverlayInteraction: false, 
        padding: 20, 
        borderRadius: 10 
      }
    },
    on: {
      beforeStep: () => {
        if (!isModalDomVisible()) {
          goToStep(2);
          return false;
        }
        return true;
      }
    }
  },
  {
    attachTo: { element: '#new-session-analysis-methods-input' },
    content: { 
      title: "Анализ данных", 
      description: "Эти данные можно будет даже проанализировать, но это будет уже в следующих обновлениях." 
    },
    options: { 
      overlay: { 
        preventOverlayInteraction: false, 
        padding: 20, 
        borderRadius: 10 
      }
    },
    on: {
      beforeStep: () => {
        if (!isModalDomVisible()) {
          goToStep(2);
          return false;
        }
        return true;
      }
    }
  },
  {
    attachTo: { element: '#new-session-submit-button' },
    content: { 
      title: "Завершение создания сеанса", 
      description: 'Отлично, теперь нажимай кнопку "Начать" и посмотри, как выглядит твой первый сеанс.' 
    },
    options: { 
      overlay: { 
        preventOverlayInteraction: false, 
        padding: 20, 
        borderRadius: 10 
      }
    },
    on: {
      beforeStep: () => {
        if (!isModalDomVisible()) {
          goToStep(2);
          return false;
        }
        return true;
      }
    }
  },
  {
    attachTo: { element: '#active-sessions-list-container > .group:first-child' },
    content: { 
      title: "Карточка сеанса", 
      description: "Эта карточка - твой сеанс." 
    },
    options: { overlay: { padding: 20, borderRadius: 10 } },
    on: {
      beforeStep: () => {
        if (isModalDomVisible()) {
          closeModal();
          return false;
        }
        return true;
      }
    }
  },
  {
    attachTo: { element: '#active-sessions-list-container > .group:first-child p.text-gray-500.mt-1' },
    content: { 
      title: "Время до завершения сеанса", 
      description: "Тут ты можешь смотреть, сколько времени осталось до завершения сеанса." 
    },
    options: { overlay: { padding: 20, borderRadius: 10 } },
    on: {
      beforeStep: () => {
        if (isModalDomVisible()) {
          closeModal();
          return false;
        }
        return true;
      }
    }
  },
  {
    attachTo: { element: '#active-sessions-list-container > .group:first-child .flex.gap-1' },
    content: { 
      title: "Редактирование сеанса", 
      description: "Тут ты можешь поставить сеанс на паузу, редактировать его или вовсе скрыть." 
    },
    options: { overlay: { padding: 20, borderRadius: 10 } },
    on: {
      beforeStep: () => {
        if (isModalDomVisible()) {
          closeModal();
          return false;
        }
        return true;
      }
    }
  },
  {
    attachTo: { element: '#active-sessions-list-container > .group:first-child button.border-dashed' },
    content: { 
      title: "База данных сеанса", 
      description: "Тут ты можешь добавить/изменить/удалить данные, собираемые для этого сеанса." 
    },
    options: { overlay: { padding: 20, borderRadius: 10 } },
    on: {
      beforeStep: () => {
        if (isModalDomVisible()) {
          closeModal();
          return false;
        }
        return true;
      }
    }
  },
  {
    attachTo: { element: '#active-sessions-list-container > .group:first-child > div.mt-4 > div.space-y-4' },
    content: { 
      title: "Визуализация данных", 
      description: "А тут ты можешь смотреть визуализации по своим собираемым данным, отслеживать их и повышать осознанность! Удачи!" 
    },
    options: { overlay: { padding: 20, borderRadius: 10 } },
    on: {
      beforeStep: () => {
        if (isModalDomVisible()) {
          closeModal();
          return false;
        }
        return true;
      }
    }
  }
];
</script>

<style>
:root {
  --v-onboarding-overlay-z: 10000; /* Above modal (9999) */
  --v-onboarding-step-z: 10001;   /* Above overlay and modal */
}
</style> 