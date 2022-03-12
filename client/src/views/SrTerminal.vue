<script setup>
import { computed, ref } from "vue";
import SrHeader from "../components/SrHeader.vue";
import SrGallery from "../components/SrGallery.vue";
import SrCart from "../components/SrCart.vue";
import SrTotal from "../components/SrTotal.vue";
import SrCheckoutButton from "../components/SrCheckoutButton.vue";
import SrReaderList from "../components/SrReaderList.vue";
import SrMessage from "../components/SrMessage.vue";

import { useCart } from "../composables/useCart";
import { usePayment } from "../composables/usePayment";
import { useReader } from "../composables/useReader";

const modalText = ref(null);
const modalTitle = ref(null);
/**
 * Composables (hooks) for keeping state of the cart, its subtotal
 * and a function for adding items to it
 */
const { cart, subTotal, addToCart } = useCart();

/** Payment Intent var and a composable (hook) for creating one */
const { paymentIntentId, createPaymentIntent } = usePayment();

/**
 * Composables (hooks) for processing a payment, simulating completing,
 * and polling a reader for the payment's status
 */
const { currentReader, processPaymentIntent, simulatePayment, pollReader } =
  useReader();

/**
 * Computes whether Checkout can be done based on having items in the cart
 * and a reader currently selected
 */
const checkoutReady = computed(() => {
  return currentReader.value && cart.value.length ? true : false;
});

/** Reactive var for maintain payment's status */
const paymentState = ref(null);

/**
 * Function for handling a payment using Payment Intents and Terminal
 */
async function handlePayment() {
  if (!paymentIntentId.value) {
    paymentIntentId.value = await createPaymentIntent(subTotal.value);
  }

  /**  1. Process payment */
  const { reader_state: processState, error: processError } =
    await processPaymentIntent(paymentIntentId.value, currentReader.value.id);
  paymentState.value = processState.action.status;

  /** 2. (Optional) Simulate result. */
  if (currentReader.value.device_type.includes("simulated")) {
    const { reader_state: simulateState, error: simulatePaymentError } =
      await simulatePayment(currentReader.value.id);
  }

  /**  3. Poll for results */
  const { reader_state: polledReaderState } = await pollReader(
    currentReader.value.id,
    paymentIntentId.value,
    500,
    10
  );
  paymentState.value = polledReaderState.action.status;
  return { readerState: polledReaderState, paymentState: paymentState.value };
}

async function checkout() {
  try {
    const { readerState, paymentState } = await handlePayment();
    const paymentTitle = "Payment " + paymentState;
    const paymentMessage = JSON.stringify(readerState, null, 2);
    setModal(paymentTitle, paymentMessage);
  } catch (error) {
    const errorMessage = JSON.stringify(error, null, 2);
    setModal("Error", errorMessage);
  }
}

function reset() {
  cart.value = [];
  paymentIntentId.value = null;
  paymentState.value = null;
}

function setModal(title, text) {
  modalTitle.value = title;
  modalText.value = text;
}

function closeModal() {
  reset();
  modalText.value = null;
  modalTitle.value = null;
}
</script>
<template>
  <sr-message
    :modal-text="modalText"
    :modal-title="modalTitle"
    @close-modal="closeModal"
  />
  <div class="max-h-full min-w-screen max-w-screen bg-color-neutral-50">
    <sr-header />
  </div>
  <div class="flex flex-row">
    <sr-gallery @add-to-cart="addToCart" />
    <div class="flex flex-col w-3/5 px-2 pt-2 mr-2 text-slate-800">
      <sr-cart :cart="cart" />
      <sr-total :total="subTotal" />
      <sr-checkout-button
        :checkout-ready="checkoutReady"
        :payment-state="paymentState"
        @handle-payment="checkout()"
        @clear-cart="reset()"
      />
      <sr-reader-list @set-reader="(reader) => (currentReader = reader)" />
    </div>
  </div>
</template>
