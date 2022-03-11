<script setup>
import { toRefs } from "vue";

import MenuItem from "./MenuItem.vue";

const props = defineProps({
  products: {
    type: Array,
    required: true,
    default() {
      return [];
    },
  },
});

const emit = defineEmits(["addToCart"]);

const { products } = toRefs(props);
</script>

<template>
  <section class="grid grid-cols-2 gap-1 mr-2 overflow-y-auto h-screen w-1/2">
    <menu-item
      v-for="product in products"
      :key="product.name"
      :name="product.name"
      :price="product.price"
      :image="product.image"
      class="border"
      @click="emit('addToCart', product)"
    />
  </section>
</template>
