<template>
  <button>
    <div class="flex flex-col">
      <h3 class="">{{ props.name }}</h3>
      <img :src="props.image" alt="Item title" class="m-1 rounded-lg" />
      <div class="flex flex-col justify-between">
        <p class="">{{ props.price }}</p>
      </div>
    </div>
  </button>
</template>
<script setup>
import { defineProps } from "vue";

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
