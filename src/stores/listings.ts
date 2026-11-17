import { defineStore } from "pinia";
import { ref, computed } from "vue";
import type { Listing, Filters } from "@/types/listing";
import listingsData from "@/data/listings.json";

const API_URL = "http://localhost:8000";

export const useListingsStore = defineStore("listings", () => {
  // Все объявления из JSON
  const allListings = ref<Listing[]>(listingsData as Listing[]);

  // Фильтры
  const filters = ref<Filters>({
    search: "",
    priceMin: null,
    priceMax: null,
    rooms: null,
    district: null,
  });

  // Выбранное объявление для детального просмотра
  const selectedListingId = ref<string | null>(null);

  // Текущий вид: "list" | "favorites" | "detail"
  const view = ref<"list" | "favorites" | "detail">("list");

  // Отфильтрованные объявления
  const filteredListings = computed(() => {
    return allListings.value.filter((item) => {
      // Поиск по названию (регистронезависимый)
      if (filters.value.search) {
        const q = filters.value.search.toLowerCase();
        if (!item.title.toLowerCase().includes(q)) {
          return false;
        }
      }

      // Фильтр по цене (от)
      if (filters.value.priceMin !== null && filters.value.priceMin > 0) {
        if (!item.price || item.price < filters.value.priceMin!) {
          return false;
        }
      }

      // Фильтр по цене (до)
      if (filters.value.priceMax !== null && filters.value.priceMax > 0) {
        if (!item.price || item.price > filters.value.priceMax!) {
          return false;
        }
      }

      // Фильтр по комнатам
      if (filters.value.rooms !== null) {
        if (!item.rooms || item.rooms !== filters.value.rooms) {
          return false;
        }
      }

      // Фильтр по району
      if (filters.value.district) {
        if (!item.district || !item.district.toLowerCase().includes(filters.value.district!.toLowerCase())) {
          return false;
        }
      }

      return true;
    });
  });

  // Список уникальных районов для выпадающего фильтра
  const districts = computed(() => {
    const set = new Set<string>();
    allListings.value.forEach((item) => {
      if (item.district) {
        set.add(item.district);
      }
    });
    return Array.from(set).sort();
  });

  // Список уникальных значений комнатности
  const roomsOptions = computed(() => {
    const set = new Set<number>();
    allListings.value.forEach((item) => {
      if (item.rooms) {
        set.add(item.rooms);
      }
    });
    return Array.from(set).sort((a, b) => a - b);
  });

  // Сброс фильтров
  function resetFilters() {
    filters.value = {
      search: "",
      priceMin: null,
      priceMax: null,
      rooms: null,
      district: null,
    };
  }

  // Установить поиск
  function setSearch(query: string) {
    filters.value.search = query;
  }

  // Установить фильтр цены
  function setPriceRange(min: number | null, max: number | null) {
    filters.value.priceMin = min;
    filters.value.priceMax = max;
  }

  // Открыть детальный просмотр объявления
  function openListing(id: string) {
    selectedListingId.value = id;
    view.value = "detail";
  }

  // Закрыть детальный просмотр (вернуться к списку)
  function closeListing() {
    selectedListingId.value = null;
    view.value = "list";
  }

  // Перейти к избранному
  function showFavorites() {
    view.value = "favorites";
  }

  // Вернуться к списку
  function showList() {
    view.value = "list";
  }

  // Получить объявление по ID
  const getListingById = (id: string): Listing | undefined => {
    return allListings.value.find((item) => item.id === id);
  };

  // Заменить список объявлений (например, после парсинга)
  function setListings(listings: Listing[]) {
    allListings.value = listings;
  }

  // Загрузить свежие объявления с бэкенда (FastAPI).
  // Если бэкенд не запущен — возвращает false, остаются данные из listings.json.
  async function fetchFromBackend(): Promise<boolean> {
    try {
      const resp = await fetch(`${API_URL}/listings`);
      if (!resp.ok) return false;
      const data: unknown = await resp.json();
      if (!Array.isArray(data)) return false;
      setListings(data as Listing[]);
      return true;
    } catch {
      return false;
    }
  }

  return {
    allListings,
    filters,
    filteredListings,
    districts,
    roomsOptions,
    selectedListingId,
    view,
    resetFilters,
    setSearch,
    setPriceRange,
    openListing,
    closeListing,
    showFavorites,
    showList,
    getListingById,
    setListings,
    fetchFromBackend,
  };
});
