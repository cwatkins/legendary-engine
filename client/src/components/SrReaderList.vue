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
    <p class="text-sm font-semibold">Readers</p>
    <div class="space-y-2 overflow-y-auto my-2">
      <transition-group
        enter-from-class="transform opacity-0"
        enter-active-class="delay-100 duration-300 ease-out"
        leave-to-class="transform opacity-0"
        leave-from-class="translation-y-0 opacity-100"
        leave-active-class="duration-300 ease-in"
      >
        <button
          v-for="reader in readers"
          :key="reader.id"
          class="flex flex-row w-full justify-between bg-gray-400 px-6 rounded-md text-xs text-neutral-50 items-center transition hover:brightness-125"
          :class="{
            'font-semibold drop-shadow-lg bg-gray-600 scale-100':
              selectedReader && reader.id === selectedReader.id,
          }"
          @click="setReader(reader)"
        >
          <div class="flex flex-row space-x-2 items-center w-full">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-5 w-5 py-1"
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
            <span class="truncate">{{ reader.label }}</span>
          </div>
        </button>
      </transition-group>
    </div>
  </div>
</template>
