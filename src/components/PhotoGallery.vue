<script setup lang="ts">
import { ref } from "vue";
import MissingField from "./MissingField.vue";

const props = defineProps<{
  photos: string[];
}>();

const emit = defineEmits(["close"]);

const activeIndex = ref(0);

const openImage = (index: number) => {
  activeIndex.value = index;
};
</script>

<template>
  <div class="photo-gallery">
    <div v-if="props.photos.length" class="gallery-thumbs">
      <img
        v-for="(photo, index) in props.photos"
        :key="index"
        :src="photo"
        :alt="`Фото ${index + 1}`"
        class="thumb"
        :class="{ active: activeIndex === index }"
        @click="openImage(index)"
      />
    </div>
    <div v-else class="no-photos">
      <MissingField label="Фотографии отсутствуют" />
    </div>

    <div v-if="props.photos.length && activeIndex >= 0" class="gallery-modal">
      <div class="modal-overlay" @click="emit('close')"></div>
      <div class="modal-content" @click.stop>
        <img :src="props.photos[activeIndex]" :alt="`Фото ${activeIndex + 1}`" class="modal-img" />
        <div class="modal-nav">
          <button @click="activeIndex = (activeIndex + props.photos.length - 1) % props.photos.length">‹</button>
          <span>Фото {{ activeIndex + 1 }} из {{ props.photos.length }}</span>
          <button @click="activeIndex = (activeIndex + 1) % props.photos.length">›</button>
        </div>
        <button class="modal-close" @click="emit('close')">Закрыть</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
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
