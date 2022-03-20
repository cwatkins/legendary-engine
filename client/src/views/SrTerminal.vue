<script setup>
import { computed, ref } from "vue";
import { useCart } from "../composables/useCart";
import { usePayment } from "../composables/usePayment";
import { useReader } from "../composables/useReader";

import SrHeader from "../components/SrHeader.vue";
import SrGallery from "../components/SrGallery.vue";
import SrCart from "../components/SrCart.vue";
import SrTotal from "../components/SrTotal.vue";
import SrCheckoutButton from "../components/SrCheckoutButton.vue";
import SrReaderList from "../components/SrReaderList.vue";

const { cart, subTotal, addToCart, clearCart } = useCart();
const { paymentIntentId, createPaymentIntent } = usePayment();
const { currentReader, processPaymentIntent, simulatePayment, pollReader } =
  useReader();

const checkoutReady = computed(() => {
  return currentReader.value && cart.value.length ? true : false;
});

const hasItems = computed(() => (subTotal.value > 0 ? true : false));

const paymentState = ref(null);

const isLoading = computed(() => {
  if (paymentState.value) {
    return (
      paymentState.value.includes("attempting") ||
      paymentState.value.includes("in_progress")
    );
  } else {
    return false;
  }
});

const error = ref(null);

async function handlePayment() {
  paymentState.value = "attempting";
  if (!paymentIntentId.value) {
    paymentIntentId.value = await createPaymentIntent(subTotal.value);
  }

  /**  1. Process payment */
  const { reader_state: processingState, error: processingError } =
    await processPaymentIntent(paymentIntentId.value, currentReader.value.id);
  if (processingError) {
    error.value = processingError.message;
    paymentState.value = null;
    return;
  }
  paymentState.value = processingState.action.status;

  /** 2. Simulate result. */
  if (currentReader.value.device_type.includes("simulated")) {
    const { reader_state: simulateState, error: simulatedError } =
      await simulatePayment(currentReader.value.id);
    if (simulatedError) {
      error.value = simulatedError.message;
      paymentState.value = null;
      return;
    }
  }

  /**  3. Poll for results */
  const { reader_state: polledReaderState, error: pollingError } =
    await pollReader(currentReader.value.id, paymentIntentId.value, 500, 10);
  if (pollingError) {
    error.value = pollingError.message;
    paymentState.value = null;
    return;
  }
  paymentState.value = polledReaderState.action.status;
  return { readerState: polledReaderState, paymentState: paymentState.value };
}

async function checkout() {
  console.log("handle_payment");
  const result = await handlePayment();
  if (result) {
    const { readerState } = result;
    const failureMessage = readerState?.action?.failure_message;
    if (failureMessage) {
      error.value = failureMessage;
    } else {
      error.value = "Payment succeeded.";
      reset();
    }
  }
}

function reset() {
  console.log("reset");
  clearCart();
  paymentIntentId.value = null;
  paymentState.value = null;
}
</script>
<template>
  <div v-if="error">{{ error }}</div>
  <sr-header class="bg-neutral-100 sticky top-0 left-0 right-0 z-10" />
  <div class="relative flex flex-row justify-center bg-neutral-100">
    <transition-group
      enter-from-class="transform translate-x-full"
      enter-active-class="delay-100 duration-300 ease-out"
      leave-to-class="transform translate-x-full"
      leave-from-class="translation-x-0"
      leave-active-class="duration-300 ease-in"
    >
      <sr-gallery
        class="transition duration-300 ease-out w-1/2"
        :class="{
          'pointer-events-none': isLoading,
          'transform translation-x-0': hasItems,
        }"
        @add-to-cart="addToCart"
      />
      <div v-if="hasItems" class="w-2/5 px-2 pt-2 mr-2 text-slate-800">
        <sr-cart :cart="cart" :class="{ 'pointer-events-none': isLoading }" />
        <sr-total :total="subTotal" />
        <sr-checkout-button
          :is-loading="isLoading"
          :checkout-ready="checkoutReady"
          :payment-state="paymentState"
          @handle-payment="checkout()"
          @clear-cart="reset()"
        />
        <sr-reader-list @set-reader="(reader) => (currentReader = reader)" />
      </div>
    </transition-group>
  </div>
</template>
