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
  <section
    class="grid grid-cols-2 gap-1 mr-2 overflow-y-auto h-screen w-1/2 pt-4 pl-1"
  >
    <transition-group
      enter-from-class="transform opacity-0"
      enter-active-class="delay-100 duration-200 ease-out"
      leave-to-class="transform opacity-0"
      leave-from-class="opacity-100"
      leave-active-class="duration-200 ease-in"
    >
      <sr-gallery-item
        v-for="product in products"
        :key="product.name"
        :name="product.name"
        :price="product.price"
        :image="product.image"
        class="border"
        @click="emit('addToCart', product)"
      />
    </transition-group>
  </section>
</template>
