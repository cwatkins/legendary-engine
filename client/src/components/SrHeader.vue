<script setup>
import { defineEmits, defineProps } from "vue";

const props = defineProps({
  checkoutOpen: Boolean,
});

const emit = defineEmits(["openCart"]);
</script>
<template>
  <div class="max-h-full min-w-screen max-w-screen bg-color-neutral-50">
    <div
      class="grid grid-cols-7 text-center text-sky-600 font-bold text-base min-w-full border-b"
    >
      <div class="col-start-2 col-span-2">
        <span>Terminal Demo</span>
      </div>
      <button class="col-start-5 col-span-2" @click="emit('openCart')">
        <div>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-5 w-5 mx-auto my-auto"
            :class="{ 'text-neutral-800': checkoutOpen }"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            stroke-width="2"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z"
            />
          </svg>
        </div>
      </button>
    </div>
  </div>
</template>
