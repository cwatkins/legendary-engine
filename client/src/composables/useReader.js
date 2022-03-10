import { ref, onBeforeMount } from "vue";

export function useReader() {
  const readers = ref([]);
  const selectedReader = ref(null);

  onBeforeMount(async () => {
    try {
      readers.value = await listReaders();
    } catch (error) {
      console.log(error); //TODO: surface issues in UI
    }
  });

  async function listReaders() {
    const response = await fetch("/api/list-terminal-readers");
    const { readers } = await response.json();
    return readers;
  }

  async function processPaymentIntent(paymentIntentId, readerId) {
    const response = await fetch("/api/process-payment-intent", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        payment_intent_id: paymentIntentId,
        reader_id: readerId,
      }),
    });
    const reader = await response.json();
    return reader;
  }

  async function simulatePayment(readerId) {
    const response = await fetch("/api/simulate-terminal-payment", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ reader_id: readerId }),
    });
    const result = await response.json();
    return result;
  }

  async function cancelTerminalAction(readerId) {
    const response = await fetch("/api/cancel-terminal-action", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ reader_id: readerId }),
    });
    const result = await response.json();
    return result;
  }

  return {
    readers,
    selectedReader,
    processPaymentIntent,
    simulatePayment,
    cancelTerminalAction,
  };
}
