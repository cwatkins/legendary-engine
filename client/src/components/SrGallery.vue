<script setup>
import { onBeforeMount, ref } from "vue";
import { useCart } from "../composables/useCart";
import SrGalleryItem from "./SrGalleryItem.vue";

const products = ref([]);

onBeforeMount(async () => {
  products.value = await listProducts();
});

async function listProducts() {
  const response = await fetch("/api/list-products");
  const { product_list } = await response.json();
  return product_list;
}

const emit = defineEmits(["addToCart"]);
</script>

<template>
  <section class="grid grid-cols-2 gap-1 mr-2 overflow-y-auto h-screen w-1/2">
    <sr-gallery-item
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
