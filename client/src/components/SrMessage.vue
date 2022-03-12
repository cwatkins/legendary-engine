<script setup>
const props = defineProps({
  modalTitle: {
    type: String,
    required: true,
    default: null,
  },
  modalText: {
    type: String,
    required: true,
    default: null,
  },
});

const emit = defineEmits(["closeModal"]);
</script>
<template>
  <transition
    enter-from-class="transform opacity-80"
    enter-active-class="duration-100 ease"
    leave-to-class="transform opacity-80"
    leave-from-class="opacity-100"
    leave-active-class="duration-100 ease"
  >
    <div
      v-if="modalText && modalTitle"
      class="bg-black/30 z-10 fade fixed top-0 left-0 w-full h-full outline-none overflow-x-hidden overflow-y-auto"
      tabindex="-1"
    >
      <div class="relative flex h-screen w-auto pointer-events-none">
        <div
          v-if="modalText && modalTitle"
          class="z-20 shadow-lg relative flex-col w-fit h-fit pointer-events-auto bg-neutral-50 mx-auto my-auto rounded-md"
        >
          <div class="flex flex-shrink-0 items-center justify-between p-4">
            <h5 class="text-xl font-medium leading-normal text-gray-800">
              {{ modalTitle }}
            </h5>
            <button type="button" @click="emit('closeModal')">X</button>
          </div>
          <div class="relative mx-2 p-4 bg-neutral-200">
            <pre>{{ modalText }}</pre>
          </div>
          <div
            class="flex flex-shrink-0 flex-wrap items-center justify-end p-4 space-x-2"
          >
            <button
              type="button"
              class="px-6 py-2.5 bg-rose-600 text-white font-medium text-xs rounded-md"
              @click="emit('closeModal')"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>
