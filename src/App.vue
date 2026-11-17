<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { useListingsStore } from "@/stores/listings";
import { useFavoritesStore } from "@/stores/favorites";
import type { Listing } from "@/types/listing";
import SearchBar from "@/components/SearchBar.vue";
import FilterPanel from "@/components/FilterPanel.vue";
import ListingCard from "@/components/ListingCard.vue";
import ListingDetail from "@/components/ListingDetail.vue";
import EmptyState from "@/components/EmptyState.vue";

const store = useListingsStore();
const favoritesStore = useFavoritesStore();

const API_URL = "http://localhost:8000";

// Избранные объявления целиком.
// ID, которых больше нет в данных (например, после перезапуска парсера),
// отфильтровываются — приложение не должно падать.
const favoriteListings = computed(() =>
  favoritesStore.favoriteIds
    .map((id) => store.getListingById(id))
    .filter((item): item is Listing => item !== undefined),
);

// Правильное склонение: 1 объявление, 2 объявления, 5 объявлений
const foundLabel = computed(() => {
  const n = store.filteredListings.length;
  const mod10 = n % 10;
  const mod100 = n % 100;
  if (mod10 === 1 && mod100 !== 11) return "объявление найдено";
  if (mod10 >= 2 && mod10 <= 4 && (mod100 < 12 || mod100 > 14)) return "объявления найдено";
  return "объявлений найдено";
});

// Применены ли поиск/фильтры (для подписи «из N»)
const filtersActive = computed(
  () =>
    store.filters.search !== "" ||
    store.filters.priceMin !== null ||
    store.filters.priceMax !== null ||
    store.filters.rooms !== null ||
    store.filters.district !== null,
);

// При загрузке страницы пробуем взять свежие данные с бэкенда.
// Если он не запущен — работаем со статическим listings.json из сборки.
onMounted(() => {
  store.fetchFromBackend();
});

// Состояние парсера
const parserStatus = ref<"idle" | "running" | "done" | "error">("idle");
const parserMessage = ref("");

async function runParser() {
  parserStatus.value = "running";
  parserMessage.value = "Парсинг… это может занять пару минут";
  try {
    const resp = await fetch(`${API_URL}/run-parser`, { method: "POST" });
    const data = await resp.json();
    if (resp.ok && data.ok) {
      // Подтягиваем обновлённые объявления в стор без перезагрузки страницы
      await store.fetchFromBackend();
      parserStatus.value = "done";
      parserMessage.value = `Готово! Найдено объявлений: ${data.count}`;
    } else {
      parserStatus.value = "error";
      parserMessage.value = data.message || "Ошибка запуска парсера";
    }
  } catch (err) {
    parserStatus.value = "error";
    parserMessage.value =
      err instanceof Error ? err.message : "Ошибка соединения с бэкендом";
  }
}
</script>

<template>
  <div id="app">
    <header class="app-header">
      <div class="container">
        <div class="header-content">
          <h1 class="app-title">Доска аренды жилья</h1>
          <nav class="app-nav">
            <button @click="store.showList()" :class="{ active: store.view === 'list' }">Объявления</button>
            <button @click="store.showFavorites()" :class="{ active: store.view === 'favorites' }">
              Избранное <span class="badge">{{ favoriteListings.length }}</span>
            </button>
            <button
              @click="runParser"
              :disabled="parserStatus === 'running'"
              class="parser-btn"
            >
              <span v-if="parserStatus === 'running'">⟳ Парсинг…</span>
              <span v-else>Запустить парсер</span>
            </button>
            <div v-if="parserMessage" class="parser-message" :class="parserStatus">
              {{ parserMessage }}
            </div>
          </nav>
        </div>
      </div>
    </header>

    <div class="container">
      <!-- Детальный просмотр объявления -->
      <ListingDetail v-if="store.view === 'detail'" :listing-id="store.selectedListingId" />

      <!-- Страница избранного -->
      <div v-else-if="store.view === 'favorites'">
        <h2>Избранное</h2>
        <button @click="store.showList()" class="back-btn">← Назад к списку</button>

        <div v-if="favoriteListings.length === 0" class="empty-favorites">
          <p>У вас пока нет избранных объявлений.</p>
        </div>

        <div v-else class="listings-grid">
          <ListingCard
            v-for="listing in favoriteListings"
            :key="listing.id"
            :listing="listing"
            @view="store.openListing(listing.id)"
          />
        </div>
      </div>

      <!-- Главный список с поиском и фильтрами -->
      <div v-else>
        <div class="controls">
          <SearchBar />
          <FilterPanel />
        </div>

        <div class="results-info">
          <strong>{{ store.filteredListings.length }}</strong>
          {{ foundLabel }}
          <span v-if="filtersActive"> из {{ store.allListings.length }}</span>
        </div>

        <div v-if="store.filteredListings.length === 0" class="empty-wrapper">
          <EmptyState />
        </div>

        <div v-else class="listings-grid">
          <ListingCard
            v-for="listing in store.filteredListings"
            :key="listing.id"
            :listing="listing"
            @view="store.openListing(listing.id)"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.app-header {
  background: #2c3e50;
  color: white;
  padding: 16px 0;
  margin-bottom: 24px;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.app-title {
  margin: 0;
  font-size: 1.5em;
}

.app-nav {
  display: flex;
  gap: 12px;
  align-items: center;
  flex-wrap: wrap;
}

.app-nav button {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  background: rgba(255, 255, 255, 0.1);
  color: white;
  cursor: pointer;
  font-size: 0.95em;
}

.app-nav button:hover {
  background: rgba(255, 255, 255, 0.2);
}

.app-nav button.active {
  background: #4a90e2;
}

.app-nav button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.parser-btn {
  background: #27ae60;
}

.parser-btn:hover:not(:disabled) {
  background: #219a52;
}

.badge {
  display: inline-block;
  min-width: 20px;
  height: 20px;
  background: #e74c3c;
  color: white;
  border-radius: 10px;
  text-align: center;
  line-height: 20px;
  font-size: 0.8em;
  margin-left: 6px;
}

.parser-message {
  margin-left: 12px;
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 0.9em;
  white-space: nowrap;
}

.parser-message.done {
  background: #d5f5e3;
  color: #27ae60;
}

.parser-message.error {
  background: #fadbd8;
  color: #e74c3c;
}

.parser-message.running {
  background: #f9e79f;
  color: #d35400;
}

.controls {
  display: flex;
  align-items: flex-start;
  gap: 20px;
  flex-wrap: wrap;
  margin-bottom: 20px;
}

.results-info {
  margin-bottom: 16px;
  font-size: 1em;
  color: #555;
}

.results-info strong {
  color: #2c3e50;
}

.listings-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(520px, 1fr));
  gap: 20px;
}

.empty-wrapper {
  margin-top: 40px;
}

.empty-favorites {
  text-align: center;
  padding: 40px 20px;
  color: #666;
}

.back-btn {
  margin-bottom: 16px;
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
</style>
