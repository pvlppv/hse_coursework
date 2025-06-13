<template>
    <div class="container mx-auto flex justify-center relative">
        <VOnboardingWrapper ref="wrapper" :steps="steps">
          <template #default="{ previous, next, step, exit, isFirst, isLast, index }">
            <VOnboardingStep>
              <div class="bg-white rounded-lg shadow-lg">
                <div class="p-4 sm:p-6">
                  <div class="absolute top-2 sm:top-4 right-2 sm:right-4">
                    <button 
                      v-if="isFirst"
                      @click="customFinishTour" 
                      class="p-1.5 rounded-lg hover:bg-gray-100 transition-colors"
                    >
                      <span class="text-xs sm:text-sm">Завершить</span>
                    </button>
                    <button
                      v-else
                      v-tippy="{ 
                        content: 'Перезагрузить',
                        trigger: 'mouseenter',
                        hideOnClick: true
                      }"
                      @click="restartOnboarding"
                      type="button"
                      class="p-1.5 sm:p-2 rounded-lg hover:bg-gray-100 transition-colors"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-gray-600" viewBox="0 0 24 24"><path d="m13 7.101.01.001a4.978 4.978 0 0 1 2.526 1.362 5.005 5.005 0 0 1 1.363 2.528 5.061 5.061 0 0 1-.001 2.016 4.976 4.976 0 0 1-1.363 2.527l1.414 1.414a7.014 7.014 0 0 0 1.908-3.54 6.98 6.98 0 0 0 0-2.819 6.957 6.957 0 0 0-1.907-3.539 6.97 6.97 0 0 0-2.223-1.5 6.921 6.921 0 0 0-1.315-.408c-.137-.028-.275-.043-.412-.063V2L9 6l4 4V7.101zm-7.45 7.623c.174.412.392.812.646 1.19.249.37.537.718.854 1.034a7.036 7.036 0 0 0 2.224 1.501c.425.18.868.317 1.315.408.167.034.338.056.508.078v2.944l4-4-4-4v3.03c-.035-.006-.072-.003-.107-.011a4.978 4.978 0 0 1-2.526-1.362 4.994 4.994 0 0 1 .001-7.071L7.051 7.05a7.01 7.01 0 0 0-1.5 2.224A6.974 6.974 0 0 0 5 12a6.997 6.997 0 0 0 .55 2.724z" fill="currentColor"></path></svg>
                    </button>
                  </div>

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
                        <!-- <template v-if="!isFirst">
                          <button 
                            @click="previous" 
                            type="button" 
                            class="inline-flex items-center justify-center rounded-lg border border-gray-300 px-3 py-1.5 text-xs sm:text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
                          >
                            Назад
                          </button>
                        </template> -->
                        <button 
                          @click="handleNextOrFinish(isLast, next)"
                          type="button" 
                          class="inline-flex items-center justify-center rounded-lg border border-transparent bg-gray-100 px-3 py-1.5 text-xs sm:text-sm font-medium text-gray-700 hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
                          :disabled="isNextManuallyDisabled"
                        >
                          {{ isLast ? 'Завершить' : 'Дальше' }}
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </VOnboardingStep>
          </template>
        </VOnboardingWrapper>

        <div id="profile" class="max-w-lg space-y-3 sm:space-y-4 text-center">
            <div class="w-28 h-28 sm:w-32 sm:h-32 rounded-full mx-auto bg-gray-100 flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="w-16 h-16 sm:w-20 sm:h-20 text-gray-400" viewBox="0 0 24 24">
                    <path d="M7.5 6.5C7.5 8.981 9.519 11 12 11s4.5-2.019 4.5-4.5S14.481 2 12 2 7.5 4.019 7.5 6.5zM20 21h1v-1c0-3.859-3.141-7-7-7h-4c-3.86 0-7 3.141-7 7v1h17z"></path>
                </svg>
            </div>
            <h1 class="text-lg sm:text-xl font-semibold">{{ email ? email.split('@')[0] : '' }}</h1>
        </div>

        <!-- Settings Icon -->
        <div class="absolute top-2 right-2 sm:top-4 sm:right-4">
          <button 
            v-tippy="'Настройки'"
            @click="showSettings = true"
            class="p-1.5 sm:p-2 hover:bg-gray-100 rounded-full transition-colors"
          >
              <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 sm:w-6 sm:h-6 text-gray-600" viewBox="0 0 24 24">
                  <path d="M12 16c2.206 0 4-1.794 4-4s-1.794-4-4-4-4 1.794-4 4 1.794 4 4 4zm0-6c1.084 0 2 .916 2 2s-.916 2-2 2-2-.916-2-2 .916-2 2-2z"></path>
                  <path d="m2.845 16.136 1 1.73c.531.917 1.809 1.261 2.73.73l.529-.306A8.1 8.1 0 0 0 9 19.402V20c0 1.103.897 2 2 2h2c1.103 0 2-.897 2-2v-.598a8.132 8.132 0 0 0 1.896-1.111l.529.306c.923.53 2.198.188 2.731-.731l.999-1.729a2.001 2.001 0 0 0-.731-2.732l-.505-.292a7.718 7.718 0 0 0 0-2.224l.505-.292a2.002 2.002 0 0 0 .731-2.732l-.999-1.729c-.531-.92-1.808-1.265-2.731-.732l-.529.306A8.1 8.1 0 0 0 15 4.598V4c0-1.103-.897-2-2-2h-2c-1.103 0-2 .897-2 2v.598a8.132 8.132 0 0 0-1.896 1.111l-.529-.306c-.924-.531-2.2-.187-2.731.732l-.999 1.729a2.001 2.001 0 0 0 .731 2.732l.505.292a7.683 7.683 0 0 0 0 2.223l-.505.292a2.003 2.003 0 0 0-.731 2.733zm3.326-2.758A5.703 5.703 0 0 1 6 12c0-.462.058-.926.17-1.378a.999.999 0 0 0-.47-1.108l-1.123-.65.998-1.729 1.145.662a.997.997 0 0 0 1.188-.142 6.071 6.071 0 0 1 2.384-1.399A1 1 0 0 0 11 5.3V4h2v1.3a1 1 0 0 0 .708.956 6.083 6.083 0 0 1 2.384 1.399.999.999 0 0 0 1.188.142l1.144-.661 1 1.729-1.124.649a1 1 0 0 0-.47 1.108c.112.452.17.916.17 1.378 0 .461-.058.925-.171 1.378a1 1 0 0 0 .471 1.108l1.123.649-.998 1.729-1.145-.661a.996.996 0 0 0-1.188.142 6.071 6.071 0 0 1-2.384 1.399A1 1 0 0 0 13 18.7l.002 1.3H11v-1.3a1 1 0 0 0-.708-.956 6.083 6.083 0 0 1-2.384-1.399.992.992 0 0 0-1.188-.141l-1.144.662-1-1.729 1.124-.651a1 1 0 0 0 .471-1.108z"></path>
              </svg>
          </button>
        </div>

        <!-- Settings Modal -->
        <SettingsModal
            :show="showSettings"
            @close="showSettings = false"
            @restart-onboarding="restartOnboarding"
        />
    </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { VOnboardingWrapper, VOnboardingStep, useVOnboarding } from 'v-onboarding';
import { directive as VTippy } from 'vue-tippy';
import SettingsModal from './SettingsModal.vue';
import { isOnboardingActive, canCloseModalOverride } from '../composables/onboarding.js';

const props = defineProps({
    email: String,
    activeSessions: Array,
});

defineEmits(['update:show-add-modal']);

const wrapper = ref(null);
const { start: originalStart, finish: originalFinish, goToStep } = useVOnboarding(wrapper);

const start = () => {
  isOnboardingActive.value = true;
  originalStart();
};

const finish = () => {
  isOnboardingActive.value = false;
  originalFinish();
};

const isNextManuallyDisabled = ref(false);
let titleInputHandler = null;
let durationInputHandler = null;
let goalObserverButton = null;
let goalExperimentButton = null;
let visualizationCards = [];
let startSessionButton = null;
let dbButton = null;
let addFirstRecordButton = null;
let addRecordButton = null;

const addRecordHandler = () => {
    isNextManuallyDisabled.value = false;
    goToStep(19);
}

const addFirstRecordHandler = () => {
    goToStep(18);
}

const dbButtonHandler = () => {
    goToStep(17);
};

const startSessionHandler = () => {
    isNextManuallyDisabled.value = false;
    setTimeout(() => {
        goToStep(11);
    }, 1000);
};

const visualizationSelectionHandler = () => {
  // Use a timeout to wait for Vue to apply the class changes
  setTimeout(() => {
    const selectedViz = document.querySelector('#new-session-visualization-preferences-input .border-gray-600');
    if (selectedViz) {
      isNextManuallyDisabled.value = false;
    } else {
      isNextManuallyDisabled.value = true;
    }
  }, 100);
};

// Обработчик глобального события выбора визуализации
const handleVisualizationSelected = () => {
  setTimeout(() => {
    isNextManuallyDisabled.value = false;
  }, 100);
};

const goalChoiceHandler = () => {
    isNextManuallyDisabled.value = false;
    // Use a timeout to allow Vue to re-render the DOM first
    setTimeout(() => {
        // The current step index is 5
        goToStep(5);
    }, 150); // A bit longer to be safe
};
  
const handleFinish = () => {
  localStorage.setItem('onboarding_completed', 'true');
  finish();
};

const showSettings = ref(false);

const customFinishTour = () => {
  handleFinish();
};

const restartOnboarding = () => {
    finish();
    start();
    showSettings.value = false;
};

const handleNextOrFinish = (isLast, nextFn) => {
  if (isLast) {
    handleFinish();
  } else {
    nextFn();
  }
};

onMounted(() => {
  const onboardingCompleted = localStorage.getItem('onboarding_completed');
  if (onboardingCompleted !== 'true') {
    start();
  }
});

const scrollStepIntoView = (step) => {
  return new Promise(resolve => {
    if (!step.attachTo?.element) {
      resolve();
      return;
    }

    // Add a small delay to ensure the modal and its elements are fully rendered.
    setTimeout(() => {
      const targetElement = document.querySelector(step.attachTo.element);
      if (!targetElement) {
        resolve();
        return;
      }

      // The scrollable container within your modal
      const addSessionScrollContainer = document.querySelector('#session-add-modal-scroll-container');
      const dbModal = document.querySelector('#session-database-modal');
      
      let scrollContainer = null;

      if (addSessionScrollContainer && addSessionScrollContainer.contains(targetElement)) {
        scrollContainer = addSessionScrollContainer;
      } else if (dbModal && dbModal.contains(targetElement)) {
        scrollContainer = dbModal.querySelector('.ag-body-viewport') || dbModal;
      }

      // Check if the target is inside the modal's scrollable container
      if (scrollContainer && scrollContainer.contains(targetElement)) {
        const containerRect = scrollContainer.getBoundingClientRect();
        const elementRect = targetElement.getBoundingClientRect();

        // Check if the element is not fully visible within the container
        if (elementRect.top < containerRect.top || elementRect.bottom > containerRect.bottom) {
          
          // Calculate the ideal scroll position to center the element
          const elementTopRelativeToContainer = elementRect.top - containerRect.top;
          const desiredScrollTop = scrollContainer.scrollTop + elementTopRelativeToContainer - (containerRect.height / 2) + (elementRect.height / 2);

          // Perform the scroll with smooth behavior
          scrollContainer.scrollTo({
            top: desiredScrollTop,
            behavior: 'smooth'
          });
        }
      } else {
        // Fallback for elements outside the modal
        targetElement.scrollIntoView({ 
          behavior: 'smooth',
          block: 'center', 
          inline: 'center' 
        });
      }
      // Allow a moment for the repaint after scrolling
      setTimeout(resolve, 300);
    }, 100);
  });
};

const steps = [
  {
    attachTo: { element: '#profile' },
    content: { 
      title: "Про инструмент", 
      description: "Цель инструмента - сделать процесс повышения осознанности нагляднее и удобнее. Давай посмотрим, как это работает:" 
    },
    options: { overlay: { preventOverlayInteraction: true, padding: 20, borderRadius: 10 } }
  },
  {
    attachTo: { element: '#sessions-list' },
    content: { 
      title: "Лента сеансов", 
      description: "Сама суть повышения осознанности лежит в отслеживании наблюдений по некоторым жизненным событиям, а после в формулировании выводов по ним и их осознании. Всё это здесь укомплектовано в концепт сеансов: у них чётко поставлена цель, и чётко выделено время на её достижение. Вот здесь как раз будут храниться твои сеансы:" 
    },
    options: { overlay: { preventOverlayInteraction: true, padding: 20, borderRadius: 10 } }
  },
  {
    attachTo: { element: '#add-session-button' },
    content: { 
      title: "Создание сеанса", 
      description: 'Чтобы создать первый сеанс, нажми на кнопку "Начать новый сеанс"' 
    },
    options: { overlay: { preventOverlayInteraction: false, padding: 20, borderRadius: 10 } },
    on: {
      beforeStep: () => {
        isNextManuallyDisabled.value = true;
        const button = document.querySelector('#add-session-button');
        if (!button) return;
        
        const actionHandler = () => {
          button.removeEventListener('click', actionHandler);
          setTimeout(() => {
            goToStep(3);
          }, 500);
        };
        button.addEventListener('click', actionHandler);
      }
    }
  },
  {
    attachTo: { element: '#new-session-title-input' },
    content: { 
      title: "Название сеанса", 
      description: "Напиши, что бы ты хотел отслеживать в этом сеансе. Название сеанса может отображать, например, тему события/ий, наблюдения по которому/ым ты хочешь отследить, или вопрос из жизни, на который хочешь ответить, в целом всё, что угодно твоей потребности или воображению" 
    },
    options: { overlay: { preventOverlayInteraction: false, padding: 20, borderRadius: 10 } },
    on: {
      beforeStep: () => {
        isNextManuallyDisabled.value = true;
        const input = document.querySelector('#new-session-title-input input');
        if (!input) return;

        titleInputHandler = () => {
          if (input.value.trim() !== '') {
            isNextManuallyDisabled.value = false;
          } else {
            isNextManuallyDisabled.value = true;
          }
        };
        input.addEventListener('input', titleInputHandler);
      },
      afterStep: () => {
        const input = document.querySelector('#new-session-title-input input');
        if (input && titleInputHandler) {
          input.removeEventListener('input', titleInputHandler);
        }
        isNextManuallyDisabled.value = false;
        titleInputHandler = null;
      }
    }
  },
  {
    attachTo: { element: '#new-session-duration-input' },
    content: { 
      title: "Продолжительность сеанса", 
      description: "Выбери, сколько по времени ты бы хотел вести этот сеанс. Продолжительность сеанса можно задать, например, такой, которой тебе, кажется, хватит для достижения цели отслеживания" 
    },
    options: { overlay: { preventOverlayInteraction: false, padding: 20, borderRadius: 10 }, scrollToStep: { enabled: false } },
    on: {
      beforeStep: async () => {
        await scrollStepIntoView(steps[4]);
        isNextManuallyDisabled.value = true;
        const input = document.querySelector('#new-session-duration-input-input');
        if (!input) return;

        // Use MutationObserver to watch for value changes on the readonly input
        durationInputHandler = new MutationObserver(() => {
          if (input.value.trim() !== '') {
            isNextManuallyDisabled.value = false;
          } else {
            isNextManuallyDisabled.value = true;
          }
        });

        durationInputHandler.observe(input, {
          attributes: true,
          attributeFilter: ['value']
        });
      },
      afterStep: () => {
        if (durationInputHandler) {
          durationInputHandler.disconnect();
        }
        isNextManuallyDisabled.value = false;
        durationInputHandler = null;
      }
    }
  },
  {
    attachTo: { element: '#new-session-goal-input' },
    content: {
      title: "Цель сеанса",
      description: "Выбери, с какой целью ты бы хотел вести этот сеанс. Цель отслеживания исходит из вашего желания либо просто понаблюдать и понять, что происходит, либо провести эксперимент и проверить свою гипотезу о том, что происходит"
    },
    options: { overlay: { preventOverlayInteraction: false, padding: 20, borderRadius: 10 }, scrollToStep: { enabled: false } },
    on: {
      beforeStep: async () => {
        isNextManuallyDisabled.value = true;
        await scrollStepIntoView(steps[5]);

        setTimeout(() => {
            goalObserverButton = document.querySelector('#new-session-observe-button');
            goalExperimentButton = document.querySelector('#new-session-experiment-button');

            if (goalObserverButton && goalExperimentButton) {
                goalObserverButton.addEventListener('click', goalChoiceHandler);
                goalExperimentButton.addEventListener('click', goalChoiceHandler);
            } else {
                // If buttons aren't found, don't block the user.
                isNextManuallyDisabled.value = false;
            }
        }, 150);
      },
      afterStep: () => {
          goalObserverButton?.removeEventListener('click', goalChoiceHandler);
          goalExperimentButton?.removeEventListener('click', goalChoiceHandler);
          isNextManuallyDisabled.value = false; // Always re-enable on leaving step
          goalObserverButton = null;
          goalExperimentButton = null;
      }
    }
  },
  {
    attachTo: { element: '#new-session-experiment-metric-input' },
    content: {
        title: "Параметры эксперимента",
        description: 'Если ты выберешь цель "Провести эксперимент", то тут ты можешь выбрать метрику, по которой будет определяться успех эксперимента'
    },
    options: { overlay: { preventOverlayInteraction: false, padding: 20, borderRadius: 10 }, scrollToStep: { enabled: false } },
    on: { 
      beforeStep: async () => {
        await scrollStepIntoView(steps[6]);
      }
    }
  },
  {
     attachTo: { element: '#new-session-data-collection-methods-input' },
    content: { 
      title: "Сбор данных", 
      description: "Выбери, как бы ты хотел собирать данные для этого сеанса. Сбор данных или наблюдений является неотъемлемым шагом для отслеживания события/ий. Кстати скоро их можно будет собирать автоматически через внешние сервисы!" 
    },
    options: { overlay: { preventOverlayInteraction: false, padding: 20, borderRadius: 10 }, scrollToStep: { enabled: false } },
    on: { 
      beforeStep: async () => {
        await scrollStepIntoView(steps[7]);
      }
    }
  },
  {
     attachTo: { element: '#new-session-visualization-preferences-input' },
    content: { 
      title: "Визуализация данных", 
      description: "Выбери, как бы ты хотел визуализировать собранные данные. Визуализации помогают взглянуть на наблюдения с разных сторон. Кстати список визуализаций постепенно пополняется!" 
    },
    options: { overlay: { preventOverlayInteraction: false, padding: 20, borderRadius: 10 }, scrollToStep: { enabled: false } },
    on: { 
      beforeStep: async () => {
        isNextManuallyDisabled.value = true;
        document.body.classList.add('onboarding-modal-scrollable');
        await scrollStepIntoView(steps[8]);

        window.addEventListener('visualization-selected', handleVisualizationSelected);

        setTimeout(() => {
            visualizationCards = document.querySelectorAll('#new-session-visualization-preferences-input .group');
            visualizationCards.forEach(card => card.addEventListener('click', visualizationSelectionHandler));
        }, 150);
      },
      afterStep: () => {
        visualizationCards.forEach(card => card.removeEventListener('click', visualizationSelectionHandler));
        window.removeEventListener('visualization-selected', handleVisualizationSelected);
        document.body.classList.remove('onboarding-modal-scrollable');
        isNextManuallyDisabled.value = false;
        visualizationCards = [];
      }
    }
  },
  {
     attachTo: { element: '#new-session-analysis-methods-input' },
    content: { 
      title: "Анализ данных", 
      description: "Эти данные можно будет даже проанализировать, но это будет уже в следующих обновлениях" 
    },
    options: { overlay: { preventOverlayInteraction: false, padding: 20, borderRadius: 10 }, scrollToStep: { enabled: false } },
    on: { 
      beforeStep: async () => {
        await scrollStepIntoView(steps[9]);
      }
    }
  },
  {
    attachTo: { element: '#new-session-submit-button' },
    content: { 
      title: "Завершение создания сеанса", 
      description: 'Отлично, теперь нажимай кнопку "Начать" и посмотри, как выглядит твой первый сеанс' 
    },
    options: { overlay: { preventOverlayInteraction: false, padding: 20, borderRadius: 10 }, scrollToStep: { enabled: false } },
    on: { 
      beforeStep: async () => {
        isNextManuallyDisabled.value = true;
        await scrollStepIntoView(steps[10]);

        setTimeout(() => {
          startSessionButton = document.querySelector('#new-session-submit-button button[type="submit"]');
          if (startSessionButton) {
            startSessionButton.addEventListener('click', startSessionHandler);
          } else {
            isNextManuallyDisabled.value = false;
          }
        }, 150)
      },
      afterStep: () => {
        if(startSessionButton) {
          startSessionButton.removeEventListener('click', startSessionHandler)
        }
        isNextManuallyDisabled.value = false;
        startSessionButton = null;
      }
    }
  },
  {
    attachTo: { element: '#session-card-inner' },
    content: {
      title: "Карточка сеанса",
      description: "Эта карточка - твой сеанс"
    },
    options: { overlay: { preventOverlayInteraction: true, padding: 20, borderRadius: 10 } },
    on: {
      beforeStep: async () => {
        await new Promise(resolve => {
          const checkElement = () => {
            const element = document.querySelector('#session-card-inner');
            if (element) {
              resolve();
            } else {
              setTimeout(checkElement, 100);
            }
          };
          checkElement();
        });
        await scrollStepIntoView(steps[11]);
      }
    }
  },
  {
    attachTo: { element: '#active-sessions-list-container > .group:first-child #session-card-goal' },
    content: {
      title: "Цель сеанса",
      description: "Тут ты можешь вспоминать о своей цели сеанса"
    },
    options: { overlay: { preventOverlayInteraction: true, padding: 20, borderRadius: 10 } }
  },
  {
    attachTo: { element: '#active-sessions-list-container > .group:first-child #session-card-time-remaining' },
    content: {
      title: "Время до завершения сеанса",
      description: "Тут ты можешь смотреть, сколько времени осталось до завершения сеанса (его можно продливать/сокращать)"
    },
    options: { overlay: { preventOverlayInteraction: true, padding: 20, borderRadius: 10 } }
  },
  {
    attachTo: { element: '#active-sessions-list-container > .group:first-child #session-card-controls' },
    content: {
      title: "Редактирование сеанса",
      description: "Тут ты можешь ставить сеанс на паузу, редактировать его или вовсе скрывать"
    },
    options: { overlay: { preventOverlayInteraction: true, padding: 20, borderRadius: 10 } }
  },
  {
    attachTo: { element: '#active-sessions-list-container > .group:first-child #session-card-visualization-area' },
    content: {
      title: "Визуализация данных",
      description: "А тут ты можешь смотреть визуализации по собираемым данным"
    },
    options: { overlay: { preventOverlayInteraction: true, padding: 20, borderRadius: 10 } }
  },
  {
    attachTo: { element: '#active-sessions-list-container > .group:first-child #session-card-database-button' },
    content: {
      title: "База данных сеанса",
      description: 'Тут ты можешь добавить/изменить/удалить данные, собираемые для этого сеанса. Нажми "Добавить данные", чтобы продолжить'
    },
    options: { overlay: { preventOverlayInteraction: false, padding: 20, borderRadius: 10 } },
    on: {
        beforeStep: () => {
            isNextManuallyDisabled.value = true;
            setTimeout(() => {
                dbButton = document.querySelector('#active-sessions-list-container > .group:first-child #session-card-database-button');
                if (dbButton) {
                    dbButton.addEventListener('click', dbButtonHandler);
                } else {
                    isNextManuallyDisabled.value = false;
                }
            }, 150);
        },
        afterStep: () => {
            if (dbButton) {
                dbButton.removeEventListener('click', dbButtonHandler);
            }
            dbButton = null;
            isNextManuallyDisabled.value = false;
        }
    }
  },
  {
      attachTo: { element: '#add-first-db-record-button-container' },
      content: {
          title: "Создание записи",
          description: 'Создай свою первую запись, нажми на кнопку "+"'
      },
      options: { overlay: { preventOverlayInteraction: false, padding: 20, borderRadius: 10 } },
      on: {
          beforeStep: () => {
            isNextManuallyDisabled.value = true;
            setTimeout(() => {
                addFirstRecordButton = document.querySelector('#add-first-db-record-button');
                if (addFirstRecordButton) {
                    addFirstRecordButton.addEventListener('click', addFirstRecordHandler);
                } else {
                    isNextManuallyDisabled.value = false;
                }
            }, 150);
          },
          afterStep: () => {
              if (addFirstRecordButton) {
                  addFirstRecordButton.removeEventListener('click', addFirstRecordHandler);
              }
              addFirstRecordButton = null;
              isNextManuallyDisabled.value = false;
          }
      }
  },
  {
       attachTo: { element: '#add-db-record-modal' },
      content: {
          title: "Добавление записи",
          description: 'Введи сюда значение для своей первой записи, это может быть слово, цифра, комбинация, что угодно твоему воображению, а после нажми "Добавить"'
      },
      options: { overlay: { preventOverlayInteraction: false, padding: 20, borderRadius: 10 } },
      on: {
        beforeStep: () => {
            isNextManuallyDisabled.value = true;
            setTimeout(() => {
                addRecordButton = document.querySelector('#add-db-record-submit-button');
                if (addRecordButton) {
                    addRecordButton.addEventListener('click', addRecordHandler);
                } else {
                    isNextManuallyDisabled.value = false;
                }
            }, 150)
        },
        afterStep: () => {
            if (addRecordButton) {
                addRecordButton.removeEventListener('click', addRecordHandler);
            }
            addRecordButton = null;
            isNextManuallyDisabled.value = false;
        }
      }
  },
  {
     attachTo: { element: '#session-database-grid .ag-row:first-child' },
    content: {
        title: "Изменение и удаление записей",
        description: 'Отлично! Чтобы изменить значение, нажми дважды на ячейку с ним, а чтобы его удалить, просто нажми на его строку и на кнопку "x" ниже'
    },
    options: { overlay: { preventOverlayInteraction: false, padding: 20, borderRadius: 10 } },
    on: {
        beforeStep: async () => {
            await new Promise(resolve => {
              const checkElement = () => {
                const element = document.querySelector('#session-database-grid .ag-row:first-child');
                if (element) {
                  resolve();
                } else {
                  setTimeout(checkElement, 100);
                }
              };
              checkElement();
            });
            await scrollStepIntoView(steps[20]);
        }
    }
  },
  {
    attachTo: { element: '#session-database-grid' },
    content: {
        title: "Переход обратно",
        description: "Теперь ты можешь вернуться обратно к сеансу, закрыв это окно, нажав сбоку/сверху/снизу"
    },
    options: { overlay: { preventOverlayInteraction: false, padding: 20, borderRadius: 10 } },
    on: {
        beforeStep: () => {
            isNextManuallyDisabled.value = true;
            canCloseModalOverride.value = true;
            
            const observer = new MutationObserver((mutationsList, observerInstance) => {
                for(const mutation of mutationsList) {
                    if (mutation.removedNodes) {
                        for (const node of mutation.removedNodes) {
                            if (node.id === 'session-database-modal') {
                                goToStep(21);
                                observerInstance.disconnect();
                                return;
                            }
                        }
                    }
                }
            });

            observer.observe(document.body, { childList: true });
        },
        afterStep: () => {
            canCloseModalOverride.value = false;
            isNextManuallyDisabled.value = false;
        }
    }
  },
  {
    attachTo: { element: '#active-sessions-list-container > .group:first-child' },
    content: {
        title: "Конец",
        description: "На этом всё! Теперь ты знаешь, из чего состоит процесс отслеживания наблюдения по событиям и последующего повышения осознанности. Как видишь, он достаточно гибкий и может подстроиться под любые потребности. Продолжи настраивать и вести сеансы. Помни, вся жизнь в твоих руках, приятного использования!"
    },
    options: { overlay: { preventOverlayInteraction: true, padding: 20, borderRadius: 10 } }
  }
];
</script>

<style>
:root {
  --v-onboarding-overlay-z: 10000;
  --v-onboarding-step-z: 10001;
}

body.onboarding-active {
  overflow: hidden;
}

body.onboarding-active #session-add-modal-scroll-container {
  overflow-y: hidden;
}

body.onboarding-active.onboarding-modal-scrollable #session-add-modal-scroll-container {
  overflow-y: auto;
}

.v-onboarding-step .bg-white {
  max-width: 350px;
}

@media (max-width: 640px) {
  .v-onboarding-step .bg-white {
    max-width: 90vw;
  }
}
</style> 