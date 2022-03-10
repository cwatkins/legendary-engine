<script setup>
import { ref, onBeforeMount, watch } from "vue";
import { useReader } from "./composables/useReader";
import { useCart } from "./composables/useCart";
import { usePayment } from "./composables/usePayment";

import MenuItem from "./components/MenuItem.vue";
import MenuModalVue from "./components/MenuModal.vue";

const products = ref([]);
const readerState = ref(null);
const modalOpen = ref(false);

const {
  readers,
  selectedReader,
  processPaymentIntent,
  cancelTerminalAction,
  simulatePayment,
} = useReader();
const { cart, subTotal, addToCart, removeItem } = useCart();
const { paymentIntentId, createPaymentIntent } = usePayment();

onBeforeMount(async () => {
  try {
    products.value = await listProducts();
  } catch (error) {
    console.log(error);
  }
});

watch(readerState, (newState, oldState) => {
  if (newState === "succeeded" && oldState === "in_progress") {
    cart.value = [];
    paymentIntentId.value = null;
    readerState.value = null;
  }
});

async function listProducts() {
  const response = await fetch("/api/list-products");
  const { product_list } = await response.json();
  return product_list;
}

async function handlePayment() {
  if (!paymentIntentId.value) {
    paymentIntentId.value = await createPaymentIntent(subTotal.value);
  }

  // Process payment
  const { reader_state: processState } = await processPaymentIntent(
    paymentIntentId.value,
    selectedReader.value.id
  );
  readerState.value = processState.action.status;

  // Simulate result
  const { reader_state: simulateState } = await simulatePayment(
    selectedReader.value.id
  );
  readerState.value = simulateState.action.status;
}
</script>

<template>
  <menu-modal-vue v-if="modalOpen" />
  <div class="max-h-full min-w-screen max-w-screen">
    <header class="bg-black text-center text-slate-50 min-w-full">
      Increment Store
      <span v-if="selectedReader">
        ({{ selectedReader.id }}) {{ readerState }}
      </span>
      <button v-else @click="modalOpen = !modalOpen">
        <span>(Select reader)</span>
      </button>
    </header>
    <main class="flex flex-row">
      <section
        class="grid grid-cols-3 gap-1 mr-2 overflow-y-auto h-screen w-3/5"
      >
        <menu-item
          v-for="product in products"
          :key="product.name"
          :name="product.name"
          :price="product.price"
          :image="product.image"
          class="border"
          @click="addToCart(product)"
        />
      </section>
      <section class="flex flex-col w-2/5 mr-2">
        <div class="h-4/5">
          <div
            v-for="(item, index) in cart"
            :key="item.name"
            class="flex flex-row justify-between mt-2 text-base"
          >
            <!-- Line item -->
            <div class="flex flex-row w-full">
              <div>
                <button
                  class="bg-black text-slate-50 px-2"
                  @click="item.quantity++"
                >
                  +
                </button>
                <input :value="item.quantity" class="w-6 text-center" />
                <button
                  class="bg-black text-slate-50 px-2"
                  @click="item.quantity--"
                >
                  -
                </button>
              </div>
              <span class="ml-2 text-left">{{ item.name }}</span>
            </div>
            <div>{{ item.price * item.quantity }}</div>
            <button class="ml-2" @click="removeItem(index)">x</button>
          </div>
        </div>
        <div>
          <hr />
          <div class="flex flex-row justify-between">
            <span>Subtotal</span> <span v-if="subTotal">{{ subTotal }}</span>
            <span v-else>0</span>
          </div>
          <button
            class="bg-black text-slate-50 w-full p-2 mt-2"
            @click="handlePayment()"
          >
            Checkout
          </button>
        </div>
      </section>
    </main>
  </div>
</template>
