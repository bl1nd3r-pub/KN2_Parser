<script setup lang="ts">
import { computed } from "vue";
import { useFavoritesStore } from "@/stores/favorites";
import type { Listing } from "@/types/listing";
import MissingField from "./MissingField.vue";

const props = defineProps<{
  listing: Listing;
}>();

const favoritesStore = useFavoritesStore();

const isFavorite = computed(() => favoritesStore.isFavorite(props.listing.id));

const toggleFavorite = () => {
  favoritesStore.toggle(props.listing.id);
};
</script>

<template>
  <div class="listing-card">
    <div class="card-image">
      <img
        v-if="listing.photos.length"
        :src="listing.photos[0]"
        :alt="listing.title"
        class="card-photo"
      />
      <div v-else class="card-no-photo">
        <MissingField label="Нет фото" />
      </div>

      <button class="favorite-btn" @click="toggleFavorite" :class="{ active: isFavorite }">
        <span class="heart">♥</span>
      </button>
    </div>

    <div class="card-info">
      <h3 class="card-title">{{ listing.title }}</h3>

      <div class="card-meta">
        <span v-if="listing.price !== null" class="card-price">{{ listing.price }} ₽</span>
        <span v-else class="card-price missing">
          <MissingField label="Цена не указана" />
        </span>
      </div>

      <div class="card-details">
        <span v-if="listing.rooms !== null">{{ listing.rooms }}-к.</span>
        <span v-else><MissingField label="Комнаты не указаны" /></span>
        <span v-if="listing.area !== null">{{ listing.area }} м²</span>
        <span v-else><MissingField label="Площадь не указана" /></span>
        <span v-if="listing.district">{{ listing.district }}</span>
        <span v-else><MissingField label="Район не указан" /></span>
      </div>

      <p v-if="listing.description" class="card-desc">{{ listing.description }}</p>
      <p v-else class="card-desc missing"><MissingField label="Описание отсутствует" /></p>

      <button class="card-details-btn" @click="$emit('view')">Подробнее</button>
    </div>
  </div>
</template>

<style scoped>
.listing-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 20px;
  display: flex;
  background: white;
  transition: box-shadow 0.2s;
}

.listing-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.card-image {
  position: relative;
  width: 300px;
  height: 200px;
  flex-shrink: 0;
  background: #f5f5f5;
  overflow: hidden;
}

.card-photo {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.card-no-photo {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #aaa;
  font-size: 0.9em;
}

.favorite-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: none;
  background: rgba(255, 255, 255, 0.9);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2em;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
}

.favorite-btn.active {
  color: #e74c3c;
}

.favorite-btn:hover {
  background: white;
}

.card-info {
  padding: 16px;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.card-title {
  margin: 0 0 10px 0;
  font-size: 1.1em;
  color: #2c3e50;
}

.card-meta {
  margin-bottom: 10px;
}

.card-price {
  font-size: 1.3em;
  font-weight: bold;
  color: #27ae60;
}

.card-price.missing {
  color: #888;
  font-weight: normal;
  font-size: 0.9em;
}

.card-details {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  margin-bottom: 10px;
  font-size: 0.9em;
  color: #666;
}

.card-desc {
  margin: 0 0 16px 0;
  font-size: 0.9em;
  color: #555;
  line-height: 1.4;
  flex: 1;
}

.card-details-btn {
  align-self: flex-start;
  padding: 8px 16px;
  background: #4a90e2;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9em;
}

.card-details-btn:hover {
  background: #357abd;
}
</style>
