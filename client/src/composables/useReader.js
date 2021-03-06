import { ref } from "vue";

export function useReader() {
  const readers = ref([]);
  const currentReader = ref(null);

  async function retrieveReader(readerId) {
    const response = await fetch(
      `/api/retrieve-terminal-reader?reader_id=${readerId}`
    );
    const reader = await response.json();
    return reader;
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

  async function pollReader(
    readerId,
    paymentIntentId,
    interval = 3000,
    maxTries = 10
  ) {
    let tries = 0;
    async function execute(resolve, reject) {
      tries++;
      console.log("Try #", tries);
      const reader = await retrieveReader(readerId);
      const { reader_state } = reader;
      if (
        reader_state.action.status === "succeeded" ||
        reader_state.action.status === "failed"
      ) {
        return resolve(reader);
      } else if (tries === maxTries) {
        return reject(new Error("Max tries exceeded"));
      } else if (
        reader_state.action.process_payment_intent !== paymentIntentId
      ) {
        return reject(
          new Error(
            `Polling for wrong Payment Intent. Got ${reader_state.action.process_payment_intent} from reader but expected ${paymentIntentId}`
          )
        );
      } else {
        setTimeout(execute, interval, resolve, reject);
      }
    }
    return new Promise(execute);
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
    currentReader,
    processPaymentIntent,
    simulatePayment,
    cancelTerminalAction,
    pollReader,
  };
}
