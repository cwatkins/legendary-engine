import { ref, computed } from "vue";

export function useCart() {
  const shadowCart = ref([]);

  const cart = computed(() => {
    return shadowCart.value.filter((x) => x.quantity >= 1);
  });

  const subTotal = computed(() => {
    return cart.value
      .map((x) => x.quantity * x.price)
      .reduce((a, b) => a + b, 0);
  });

  function addToCart(item) {
    const currentItem = shadowCart.value.filter((x) => x.id === item.id)[0];
    if (currentItem) {
      currentItem.quantity++;
    } else {
      shadowCart.value.push({
        ...item,
        quantity: 1,
      });
    }
  }

  function clearCart() {
    shadowCart.value = [];
  }

  return {
    subTotal,
    addToCart,
    cart,
    clearCart,
  };
}
