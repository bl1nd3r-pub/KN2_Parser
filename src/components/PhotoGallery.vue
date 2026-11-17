<script setup lang="ts">
import { ref, watch } from "vue";
import MissingField from "./MissingField.vue";

const props = defineProps<{
  photos: string[];
}>();

// Индекс текущего фото и состояние полноэкранной модалки
const activeIndex = ref(0);
const modalOpen = ref(false);

// Если сменилось объявление — сбрасываем состояние галереи
watch(
  () => props.photos,
  () => {
    activeIndex.value = 0;
    modalOpen.value = false;
  },
);

const openModal = (index: number) => {
  activeIndex.value = index;
  modalOpen.value = true;
};

const closeModal = () => {
  modalOpen.value = false;
};

const showPrev = () => {
  activeIndex.value = (activeIndex.value + props.photos.length - 1) % props.photos.length;
};

const showNext = () => {
  activeIndex.value = (activeIndex.value + 1) % props.photos.length;
};
</script>

<template>
  <div class="photo-gallery">
    <template v-if="photos.length">
      <!-- Главное фото (клик открывает полноэкранный просмотр) -->
      <img
        :src="photos[activeIndex]"
        :alt="`Фото ${activeIndex + 1}`"
        class="main-photo"
        @click="openModal(activeIndex)"
      />

      <!-- Миниатюры -->
      <div class="gallery-thumbs">
        <img
          v-for="(photo, index) in photos"
          :key="index"
          :src="photo"
          :alt="`Миниатюра ${index + 1}`"
          class="thumb"
          :class="{ active: activeIndex === index }"
          @click="activeIndex = index"
        />
      </div>

      <!-- Полноэкранная модалка -->
      <div v-if="modalOpen" class="gallery-modal">
        <div class="modal-overlay" @click="closeModal"></div>
        <div class="modal-content" @click.stop>
          <img :src="photos[activeIndex]" :alt="`Фото ${activeIndex + 1}`" class="modal-img" />
          <div class="modal-nav">
            <button @click="showPrev" aria-label="Предыдущее фото">‹</button>
            <span>Фото {{ activeIndex + 1 }} из {{ photos.length }}</span>
            <button @click="showNext" aria-label="Следующее фото">›</button>
          </div>
          <button class="modal-close" @click="closeModal">Закрыть</button>
        </div>
      </div>
    </template>

    <div v-else class="no-photos">
      <MissingField label="Фотографии отсутствуют" />
    </div>
  </div>
</template>

<style scoped>
.main-photo {
  width: 100%;
  max-height: 380px;
  object-fit: cover;
  border-radius: 8px;
  cursor: zoom-in;
  margin-bottom: 12px;
  background: #f5f5f5;
}

.gallery-thumbs {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-bottom: 16px;
}

.thumb {
  width: 80px;
  height: 60px;
  object-fit: cover;
  border-radius: 6px;
  cursor: pointer;
  border: 2px solid transparent;
  opacity: 0.8;
  transition: all 0.2s;
}

.thumb:hover,
.thumb.active {
  opacity: 1;
  border-color: #4a90e2;
}

.no-photos {
  text-align: center;
  color: #888;
  font-style: italic;
  margin: 20px 0;
}

.gallery-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1000;
}

.modal-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.9);
}

.modal-content {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  max-width: 90%;
  max-height: 90%;
  text-align: center;
}

.modal-img {
  max-width: 100%;
  max-height: 70vh;
  border-radius: 8px;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
}

.modal-nav {
  margin-top: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
}

.modal-nav button {
  background: none;
  border: none;
  color: white;
  font-size: 2em;
  cursor: pointer;
  padding: 0 8px;
}

.modal-nav span {
  color: white;
  font-size: 1em;
}

.modal-close {
  margin-top: 16px;
  padding: 8px 20px;
  background: #4a90e2;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.modal-close:hover {
  background: #357abd;
}
</style>
