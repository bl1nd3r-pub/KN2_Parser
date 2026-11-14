<script setup lang="ts">
import { ref } from "vue";
import { useListingsStore } from "@/stores/listings";

const store = useListingsStore();

const priceMin = ref<string>("");
const priceMax = ref<string>("");
</script>

<template>
  <div class="filter-panel">
    <h3>Фильтры</h3>

    <div class="filter-group">
      <label>Цена от:</label>
      <input type="number" v-model="priceMin" placeholder=" мин" @change="store.setPriceRange(priceMin ? Number(priceMin) : null, priceMax ? Number(priceMax) : null)" class="filter-input" />
    </div>

    <div class="filter-group">
      <label>Цена до:</label>
      <input type="number" v-model="priceMax" placeholder=" макс" @change="store.setPriceRange(priceMin ? Number(priceMin) : null, priceMax ? Number(priceMax) : null)" class="filter-input" />
    </div>

    <div class="filter-group">
      <label>Количество комнат:</label>
      <select v-model.number="store.filters.rooms" @change="store.setRooms(store.filters.rooms)" class="filter-select">
        <option value="">Любые</option>
        <option v-for="r in store.roomsOptions" :key="r" :value="r">{{ r }}-к.</option>
      </select>
    </div>

    <div class="filter-group">
      <label>Район:</label>
      <select v-model="store.filters.district" @change="store.setDistrict(store.filters.district)" class="filter-select">
        <option value="">Все районы</option>
        <option v-for="d in store.districts" :key="d" :value="d">{{ d }}</option>
      </select>
    </div>

    <button @click="store.resetFilters(); priceMin = ''; priceMax = ''" class="reset-btn">Сброс фильтров</button>
  </div>
</template>

<style scoped>
.filter-panel {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 24px;
  background: #fafafa;
}

.filter-panel h3 {
  margin: 0 0 16px 0;
  font-size: 1.1em;
  color: #333;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 12px;
}

.filter-group label {
  width: 110px;
  font-size: 0.9em;
  color: #555;
}

.filter-input {
  flex: 1;
  padding: 8px 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 0.9em;
}

.filter-select {
  flex: 1;
  padding: 8px 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 0.9em;
  background: white;
}

.reset-btn {
  margin-top: 8px;
  padding: 8px 16px;
  background: transparent;
  border: 1px solid #ccc;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9em;
  color: #666;
}

.reset-btn:hover {
  background: #e8e8e8;
}
</style>
