<script setup>
import { computed, ref, onBeforeMount, watch } from "vue";
import { useReader } from "./composables/useReader";
import { useCart } from "./composables/useCart";
import { usePayment } from "./composables/usePayment";

import MenuItem from "./components/MenuItem.vue";

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
  return subTotal.value > 100 && selectedReader.value;
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
  const { reader_state: processState, error: processError } =
    await processPaymentIntent(paymentIntentId.value, selectedReader.value.id);
  readerState.value = processState.action.status;

  // Simulate result
  const { reader_state: simulateState, error: simulatePaymentError } =
    await simulatePayment(selectedReader.value.id);
  // readerState.value = simulateState.action.status;

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
  <div class="max-h-full min-w-screen max-w-screen">
    <header class="bg-black text-center text-slate-50 min-w-full">
      Increment Store
      <span v-if="selectedReader">
        ({{ selectedReader.id }}) {{ readerState }}
      </span>
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
        <div class="h-1/2 overflow-y-auto">
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
              'bg-black': !isComplete,
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
        <!-- TODO: Add test card options -->
        <div v-show="false" class="text-xl pt-2">
          <h2>Test Card</h2>
          <input id="" type="radio" name="" />
        </div>
        <div class="flex flex-col pt-4">
          <hr />
          <span class="text-xl">Readers</span>
          <div class="space-y-2 overflow-y-auto mt-2">
            <div
              v-for="reader in readers"
              :key="reader.id"
              class="flex flex-row justify-between"
            >
              <div class="flex flex-row items-center space-x-2">
                <svg
                  v-if="selectedReader && reader.id === selectedReader.id"
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-4 w-4"
                  viewBox="0 0 20 20"
                  fill="green"
                >
                  <path
                    fill-rule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                    clip-rule="evenodd"
                  />
                </svg>
                <span class="truncate">
                  {{ reader.label }}
                </span>
              </div>

              <button @click="selectedReader = reader">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-5 w-5"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  stroke-width="2"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"
                  />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>
