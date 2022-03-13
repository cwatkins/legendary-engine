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
    <div class="flex flex-col hover:brightness-105 transition duration-100">
      <h3 class="font-bold text-sky-800">{{ props.name }}</h3>
      <img :src="props.image" alt="Item title" class="m-1 rounded-lg" />
      <div class="flex flex-col justify-between">
        <p class="font-medium">{{ formatter.format(props.price / 100) }}</p>
      </div>
    </div>
  </button>
</template>
