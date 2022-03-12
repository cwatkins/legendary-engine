<script setup>
import { toRefs } from "vue";
const props = defineProps({
  paymentState: {
    type: String,
    default: null,
  },
  checkoutReady: Boolean,
});

const { paymentState } = toRefs(props);

function handleClick() {
  if (paymentState.value === "succeeded") {
    emit("clearCart");
  } else {
    emit("handlePayment");
  }
}

const emit = defineEmits(["clearCart", "handlePayment"]);
</script>
<template>
  <button
    class="text-slate-50 w-full p-2 mt-2 transition duration-300"
    :class="{
      'bg-emerald-500': paymentState === 'succeeded',
      'bg-sky-600': paymentState !== 'succeeded',
      'opacity-50': !checkoutReady,
    }"
    :disabled="!checkoutReady || paymentState === 'in_progress'"
    @click="handleClick"
  >
    <span v-if="paymentState === 'succeeded'">Clear cart</span>
    <span
      v-if="paymentState === 'in_progress'"
      class="flex items-center justify-center"
    >
      Loading...
    </span>
    <span v-if="!paymentState">Checkout</span>
  </button>
</template>
