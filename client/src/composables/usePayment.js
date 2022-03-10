import { ref } from "vue";

export function usePayment() {
  const paymentIntentId = ref(null);

  async function createPaymentIntent(amount) {
    const response = await fetch("/api/create-payment-intent", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ amount }),
    });
    const { payment_intent_id } = await response.json();
    return payment_intent_id;
  }

  return {
    paymentIntentId,
    createPaymentIntent,
  };
}
