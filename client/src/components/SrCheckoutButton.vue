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
    <transition
      enter-from-class="transform opacity-0"
      enter-active-class="delay-700 duration-500 ease-out"
      leave-to-class="transform opacity-0"
      leave-from-class="opacity-100"
      leave-active-class="duration-400 ease-in"
    >
      <span v-if="paymentState === 'succeeded'">Clear cart</span>
    </transition>
    <transition
      enter-from-class="transform opacity-0"
      enter-active-class="delay-700 duration-500 ease-out"
      leave-to-class="transform opacity-0"
      leave-from-class="opacity-100"
      leave-active-class="duration-400 ease-in"
    >
      <span
        v-if="paymentState === 'in_progress'"
        class="flex items-center justify-center"
      >
        Loading...
      </span>
    </transition>
    <transition
      enter-from-class="transform opacity-0"
      enter-active-class="delay-700 duration-500 ease-out"
      leave-to-class="transform opacity-0"
      leave-from-class="opacity-100"
      leave-active-class="duration-400 ease-in"
    >
      <span v-if="!paymentState">Checkout</span>
    </transition>
  </button>
</template>
