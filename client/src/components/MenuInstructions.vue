<script setup>
const props = defineProps({
  isReady: Boolean,
  selectedReader: {
    type: Object,
    default() {
      return null;
    },
  },
  hasEmptyCart: Boolean,
});
</script>

<template>
  <div v-if="!isReady" class="mt-2">
    <p class="font-semibold">Demo Instructions</p>
    <p v-if="!selectedReader">
      Select a reader by clicking the link icon under "Readers".
    </p>
    <p v-if="!hasEmptyCart">Add at least one book to the cart.</p>
  </div>
</template>
