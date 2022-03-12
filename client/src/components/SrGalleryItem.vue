<script setup>
import { defineProps } from "vue";
import { formatter } from "../helpers";

const props = defineProps({
  name: {
    type: String,
    required: true,
    default: null,
  },
  price: {
    type: Number,
    required: true,
    default: null,
  },
  image: {
    type: String,
    required: true,
    default: null,
  },
});
</script>
<template>
  <button>
    <div
      class="flex flex-col hover:brightness-105 transition hover:scale-100 scale-95 duration-100"
    >
      <h3 class="font-bold text-slate-700">{{ props.name }}</h3>
      <img :src="props.image" alt="Item title" class="m-1 rounded-lg" />
      <div class="flex flex-col justify-between">
        <p class="">{{ formatter.format(props.price / 100) }}</p>
      </div>
    </div>
  </button>
</template>
