<script setup>
const props = defineProps({
  modalTitle: {
    type: String,
    default: null,
  },
  modalText: {
    type: String,
    default: null,
  },
});

const emit = defineEmits(["closeModal"]);
</script>
<template>
  <transition
    enter-from-class="transform opacity-80"
    enter-active-class="delay-100 duration-100 ease-out"
    leave-to-class="transform opacity-80"
    leave-from-class="opacity-100"
    leave-active-class="delay-100"
  >
    <div
      v-if="modalText && modalTitle"
      class="bg-black/40 z-10 fade fixed top-0 left-0 w-full h-full outline-none overflow-x-hidden overflow-y-auto"
      tabindex="-1"
    >
      <div class="relative flex h-screen w-auto pointer-events-none">
        <div
          v-if="modalText && modalTitle"
          class="z-20 shadow-lg h-5/6 flex flex-col w-3/5 pointer-events-auto bg-neutral-50 mx-auto my-auto rounded-md px-2 rounded-md"
        >
          <div class="flex flex-shrink-0 items-center justify-between p-4">
            <h5 class="text-xl font-medium leading-normal text-gray-800">
              {{ modalTitle }}
            </h5>
            <button type="button" @click="emit('closeModal')">X</button>
          </div>
          <div
            class="flex flex-wrap break-words relative mx-2 p-4 bg-neutral-200 mx-2 overflow-y-auto rounded-md"
          >
            <pre>{{ modalText }}</pre>
          </div>
          <div
            class="flex flex-shrink-0 flex-wrap items-center justify-end p-4 space-x-2"
          ></div>
        </div>
      </div>
    </div>
  </transition>
</template>
