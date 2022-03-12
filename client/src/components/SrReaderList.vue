<script setup>
import { ref, onBeforeMount } from "vue";

const readers = ref([]);
const selectedReader = ref(null);

onBeforeMount(async () => {
  try {
    readers.value = await listReaders();
  } catch (error) {
    console.log("error", error);
  }
});

async function listReaders() {
  const response = await fetch("/api/list-terminal-readers");
  const { readers } = await response.json();
  return readers;
}

function setReader(reader) {
  emit("setReader", reader);
  selectedReader.value = reader;
}

const emit = defineEmits(["setReader"]);
</script>
<template>
  <div class="flex flex-col pt-4 text-slate-800">
    <hr />
    <p v-if="!selectedReader">2. Select a reader</p>
    <p class="text-xl">Readers</p>
    <div class="space-y-2 overflow-y-auto mt-2">
      <div
        v-for="reader in readers"
        :key="reader.id"
        class="flex flex-row justify-between"
      >
        <div class="flex flex-row items-center space-x-2">
          <transition
            enter-from-class="transform opacity-0"
            enter-active-class="delay-600 duration-500 ease-out"
            leave-to-class="transform opacity-0"
            leave-from-class="opacity-100"
            leave-active-class="duration-400 ease-in"
          >
            <svg
              v-if="selectedReader && reader.id === selectedReader.id"
              xmlns="http://www.w3.org/2000/svg"
              class="h-4 w-4"
              viewBox="0 0 20 20"
              fill="green"
            >
              <path
                fill-rule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                clip-rule="evenodd"
              />
            </svg>
          </transition>
          <span class="truncate">
            {{ reader.label }}
          </span>
        </div>
        <button @click="setReader(reader)">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-5 w-5"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            stroke-width="2"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"
            />
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>
