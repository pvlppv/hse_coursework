<template>
  <div class="relative inline-block">
    <div
      ref="triggerRef"
      @mouseenter="showTooltip = true"
      @mouseleave="showTooltip = false"
      @focus="showTooltip = true"
      @blur="showTooltip = false"
      class="inline-block"
    >
      <slot></slot>
    </div>
    
    <Teleport to="body">
      <Transition
        enter-active-class="transition duration-200"
        enter-from-class="opacity-0 scale-95"
        enter-to-class="opacity-100 scale-100"
        leave-active-class="transition duration-150"
        leave-from-class="opacity-100 scale-100"
        leave-to-class="opacity-0 scale-95"
      >
        <div
          v-if="showTooltip"
          ref="tooltipRef"
          :style="tooltipStyle"
          class="fixed z-[9999] px-2 py-1 text-xs sm:text-sm text-white bg-black rounded shadow-lg whitespace-nowrap"
          role="tooltip"
        >
          {{ text }}
          <div
            :class="[
              'absolute w-2 h-2 bg-black transform rotate-45',
              arrowClasses[position]
            ]"
          ></div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed, watch, nextTick } from 'vue'

const props = defineProps({
  text: {
    type: String,
    required: true
  },
  position: {
    type: String,
    default: 'top',
    validator: (value) => ['top', 'bottom', 'left', 'right'].includes(value)
  }
})

const showTooltip = ref(false)
const triggerRef = ref(null)
const tooltipRef = ref(null)

const updatePosition = () => {
  if (!triggerRef.value || !tooltipRef.value || !showTooltip.value) return

  const triggerRect = triggerRef.value.getBoundingClientRect()
  const tooltipRect = tooltipRef.value.getBoundingClientRect()
  
  let top = 0
  let left = 0

  // Add some padding from the viewport edges
  const viewportPadding = 8
  const tooltipPadding = 8
  const horizontalOffset = -4 // Consistent offset for all positions

  // Calculate the actual content width (excluding padding)
  const contentWidth = tooltipRect.width - 16 // 8px padding on each side

  switch (props.position) {
    case 'top':
      top = Math.max(viewportPadding, triggerRect.top - tooltipRect.height - tooltipPadding)
      left = Math.min(
        window.innerWidth - tooltipRect.width - viewportPadding,
        Math.max(viewportPadding, triggerRect.left + (triggerRect.width - contentWidth) / 2 + horizontalOffset)
      )
      break
    case 'bottom':
      top = Math.min(
        window.innerHeight - tooltipRect.height - viewportPadding,
        triggerRect.bottom + tooltipPadding
      )
      left = Math.min(
        window.innerWidth - tooltipRect.width - viewportPadding,
        Math.max(viewportPadding, triggerRect.left + (triggerRect.width - contentWidth) / 2 + horizontalOffset)
      )
      break
    case 'left':
      top = Math.min(
        window.innerHeight - tooltipRect.height - viewportPadding,
        Math.max(viewportPadding, triggerRect.top + (triggerRect.height - tooltipRect.height) / 2)
      )
      left = Math.max(viewportPadding, triggerRect.left - tooltipRect.width - tooltipPadding + horizontalOffset)
      break
    case 'right':
      top = Math.min(
        window.innerHeight - tooltipRect.height - viewportPadding,
        Math.max(viewportPadding, triggerRect.top + (triggerRect.height - tooltipRect.height) / 2)
      )
      left = Math.min(
        window.innerWidth - tooltipRect.width - viewportPadding,
        triggerRect.right + tooltipPadding + horizontalOffset
      )
      break
  }

  tooltipRef.value.style.top = `${top}px`
  tooltipRef.value.style.left = `${left}px`
}

// Watch for changes in showTooltip to update position immediately
watch(showTooltip, (newValue) => {
  if (newValue) {
    // Use nextTick to ensure the tooltip is rendered before calculating position
    nextTick(() => {
      updatePosition()
    })
  }
})

const tooltipStyle = computed(() => ({
  position: 'fixed',
  zIndex: 9999
}))

let resizeObserver = null

onMounted(() => {
  resizeObserver = new ResizeObserver(() => {
    if (showTooltip.value) {
      // Use requestAnimationFrame for smoother updates
      requestAnimationFrame(updatePosition)
    }
  })
  
  if (triggerRef.value) {
    resizeObserver.observe(triggerRef.value)
  }
  
  window.addEventListener('scroll', () => requestAnimationFrame(updatePosition), true)
  window.addEventListener('resize', () => requestAnimationFrame(updatePosition))
})

onUnmounted(() => {
  if (resizeObserver) {
    resizeObserver.disconnect()
  }
  window.removeEventListener('scroll', () => requestAnimationFrame(updatePosition), true)
  window.removeEventListener('resize', () => requestAnimationFrame(updatePosition))
})

const arrowClasses = {
  top: 'bottom-[-4px] left-1/2 -translate-x-1/2',
  bottom: 'top-[-4px] left-1/2 -translate-x-1/2',
  left: 'right-[-4px] top-1/2 -translate-y-1/2',
  right: 'left-[-4px] top-1/2 -translate-y-1/2'
}
</script> 