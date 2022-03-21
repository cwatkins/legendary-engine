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
  <div class="flex flex-row justify-between text-sm font-semibold">
    <span>Total</span>
    <span>{{ formatter.format(total / 100) }}</span>
  </div>
</template>
