<script setup>
import { computed, ref, onBeforeMount, watch } from "vue";
import { useReader } from "./composables/useReader";
import { useCart } from "./composables/useCart";
import { usePayment } from "./composables/usePayment";

import MenuGallery from "./components/MenuGallery.vue";
import MenuInstructions from "./components/MenuInstructions.vue";
import ReaderMenu from "./components/ReaderMenu.vue";

const products = ref([]);
const readerState = ref(null);

const {
  readers,
  selectedReader,
  processPaymentIntent,
  simulatePayment,
  pollReader,
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

const isLoading = computed(() => {
  return readerState.value === "in_progress";
});

const isComplete = computed(() => {
  return readerState.value === "succeeded";
});

const isReady = computed(() => {
  return subTotal.value > 100 && selectedReader.value ? true : false;
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

  // 1. Process payment
  const { reader_state: processState, error: processError } =
    await processPaymentIntent(paymentIntentId.value, selectedReader.value.id);
  readerState.value = processState.action.status;

  // 2. (Optional) Simulate result
  const { reader_state: simulateState, error: simulatePaymentError } =
    await simulatePayment(selectedReader.value.id);

  // 3. Poll for results
  const { reader_state: polledReaderState } = await pollReader(
    selectedReader.value.id,
    paymentIntentId.value,
    500,
    10
  );
  readerState.value = polledReaderState.action.status;
}

function reset() {
  cart.value = [];
  paymentIntentId.value = null;
  readerState.value = null;
}
</script>

<template>
  <div class="max-h-full min-w-screen max-w-screen bg-color-neutral-50">
    <div
      class="flex justify-around px-2 bg-sky-600 text-center text-slate-50 min-w-full"
    >
      <span> Increment Store </span>
      <div class="w-1/3 flex">
        <pre>Reader: </pre>
        <span v-if="selectedReader" class="truncate justify-start">
          {{ selectedReader.label }} {{ readerState }}
        </span>
      </div>
    </div>
    <main class="flex flex-row">
      <menu-gallery :products="products" @add-to-cart="addToCart" />
      <section class="flex flex-col w-3/5 mr-2 text-slate-800">
        <div class="h-1/2 overflow-y-auto">
          <menu-instructions
            :selected-reader="selectedReader"
            :is-ready="isReady"
            :has-empty-cart="cart.length > 0"
          />
          <div
            v-for="(item, index) in cart"
            :key="item.name"
            class="flex flex-row justify-between mt-2 text-base text-slate-800"
          >
            <!-- Line item -->
            <div class="flex flex-row w-full">
              <div>
                <button
                  class="bg-sky-600 text-slate-50 px-2"
                  @click="item.quantity++"
                >
                  +
                </button>
                <input :value="item.quantity" class="w-6 text-center" />
                <button
                  class="bg-sky-600 text-slate-50 px-2"
                  @click="item.quantity--"
                >
                  -
                </button>
              </div>
              <span class="ml-2 text-left">{{ item.name }}</span>
            </div>
            <div>{{ item.price * item.quantity }}</div>
            <button class="ml-2" @click="removeItem(index)">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-5 w-5"
                viewBox="0 0 20 20"
                fill="currentColor"
              >
                <path
                  fill-rule="evenodd"
                  d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z"
                  clip-rule="evenodd"
                />
              </svg>
            </button>
          </div>
        </div>
        <div>
          <hr />
          <div class="flex flex-row justify-between">
            <span class="text-xl">Total</span>
            <span v-if="subTotal">{{ subTotal }}</span>
            <span v-else>0</span>
          </div>
          <button
            class="text-slate-50 w-full p-2 mt-2"
            :class="{
              'bg-emerald-500': isComplete,
              'bg-sky-600': !isComplete,
              'opacity-50': !isReady,
            }"
            :disabled="!isReady"
          >
            <span v-if="isComplete" @click="reset()">Clear cart</span>
            <div v-else-if="isLoading" class="flex items-center justify-center">
              <svg
                role="status"
                class="mr-2 w-6 h-6 text-gray-200 animate-spin dark:text-gray-600 fill-blue-600"
                viewBox="0 0 100 101"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
                  fill="currentColor"
                />
                <path
                  d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
                  fill="grey"
                />
                <span class="sr-only">Loading...</span>
              </svg>
            </div>
            <span v-else @click="handlePayment()">Checkout</span>
          </button>
        </div>
        <reader-menu
          :readers="readers"
          :selected-reader="selectedReader"
          @set-reader="(reader) => (selectedReader = reader)"
          @clear-cart="reset"
        />
      </section>
    </main>
  </div>
</template>
