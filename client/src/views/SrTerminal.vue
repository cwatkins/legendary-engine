<script setup>
import { computed, ref } from "vue";
import SrHeader from "../components/SrHeader.vue";
import SrGallery from "../components/SrGallery.vue";
import SrCart from "../components/SrCart.vue";
import SrTotal from "../components/SrTotal.vue";
import SrCheckoutButton from "../components/SrCheckoutButton.vue";
import SrReaderList from "../components/SrReaderList.vue";

import { useCart } from "../composables/useCart";
import { usePayment } from "../composables/usePayment";
import { useReader } from "../composables/useReader";

const { cart, subTotal, addToCart } = useCart();

const currentReader = ref(null);
const paymentState = ref(null);

const checkoutReady = computed(() => {
  return currentReader.value && cart.value.length ? true : false;
});

const { processPaymentIntent, simulatePayment, pollReader } = useReader();
const { paymentIntentId, createPaymentIntent } = usePayment();

async function handlePayment() {
  if (!paymentIntentId.value) {
    paymentIntentId.value = await createPaymentIntent(subTotal.value);
  }

  // 1. Process payment
  const { reader_state: processState, error: processError } =
    await processPaymentIntent(paymentIntentId.value, currentReader.value.id);
  paymentState.value = processState.action.status;

  // 2. (Optional) Simulate result
  const { reader_state: simulateState, error: simulatePaymentError } =
    await simulatePayment(currentReader.value.id);

  // 3. Poll for results
  const { reader_state: polledReaderState } = await pollReader(
    currentReader.value.id,
    paymentIntentId.value,
    500,
    10
  );
  paymentState.value = polledReaderState.action.status;
}

function reset() {
  cart.value = [];
  paymentIntentId.value = null;
  paymentState.value = null;
}
</script>
<template>
  <div class="max-h-full min-w-screen max-w-screen bg-color-neutral-50">
    <sr-header />
  </div>
  <div class="flex flex-row">
    <sr-gallery @add-to-cart="addToCart" />
    <div class="flex flex-col w-3/5 mr-2 text-slate-800">
      <sr-cart :cart="cart" />
      <div>
        <hr />
        <sr-total :total="subTotal" />
        <sr-checkout-button
          :checkout-ready="checkoutReady"
          :payment-state="paymentState"
          @handle-payment="handlePayment()"
          @clear-cart="reset()"
        />
      </div>
      <sr-reader-list @set-reader="(reader) => (currentReader = reader)" />
    </div>
  </div>
</template>
