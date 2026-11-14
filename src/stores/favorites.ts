import { defineStore } from "pinia";
import { ref, computed } from "vue";

export const useFavoritesStore = defineStore("favorites", () => {
  // ID избранных объявлений, храним в localStorage
  const favoriteIds = ref<string[]>([]);

  // Загрузка из localStorage при инициализации
  function init() {
    try {
      const stored = localStorage.getItem("favorite_listing_ids");
      if (stored) {
        favoriteIds.value = JSON.parse(stored);
      }
    } catch {
      favoriteIds.value = [];
    }
  }

  // Сохранение в localStorage
  function save() {
    localStorage.setItem("favorite_listing_ids", JSON.stringify(favoriteIds.value));
  }

  // Добавить / убрать из избранного
  function toggle(id: string) {
    if (favoriteIds.value.includes(id)) {
      favoriteIds.value = favoriteIds.value.filter((fid) => fid !== id);
    } else {
      favoriteIds.value.push(id);
    }
    save();
  }

  // Проверка, в избранном ли объявление
  const isFavorite = (id: string): boolean => {
    return favoriteIds.value.includes(id);
  };

  return {
    favoriteIds,
    init,
    toggle,
    isFavorite,
  };
});
