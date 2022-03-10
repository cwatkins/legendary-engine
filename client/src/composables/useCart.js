import { ref, watchEffect, computed, onBeforeMount } from "vue";

export function useCart() {
  const cart = ref([]);

  watchEffect(() => {
    cart.value.forEach((x, index) => {
      if (x.quantity < 1) {
        cart.value.splice(index, 1);
      }
    });
  });

  const subTotal = computed(() => {
    return cart.value
      .map((x) => x.quantity * x.price)
      .reduce((a, b) => a + b, 0);
  });

  function addToCart(item) {
    const currentItem = cart.value.filter((x) => x.id === item.id)[0];
    if (currentItem) {
      currentItem.quantity++;
    } else {
      cart.value.push({
        ...item,
        quantity: 1,
      });
    }
  }

  function removeItem(index) {
    console.log(index);
    cart.value.splice(index, 1);
  }

  return {
    subTotal,
    addToCart,
    cart,
    removeItem,
  };
}
