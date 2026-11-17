import { createApp } from "vue";
import { createPinia } from "pinia";

import App from "./App.vue";
import { useFavoritesStore } from "./stores/favorites";

const app = createApp(App);

// Один экземпляр Pinia на всё приложение
const pinia = createPinia();
app.use(pinia);

// Инициализация стора избранного (загрузка из localStorage) до монтирования
const favoritesStore = useFavoritesStore(pinia);
favoritesStore.init();

app.mount("#app");
