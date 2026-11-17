<script setup lang="ts">
import { useListingsStore } from "@/stores/listings";

const store = useListingsStore();
</script>

<template>
  <div class="search-bar">
    <input
      type="text"
      v-model="store.filters.search"
      placeholder="Поиск по названию объявления..."
      class="search-input"
    />
    <button @click="store.setSearch('')" class="search-clear" v-if="store.filters.search">×</button>
  </div>
</template>

<style scoped>
.search-bar {
  display: flex;
  gap: 8px;
  margin-bottom: 20px;
  flex: 1;
  min-width: 300px;
}

.search-input {
  flex: 1;
  padding: 10px 14px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1em;
}

.search-input:focus {
  outline: none;
  border-color: #4a90e2;
}

.search-clear {
  padding: 10px 14px;
  border: 1px solid #ddd;
  border-radius: 6px;
  background: #f5f5f5;
  cursor: pointer;
  font-size: 1.2em;
  color: #999;
}

.search-clear:hover {
  background: #e8e8e8;
  color: #666;
}
</style>
