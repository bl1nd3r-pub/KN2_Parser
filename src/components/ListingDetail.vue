<script setup lang="ts">
import { ref, computed } from "vue";
import { useListingsStore } from "@/stores/listings";
import { useFavoritesStore } from "@/stores/favorites";
import type { Listing } from "@/types/listing";
import MissingField from "./MissingField.vue";
import PhotoGallery from "./PhotoGallery.vue";

const store = useListingsStore();
const favoritesStore = useFavoritesStore();

const props = defineProps<{
  listingId: string;
}>();

const listing = computed(() => store.getListingById(props.listingId));
const isFavorite = computed(() => favoritesStore.isFavorite(props.listingId));

const toggleFavorite = () => {
  favoritesStore.toggle(props.listingId);
};

const closeDetail = () => {
  store.closeListing();
};

const photoModalOpen = ref(false);
</script>

<template>
  <div v-if="listing" class="listing-detail">
    <button class="back-btn" @click="closeDetail">← Вернуться к списку</button>

    <div class="detail-header">
      <h1>{{ listing.title }}</h1>
      <button class="favorite-btn" @click="toggleFavorite" :class="{ active: isFavorite }">
        <span class="heart">♥</span>
        <span v-if="isFavorite">В избранном</span>
        <span v-else>В избранное</span>
      </button>
    </div>

    <div class="detail-content">
      <div class="detail-images">
        <PhotoGallery :photos="listing.photos" @close="photoModalOpen = false" />
      </div>

      <div class="detail-info">
        <div class="detail-price">
          <span v-if="listing.price !== null">{{ listing.price }} ₽ / месяц</span>
          <span v-else><MissingField label="Цена не указана" /></span>
        </div>

        <div class="detail-meta">
          <div>
            <strong>Комнаты:</strong>
            <span v-if="listing.rooms !== null">{{ listing.rooms }}-к.</span>
            <span v-else><MissingField label="Количество комнат не указано" /></span>
          </div>
          <div>
            <strong>Площадь:</strong>
            <span v-if="listing.area !== null">{{ listing.area }} м²</span>
            <span v-else><MissingField label="Площадь не указана" /></span>
          </div>
          <div>
            <strong>Район:</strong>
            <span v-if="listing.district">{{ listing.district }}</span>
            <span v-else><MissingField label="Район не указан" /></span>
          </div>
          <div v-if="listing.address">
            <strong>Адрес:</strong> {{ listing.address }}
          </div>
          <div v-if="listing.metro">
            <strong>Метро:</strong> {{ listing.metro }}
          </div>
        </div>

        <div class="detail-description">
          <h3>Описание</h3>
          <p v-if="listing.description">{{ listing.description }}</p>
          <p v-else><MissingField label="Описание отсутствует" /></p>
        </div>

        <div v-if="listing.source_url" class="detail-source">
          <a :href="listing.source_url" target="_blank" rel="noopener">Источник объявления</a>
        </div>
      </div>
    </div>
  </div>
  <div v-else class="listing-detail">
    <p>Объявление не найдено.</p>
    <button @click="closeDetail">Назад</button>
  </div>
</template>

<style scoped>
.listing-detail {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
}

.back-btn {
  margin-bottom: 20px;
  padding: 8px 16px;
  background: transparent;
  border: 1px solid #ccc;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9em;
}

.back-btn:hover {
  background: #f5f5f5;
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.detail-header h1 {
  margin: 0;
  font-size: 1.6em;
  color: #2c3e50;
}

.favorite-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  border: 1px solid #ddd;
  border-radius: 6px;
  background: white;
  cursor: pointer;
  font-size: 0.95em;
}

.favorite-btn.active {
  border-color: #e74c3c;
  color: #e74c3c;
}

.heart {
  font-size: 1.2em;
}

.detail-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.detail-images {
  flex: 1;
}

.detail-info {
  flex: 1;
}

.detail-price {
  font-size: 1.5em;
  font-weight: bold;
  color: #27ae60;
  margin-bottom: 20px;
}

.detail-meta {
  margin-bottom: 24px;
}

.detail-meta div {
  margin-bottom: 10px;
  font-size: 1em;
  color: #444;
}

.detail-meta strong {
  color: #2c3e50;
}

.detail-description h3 {
  margin-top: 0;
  margin-bottom: 10px;
  color: #2c3e50;
}

.detail-description p {
  line-height: 1.6;
  color: #555;
  white-space: pre-line;
}

.detail-source {
  margin-top: 24px;
}

.detail-source a {
  color: #4a90e2;
  text-decoration: none;
}

.detail-source a:hover {
  text-decoration: underline;
}

@media (max-width: 768px) {
  .detail-content {
    grid-template-columns: 1fr;
  }
  .detail-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
}
</style>
