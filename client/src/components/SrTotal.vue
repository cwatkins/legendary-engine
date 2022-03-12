<script setup>
import { formatter } from "../helpers";
const props = defineProps({
  total: {
    type: Number,
    required: true,
    default: 0,
  },
});
</script>

<template>
  <hr />
  <div class="flex flex-row justify-between">
    <span class="text-xl">Total</span>
    <span>{{ formatter.format(total / 100) }}</span>
  </div>
</template>
