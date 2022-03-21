<script setup>
import { formatter } from "../helpers";

const props = defineProps({
  cart: {
    type: Array,
    required: true,
    default() {
      return [];
    },
  },
});
</script>
<template>
  <div class="h-1/2 overflow-y-auto">
    <transition-group
      enter-from-class="transform opacity-0"
      enter-active-class="duration-100 ease-out"
    >
      <div
        v-for="(item, index) in cart"
        :key="index"
        class="flex flex-row justify-between mt-2 text-xs text-slate-800 font-medium"
      >
        <div class="flex flex-row w-full">
          <div>
            <button
              class="bg-sky-600 text-slate-50 px-1 rounded-sm hover:brightness-125 hover:scale-105 drop-shadow"
              @click="item.quantity++"
            >
              +
            </button>
            <input :value="item.quantity" class="w-6 text-center" />
            <button
              class="bg-sky-600 text-slate-50 px-1 rounded-sm hover:brightness-125 hover:scale-105 drop-shadow"
              @click="item.quantity--"
            >
              -
            </button>
          </div>
          <span class="ml-2 text-left">Issue {{ item.id }}</span>
        </div>
        <div>{{ formatter.format((item.price / 100) * item.quantity) }}</div>
        <button
          class="ml-2 hover:brightness-200 hover:scale-110"
          @click="item.quantity = 0"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-5 w-5"
            viewBox="0 0 20 20"
            fill="currentColor"
          >
            <path
              fill-rule="evenodd"
              d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z"
              clip-rule="evenodd"
            />
          </svg>
        </button>
      </div>
    </transition-group>
  </div>
</template>
